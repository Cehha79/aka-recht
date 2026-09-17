#!/usr/bin/env python3
"""Schema und Prüfung für akte.json (AKA Recht, Datenmodell Version 1).

Aufruf:   python3 "06 Werkzeuge/akte_schema.py" <Pfad zu akte.json>
Ausgabe:  Fehler (Datei ist ungültig) und Warnungen (Datei ist gültig, aber
          etwas fehlt oder ist unüblich). Exit 0 bei keinem Fehler.
Nur Standardbibliothek. Der Dienst (Stufe 3) nutzt validate() vor dem Speichern.
"""
import sys

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); Ausgaben für Assistenten und Tests müssen UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
import json, re, sys
from datetime import date
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
TEXTSTAND = ['direkt ausgelesen', 'OCR-erkannt', 'visuell geprüft', 'teilweise lesbar', 'nicht lesbar']   # was vom Dokument tatsächlich gelesen wurde (F34)
ZEITPUNKT = ['genau', 'ungefähr', 'zeitraum', 'unbekannt']   # Sicherheit des Ereigniszeitpunkts; datum bleibt Sortierdatum (F13)

KENNUNG = {
    'dokumente': r'D\d{4,}', 'beteiligte': r'P\d{2,}', 'verfahren': r'V\d{2,}',
    'ereignisse': r'E\d{2,}', 'fristen': r'F\d{2,}', 'aufgaben': r'A\d{2,}',
    'entwuerfe': r'W\d{2,}', 'notizen': r'N\d{2,}',
}
DATUM = re.compile(r'^\d{4}-\d{2}-\d{2}$')
MARKER = re.compile(r'\[(PRÜFEN|QUELLE|BELEG)\b[^\]]*\]?')   # offene Marker in Texten (REGELN Nr. 14)

def ereignis_sicher(e):
    """Wahr, wenn der Zeitpunkt des Ereignisses genau ist (kein zeitpunkt oder „genau“)."""
    return isinstance(e, dict) and (e.get('zeitpunkt') or 'genau') == 'genau'

def frist_eigenschaften(fr, akte=None):
    """Eigenschaften einer Frist (Prüfbericht 16.09.2026, F12 und F13), aus den Feldern abgeleitet:
    gerechnet  die Rechnung nennt das Fristende (bei Terminen nicht anwendbar, None)
    belegt     Quelle ist eine D-Kennung und der Auslöser ist benannt (Termin: Quelle genügt)
    geprueft   Prüfstatus bestätigt mit Prüfdatum (geprueft_am)
    ausloeser_sicher  das verknüpfte Auslöser-Ereignis (ausloeser_ereignis) hat einen genauen Zeitpunkt; ohne Verknüpfung None
    offene_marker  Marker [PRÜFEN …], [QUELLE …], [BELEG …] in Titel, Auslöser, Grundlage oder Rechnung."""
    if not isinstance(fr, dict): return {'gerechnet': None, 'belegt': False, 'geprueft': False, 'ausloeser_sicher': None, 'offene_marker': []}
    sicher = None
    if fr.get('ausloeser_ereignis') and isinstance(akte, dict):
        e = next((x for x in akte.get('ereignisse', []) if isinstance(x, dict) and x.get('id') == fr['ausloeser_ereignis']), None)
        sicher = ereignis_sicher(e) if e else False
    d = str(fr.get('datum', '')); termin = fr.get('art') == 'Termin'
    deutsch = f'{d[8:10]}.{d[5:7]}.{d[0:4]}' if DATUM.match(d) else ''
    rechnung = str(fr.get('berechnung', '') or '')
    gerechnet = None if termin else bool(d and (d in rechnung or (deutsch and deutsch in rechnung)))
    quelle = re.fullmatch(KENNUNG['dokumente'], str(fr.get('quelle', '') or '')) is not None
    belegt = quelle and (termin or bool(str(fr.get('ausloeser', '') or '').strip()))
    geprueft = fr.get('pruefstatus') == 'bestätigt' and bool(str(fr.get('geprueft_am', '') or '').strip())
    marker = [m.group(0) for feld in ('titel', 'ausloeser', 'rechtsgrundlage', 'berechnung') for m in MARKER.finditer(str(fr.get(feld, '') or ''))]
    return {'gerechnet': gerechnet, 'belegt': belegt, 'geprueft': geprueft, 'ausloeser_sicher': sicher, 'offene_marker': marker}

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
        'zaehler': {},   # höchste je vergebene Nummer je Kennungsart (P, V, E, F, A, W, N); entfernte Kennungen kommen nie wieder
    }

