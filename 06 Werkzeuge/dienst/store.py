#!/usr/bin/env python3
"""Speicher des Dienstes: zentrale.json, akte.json je Fall, JOURNAL.md.

Schreibregeln: atomar (temporäre Datei, dann umbenennen), mit Sperre, und bei
akte.json nur mit Revision (Prüfsumme des Standes, den der Schreiber gelesen
hat). Vor jedem Schreiben von akte.json wird die alte Fassung außerhalb des
Projekts gesichert und die neue mit akte_schema geprüft.
Nur Standardbibliothek.
"""
import hashlib, json, os, re, shutil, stat, sys, tempfile, unicodedata, uuid
try: import fcntl   # macOS und Linux
except ImportError: fcntl = None; import msvcrt   # Windows
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import akte_schema

ROOT = Path(__file__).resolve().parents[2]
GRUPPEN = ['01 Eingang', '02 Grundlagen', '03 Schriftverkehr', '04 Verfahren',
           '05 Beweise', '06 Entwürfe', '07 Recherche', '08 Archiv']
VORLAGE = '05 Vorlagen/Fallvorlage'

MINDEST_PYTHON = (3, 12)

def python_hinweis():
    """Meldung, wenn die laufende Python-Fassung älter als die Mindestfassung ist, sonst ''. Ältere Fassungen
    scheitern nicht beim Start, sondern erst mitten in einem Ablauf (tomllib ab 3.11, Rückstrich im
    f-String ab 3.12); deshalb prüfen Dienst, cli.py, MCP-Server und Sitzungsstart vorher (AUDIT-004, 08.10.2026)."""
    if sys.version_info >= MINDEST_PYTHON: return ''
    return (f'AKA Recht braucht Python {MINDEST_PYTHON[0]}.{MINDEST_PYTHON[1]} oder neuer, gestartet wurde '
            f'{sys.version.split()[0]} ({sys.executable}). Neuere Fassung von python.org installieren und '
            'dafür sorgen, dass „python3“ (Windows: „python“) auf sie zeigt.')

def konfigurieren(root, schluessel_datei=None):
    global ROOT
    ROOT = Path(root).resolve()

def sha(daten): return hashlib.sha256(daten).hexdigest()
def instanz(): return sha(str(ROOT).encode())[:14]

def sicher(relativ, basis=None):
    """Pfad innerhalb des Projekts (oder eines Fallordners); keine Verknüpfungen, kein Ausbruch."""
    basis = Path(basis) if basis else ROOT
    p = (basis / relativ)
    aufgeloest = p.resolve()
    if aufgeloest != basis.resolve() and basis.resolve() not in aufgeloest.parents:
        raise ValueError('Pfad außerhalb des erlaubten Ordners.')
    for teil in [p, *p.parents]:
        if teil == basis.parent: break
        if teil.is_symlink(): raise ValueError('Symbolische Verknüpfung nicht zugelassen.')
    return aufgeloest

def atomar(pfad, daten):
    roh = daten if isinstance(daten, bytes) else daten.encode('utf-8')
    pfad = Path(pfad); pfad.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.schreiben-', dir=pfad.parent)
    try:
        with os.fdopen(fd, 'wb') as f: f.write(roh); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, pfad)
    finally:
        if Path(tmp).exists(): Path(tmp).unlink()

def laufzeit_ordner():
    """Eigener Ordner für Sperr-, Laufzeit- und Protokolldatei, nur für diesen Benutzer (Rechte 0700). Vorher lagen die
    Dateien unter festen Namen direkt im System-Temp-Ordner; unter Linux ist das meist das gemeinsame /tmp, und ein
    anderes Konto hätte sie vorab anlegen können (AUDIT-007, 08.10.2026). Unter Linux bevorzugt $XDG_RUNTIME_DIR."""
    xdg = os.environ.get('XDG_RUNTIME_DIR')
    basis = Path(xdg) if xdg and Path(xdg).is_dir() else Path(tempfile.gettempdir())
    uid = os.getuid() if hasattr(os, 'getuid') else None   # Windows: Temp-Ordner liegt ohnehin im Benutzerprofil
    ordner = basis / (f'aka-recht-{uid}' if uid is not None else 'aka-recht')
    try: ordner.mkdir(mode=0o700)
    except FileExistsError: pass
    if uid is not None:
        s = os.lstat(ordner)
        if not stat.S_ISDIR(s.st_mode) or s.st_uid != uid or s.st_mode & 0o077:
            raise RuntimeError(f'Laufzeitordner {ordner} ist kein eigener Ordner dieses Benutzers mit Rechten 0700. '
                               'Bitte prüfen und entfernen; AKA Recht legt ihn beim nächsten Start neu an.')
    return ordner

