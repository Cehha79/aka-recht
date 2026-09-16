#!/usr/bin/env python3
"""Schema und Prüfung für akte.json (AKA Recht, Datenmodell Version 1).

Aufruf:   python3 "06 Werkzeuge/akte_schema.py" <Pfad zu akte.json>
Ausgabe:  Fehler (Datei ist ungültig) und Warnungen (Datei ist gültig, aber
          etwas fehlt oder ist unüblich). Exit 0 bei keinem Fehler.
Nur Standardbibliothek. Der Dienst (Stufe 3) nutzt validate() vor dem Speichern.
"""
import sys
sys.dont_write_bytecode = True
import json, re, sys
from pathlib import Path

SCHEMA_VERSION = 1

# Feste Werte. "Vorgeschlagen" = frei erweiterbar, nur Warnung bei Abweichung.
FALL_STATUS = ['offen', 'ruhend', 'abgeschlossen']
BEREICHE = ['Arbeit', 'Verkehr und Bußgeld', 'Steuern und Abgaben', 'Behörden und Bescheide',
            'Sozialleistungen und Rente', 'Gesundheit und Pflege', 'Wohnen und Miete', 'Bauen und Nachbarn',
            'Verträge und Verbraucher', 'Forderungen und Inkasso', 'Versicherungen', 'Familie und Unterhalt',
            'Erbe und Vorsorge', 'Strafsachen und Anzeigen', 'Schule, Ausbildung und Studium', 'Aufenthalt und Staatsangehörigkeit',
            'Geschäft, Datenschutz und Internet', 'Vereine und Ehrenamt', 'Allgemein']   # 18 Bereiche plus Allgemein (seit 16.09.2026)
DOKUMENT_STAND = ['Original', 'Entwurf', 'Versandt', 'Zugegangen', 'Historisch', 'Vermerk']
DOKUMENT_ART_VORSCHLAG = ['Schreiben', 'E-Mail', 'Foto', 'Vertrag', 'Bescheid',
                          'Urteil', 'Entwurf', 'Beleg', 'Übersicht', 'Gesetz', 'Sonstiges']
BETEILIGTE_ROLLE_VORSCHLAG = ['Ich', 'Gegner', 'Gericht', 'Behörde', 'Anwalt',
                              'Zeuge', 'Stelle', 'Versicherung', 'Sonstige']
EREIGNIS_ART_VORSCHLAG = ['Zugang', 'Versand', 'Termin', 'Gespräch', 'Vorfall',
                          'Entscheidung', 'Vermerk', 'Arbeitsstand']
FRIST_ART = ['gesetzlich', 'selbst gesetzt', 'von Gegenseite gesetzt', 'vorsorglich', 'Termin']
FRIST_STATUS = ['offen', 'bestätigt', 'abgelaufen', 'erledigt']
ENTWURF_STATUS = ['in Arbeit', 'geprüft', 'versandt', 'verworfen']

KENNUNG = {
    'dokumente': r'D\d{4,}', 'beteiligte': r'P\d{2,}', 'verfahren': r'V\d{2,}',
    'ereignisse': r'E\d{2,}', 'fristen': r'F\d{2,}', 'aufgaben': r'A\d{2,}',
    'entwuerfe': r'W\d{2,}', 'notizen': r'N\d{2,}',
}
DATUM = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def leer():
    """Leere, gültige Akte für neue Fälle."""
    return {
        'schema': SCHEMA_VERSION,
        'fall': {'id': '', 'titel': '', 'untertitel': '', 'bereich': 'Allgemein',
                 'themen': [], 'rolle': '', 'ziel': '', 'rechtsordnung': 'DE',
                 'status': 'offen', 'angelegt': '', 'angeheftet': []},
        'beteiligte': [], 'dokumente': {}, 'verfahren': [], 'ereignisse': [],
        'fristen': [], 'aufgaben': [], 'entwuerfe': [], 'kosten': [],
        'notizen': [], 'quellen': [],
    }

