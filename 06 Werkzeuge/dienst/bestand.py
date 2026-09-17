#!/usr/bin/env python3
"""Bestand eines Falls: Kennungen vergeben, Prüfsummen führen, Verschiebungen erkennen.

bestand.json schreibt nur dieses Modul, und nur in abgleichen() (schreibender
Abgleich) und verschieben(). Dateien in den Ordnern 01 bis 08 bekommen beim
Abgleich eine D-Kennung und eine erste Prüfsumme (sha256_erst), die bleibt.
Verschobene Dateien werden über die Prüfsumme wiedergefunden, wenn der alte
Pfad nicht mehr existiert und die Zuordnung eindeutig ist. abgleich() rechnet
dasselbe nur lesend und meldet Abweichungen (Prüfbericht 16.09.2026, F03).
Nur Standardbibliothek.
"""
import hashlib, json, re
from datetime import datetime
from pathlib import Path
import store

HASH_CACHE = {}

def sha_datei(p):
    s = p.stat(); k = (str(p), s.st_mtime_ns, s.st_size)
    if k not in HASH_CACHE: HASH_CACHE[k] = hashlib.sha256(p.read_bytes()).hexdigest()
    return HASH_CACHE[k]

def lese(ordner):
    p = Path(ordner) / 'bestand.json'
    return json.loads(p.read_text('utf-8')) if p.exists() else {'schema': 1, 'dateien': {}, 'verschiebungen': []}

def dateien(ordner):
    """Alle Inhaltsdateien der Gruppen 01 bis 08, relativ, sortiert."""
    ordner = Path(ordner); liste = []
    for g in store.GRUPPEN:
        basis = ordner / g
        if not basis.is_dir(): continue
        for p in sorted(basis.rglob('*')):
            if p.is_file() and not p.is_symlink() and p.name != '.DS_Store' and not p.name.startswith('.'):
                try: store.sicher(p.relative_to(ordner).as_posix(), ordner)
                except ValueError: continue
                liste.append(p.relative_to(ordner).as_posix())
    return liste

def _rechnen(ordner, weg, kennungen_vergeben):
    """Vergleicht bestand.json mit den Dateien der Gruppen 01 bis 08, ohne zu schreiben.

    Liefert (daten, alt, ergebnis, bericht): daten ist der abgeglichene Stand (Kopie), alt der gelesene,
    ergebnis {kennung: pfad} der vorhandenen registrierten Dateien, bericht die Abweichungen:
    neu (frisch vergebene Kennungen, nur mit kennungen_vergeben), nicht_erfasst (Dateien ohne Kennung),
    verschoben (über die Prüfsumme wiedergefunden), fehlend (registriert, aber nicht mehr vorhanden)."""
    ordner = Path(ordner)
    alt = lese(ordner); daten = json.loads(json.dumps(alt))
    vorhanden = dateien(ordner); vorhanden_set = set(vorhanden)
    pfad_zu_id = {e['pfad']: k for k, e in daten['dateien'].items()}
    bericht = {'neu': [], 'nicht_erfasst': [], 'verschoben': [], 'fehlend': []}
    # Kennungen, die akte.json schon vergibt (etwa eine mitgelieferte Beispielakte), gelten vor neuen Nummern
    akte_pfade = {}
    try:
        akte_datei = ordner / 'akte.json'
        if akte_datei.exists():
            for k, d in json.loads(akte_datei.read_text('utf-8')).get('dokumente', {}).items():
                if re.fullmatch(r'D\d+', k) and d.get('pfad') and k not in daten['dateien']: akte_pfade[d['pfad']] = k
    except (ValueError, OSError): akte_pfade = {}
    naechste = max([int(k[1:]) for k in list(daten['dateien']) + list(akte_pfade.values()) if re.fullmatch(r'D\d+', k)], default=0) + 1
    ergebnis = {}; heute = datetime.now().date().isoformat()
    for rel in vorhanden:
        p = ordner / rel; h = sha_datei(p); kennung = pfad_zu_id.get(rel)
        if not kennung:
            treffer = [k for k, e in daten['dateien'].items() if e['pfad'] not in vorhanden_set and e['sha256'] == h]
            if len(treffer) == 1:
                kennung = treffer[0]
                bericht['verschoben'].append({'id': kennung, 'von': daten['dateien'][kennung]['pfad'], 'nach': rel})
                daten['verschiebungen'].append({'id': kennung, 'von': daten['dateien'][kennung]['pfad'], 'nach': rel,
                                                'zeit': datetime.now().isoformat(timespec='seconds'), 'weg': weg + ', über Prüfsumme erkannt'})
                pfad_zu_id.pop(daten['dateien'][kennung]['pfad'], None)
            elif kennungen_vergeben:
                kennung = akte_pfade.pop(rel, None)
                if not kennung: kennung = f'D{naechste:04d}'; naechste += 1
                daten['dateien'][kennung] = {'pfad': rel, 'sha256_erst': h, 'sha256': h, 'alt': '', 'erfasst': heute}
                bericht['neu'].append({'id': kennung, 'pfad': rel})
            else:
                bericht['nicht_erfasst'].append(rel); continue
            pfad_zu_id[rel] = kennung
        e = daten['dateien'][kennung]; e['pfad'] = rel; e['sha256'] = h
        e.setdefault('sha256_erst', h); e.setdefault('erfasst', heute); e.setdefault('alt', '')
        ergebnis[kennung] = rel
    bericht['fehlend'] = [{'id': k, 'pfad': e['pfad']} for k, e in daten['dateien'].items() if k not in ergebnis]
    return daten, alt, ergebnis, bericht