@contextmanager
def sperre(*, start=False):
    """Startversuche getrennt von Datenänderungen sperren: der Kinddienst braucht die Datensperre."""
    datei = laufzeit_ordner() / f'{"start-" if start else ""}{instanz()}.lock'
    with datei.open('a+') as f:
        if fcntl: fcntl.flock(f, fcntl.LOCK_EX)
        else: f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)   # Windows: ein Byte sperren, wartet bis frei
        try: yield
        finally:
            if fcntl: fcntl.flock(f, fcntl.LOCK_UN)
            else: f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

# ---------------------------------------------------------------- zentrale
ABSENDER_FELDER = ('name', 'strasse', 'plz_ort', 'telefon', 'email')   # Standard-Absender für Entwürfe (Einstellungen, bleibt lokal)

def zentrale_standard():
    return {'schema': 1, 'app': 'AKA Recht', 'faelle': [],
            'sicherung': {'ziel': str(Path.home() / 'Desktop/AKA Recht Sicherungen'),
                          'zweites_ziel': '',   # ab Werk leer: eine Sicherung geht nur nach ausdrücklicher Wahl in den Einstellungen in einen Cloud-Ordner (AUDIT-003, 08.10.2026; vorher iCloud Drive, wo vorhanden)
                          'letzte': None},
            'einstellungen': {'feiertagsland': 'BW', 'sprache': 'de', 'absender': dict.fromkeys(ABSENDER_FELDER, '')},
            'verbindungen': {}}

# Sprache der Oberfläche (Stufe 11): je Sprache eine Datei `oberflaeche/sprachen/<kürzel>.json` mit den Texten
# und `anleitung.<kürzel>.html` mit der Anleitung. Vorhanden ist, was als Datei da liegt; Standard und Rückfall ist Deutsch.
SPRACHEN_ORDNER = Path(__file__).resolve().parent.parent / 'oberflaeche' / 'sprachen'
SPRACHE_MUSTER = re.compile(r'^[a-z]{2}$')

def sprachen():
    """Kürzel aller Sprachen, für die eine Textdatei vorliegt, alphabetisch; Deutsch immer zuerst."""
    vorhanden = sorted(p.stem for p in SPRACHEN_ORDNER.glob('*.json') if SPRACHE_MUSTER.match(p.stem)) if SPRACHEN_ORDNER.is_dir() else []
    return ['de'] + [s for s in vorhanden if s != 'de'] if 'de' in vorhanden or not vorhanden else vorhanden

def sprache():
    """Eingestellte Sprache; fehlt ihre Datei, Deutsch."""
    s = str(lade_zentrale()['einstellungen'].get('sprache') or 'de').lower()
    return s if s in sprachen() else 'de'

def zentrale_pfad(): return ROOT / 'zentrale.json'

def eingerichtet(): return zentrale_pfad().exists()

def einrichten():
    """Legt zentrale.json an, wenn sie fehlt. Nur beim Start des Dienstes (Einrichtung durch den Nutzer),
    nie beim bloßen Lesen. Liefert True, wenn die Datei neu angelegt wurde."""
    p = zentrale_pfad()
    with sperre():
        if p.exists(): return False
        atomar(p, json.dumps(zentrale_standard(), ensure_ascii=False, indent=2, allow_nan=False) + '\n'); return True

