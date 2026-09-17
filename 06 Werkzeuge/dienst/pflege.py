#!/usr/bin/env python3
"""Pflege der Rechtsinhalte (Stufe 12): welche mitgelieferten Inhalte wieder zu prüfen sind.

Liest nur, ohne Netz. Regeln aus DOKU/md/Rechtsinhalte.md Abschnitt 3:
  Merkblätter        zwölf Monate nach der Zeile „Letzte vollständige Prüfung: TT.MM.JJJJ“ im Kopf
  Feiertagstabelle   ab 1. Dezember, wenn im laufenden Jahr noch nicht fürs Folgejahr geprüft
                     (fristen.FEIERTAGE_GEPRUEFT)
  Quellenkatalog     sechs Monate nach catalog_checked je Eintrag in 04 Rechtsquellen/Quellen.md
„Bald fällig“ heißt: innerhalb von 30 Tagen. Teilweises Nachlesen zählt nicht als vollständige Prüfung.
Nur Standardbibliothek.
"""
import calendar, json, re
from datetime import date, timedelta
from pathlib import Path

VORLAUF_TAGE = 30
MERKBLATT_MUSTER = re.compile(r'Letzte vollständige Prüfung:\s*(\d{2})\.(\d{2})\.(\d{4})')

def monate_spaeter(d, monate):
    """Gleicher Tag n Monate später; fehlt der Tag (31., 29.02.), gilt der letzte des Monats."""
    jahr, monat = divmod(d.month - 1 + monate, 12)
    jahr += d.year; monat += 1
    return date(jahr, monat, min(d.day, calendar.monthrange(jahr, monat)[1]))

def _status(faellig_ab, stichtag):
    if stichtag >= faellig_ab: return 'fällig'
    if stichtag >= faellig_ab - timedelta(days=VORLAUF_TAGE): return 'bald fällig'
    return 'in Ordnung'

def _eintrag(art, name, zuletzt, faellig_ab, stichtag, hinweis=''):
    return {'art': art, 'name': name, 'zuletzt': zuletzt.isoformat(), 'faellig_ab': faellig_ab.isoformat(),
            'status': _status(faellig_ab, stichtag), 'hinweis': hinweis}

def _unbekannt(art, name, hinweis):
    return {'art': art, 'name': name, 'zuletzt': '', 'faellig_ab': '', 'status': 'unbekannt', 'hinweis': hinweis}

def merkblaetter(root, stichtag):
    ergebnis = []
    for p in sorted((root / '04 Rechtsquellen' / 'Verfahren').glob('*.md')):
        try:
            kopf = '\n'.join(p.read_text('utf-8').splitlines()[:15])
            m = MERKBLATT_MUSTER.search(kopf)
            if not m: ergebnis.append(_unbekannt('Merkblatt', p.name, 'Zeile „Letzte vollständige Prüfung: TT.MM.JJJJ“ fehlt im Kopf')); continue
            zuletzt = date(int(m[3]), int(m[2]), int(m[1]))
        except (OSError, UnicodeDecodeError, ValueError) as e:
            ergebnis.append(_unbekannt('Merkblatt', p.name, f'Datum nicht lesbar ({e})')); continue
        ergebnis.append(_eintrag('Merkblatt', p.name, zuletzt, monate_spaeter(zuletzt, 12), stichtag))
    return ergebnis

def feiertage(stichtag, geprueft_am):
    try: zuletzt = date.fromisoformat(geprueft_am)
    except (TypeError, ValueError): return [_unbekannt('Feiertage', 'Feiertagstabelle (fristen.py)', 'FEIERTAGE_GEPRUEFT fehlt oder ist kein Datum')]
    dezember = date(zuletzt.year, 12, 1)
    faellig_ab = dezember if zuletzt < dezember else date(zuletzt.year + 1, 12, 1)
    return [_eintrag('Feiertage', 'Feiertagstabelle (fristen.py)', zuletzt, faellig_ab, stichtag, f'Prüfung für das Jahr {faellig_ab.year + 1}')]

def quellenkatalog(root, stichtag):
    p = root / '04 Rechtsquellen' / 'Quellen.md'
    if not p.is_file(): return []
    try:
        text = p.read_text('utf-8')
        teil = text.split('<!-- RECHT:ANFANG -->', 1)[1].split('<!-- RECHT:ENDE -->', 1)[0].strip()
        liste = json.loads(teil.removeprefix('```json').removesuffix('```').strip())
    except (OSError, IndexError, ValueError) as e:
        return [_unbekannt('Quellenkatalog', 'Quellen.md', f'Katalog nicht lesbar ({e})')]
    ergebnis = []
    for q in liste:
        name = f"{q.get('id', '?')} {q.get('title', '')}".strip()
        try: zuletzt = date.fromisoformat(q.get('catalog_checked') or '')
        except ValueError: ergebnis.append(_unbekannt('Quellenkatalog', name, 'catalog_checked fehlt oder ist kein Datum')); continue
        ergebnis.append(_eintrag('Quellenkatalog', name, zuletzt, monate_spaeter(zuletzt, 6), stichtag))
    return ergebnis

def faelligkeiten(root, stichtag, feiertage_geprueft):
    root = Path(root)
    eintraege = merkblaetter(root, stichtag) + feiertage(stichtag, feiertage_geprueft) + quellenkatalog(root, stichtag)
    zahl = {s: sum(e['status'] == s for e in eintraege) for s in ('fällig', 'bald fällig', 'unbekannt', 'in Ordnung')}
    return {'stichtag': stichtag.isoformat(), 'faellig': zahl['fällig'], 'bald_faellig': zahl['bald fällig'],
            'unbekannt': zahl['unbekannt'], 'in_ordnung': zahl['in Ordnung'], 'eintraege': eintraege,
            'hinweis': 'Regeln in DOKU/md/Rechtsinhalte.md Abschnitt 3 und 4. Geprüft wird am amtlichen Volltext; danach die Datumsangabe an genau einer Stelle setzen.'}