def abgleich(ordner):
    """Nur lesen: registrierte Dateien und Abweichungen, ohne bestand.json anzufassen.
    Liefert (ergebnis, bericht). Verschobene Dateien stehen mit ihrem neuen Pfad im Ergebnis,
    neue Dateien nur in bericht['nicht_erfasst']; Kennungen vergibt erst abgleichen()."""
    _, _, ergebnis, bericht = _rechnen(ordner, 'Lesen', kennungen_vergeben=False)
    return ergebnis, bericht

def abgleichen(ordner, weg='Abgleich'):
    """Schreibend: vergibt Kennungen für neue Dateien, übernimmt Verschiebungen, schreibt bestand.json.
    Liefert (ergebnis, bericht)."""
    ordner = Path(ordner)
    with store.sperre():
        daten, alt, ergebnis, bericht = _rechnen(ordner, weg, kennungen_vergeben=True)
        if daten != alt: store.atomar(ordner / 'bestand.json', json.dumps(daten, ensure_ascii=False, indent=2) + '\n')
    return ergebnis, bericht

def aktualisieren(ordner, weg='Dienst'):
    """Schreibender Abgleich, liefert nur {kennung: pfad}. Für Import und Zuordnung im Dienst."""
    return abgleichen(ordner, weg)[0]

def pruefen(ordner):
    """Vergleicht jede registrierte Datei mit ihrer ersten Prüfsumme."""
    ordner = Path(ordner); daten = lese(ordner)
    geprueft = 0; veraendert = []; fehlend = []
    for k, e in daten['dateien'].items():
        p = ordner / e['pfad']
        if not p.is_file(): fehlend.append({'id': k, 'pfad': e['pfad']})
        elif sha_datei(p) != e['sha256_erst']: veraendert.append({'id': k, 'pfad': e['pfad']})
        else: geprueft += 1
    return {'geprueft': geprueft, 'veraendert': veraendert, 'fehlend': fehlend,
            'hinweis': 'Eine Prüfsumme belegt Gleichheit mit dem registrierten Stand, nicht Echtheit oder Beweiskraft.'}

def verschieben(ordner, kennung, zielgruppe, unterordner=''):
    """Verschiebt eine Datei innerhalb der Fallordner. Kennung bleibt, nichts wird überschrieben."""
    ordner = Path(ordner)
    if zielgruppe not in store.GRUPPEN: raise ValueError('Ziel muss einer der Aktenbereiche 01 bis 08 sein.')
    unterordner = str(unterordner or '').strip().strip('/')
    for teil in unterordner.split('/') if unterordner else []:
        if teil != Path(teil).name or teil.startswith('.') or len(teil) > 100 or any(c in teil for c in '\\\x00:'): raise ValueError('Ungültiger Unterordnername.')
    with store.sperre():
        daten = lese(ordner); e = daten['dateien'].get(kennung)
        if not e: raise ValueError('Unbekannte Dokumentkennung.')
        quelle = store.sicher(e['pfad'], ordner)
        if not quelle.is_file(): raise ValueError('Datei fehlt am registrierten Ort. Bestand neu einlesen.')
        zielordner = store.sicher(f'{zielgruppe}/{unterordner}' if unterordner else zielgruppe, ordner)
        ziel = zielordner / quelle.name
        if ziel == quelle: return e['pfad']
        if ziel.exists(): raise ValueError('Am Ziel liegt schon eine gleichnamige Datei. Es wird nichts überschrieben.')
        zielordner.mkdir(parents=True, exist_ok=True)
        quelle.rename(ziel); neu = ziel.relative_to(ordner).as_posix()
        daten['verschiebungen'].append({'id': kennung, 'von': e['pfad'], 'nach': neu, 'zeit': datetime.now().isoformat(timespec='seconds'), 'weg': 'Oberfläche'})
        e['pfad'] = neu
        store.atomar(ordner / 'bestand.json', json.dumps(daten, ensure_ascii=False, indent=2) + '\n')
        return neu