def lade_zentrale():
    """Liest zentrale.json; fehlt sie, den Standard nur im Speicher (schreibt nichts, Prüfbericht F03)."""
    p = zentrale_pfad()
    z = akte_schema.json_laden(p.read_text('utf-8')) if p.exists() else zentrale_standard()
    z.setdefault('einstellungen', {}).setdefault('feiertagsland', 'BW')   # ältere zentrale.json
    z['einstellungen'].setdefault('sprache', 'de')
    a = z['einstellungen'].setdefault('absender', {})
    for k in ABSENDER_FELDER: a.setdefault(k, '')
    return z

def absender(fall_id=None):
    """Absender für Entwürfe: der Beteiligte mit Rolle „Ich“ des Falls (Name, Anschrift, Kontakt) gewinnt,
    sonst der Standard aus den Einstellungen. Liefert die Felder, eine fertige Zeile und die Herkunft."""
    a = {k: str(v or '').strip() for k, v in lade_zentrale()['einstellungen']['absender'].items()}
    zeile = ', '.join(x for x in (a['name'], a['strasse'], a['plz_ort'], a['telefon'], a['email']) if x)
    ergebnis = {**a, 'zeile': zeile, 'quelle': 'Einstellungen' if zeile else ''}
    if fall_id:
        akte, _ = lese_akte(fall_id)
        ich = next((p for p in akte['beteiligte'] if p.get('rolle') == 'Ich' and str(p.get('name', '')).strip()), None)
        if ich and (str(ich.get('anschrift', '')).strip() or not zeile):
            teile = [str(ich.get(k, '')).strip() for k in ('name', 'anschrift', 'kontakt')]
            ergebnis = {'name': teile[0], 'strasse': '', 'plz_ort': teile[1], 'telefon': '', 'email': teile[2],
                        'zeile': ', '.join(x for x in teile if x), 'quelle': f'Beteiligter {ich["id"]} (Rolle Ich)'}
    return ergebnis

def feiertagsland(): return lade_zentrale()['einstellungen'].get('feiertagsland') or 'BW'

