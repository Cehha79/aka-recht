#!/usr/bin/env python3
"""Übergabepaket als ZIP außerhalb des Projekts, für einen benannten Empfänger.

Empfänger und Umfang werden vorher festgelegt (Prüfbericht 16.09.2026, F08):
  --empfaenger anwalt      Umfang „voll“: Inhaltsverzeichnis mit Beteiligten, Verfahren,
                           Chronologie, Fristen, offenen Aufgaben, Journal und alle Originale
                           aus 01 bis 05 (Entwürfe nur mit --mit-entwuerfen)
  --empfaenger behoerde | gericht | gegenseite | beratung
                           Umfang „dokumente“: nur die mit --nur gewählten Dokumente und ein
                           Verzeichnis dieser Dokumente mit Anlagenkennungen. Keine Chronologie,
                           keine Fristen, keine Aufgaben, kein Journal, keine internen Angaben.
  --umfang voll|dokumente  überschreibt die Vorgabe des Empfängers
  --mit-journal, --mit-chronologie   einzelne Teile zum Umfang „dokumente“ dazunehmen

Vollständigkeit und Abschluss (F27): Jede mit --nur genannte Kennung muss existieren und ihre
Datei vorhanden sein, sonst Abbruch ohne Paket. Das Paket wird zuerst als vorläufige Datei
geschrieben, dann geöffnet und Datei für Datei gegen das Manifest (Name, Größe, SHA-256)
geprüft; erst dann bekommt es seinen Namen. Das Manifest liegt als „00 Manifest.json“ im Paket.

Aufruf:
  python3 uebergabe_paket.py R-0001 --empfaenger anwalt [--mit-entwuerfen] [--ziel "/Pfad/Paket.zip"]
  python3 uebergabe_paket.py R-0001 --empfaenger gericht --nur D0001,D0002 [--vorschau]
--vorschau zeigt nur, was ins Paket käme, und schreibt nichts.
Ziel liegt außerhalb des Projekts, Standard: ~/Desktop/AKA Recht Übergabe <Fall> <Empfänger> <Datum>.zip
Das Paket wird nicht verschickt. Nur Standardbibliothek.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, os, zipfile
from datetime import date, datetime
from pathlib import Path

EMPFAENGER = {'anwalt': 'voll', 'beratung': 'dokumente', 'behoerde': 'dokumente', 'gericht': 'dokumente', 'gegenseite': 'dokumente'}
ORIGINALE = ['01 Eingang', '02 Grundlagen', '03 Schriftverkehr', '04 Verfahren', '05 Beweise']   # neue Post im Eingang ist Original

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def auswahl(daten, args):
    """Dokumente für das Paket. Unbekannte oder fehlende Kennungen sind ein Fehler, kein stilles Weglassen."""
    alle = {d['id']: d for d in daten['dokumente']}
    if args.nur:
        gewuenscht = [x.strip().upper() for x in args.nur.split(',') if x.strip()]
        unbekannt = [k for k in gewuenscht if k not in alle]
        if unbekannt: sys.exit('Abbruch: unbekannte Dokumentkennung(en) ' + ', '.join(unbekannt) + '. Kein Paket erzeugt.')
        fehlend = [k for k in gewuenscht if alle[k]['fehlt']]
        if fehlend: sys.exit('Abbruch: Datei fehlt am registrierten Ort für ' + ', '.join(fehlend) + '. Erst bestand_abgleichen, kein Paket erzeugt.')
        return [alle[k] for k in gewuenscht], []
    if args.umfang == 'dokumente': sys.exit('Abbruch: Umfang „dokumente“ braucht --nur mit den Kennungen, die der Empfänger bekommen soll.')
    gruppen = ORIGINALE + (['06 Entwürfe'] if args.mit_entwuerfen else [])
    docs = [d for d in daten['dokumente'] if d['gruppe'] in gruppen]
    return [d for d in docs if not d['fehlt']], [d for d in docs if d['fehlt']]

def verzeichnis(ak, docs, fehlend, args):
    f = ak['fall']; pers = {b['id']: b for b in ak['beteiligte']}
    z = [f'# Übergabe {f["id"]} · {f["titel"]}', f'Stand: {date.today():%d.%m.%Y} · Empfänger: {args.empfaenger} · Umfang: {args.umfang}', '']
    if args.umfang == 'voll':
        z += [f'Bereich: {f["bereich"]} · Rolle: {f["rolle"]} · Status: {f["status"]}', '', f'Ziel: {f["ziel"]}', '', '## Beteiligte']
        z += [f'- {b["id"]} {b["name"]} ({b["rolle"]}){" · " + b["aktenzeichen"] if b["aktenzeichen"] else ""}' for b in ak['beteiligte']]
        z += ['', '## Verfahren'] + [f'- {v["id"]} {v["art"]} · {pers.get(v["stelle"], {}).get("name", "")} · Az. {v["aktenzeichen"] or "offen"} · Stand: {v["stand"]}' for v in ak['verfahren']]
    if args.umfang == 'voll' or args.mit_chronologie:
        def zeit(e):   # F13: unsichere Zeitpunkte sichtbar, datum ist dann nur das Sortierdatum
            z = e.get('zeitpunkt') or 'genau'; t = f' ({e["zeitpunkt_text"]})' if e.get('zeitpunkt_text') else ''
            if z == 'ungefähr': return f'ca. {e["datum"]}{t}'
            if z == 'zeitraum': return f'{e["datum"]} bis {e.get("datum_bis") or e["datum"]}{t}'
            if z == 'unbekannt': return f'Zeitpunkt unbekannt, einsortiert bei {e["datum"]}{t}'
            return e['datum']
        z += ['', '## Chronologie'] + [f'- {zeit(e)} {e["titel"]} ({e["art"]}){" · Quelle " + e["quelle"] if e["quelle"] else ""}: {e["detail"]}' for e in sorted(ak['ereignisse'], key=lambda x: x['datum'])]
    if args.umfang == 'voll':
        z += ['', '## Fristen und Termine'] + [f'- {x["datum"]} {x["titel"]} · {x["art"]} · Prüfstatus {x["pruefstatus"]} · Auslöser: {x["ausloeser"]} · Grundlage: {x["rechtsgrundlage"]}' for x in sorted(ak['fristen'], key=lambda x: x['datum'])]
        z += ['', '## Offene Aufgaben'] + [f'- {x["titel"]}{" (fällig " + x["faellig"] + ")" if x["faellig"] else ""}: {x["detail"]}' for x in ak['aufgaben'] if not x['erledigt']]
    z += ['', '## Anlagenverzeichnis'] + [f'- {d["anlage"]}: {d["titel"]} ({d["id"]})' for d in sorted((d for d in docs if d['anlage']), key=lambda d: d['anlage'])]
    z += ['', '## Enthaltene Dokumente'] + [f'- {d["id"]} · {d["titel"]} · {d["datum"] or "ohne Datum"} · {d["stand"]}' for d in docs]
    if fehlend: z += ['', '## Nicht enthalten (Datei fehlt am registrierten Ort)'] + [f'- {d["id"]} · {d["titel"]} · {d["pfad"]}' for d in fehlend]
    z += ['', 'Hinweis: Zusammenstellung aus der lokalen Akte. Ordnungsangaben sind kein Nachweis von Zugang oder Einreichung. Entwürfe sind keine versandten Schreiben. Prüfsummen aller Dateien stehen in 00 Manifest.json.']
    return '\n'.join(z)

def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('fall'); a.add_argument('--empfaenger', required=True, choices=sorted(EMPFAENGER)); a.add_argument('--umfang', choices=['voll', 'dokumente'])
    a.add_argument('--nur', help='Dokumentkennungen, durch Komma getrennt'); a.add_argument('--ziel')
    a.add_argument('--mit-entwuerfen', action='store_true'); a.add_argument('--mit-journal', action='store_true'); a.add_argument('--mit-chronologie', action='store_true')
    a.add_argument('--vorschau', action='store_true', help='nur anzeigen, nichts schreiben')
    args = a.parse_args(); args.umfang = args.umfang or EMPFAENGER[args.empfaenger]
    root = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[3])
    sys.path.insert(0, str(root / '06 Werkzeuge/dienst')); import store, werkzeuge
    store.konfigurieren(root)
    daten = werkzeuge.fall_lesen(args.fall); ak = daten['akte']; f = ak['fall']; ordner = store.fall_ordner(args.fall)
    if daten['abweichungen']['nicht_erfasst']: print('Hinweis: Dateien ohne Kennung im Fall (nicht im Paket): ' + ', '.join(daten['abweichungen']['nicht_erfasst']))
    docs, fehlend = auswahl(daten, args)
    if not docs: sys.exit('Abbruch: kein Dokument ausgewählt.')
    einzeln = args.umfang == 'dokumente' or bool(args.nur)
    eintraege = [{'name': f'{d["id"]} {Path(d["pfad"]).name}' if einzeln else d['pfad'], 'dokument': d['id'], 'titel': d['titel'], 'stand': d['stand'],
                  'groesse': (ordner / d['pfad']).stat().st_size, 'sha256': sha(ordner / d['pfad'])} for d in docs]
    mit_journal = args.umfang == 'voll' or args.mit_journal
    manifest = {'fall': f['id'], 'titel': f['titel'], 'empfaenger': args.empfaenger, 'umfang': args.umfang, 'erstellt': datetime.now().isoformat(timespec='seconds'),
                'journal': mit_journal and (ordner / 'JOURNAL.md').exists(), 'chronologie': args.umfang == 'voll' or args.mit_chronologie,
                'dokumente': eintraege, 'nicht_enthalten_fehlend': [d['id'] for d in fehlend]}
    print(f'Paket für {args.empfaenger} ({args.umfang}): {len(eintraege)} Dokument(e)' + (', Journal' if manifest['journal'] else ', ohne Journal') + (', Chronologie' if manifest['chronologie'] else ', ohne Chronologie'))
    for e in eintraege: print(f'  {e["dokument"]} · {e["titel"]} · {e["stand"]} · {e["groesse"]} Bytes · {e["name"]}')
    if fehlend: print('  nicht enthalten, Datei fehlt: ' + ', '.join(d['id'] for d in fehlend))
    if args.vorschau: print('Vorschau, nichts geschrieben.'); return 0
    ziel = Path(args.ziel).expanduser() if args.ziel else Path.home() / 'Desktop' / f'AKA Recht Übergabe {f["id"]} {args.empfaenger} {date.today().isoformat()}.zip'
    if root == ziel.resolve() or root in ziel.resolve().parents: sys.exit('Ziel muss außerhalb des Projekts liegen.')
    if ziel.exists(): sys.exit(f'Ziel existiert schon: {ziel}. Nichts wird überschrieben.')
    vorlaeufig = ziel.with_name(ziel.name + '.teil')
    try:
        with zipfile.ZipFile(vorlaeufig, 'x', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('00 Manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
            zf.writestr('00 Inhaltsverzeichnis.md', verzeichnis(ak, docs, fehlend, args))
            if manifest['journal']: zf.write(ordner / 'JOURNAL.md', '00 Journal.md')
            for d, e in zip(docs, eintraege): zf.write(ordner / d['pfad'], e['name'])
        # Abschlussprüfung: Paket wieder öffnen, jede Datei gegen das Manifest
        with zipfile.ZipFile(vorlaeufig) as zf:
            namen = set(zf.namelist()); erwartet = {'00 Manifest.json', '00 Inhaltsverzeichnis.md'} | ({'00 Journal.md'} if manifest['journal'] else set()) | {e['name'] for e in eintraege}
            if namen != erwartet: raise RuntimeError('Inhalt weicht vom Manifest ab: ' + ', '.join(sorted(namen ^ erwartet)))
            for e in eintraege:
                roh = zf.read(e['name'])
                if len(roh) != e['groesse'] or hashlib.sha256(roh).hexdigest() != e['sha256']: raise RuntimeError(f'{e["name"]}: Inhalt im Paket stimmt nicht mit der Akte überein.')
            if json.loads(zf.read('00 Manifest.json'))['dokumente'] != eintraege: raise RuntimeError('Manifest im Paket unvollständig.')
    except Exception as e:
        if vorlaeufig.exists(): vorlaeufig.unlink()
        sys.exit(f'Abbruch, kein Paket: {e}')
    vorlaeufig.rename(ziel); ziel.chmod(0o600)
    print(f'Übergabepaket geprüft: {ziel} ({len(eintraege)} Dokumente, {ziel.stat().st_size} Bytes)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