ZAEHLER_BUCHSTABEN = {'beteiligte': 'P', 'verfahren': 'V', 'ereignisse': 'E', 'fristen': 'F', 'aufgaben': 'A', 'entwuerfe': 'W', 'notizen': 'N'}

def naechste_kennung(akte, block):
    """Nächste freie Kennung eines Blocks und Zähler fortschreiben. Der Zähler merkt sich die höchste je
    vergebene Nummer, damit eine entfernte Kennung nie neu vergeben wird (Prüfbericht 16.09.2026, F11)."""
    b = ZAEHLER_BUCHSTABEN[block]; z = akte.setdefault('zaehler', {})
    hoechste = max([int(e['id'][1:]) for e in akte.get(block, []) if isinstance(e, dict) and re.fullmatch(b + r'\d+', str(e.get('id', '')))], default=0)
    n = max(int(z.get(b, 0) or 0), hoechste) + 1; z[b] = n
    return f'{b}{n:02d}'

def validate(akte):
    """Gibt (fehler, warnungen) als Listen von Sätzen zurück."""
    f, w = [], []
    def datum(wert, wo, pflicht=False):
        if wert in ('', None):
            if pflicht: f.append(f'{wo}: Datum fehlt.')
            return
        if not isinstance(wert, str) or not DATUM.match(wert):
            f.append(f'{wo}: Datum „{wert}“ nicht im Format JJJJ-MM-TT.'); return
        try: date.fromisoformat(wert)   # echter Kalendertag: 2026-02-31 oder Monat 13 fallen hier durch (Prüfbericht F10)
        except ValueError: f.append(f'{wo}: Datum „{wert}“ gibt es im Kalender nicht.')
    def zahl(wert): return isinstance(wert, (int, float)) and not isinstance(wert, bool)   # true zählt in Python als 1, hier nicht
    if not isinstance(akte, dict): return ['Akte ist kein Objekt.'], []
    if akte.get('schema') != SCHEMA_VERSION:
        f.append(f'schema muss {SCHEMA_VERSION} sein, ist {akte.get("schema")!r}.')
    for block in ['fall', 'beteiligte', 'dokumente', 'verfahren', 'ereignisse',
                  'fristen', 'aufgaben', 'entwuerfe', 'kosten', 'notizen', 'quellen']:
        if block not in akte: f.append(f'Block „{block}“ fehlt.')
    unbekannt = set(akte) - {'schema', 'fall', 'beteiligte', 'dokumente', 'verfahren',
                             'ereignisse', 'fristen', 'aufgaben', 'entwuerfe', 'kosten',
                             'notizen', 'quellen', 'zaehler'}
    if unbekannt: f.append('Unbekannte Blöcke: ' + ', '.join(sorted(unbekannt)) + '.')
    if not isinstance(akte.get('fall'), dict): f.append('fall muss ein Objekt sein.')
    if 'zaehler' in akte and not isinstance(akte['zaehler'], dict): f.append('zaehler muss ein Objekt sein.')
    if f: return f, w

    fall = akte['fall']
    if not re.fullmatch(r'R-\d{4,}', str(fall.get('id', ''))): f.append('fall.id muss wie R-0001 aussehen.')
    if not str(fall.get('titel', '')).strip(): f.append('fall.titel fehlt.')
    if fall.get('status') not in FALL_STATUS: f.append(f'fall.status muss eines von {FALL_STATUS} sein.')
    if fall.get('bereich') not in BEREICHE: w.append(f'fall.bereich „{fall.get("bereich")}“ ist kein bekannter Bereich.')
    if not isinstance(fall.get('themen', []), list): f.append('fall.themen muss eine Liste sein.')
    if not isinstance(fall.get('angeheftet', []), list): f.append('fall.angeheftet muss eine Liste sein.')
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
            if d.get('textstand') and d['textstand'] not in TEXTSTAND: f.append(f'{k}: textstand muss eines von {TEXTSTAND} sein.')
            datum(d.get('datum', ''), k)
            for feld in ('themen', 'personen', 'verweise'):
                if feld in d and not isinstance(d[feld], list): f.append(f'{k}: {feld} muss eine Liste sein.')
    for block in ['beteiligte', 'verfahren', 'ereignisse', 'fristen', 'aufgaben', 'entwuerfe', 'notizen']:
        if not isinstance(akte[block], list): f.append(f'{block} muss eine Liste sein.'); ids[block] = set()
        else: kennungen(block, akte[block])
    for block in ['kosten', 'quellen']:
        if not isinstance(akte[block], list): f.append(f'{block} muss eine Liste sein.')
        else:
            for i, e in enumerate(akte[block]):
                if not isinstance(e, dict): f.append(f'{block}[{i}]: kein Objekt.')
    # Zähler: optional (ältere Akten haben keinen), aber nie kleiner als die höchste vorhandene Kennung
    for block, b in ZAEHLER_BUCHSTABEN.items():
        wert = akte.get('zaehler', {}).get(b) if isinstance(akte.get('zaehler'), dict) else None
        if wert is None: continue
        if not isinstance(wert, int) or isinstance(wert, bool) or wert < 0: f.append(f'zaehler.{b} muss eine ganze Zahl ab 0 sein.'); continue
        hoechste = max([int(k[1:]) for k in ids.get(block, set())], default=0)
        if wert < hoechste: f.append(f'zaehler.{b} ist {wert}, aber {b}{hoechste:02d} existiert. Der Zähler darf nie zurückgehen.')
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
        # F13: unsichere Zeitpunkte sichtbar statt scheingenau; datum bleibt der Tag, an dem das Ereignis einsortiert wird
        zp = e.get('zeitpunkt', 'genau') or 'genau'
        if zp not in ZEITPUNKT: f.append(f'{e["id"]}: zeitpunkt muss eines von {ZEITPUNKT} sein.')
        datum(e.get('datum_bis', ''), f'{e["id"]}.datum_bis')
        if zp == 'zeitraum':
            if not e.get('datum_bis'): f.append(f'{e["id"]}: Zeitraum braucht datum_bis (Ende des Zeitraums).')
            elif DATUM.match(str(e.get('datum', ''))) and DATUM.match(str(e['datum_bis'])) and e['datum_bis'] < e['datum']: f.append(f'{e["id"]}: datum_bis liegt vor datum.')
        if zp == 'unbekannt' and not str(e.get('zeitpunkt_text', '')).strip(): f.append(f'{e["id"]}: Zeitpunkt unbekannt braucht zeitpunkt_text (was bekannt ist, etwa „vor dem Gespräch am …“); datum ist nur das Sortierdatum.')
        if zp == 'ungefähr' and not str(e.get('zeitpunkt_text', '')).strip(): w.append(f'{e["id"]}: Zeitpunkt ungefähr, zeitpunkt_text fehlt (woher die Schätzung stammt).')
        if 'zeitpunkt_text' in e and not isinstance(e['zeitpunkt_text'], str): f.append(f'{e["id"]}: zeitpunkt_text muss Text sein.')
    for fr in akte['fristen']:
        datum(fr.get('datum', ''), fr['id'], pflicht=True)
        if not str(fr.get('titel', '')).strip(): f.append(f'{fr["id"]}: titel fehlt.')
        if fr.get('art') not in FRIST_ART: f.append(f'{fr["id"]}: art muss eines von {FRIST_ART} sein.')
        if fr.get('pruefstatus') not in FRIST_STATUS: f.append(f'{fr["id"]}: pruefstatus muss eines von {FRIST_STATUS} sein.')
        verweis(fr.get('quelle', ''), 'dokumente', f'{fr["id"]}.quelle')
        verweis(fr.get('verfahren', ''), 'verfahren', f'{fr["id"]}.verfahren')                 # F13: fester Bezug statt Freitext
        verweis(fr.get('ausloeser_ereignis', ''), 'ereignisse', f'{fr["id"]}.ausloeser_ereignis')
        datum(fr.get('geprueft_am', ''), f'{fr["id"]}.geprueft_am')
        if 'geprueft_von' in fr and not isinstance(fr['geprueft_von'], str): f.append(f'{fr["id"]}: geprueft_von muss Text sein.')
        if fr.get('pruefstatus') == 'bestätigt':
            # F12: „bestätigt“ heißt gerechnet, belegt und ohne offene Marker; Prüfdatum fehlt nur als Warnung (ältere Akten)
            eig = frist_eigenschaften(fr, akte)
            if eig['ausloeser_sicher'] is False: f.append(f'{fr["id"]}: bestätigte Frist, aber das Auslöser-Ereignis {fr.get("ausloeser_ereignis")} hat keinen genauen Zeitpunkt. Erst klären, bis dahin offen oder vorsorglich.')
            if fr.get('art') == 'Termin':
                if not str(fr.get('quelle', '')).strip(): f.append(f'{fr["id"]}: bestätigter Termin ohne quelle (Ladung, Einladung oder Terminbestätigung). Erst Nachweis, dann Bestätigung.')
            else:
                for feld in ('ausloeser', 'rechtsgrundlage', 'berechnung', 'quelle'):
                    if not str(fr.get(feld, '')).strip():
                        f.append(f'{fr["id"]}: bestätigte Frist ohne {feld}. Erst Nachweis, dann Bestätigung.')
                if str(fr.get('berechnung', '')).strip() and eig['gerechnet'] is False:
                    f.append(f'{fr["id"]}: bestätigte Frist, aber die Rechnung nennt das Fristende {fr.get("datum")} nicht.')
            if eig['offene_marker']: f.append(f'{fr["id"]}: bestätigte Frist mit offenem Marker {eig["offene_marker"][0]}. Erst auflösen, dann bestätigen.')
            if not eig['geprueft']: w.append(f'{fr["id"]}: bestätigt ohne Prüfdatum (geprueft_am).')
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
        if not isinstance(e.get('fassung', 1), int) or isinstance(e.get('fassung', 1), bool) or e.get('fassung', 1) < 1: f.append(f'{e["id"]}: fassung muss eine ganze Zahl ab 1 sein.')
        if 'fassungen' in e:   # eingefrorene Fassungen (seit 17.09.2026, F28)
            if not isinstance(e['fassungen'], list): f.append(f'{e["id"]}: fassungen muss eine Liste sein.'); continue
            for i, x in enumerate(e['fassungen']):
                wo = f'{e["id"]}.fassungen[{i}]'
                if not isinstance(x, dict): f.append(f'{wo}: kein Objekt.'); continue
                if not isinstance(x.get('fassung'), int) or isinstance(x.get('fassung'), bool): f.append(f'{wo}: fassung fehlt oder ist keine Zahl.')
                if not re.fullmatch(r'[0-9a-f]{64}', str(x.get('sha256', ''))): f.append(f'{wo}: sha256 fehlt oder ist keine Prüfsumme.')
                if x.get('status') not in ENTWURF_STATUS: f.append(f'{wo}: status muss eines von {ENTWURF_STATUS} sein.')
                verweis(x.get('kopie_dokument', ''), 'dokumente', f'{wo}.kopie_dokument')
    for i, k in enumerate(akte['kosten']):
        datum(k.get('datum', ''), f'kosten[{i}]')
        if not zahl(k.get('betrag', 0)): f.append(f'kosten[{i}]: betrag muss eine Zahl sein.')
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
    try: akte = json.loads(Path(argv[1]).read_text('utf-8'))
    except FileNotFoundError: print('FEHLER    Datei nicht gefunden:', argv[1]); return 1
    except json.JSONDecodeError as e: print(f'FEHLER    Kein gültiges JSON (Zeile {e.lineno}, Spalte {e.colno}): {e.msg}.'); return 1
    fehler, warnungen = validate(akte)
    for s in fehler: print('FEHLER   ', s)
    for s in warnungen: print('Warnung  ', s)
    print(f'{len(fehler)} Fehler, {len(warnungen)} Warnungen.')
    return 1 if fehler else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