def validate(akte):
    """Gibt (fehler, warnungen) als Listen von Sätzen zurück."""
    f, w = [], []
    def datum(wert, wo, pflicht=False):
        if wert in ('', None):
            if pflicht: f.append(f'{wo}: Datum fehlt.')
            return
        if not isinstance(wert, str) or not DATUM.match(wert):
            f.append(f'{wo}: Datum „{wert}“ nicht im Format JJJJ-MM-TT.')
    if not isinstance(akte, dict): return ['Akte ist kein Objekt.'], []
    if akte.get('schema') != SCHEMA_VERSION:
        f.append(f'schema muss {SCHEMA_VERSION} sein, ist {akte.get("schema")!r}.')
    for block in ['fall', 'beteiligte', 'dokumente', 'verfahren', 'ereignisse',
                  'fristen', 'aufgaben', 'entwuerfe', 'kosten', 'notizen', 'quellen']:
        if block not in akte: f.append(f'Block „{block}“ fehlt.')
    unbekannt = set(akte) - {'schema', 'fall', 'beteiligte', 'dokumente', 'verfahren',
                             'ereignisse', 'fristen', 'aufgaben', 'entwuerfe', 'kosten',
                             'notizen', 'quellen'}
    if unbekannt: f.append('Unbekannte Blöcke: ' + ', '.join(sorted(unbekannt)) + '.')
    if f: return f, w

    fall = akte['fall']
    if not re.fullmatch(r'R-\d{4,}', str(fall.get('id', ''))): f.append('fall.id muss wie R-0001 aussehen.')
    if not str(fall.get('titel', '')).strip(): f.append('fall.titel fehlt.')
    if fall.get('status') not in FALL_STATUS: f.append(f'fall.status muss eines von {FALL_STATUS} sein.')
    if fall.get('bereich') not in BEREICHE: w.append(f'fall.bereich „{fall.get("bereich")}“ ist kein bekannter Bereich.')
    if not isinstance(fall.get('themen', []), list): f.append('fall.themen muss eine Liste sein.')
    datum(fall.get('angelegt', ''), 'fall.angelegt')
    if not str(fall.get('rolle', '')).strip(): w.append('fall.rolle ist leer (eigene Rolle noch klären).')
    if not str(fall.get('ziel', '')).strip(): w.append('fall.ziel ist leer.')

    ids = {}
    def kennungen(block, eintraege):
        gesehen = set()
        for i, e in enumerate(eintraege):
            k = e.get('id') if isinstance(e, dict) else None
            if not isinstance(k, str) or not re.fullmatch(KENNUNG[block], k):
                f.append(f'{block}[{i}]: Kennung {k!r} passt nicht zu {KENNUNG[block]}.'); continue
            if k in gesehen: f.append(f'{block}: Kennung {k} doppelt.')
            gesehen.add(k)
        ids[block] = gesehen

    if not isinstance(akte['dokumente'], dict): f.append('dokumente muss ein Objekt mit D-Kennungen sein.')
    else:
        ids['dokumente'] = set()
        for k, d in akte['dokumente'].items():
            if not re.fullmatch(KENNUNG['dokumente'], k): f.append(f'dokumente: Kennung {k!r} ungültig.'); continue
            ids['dokumente'].add(k)
            if not isinstance(d, dict): f.append(f'{k}: kein Objekt.'); continue
            if not str(d.get('pfad', '')).strip(): f.append(f'{k}: pfad fehlt.')
            elif str(d['pfad']).startswith('/') or '..' in str(d['pfad']).split('/'): f.append(f'{k}: pfad muss relativ zum Fallordner sein.')
            if d.get('stand', 'Original') not in DOKUMENT_STAND: f.append(f'{k}: stand muss eines von {DOKUMENT_STAND} sein.')
            if d.get('art') and d['art'] not in DOKUMENT_ART_VORSCHLAG: w.append(f'{k}: art „{d["art"]}“ ist unüblich.')
            datum(d.get('datum', ''), k)
            for feld in ('themen', 'personen', 'verweise'):
                if feld in d and not isinstance(d[feld], list): f.append(f'{k}: {feld} muss eine Liste sein.')
    for block in ['beteiligte', 'verfahren', 'ereignisse', 'fristen', 'aufgaben', 'entwuerfe', 'notizen']:
        if not isinstance(akte[block], list): f.append(f'{block} muss eine Liste sein.'); ids[block] = set()
        else: kennungen(block, akte[block])
    for block in ['kosten', 'quellen']:
        if not isinstance(akte[block], list): f.append(f'{block} muss eine Liste sein.')
    if f: return f, w

    def verweis(wert, ziel, wo, pflicht=False):
        if wert in ('', None):
            if pflicht: f.append(f'{wo}: Verweis auf {ziel} fehlt.')
            return
        if wert not in ids.get(ziel, set()): f.append(f'{wo}: verweist auf {wert}, das gibt es in {ziel} nicht.')

    for k, d in akte['dokumente'].items():
        for p in d.get('personen', []): verweis(p, 'beteiligte', f'{k}.personen')
        for v in d.get('verweise', []): verweis(v, 'dokumente', f'{k}.verweise')
    for b in akte['beteiligte']:
        if not str(b.get('name', '')).strip(): f.append(f'{b["id"]}: name fehlt.')
        if b.get('rolle') and b['rolle'] not in BETEILIGTE_ROLLE_VORSCHLAG: w.append(f'{b["id"]}: rolle „{b["rolle"]}“ ist unüblich.')
    for v in akte['verfahren']:
        if not str(v.get('art', '')).strip(): f.append(f'{v["id"]}: art fehlt.')
        verweis(v.get('stelle', ''), 'beteiligte', f'{v["id"]}.stelle')
    for e in akte['ereignisse']:
        datum(e.get('datum', ''), e['id'], pflicht=True)
        if not str(e.get('titel', '')).strip(): f.append(f'{e["id"]}: titel fehlt.')
        if e.get('art') and e['art'] not in EREIGNIS_ART_VORSCHLAG: w.append(f'{e["id"]}: art „{e["art"]}“ ist unüblich.')
        verweis(e.get('quelle', ''), 'dokumente', f'{e["id"]}.quelle')
    for fr in akte['fristen']:
        datum(fr.get('datum', ''), fr['id'], pflicht=True)
        if not str(fr.get('titel', '')).strip(): f.append(f'{fr["id"]}: titel fehlt.')
        if fr.get('art') not in FRIST_ART: f.append(f'{fr["id"]}: art muss eines von {FRIST_ART} sein.')
        if fr.get('pruefstatus') not in FRIST_STATUS: f.append(f'{fr["id"]}: pruefstatus muss eines von {FRIST_STATUS} sein.')
        verweis(fr.get('quelle', ''), 'dokumente', f'{fr["id"]}.quelle')
        if fr.get('pruefstatus') == 'bestätigt' and fr.get('art') != 'Termin':
            for feld in ('ausloeser', 'rechtsgrundlage', 'berechnung', 'quelle'):
                if not str(fr.get(feld, '')).strip():
                    f.append(f'{fr["id"]}: bestätigte Frist ohne {feld}. Erst Nachweis, dann Bestätigung.')
        elif fr.get('pruefstatus') == 'offen':
            for feld in ('ausloeser', 'rechtsgrundlage'):
                if not str(fr.get(feld, '')).strip(): w.append(f'{fr["id"]}: {feld} fehlt noch.')
    for a in akte['aufgaben']:
        if not str(a.get('titel', '')).strip(): f.append(f'{a["id"]}: titel fehlt.')
        datum(a.get('faellig', ''), a['id'])
        if not isinstance(a.get('erledigt', False), bool): f.append(f'{a["id"]}: erledigt muss true oder false sein.')
        verweis(a.get('quelle', ''), 'dokumente', f'{a["id"]}.quelle')
    for e in akte['entwuerfe']:
        if not str(e.get('titel', '')).strip(): f.append(f'{e["id"]}: titel fehlt.')
        if e.get('status') not in ENTWURF_STATUS: f.append(f'{e["id"]}: status muss eines von {ENTWURF_STATUS} sein.')
        if e.get('status') == 'versandt': verweis(e.get('versandt_als', ''), 'dokumente', f'{e["id"]}.versandt_als', pflicht=True)
        if not isinstance(e.get('fassung', 1), int) or e.get('fassung', 1) < 1: f.append(f'{e["id"]}: fassung muss eine ganze Zahl ab 1 sein.')
    for i, k in enumerate(akte['kosten']):
        datum(k.get('datum', ''), f'kosten[{i}]')
        if not isinstance(k.get('betrag', 0), (int, float)): f.append(f'kosten[{i}]: betrag muss eine Zahl sein.')
        verweis(k.get('beleg', ''), 'dokumente', f'kosten[{i}].beleg')
    for n in akte['notizen']:
        if not str(n.get('titel', '')).strip() and not str(n.get('text', '')).strip(): f.append(f'{n["id"]}: leer.')
        datum(n.get('datum', ''), n['id'])
    for i, q in enumerate(akte['quellen']):
        if not str(q.get('titel', '')).strip(): f.append(f'quellen[{i}]: titel fehlt.')
        datum(q.get('geprueft', ''), f'quellen[{i}]')
    for p in fall.get('angeheftet', []): verweis(p, 'dokumente', 'fall.angeheftet')
    return f, w

def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    akte = json.loads(Path(argv[1]).read_text('utf-8'))
    fehler, warnungen = validate(akte)
    for s in fehler: print('FEHLER   ', s)
    for s in warnungen: print('Warnung  ', s)
    print(f'{len(fehler)} Fehler, {len(warnungen)} Warnungen.')
    return 1 if fehler else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
