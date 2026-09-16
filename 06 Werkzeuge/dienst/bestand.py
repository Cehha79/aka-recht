#!/usr/bin/env python3
"""Bestand eines Falls: Kennungen vergeben, Prüfsummen führen, Verschiebungen erkennen.

bestand.json schreibt nur dieses Modul. Dateien in den Ordnern 01 bis 08
bekommen beim ersten Einlesen eine D-Kennung und eine erste Prüfsumme
(sha256_erst), die bleibt. Verschobene Dateien werden über die Prüfsumme
wiedergefunden, wenn der alte Pfad nicht mehr existiert und die Zuordnung
eindeutig ist. Nur Standardbibliothek.
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
                try: store.sicher(str(p.relative_to(ordner)), ordner)
                except ValueError: continue
                liste.append(str(p.relative_to(ordner)))
    return liste

def aktualisieren(ordner, weg='Dienst'):
    """Gleicht bestand.json mit den Dateien ab. Liefert {kennung: pfad} der vorhandenen Dateien."""
    ordner = Path(ordner)
    with store.sperre():
        alt = lese(ordner); daten = json.loads(json.dumps(alt))
        vorhanden = dateien(ordner); vorhanden_set = set(vorhanden)
        pfad_zu_id = {e['pfad']: k for k, e in daten['dateien'].items()}
        naechste = max([int(k[1:]) for k in daten['dateien'] if re.fullmatch(r'D\d+', k)], default=0) + 1
        ergebnis = {}
        for rel in vorhanden:
            p = ordner / rel; h = sha_datei(p); kennung = pfad_zu_id.get(rel)
            if not kennung:
                treffer = [k for k, e in daten['dateien'].items() if e['pfad'] not in vorhanden_set and e['sha256'] == h]
                if len(treffer) == 1:
                    kennung = treffer[0]
                    daten['verschiebungen'].append({'id': kennung, 'von': daten['dateien'][kennung]['pfad'], 'nach': rel,
                                                    'zeit': datetime.now().isoformat(timespec='seconds'), 'weg': weg + ', über Prüfsumme erkannt'})
                    pfad_zu_id.pop(daten['dateien'][kennung]['pfad'], None)
                else:
                    kennung = f'D{naechste:04d}'; naechste += 1
                    daten['dateien'][kennung] = {'pfad': rel, 'sha256_erst': h, 'sha256': h, 'alt': '', 'erfasst': datetime.now().date().isoformat()}
                pfad_zu_id[rel] = kennung
            e = daten['dateien'][kennung]; e['pfad'] = rel; e['sha256'] = h
            e.setdefault('sha256_erst', h); e.setdefault('erfasst', datetime.now().date().isoformat()); e.setdefault('alt', '')
            ergebnis[kennung] = rel
        if daten != alt: store.atomar(ordner / 'bestand.json', json.dumps(daten, ensure_ascii=False, indent=2) + '\n')
        return ergebnis

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
        quelle.rename(ziel); neu = str(ziel.relative_to(ordner))
        daten['verschiebungen'].append({'id': kennung, 'von': e['pfad'], 'nach': neu, 'zeit': datetime.now().isoformat(timespec='seconds'), 'weg': 'Oberfläche'})
        e['pfad'] = neu
        store.atomar(ordner / 'bestand.json', json.dumps(daten, ensure_ascii=False, indent=2) + '\n')
        return neu
