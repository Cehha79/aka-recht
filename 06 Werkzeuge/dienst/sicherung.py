#!/usr/bin/env python3
"""Geprüfte ZIP-Sicherung des ganzen Projekts an ein Ziel außerhalb, optional
mit Kopie an ein zweites Ziel (zum Beispiel iCloud Drive).

Ablauf: ZIP schreiben (Endung .unvollstaendig), ZIP lesen und jede Datei mit
dem Arbeitsstand vergleichen, umbenennen, SHA-256-Datei daneben schreiben,
Kopie ans zweite Ziel (Rechte 0600) und dort erneut prüfen, Ergebnis in
zentrale.json.

Wiederherstellung (Prüfbericht 16.09.2026, F19): wiederherstellen() entpackt
ein Archiv in einen neuen, leeren Ordner außerhalb des Projekts und prüft dort
Prüfsummendatei, Archiv, Dateizahl, jede Akte gegen das Schema und jede
registrierte Datei gegen die Prüfsumme in bestand.json. Die laufende Mappe
wird dabei nie angefasst. probe() macht dasselbe in einem Zwischenordner und
räumt ihn wieder ab. Nur Standardbibliothek.
"""
import hashlib, json, shutil, sys, tempfile, uuid, zipfile
from datetime import datetime
from pathlib import Path
import store
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import akte_schema

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
        for p in eintraege: zf.write(p, p.relative_to(root).as_posix())   # immer Schrägstrich, auch unter Windows
    vorlaeufig.chmod(0o600)
    with zipfile.ZipFile(vorlaeufig) as zf:
        if zf.testzip(): raise RuntimeError('ZIP-Prüfung fehlgeschlagen; keine fertige Sicherung gemeldet.')
        for p in eintraege:
            if sha(zf.read(p.relative_to(root).as_posix())) != sha(p.read_bytes()): raise RuntimeError('Datei während der Sicherung verändert: ' + p.relative_to(root).as_posix())
    vorlaeufig.rename(fertig); pruefsumme = sha(fertig.read_bytes())
    (fertig.with_suffix('.zip.sha256')).write_text(pruefsumme + '  ' + fertig.name + '\n', encoding='utf-8')
    ergebnis = {'pfad': str(fertig), 'sha256': pruefsumme, 'dateien': len(eintraege), 'groesse': fertig.stat().st_size,
                'zeit': datetime.now().isoformat(timespec='seconds'), 'zweites_ziel': None, 'zweites_ziel_hinweis': ''}
    if zweites:
        if zweites.parent.exists():
            zweites.mkdir(parents=True, exist_ok=True); kopie = zweites / fertig.name
            shutil.copyfile(fertig, kopie); shutil.copyfile(fertig.with_suffix('.zip.sha256'), kopie.with_suffix('.zip.sha256'))
            kopie.chmod(0o600); kopie.with_suffix('.zip.sha256').chmod(0o600)   # copyfile überträgt keine Rechte (F20)
            if sha(kopie.read_bytes()) != pruefsumme: raise RuntimeError('Kopie am zweiten Ziel weicht ab: ' + str(kopie))
            ergebnis['zweites_ziel'] = str(kopie)
        else:
            ergebnis['zweites_ziel_hinweis'] = f'Zweites Ziel nicht erreichbar: {zweites.parent} fehlt (iCloud Drive nicht eingerichtet?).'
    z = store.lade_zentrale(); z['sicherung']['letzte'] = ergebnis; store.speichere_zentrale(z)
    return ergebnis

def _cloud_hinweis(pfad):
    p = str(pfad or '').replace('\\', '/')   # Windows-Pfade mit Schrägstrich vergleichen
    if 'com~apple~CloudDocs' in p or '/iCloud' in p or 'iCloudDrive' in p: return 'iCloud Drive: das Betriebssystem lädt die Kopie unverschlüsselt zu Apple hoch.'
    if any(t in p for t in ('Dropbox', 'OneDrive', 'Google Drive', 'GoogleDrive', 'Nextcloud')): return 'Synchronisierter Ordner: der Dienst des Anbieters lädt die Kopie hoch.'
    return ''

def status():
    """Letzte Sicherung mit Prüfung beider Archive, dazu die eingestellten Ziele mit Cloud-Hinweis (F19, F20)."""
    z = store.lade_zentrale(); l = z['sicherung'].get('letzte')
    ziele = {'ziel': z['sicherung'].get('ziel', ''), 'zweites_ziel_eingestellt': z['sicherung'].get('zweites_ziel', ''),
             'ziel_hinweis': _cloud_hinweis(z['sicherung'].get('ziel', '')), 'zweites_ziel_hinweis_cloud': _cloud_hinweis(z['sicherung'].get('zweites_ziel', ''))}
    if not l: return {'vorhanden': False, **ziele}
    p = Path(l['pfad']); vorhanden = p.is_file()
    erg = {**l, **ziele, 'vorhanden': vorhanden, 'unveraendert': vorhanden and p.stat().st_size == l['groesse'] and sha(p.read_bytes()) == l['sha256']}
    if l.get('zweites_ziel'):
        k = Path(l['zweites_ziel']); erg['zweites_ziel_vorhanden'] = k.is_file()
        erg['zweites_ziel_unveraendert'] = k.is_file() and k.stat().st_size == l['groesse'] and sha(k.read_bytes()) == l['sha256']
    return erg