def speichere_zentrale(z):
    """Nur unter sperre() mit frisch gelesenem Stand aufrufen; von außen über zentrale_aendern."""
    atomar(zentrale_pfad(), json.dumps(z, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

def zentrale_aendern(aendern):
    """Einziger Weg, zentrale.json von außerhalb dieses Moduls zu ändern: unter Sperre frisch lesen,
    aendern(z) anwenden, schreiben. Vorher lasen Einstellungen und Sicherung ohne Sperre und schrieben den
    alten Stand zurück; ein Fall, der dazwischen angelegt wurde, verschwand aus dem Verzeichnis (AUDIT-001,
    08.10.2026). aendern darf selbst nicht sperren, die Sperre ist nicht wiedereintrittsfähig."""
    with sperre():
        z = lade_zentrale(); ergebnis = aendern(z); speichere_zentrale(z)
    return ergebnis

def verwaiste_faelle():
    """Fallordner mit akte.json unter 02 Fälle, die in zentrale.json fehlen (Folge eines früheren Wettlaufs,
    AUDIT-001, oder eines Abbruchs). Nur lesen; Eintragen bleibt Sache des Nutzers."""
    ordner = ROOT / '02 Fälle'
    if not ordner.is_dir(): return []
    bekannt = {unicodedata.normalize('NFC', f['ordner']) for f in faelle()}
    return sorted(p.name for p in ordner.iterdir() if p.is_dir() and re.match(r'R-\d+', p.name) and (p / 'akte.json').is_file()
                  and unicodedata.normalize('NFC', f'02 Fälle/{p.name}') not in bekannt)

def sicherungsziel(): return Path(lade_zentrale()['sicherung']['ziel']).expanduser()

def sicherungsziele_pruefen(werte):
    """Übergebene Ziele prüfen, ohne Ordner anzulegen oder Einstellungen zu ändern (AUDIT-20261008-008)."""
    if not isinstance(werte, dict): raise ValueError('Sicherungseinstellungen müssen ein Objekt sein.')
    geprueft = {}
    for feld in ('ziel', 'zweites_ziel'):
        if feld not in werte: continue
        wert = werte[feld]
        name = 'Sicherungsziel' if feld == 'ziel' else 'Zweites Sicherungsziel'
        if not isinstance(wert, str): raise ValueError(f'{name}: Bitte einen Ordnerpfad als Text angeben.')
        if any(ord(c) < 32 or ord(c) == 127 for c in wert):
            raise ValueError(f'{name}: Der Pfad darf keine Steuerzeichen enthalten.')
        wert = wert.strip()
        if not wert:
            if feld == 'ziel': raise ValueError('Sicherungsziel darf nicht leer sein.')
            geprueft[feld] = ''; continue
        try:
            pfad = Path(wert).expanduser()
            if not pfad.is_absolute(): raise ValueError(f'{name}: Bitte einen vollständigen Ordnerpfad oder ~/… angeben.')
            pfad = pfad.resolve()
            if pfad == ROOT or ROOT in pfad.parents:
                raise ValueError(f'{name} muss außerhalb des Projekts liegen.')
            if any(p.exists() and not p.is_dir() for p in (pfad, *pfad.parents)):
                raise ValueError(f'{name}: Der Pfad führt zu einer Datei statt zu einem Ordner.')
        except (OSError, RuntimeError):
            raise ValueError(f'{name}: Der Ordnerpfad konnte nicht geprüft werden. Bitte Pfad und Zugriff prüfen.') from None
        geprueft[feld] = wert
    return geprueft

def faelle(): return lade_zentrale()['faelle']

def fall_eintrag(fall_id):
    if not re.fullmatch(r'R-\d{4,}', str(fall_id)): raise ValueError('Ungültige Fallkennung.')
    e = next((f for f in faelle() if f['id'] == fall_id), None)
    if not e: raise ValueError(f'Unbekannter Fall {fall_id}.')
    if not e['ordner'].startswith('02 Fälle/' + fall_id + ' '): raise ValueError('Ungültige Fallablage.')
    return e

def fall_ordner(fall_id): return sicher(fall_eintrag(fall_id)['ordner'])

# ---------------------------------------------------------------- akte
def lese_akte(fall_id):
    roh = (fall_ordner(fall_id) / 'akte.json').read_bytes()
    return akte_schema.json_laden(roh.decode('utf-8')), sha(roh)

def speichere_akte(fall_id, akte, revision, ohne_sicherung=False, hinfaellig=None):
    """Schreibt akte.json nur, wenn revision zum aktuellen Stand passt. Liefert neue Revision.
    hinfaellig: von einem Werkzeug bereits ermittelte Liste zurückgesetzter Fristen (N02),
    damit der Journaleintrag auch dann entsteht, wenn die Nachprüfung schon dort lief."""
    ordner = fall_ordner(fall_id); pfad = ordner / 'akte.json'
    if akte.get('fall', {}).get('id') != fall_id: raise ValueError('Fallkennung in der Akte passt nicht zum Fall.')
    # N02: Eine Bestätigung gilt nur für den geprüften Stand. Hier, weil jeder Weg
    # (Oberfläche, cli.py, MCP) durch diese Funktion läuft.
    zurueckgesetzt = list(hinfaellig or []) + akte_schema.fristen_nachpruefen(akte)
    fehler, _ = akte_schema.validate(akte)
    if fehler: raise ValueError('Akte nicht gespeichert: ' + ' '.join(fehler[:5]))
    with sperre():
        alt = pfad.read_bytes()
        if sha(alt) != revision: raise RuntimeError('Die Akte wurde inzwischen an anderer Stelle geändert. Bitte neu laden.')
        # Derselbe gesperrte Stand liefert Revision und historische Kennungszähler.
        # Vor Sicherung und Schreiben prüfen; ältere Clients dürfen Zähler weglassen.
        akte_schema.zaehler_bewahren(akte, akte_schema.json_laden(alt.decode('utf-8')))
        neu = json.dumps(akte, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        if not ohne_sicherung:
            ablage = sicherungsziel() / 'Ordnungsstände' / fall_id
            ablage.mkdir(parents=True, exist_ok=True)
            kopie = ablage / (datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_' + uuid.uuid4().hex[:8] + '_akte.json')
            with kopie.open('xb') as f: f.write(alt)
            kopie.chmod(0o600)
        atomar(pfad, neu)
        revision_neu = sha(neu.encode('utf-8'))
    if zurueckgesetzt:   # außerhalb der Sperre: journal_anhaengen sperrt selbst (sonst wartet der Prozess auf sich)
        try:
            journal_anhaengen(fall_id, 'Vermerk', 'Fristbestätigung hinfällig',
                              'Die Grundlagen haben sich geändert; die Bestätigung gilt nicht mehr für '
                              + ', '.join(f'{z["id"]} ({z["titel"]})' for z in zurueckgesetzt)
                              + '. Prüfstatus steht wieder auf offen, die Rechnung trägt einen Marker [PRÜFEN].')
        except Exception:
            pass   # der Hinweis steht schon in der Akte selbst; ein Journal-Fehler darf das Speichern nicht nachträglich zerreißen
    return revision_neu

def neuer_fall(titel, bereich='Allgemein', rolle='', ziel=''):
    titel = str(titel or '').strip()
    if not titel or len(titel) > 120 or any(ord(c) < 32 for c in titel): raise ValueError('Bitte eine kurze Fallbezeichnung angeben.')
    with sperre():
        z = lade_zentrale()
        nummern = [int(f['id'].split('-')[1]) for f in z['faelle']]
        ordner_faelle = sicher('02 Fälle'); ordner_faelle.mkdir(exist_ok=True)
        nummern += [int(m[1]) for p in ordner_faelle.iterdir() if (m := re.match(r'R-(\d+)', p.name))]
        kennung = 'R-' + str(max(nummern, default=0) + 1).zfill(4)
        name = re.sub(r'[^\w äöüÄÖÜß.-]', '', titel).strip(' .')[:65] or 'Vorgang'
        rel = f'02 Fälle/{kennung} {name}'; ziel_ordner = sicher(rel)
        vorlage = sicher(VORLAGE)
        if vorlage.exists(): shutil.copytree(vorlage, ziel_ordner, ignore=shutil.ignore_patterns('.DS_Store'))
        else: ziel_ordner.mkdir()
        for g in GRUPPEN: (ziel_ordner / g).mkdir(exist_ok=True)   # immer, auch wenn die Vorlage ohne leere Ordner kam (git überträgt keine, Prüfbericht F09)
        akte = akte_schema.leer()
        akte['fall'].update({'id': kennung, 'titel': titel, 'bereich': bereich or 'Allgemein', 'rolle': rolle or '',
                             'ziel': ziel or '', 'angelegt': datetime.now().date().isoformat()})
        atomar(ziel_ordner / 'akte.json', json.dumps(akte, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
        if not (ziel_ordner / 'bestand.json').exists():
            atomar(ziel_ordner / 'bestand.json', json.dumps({'schema': 1, 'dateien': {}, 'verschiebungen': []}, ensure_ascii=False, indent=2) + '\n')
        if not (ziel_ordner / 'JOURNAL.md').exists():
            atomar(ziel_ordner / 'JOURNAL.md', '# Journal\n\nVerlauf dieses Falls. Nur anhängen, nie umschreiben.\n\n')
        z['faelle'].append({'id': kennung, 'ordner': rel}); speichere_zentrale(z)
    journal_anhaengen(kennung, 'Arbeit', 'Fall angelegt', f'Fall {kennung} „{titel}“ angelegt. Bereich: {bereich or "Allgemein"}.')
    return {'id': kennung, 'ordner': rel}

BEISPIEL = '05 Vorlagen/Beispielakte'

def beispiel_laden():
    """Kopiert die mitgelieferte Beispielakte als neuen Fall mit der nächsten freien Kennung."""
    quelle = sicher(BEISPIEL)
    if not (quelle / 'akte.json').exists(): raise ValueError('Keine Beispielakte unter ' + BEISPIEL + '.')
    with sperre():
        z = lade_zentrale()
        nummern = [int(f['id'].split('-')[1]) for f in z['faelle']]
        ordner_faelle = sicher('02 Fälle'); ordner_faelle.mkdir(exist_ok=True)
        nummern += [int(m[1]) for p in ordner_faelle.iterdir() if (m := re.match(r'R-(\d+)', p.name))]
        kennung = 'R-' + str(max(nummern, default=0) + 1).zfill(4)
        akte = akte_schema.json_laden((quelle / 'akte.json').read_text('utf-8'))
        titel = akte['fall'].get('titel') or 'Beispielfall'
        name = re.sub(r'[^\w äöüÄÖÜß.-]', '', titel).strip(' .')[:65] or 'Beispiel'
        rel = f'02 Fälle/{kennung} {name}'; ziel_ordner = sicher(rel)
        akte['fall']['id'] = kennung; akte['fall']['angelegt'] = datetime.now().date().isoformat()
        fehler, _ = akte_schema.validate(akte)   # erst prüfen, dann kopieren: sonst bliebe ein Ordner ohne Eintrag (AUDIT-012)
        if fehler: raise ValueError('Beispielakte fehlerhaft: ' + '; '.join(fehler[:3]))
        shutil.copytree(quelle, ziel_ordner, ignore=shutil.ignore_patterns('.DS_Store'))
        for g in GRUPPEN: (ziel_ordner / g).mkdir(exist_ok=True)
        atomar(ziel_ordner / 'akte.json', json.dumps(akte, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
        if not (ziel_ordner / 'JOURNAL.md').exists(): atomar(ziel_ordner / 'JOURNAL.md', '# Journal\n\n')
        z['faelle'].append({'id': kennung, 'ordner': rel}); speichere_zentrale(z)
    journal_anhaengen(kennung, 'Arbeit', 'Beispielfall geladen', f'Beispielakte als {kennung} übernommen. Erfundener Fall zum Ausprobieren.')
    return {'id': kennung, 'ordner': rel, 'titel': titel}

def fall_status(fall_id, status):
    akte, rev = lese_akte(fall_id)
    if status not in akte_schema.FALL_STATUS: raise ValueError('Unbekannter Fallstatus.')
    akte['fall']['status'] = status
    return speichere_akte(fall_id, akte, rev)

# ---------------------------------------------------------------- journal
JOURNAL_ARTEN = ['Eingang', 'Versand', 'Entscheidung', 'Gespräch', 'Termin', 'Arbeit', 'Vermerk']

def journal_anhaengen(fall_id, art, titel, text):
    if art not in JOURNAL_ARTEN: raise ValueError('Journal-Art muss eine von ' + ', '.join(JOURNAL_ARTEN) + ' sein.')
    titel = ' '.join(str(titel).split()); text = str(text).strip()
    if not titel: raise ValueError('Journal-Eintrag braucht einen Kurztitel.')
    if '\n## ' in '\n' + text: raise ValueError('Der Text darf keine eigene Eintragsüberschrift enthalten.')
    pfad = fall_ordner(fall_id) / 'JOURNAL.md'
    with sperre():
        alt = pfad.read_text('utf-8') if pfad.exists() else '# Journal\n\n'
        eintrag = f'## {datetime.now().date().isoformat()} · {art} · {titel}\n{text}\n\n'
        atomar(pfad, alt.rstrip('\n') + '\n\n' + eintrag)
    return {'datum': datetime.now().date().isoformat(), 'art': art, 'titel': titel}

def journal_lesen(fall_id):
    pfad = fall_ordner(fall_id) / 'JOURNAL.md'
    if not pfad.exists(): return []
    eintraege = []
    for block in re.split(r'\n(?=## )', pfad.read_text('utf-8')):
        m = re.match(r'## (\d{4}-\d{2}-\d{2}) · ([^·\n]+) · (.+)\n?([\s\S]*)', block)
        if m: eintraege.append({'datum': m[1], 'art': m[2].strip(), 'titel': m[3].strip(), 'text': m[4].strip()})
    return eintraege
