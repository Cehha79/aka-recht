#!/usr/bin/env python3
"""Geprüfte ZIP-Sicherung des ganzen Projekts an ein Ziel außerhalb, optional
mit Kopie an ein zweites Ziel (zum Beispiel iCloud Drive).

Ablauf: ZIP schreiben (Endung .unvollstaendig), ZIP lesen und jede Datei mit
dem Arbeitsstand vergleichen, umbenennen, SHA-256-Datei daneben schreiben,
Kopie ans zweite Ziel und dort erneut prüfen, Ergebnis in zentrale.json.
Nur Standardbibliothek.
"""
import hashlib, json, shutil, uuid, zipfile
from datetime import datetime
from pathlib import Path
import store

AUSGESCHLOSSEN = {'__pycache__', '.DS_Store', '.git'}

def sha(daten): return hashlib.sha256(daten).hexdigest()

def _dateien(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()
            and not any(t in AUSGESCHLOSSEN for t in p.relative_to(root).parts)]

def erstellen(root=None, ziel=None, zweites_ziel=None):
    root = Path(root or store.ROOT).resolve(); z = store.lade_zentrale()
    ziel = Path(ziel or z['sicherung']['ziel']).expanduser()
    zweites = Path(zweites_ziel) if zweites_ziel else (Path(z['sicherung'].get('zweites_ziel')).expanduser() if z['sicherung'].get('zweites_ziel') else None)
    for k in (ziel, zweites):
        if k and (k.resolve() == root or root in k.resolve().parents): raise ValueError('Sicherungsziel muss außerhalb des Projekts liegen.')
    if any(p.is_symlink() for p in root.rglob('*')): raise ValueError('Sicherung abgebrochen: symbolische Verknüpfung im Projekt.')
    ziel.mkdir(parents=True, exist_ok=True)
    name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_' + uuid.uuid4().hex[:6] + '_Recht.zip'
    fertig = ziel / name; vorlaeufig = ziel / (name + '.unvollstaendig')
    eintraege = _dateien(root)
    with zipfile.ZipFile(vorlaeufig, 'x', zipfile.ZIP_DEFLATED) as zf:
        for p in eintraege: zf.write(p, str(p.relative_to(root)))
    vorlaeufig.chmod(0o600)
    with zipfile.ZipFile(vorlaeufig) as zf:
        if zf.testzip(): raise RuntimeError('ZIP-Prüfung fehlgeschlagen; keine fertige Sicherung gemeldet.')
        for p in eintraege:
            if sha(zf.read(str(p.relative_to(root)))) != sha(p.read_bytes()): raise RuntimeError('Datei während der Sicherung verändert: ' + str(p.relative_to(root)))
    vorlaeufig.rename(fertig); pruefsumme = sha(fertig.read_bytes())
    (fertig.with_suffix('.zip.sha256')).write_text(pruefsumme + '  ' + fertig.name + '\n')
    ergebnis = {'pfad': str(fertig), 'sha256': pruefsumme, 'dateien': len(eintraege), 'groesse': fertig.stat().st_size,
                'zeit': datetime.now().isoformat(timespec='seconds'), 'zweites_ziel': None, 'zweites_ziel_hinweis': ''}
    if zweites:
        if zweites.parent.exists():
            zweites.mkdir(parents=True, exist_ok=True); kopie = zweites / fertig.name
            shutil.copyfile(fertig, kopie); shutil.copyfile(fertig.with_suffix('.zip.sha256'), kopie.with_suffix('.zip.sha256'))
            if sha(kopie.read_bytes()) != pruefsumme: raise RuntimeError('Kopie am zweiten Ziel weicht ab: ' + str(kopie))
            ergebnis['zweites_ziel'] = str(kopie)
        else:
            ergebnis['zweites_ziel_hinweis'] = f'Zweites Ziel nicht erreichbar: {zweites.parent} fehlt (iCloud Drive nicht eingerichtet?).'
    z = store.lade_zentrale(); z['sicherung']['letzte'] = ergebnis; store.speichere_zentrale(z)
    return ergebnis

def status():
    z = store.lade_zentrale(); l = z['sicherung'].get('letzte')
    if not l: return {'vorhanden': False}
    p = Path(l['pfad']); vorhanden = p.is_file()
    return {**l, 'vorhanden': vorhanden, 'unveraendert': vorhanden and p.stat().st_size == l['groesse'] and sha(p.read_bytes()) == l['sha256']}
