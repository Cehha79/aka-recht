#!/usr/bin/env python3
"""Übergabepaket für Anwalt, Behörde oder Gericht: ZIP mit Inhaltsverzeichnis,
Chronologie, Fristen, Anlagenverzeichnis, Journal und den Originalen aus
02 Grundlagen, 03 Schriftverkehr, 04 Verfahren, 05 Beweise. Entwürfe und Archiv
sind nicht enthalten, außer ausdrücklich angegeben.

Aufruf: python3 uebergabe_paket.py R-0001 [--ziel "/Pfad/Paket.zip"] [--mit-entwuerfen] [--nur D0001,D0002]
Ziel liegt außerhalb des Projekts, Standard: ~/Desktop/AKA Recht Übergabe <Fall> <Datum>.zip
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, os, zipfile
from datetime import date
from pathlib import Path

def main():
    a = argparse.ArgumentParser(description=__doc__); a.add_argument('fall'); a.add_argument('--ziel'); a.add_argument('--mit-entwuerfen', action='store_true'); a.add_argument('--nur')
    args = a.parse_args()
    root = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[3])
    sys.path.insert(0, str(root / '06 Werkzeuge/dienst')); import store, werkzeuge
    store.konfigurieren(root)
    daten = werkzeuge.fall_lesen(args.fall); ak = daten['akte']; f = ak['fall']; ordner = store.fall_ordner(args.fall)
    nur = set(x.strip() for x in args.nur.split(',')) if args.nur else None
    gruppen = ['02 Grundlagen', '03 Schriftverkehr', '04 Verfahren', '05 Beweise'] + (['06 Entwürfe'] if args.mit_entwuerfen else [])
    docs = [d for d in daten['dokumente'] if not d['fehlt'] and (d['id'] in nur if nur else d['gruppe'] in gruppen)]
    pers = {b['id']: b for b in ak['beteiligte']}
    z = [f'# Übergabe {f["id"]} · {f["titel"]}', f'Stand: {date.today():%d.%m.%Y} · Bereich: {f["bereich"]} · Rolle: {f["rolle"]} · Status: {f["status"]}', '', f'Ziel: {f["ziel"]}', '',
         '## Beteiligte'] + [f'- {b["id"]} {b["name"]} ({b["rolle"]}){" · " + b["aktenzeichen"] if b["aktenzeichen"] else ""}' for b in ak['beteiligte']] + ['', '## Verfahren'] + \
        [f'- {v["id"]} {v["art"]} · {pers.get(v["stelle"], {}).get("name", "")} · Az. {v["aktenzeichen"] or "offen"} · Stand: {v["stand"]}' for v in ak['verfahren']] + ['', '## Chronologie'] + \
        [f'- {e["datum"]} {e["titel"]} ({e["art"]}){" · Quelle " + e["quelle"] if e["quelle"] else ""}: {e["detail"]}' for e in sorted(ak['ereignisse'], key=lambda x: x['datum'])] + ['', '## Fristen und Termine'] + \
        [f'- {x["datum"]} {x["titel"]} · {x["art"]} · Prüfstatus {x["pruefstatus"]} · Auslöser: {x["ausloeser"]} · Grundlage: {x["rechtsgrundlage"]}' for x in sorted(ak['fristen'], key=lambda x: x['datum'])] + ['', '## Offene Aufgaben'] + \
        [f'- {x["titel"]}{" (fällig " + x["faellig"] + ")" if x["faellig"] else ""}: {x["detail"]}' for x in ak['aufgaben'] if not x['erledigt']] + ['', '## Anlagenverzeichnis'] + \
        [f'- {d["anlage"]}: {d["titel"]} ({d["id"]}, {d["pfad"]})' for d in sorted((d for d in docs if d['anlage']), key=lambda d: d['anlage'])] + ['', '## Enthaltene Dokumente'] + \
        [f'- {d["id"]} · {d["titel"]} · {d["datum"] or "ohne Datum"} · {d["stand"]} · {d["pfad"]} · SHA-256 {hashlib.sha256((ordner / d["pfad"]).read_bytes()).hexdigest()[:16]}…' for d in docs] + \
        ['', 'Hinweis: Zusammenstellung aus der lokalen Akte. Ordnungsangaben sind kein Nachweis von Zugang oder Einreichung. Entwürfe sind keine versandten Schreiben.']
    ziel = Path(args.ziel).expanduser() if args.ziel else Path.home() / 'Desktop' / f'AKA Recht Übergabe {f["id"]} {date.today().isoformat()}.zip'
    if root in ziel.resolve().parents: sys.exit('Ziel muss außerhalb des Projekts liegen.')
    with zipfile.ZipFile(ziel, 'x', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('00 Inhaltsverzeichnis.md', '\n'.join(z))
        if (ordner / 'JOURNAL.md').exists(): zf.write(ordner / 'JOURNAL.md', '00 Journal.md')
        for d in docs: zf.write(ordner / d['pfad'], f'{d["id"]} {Path(d["pfad"]).name}' if nur else d['pfad'])
    print(f'Übergabepaket: {ziel} ({len(docs)} Dokumente)')

if __name__ == '__main__':
    main()