def wiederherstellen(archiv, zielordner, erwartete_pruefsumme=None):
    """Archiv in einen neuen, leeren Ordner außerhalb des Projekts entpacken und dort prüfen. Liefert den Prüfbericht.
    Die laufende Mappe bleibt unberührt; der Nutzer entscheidet danach selbst, ob er den Ordner verwendet."""
    archiv = Path(archiv).expanduser().resolve(); ziel = Path(zielordner).expanduser().resolve(); root = Path(store.ROOT).resolve()
    if not archiv.is_file(): raise ValueError(f'Archiv fehlt: {archiv}')
    if ziel == root or root in ziel.parents or ziel in root.parents: raise ValueError('Der Prüfordner muss außerhalb des Projekts liegen.')
    if ziel.exists() and any(ziel.iterdir()): raise ValueError(f'Der Prüfordner ist nicht leer: {ziel}. Nichts wird überschrieben.')
    bericht = {'archiv': str(archiv), 'ordner': str(ziel), 'pruefsummendatei': None, 'dateien': 0, 'faelle': [], 'fehler': []}
    inhalt = archiv.read_bytes(); pruefsumme = sha(inhalt)
    sha_datei = archiv.with_suffix('.zip.sha256')
    if sha_datei.is_file():
        bericht['pruefsummendatei'] = sha_datei.read_text('utf-8').split()[0] == pruefsumme
        if not bericht['pruefsummendatei']: bericht['fehler'].append('Prüfsumme in der .sha256-Datei passt nicht zum Archiv.')
    if erwartete_pruefsumme and erwartete_pruefsumme != pruefsumme: bericht['fehler'].append('Archiv weicht von der in zentrale.json gemerkten Prüfsumme ab.')
    with zipfile.ZipFile(archiv) as zf:
        if zf.testzip(): bericht['fehler'].append('Archiv beschädigt (testzip).'); return bericht
        namen = zf.namelist()
        for n in namen:
            if n.startswith('/') or '..' in Path(n).parts: bericht['fehler'].append('Unzulässiger Pfad im Archiv: ' + n); return bericht
        ziel.mkdir(parents=True, exist_ok=True); zf.extractall(ziel); bericht['dateien'] = len(namen)
    zentrale = ziel / 'zentrale.json'
    if not zentrale.is_file(): bericht['fehler'].append('zentrale.json fehlt im Archiv.'); return bericht
    for eintrag in json.loads(zentrale.read_text('utf-8')).get('faelle', []):
        fall = {'fall': eintrag['id'], 'schema_fehler': [], 'geprueft': 0, 'veraendert': [], 'fehlend': []}
        ordner = ziel / eintrag['ordner']
        try: fall['schema_fehler'] = akte_schema.validate(json.loads((ordner / 'akte.json').read_text('utf-8')))[0]
        except Exception as e: fall['schema_fehler'] = [f'akte.json nicht lesbar: {e}']
        try: bestand = json.loads((ordner / 'bestand.json').read_text('utf-8'))
        except Exception as e: bestand = {'dateien': {}}; fall['schema_fehler'].append(f'bestand.json nicht lesbar: {e}')
        for k, e in bestand.get('dateien', {}).items():
            p = ordner / e['pfad']
            if not p.is_file(): fall['fehlend'].append(k)
            elif sha(p.read_bytes()) != e.get('sha256'): fall['veraendert'].append(k)   # sha256 = zuletzt gesehener Stand vor der Sicherung
            else: fall['geprueft'] += 1
        bericht['faelle'].append(fall)
        if fall['schema_fehler'] or fall['veraendert']: bericht['fehler'].append(f'{eintrag["id"]}: Schemafehler {len(fall["schema_fehler"])}, verändert {len(fall["veraendert"])}.')
        if fall['fehlend']: bericht.setdefault('hinweise', []).append(f'{eintrag["id"]}: {len(fall["fehlend"])} in bestand.json registrierte Datei(en) nicht im Archiv ({", ".join(fall["fehlend"][:5])}). Fehlten sie schon in der Mappe (server.py --check), ist das kein Sicherungsfehler.')
    bericht.setdefault('hinweise', [])
    bericht['bestanden'] = not bericht['fehler']
    return bericht

def probe(archiv=None):
    """Wiederherstellungsprobe der letzten (oder einer angegebenen) Sicherung in einem Zwischenordner, der danach wieder abgeräumt wird."""
    z = store.lade_zentrale(); l = z['sicherung'].get('letzte') or {}
    archiv = archiv or l.get('pfad')
    if not archiv: raise ValueError('Keine Sicherung vorhanden.')
    tmp = Path(tempfile.mkdtemp(prefix='aka-recht-wiederherstellung-'))
    try:
        bericht = wiederherstellen(archiv, tmp / 'Recht', l.get('sha256') if str(Path(archiv).resolve()) == str(Path(l.get('pfad', '')).resolve()) else None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)   # nur der eigene Zwischenordner, nie Projekt oder Sicherung
    bericht['ordner'] = 'Zwischenordner, nach der Probe entfernt'
    bericht['hinweis'] = 'Die Probe belegt, dass sich das Archiv vollständig entpacken lässt und Akten und Prüfsummen stimmen. Zum echten Wiederherstellen: server.py --restore <Archiv> <neuer Ordner>.'
    return bericht
