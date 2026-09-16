#!/usr/bin/env python3
"""Werkzeugkatalog: jede Funktion des Dienstes einmal beschrieben, mit
Parametern, Kennzeichen lesend/schreibend und Ausführung.

Oberfläche, Befehlszeile und angebundene KI-Assistenten rufen dieselben
Werkzeuge. Schreibende Werkzeuge laufen für Assistenten nur mit Bestätigung. Werkzeuge für Versand,
Löschen oder Ändern von Originalen gibt es absichtlich nicht.
Nur Standardbibliothek.
"""
import json, re, shutil, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import akte_schema, bestand, dokumente, fristen, sicherung, store

KATALOG = []

def werkzeug(name, beschreibung, parameter, schreibend=False, pflicht=None, ki=True):
    def deko(fn):
        schema = {'type': 'object', 'properties': parameter, 'required': pflicht or [], 'additionalProperties': False}
        KATALOG.append({'name': name, 'beschreibung': beschreibung, 'parameter': schema, 'schreibend': schreibend, 'ki': ki, 'fn': fn})
        return fn
    return deko

def beschreibung():
    """Katalog ohne Funktionen, für Oberfläche und KI."""
    return [{k: v for k, v in w.items() if k != 'fn'} for w in KATALOG]

def finde(name):
    w = next((w for w in KATALOG if w['name'] == name), None)
    if not w: raise ValueError(f'Unbekanntes Werkzeug „{name}“.')
    return w

def _pruefe_parameter(w, args):
    if not isinstance(args, dict): raise ValueError('Parameter müssen ein Objekt sein.')
    erlaubt = w['parameter']['properties']
    fremd = set(args) - set(erlaubt)
    if fremd: raise ValueError('Unbekannte Parameter: ' + ', '.join(sorted(fremd)))
    for p in w['parameter']['required']:
        if p not in args or args[p] in ('', None): raise ValueError(f'Parameter „{p}“ fehlt. Erhalten: {", ".join(sorted(args)) or "keine"}. Erwartet: {", ".join(w["parameter"]["required"])}.')
    for p, wert in list(args.items()):
        typ = erlaubt[p].get('type')
        # Sprachmodelle liefern Zahlen und Wahrheitswerte oft als Text: verständlich umwandeln
        if typ == 'integer' and isinstance(wert, str) and wert.strip().lstrip('-').isdigit(): args[p] = wert = int(wert.strip())
        if typ == 'boolean' and isinstance(wert, str) and wert.strip().lower() in ('true', 'false', 'ja', 'nein'): args[p] = wert = wert.strip().lower() in ('true', 'ja')
        if typ == 'string' and isinstance(wert, (int, float)) and not isinstance(wert, bool): args[p] = wert = str(wert)
        if typ == 'string' and not isinstance(wert, str): raise ValueError(f'„{p}“ muss Text sein.')
        if typ == 'integer' and not (isinstance(wert, int) and not isinstance(wert, bool)): raise ValueError(f'„{p}“ muss eine ganze Zahl sein.')
        if typ == 'boolean' and not isinstance(wert, bool): raise ValueError(f'„{p}“ muss true oder false sein.')
        if typ == 'array' and not isinstance(wert, list): raise ValueError(f'„{p}“ muss eine Liste sein.')
        if typ == 'object' and not isinstance(wert, dict): raise ValueError(f'„{p}“ muss ein Objekt sein.')
        if 'enum' in erlaubt[p] and wert not in erlaubt[p]['enum']: raise ValueError(f'„{p}“ muss eines von {erlaubt[p]["enum"]} sein.')

def ausfuehren(name, args, bestaetigt=False):
    """Führt ein Werkzeug aus. Schreibende Werkzeuge nur mit bestaetigt=True.

    Als Bestätigung zählt allein der JSON-Wahrheitswert true. Text („true“, „false“), Zahlen oder null
    werden abgewiesen, denn bool("false") wäre wahr (Prüfbericht 16.09.2026, F05)."""
    w = finde(name); args = dict(args or {})
    if not isinstance(bestaetigt, bool):
        raise ValueError(f'„bestaetigt“ muss der JSON-Wahrheitswert true oder false sein, kein Text und keine Zahl. Erhalten: {json.dumps(bestaetigt, ensure_ascii=False)}.')
    _pruefe_parameter(w, args)
    if w['schreibend'] and not bestaetigt:
        return {'bestaetigung_noetig': True, 'werkzeug': name, 'parameter': args,
                'hinweis': 'Dieses Werkzeug ändert Daten. Bitte bestätigen.'}
    return w['fn'](**args)

# ---------------------------------------------------------------- lesend
# Lesende Werkzeuge schreiben nichts: weder akte.json noch bestand.json noch zentrale.json (Prüfbericht 16.09.2026, F03).
# Neue oder verschobene Dateien melden sie als Abweichung; registriert werden sie erst durch bestand_abgleichen.
ABGLEICH_HINWEIS = 'Nicht erfasste Dateien bekommen ihre Kennung erst durch das schreibende Werkzeug bestand_abgleichen.'

@werkzeug('faelle_auflisten', 'Alle Fälle mit Kennung, Titel, Bereich, Status, Zahl der Dokumente, nicht erfassten Dateien und offenen Aufgaben.', {})
def faelle_auflisten():
    zeilen = []
    for e in store.faelle():
        try:
            akte, _ = store.lese_akte(e['id']); f = akte['fall']
            vorhanden, abweichungen = bestand.abgleich(store.fall_ordner(e['id']))
            zeilen.append({'id': e['id'], 'titel': f['titel'], 'bereich': f['bereich'], 'status': f['status'], 'rolle': f['rolle'],
                           'dokumente': len(vorhanden), 'nicht_erfasst': len(abweichungen['nicht_erfasst']), 'offene_aufgaben': sum(not a['erledigt'] for a in akte['aufgaben']),
                           'fristen_offen': sum(fr['pruefstatus'] != 'erledigt' for fr in akte['fristen']),
                           'fristen': [{'id': fr['id'], 'datum': fr['datum'], 'titel': fr['titel'], 'art': fr['art'], 'pruefstatus': fr['pruefstatus'], 'eigenschaften': akte_schema.frist_eigenschaften(fr)} for fr in akte['fristen'] if fr['pruefstatus'] != 'erledigt']})
        except Exception as ex:
            zeilen.append({'id': e['id'], 'titel': e['id'], 'fehler': str(ex)})
    return zeilen

@werkzeug('fall_lesen', 'Die vollständige Akte eines Falls (akte.json) mit Dokumentliste und Revision. Groß; für die KI gibt es fall_uebersicht.',
          {'fall': {'type': 'string', 'description': 'Fallkennung wie R-0001'}}, pflicht=['fall'], ki=False)
def fall_lesen(fall):
    akte, rev = store.lese_akte(fall)
    liste, ergaenzt, abweichungen = dokumente.katalog(fall, akte)
    return {'akte': akte, 'revision': rev, 'dokumente': liste, 'ergaenzt': ergaenzt, 'abweichungen': abweichungen,
            'journal': store.journal_lesen(fall), 'ordner': store.fall_eintrag(fall)['ordner']}

@werkzeug('fall_uebersicht', 'Kompakte Übersicht eines Falls: Fall, Beteiligte, Verfahren, offene Fristen und Aufgaben, Ereignisse, Dokumentliste mit Kennung, Titel, Datum, Stand, dazu nicht erfasste Dateien. Dokumentinhalte über dokument_text.',
          {'fall': {'type': 'string', 'description': 'Fallkennung wie R-0001'}}, pflicht=['fall'])
def fall_uebersicht(fall):
    akte, _ = store.lese_akte(fall); liste, _, abweichungen = dokumente.katalog(fall, akte)
    kurz = lambda s, n=160: (s or '')[:n]
    return {'fall': {k: akte['fall'].get(k, '') for k in ('id', 'titel', 'bereich', 'rolle', 'ziel', 'status', 'themen')},
            'beteiligte': [{'id': b['id'], 'name': b['name'], 'rolle': b.get('rolle', ''), 'aktenzeichen': b.get('aktenzeichen', '')} for b in akte['beteiligte']],
            'verfahren': [{'id': v['id'], 'art': v['art'], 'stelle': v.get('stelle', ''), 'aktenzeichen': v.get('aktenzeichen', ''), 'stand': kurz(v.get('stand'))} for v in akte['verfahren']],
            'fristen': [{'id': f['id'], 'datum': f['datum'], 'titel': f['titel'], 'art': f['art'], 'pruefstatus': f['pruefstatus'], 'quelle': f.get('quelle', ''), 'geprueft_am': f.get('geprueft_am', ''), 'eigenschaften': akte_schema.frist_eigenschaften(f)} for f in sorted(akte['fristen'], key=lambda x: x['datum']) if f['pruefstatus'] != 'erledigt'],
            'aufgaben_offen': [{'id': a['id'], 'titel': a['titel'], 'faellig': a.get('faellig', ''), 'quelle': a.get('quelle', '')} for a in akte['aufgaben'] if not a['erledigt']],
            'ereignisse': [{'id': e['id'], 'datum': e['datum'], 'titel': e['titel'], 'art': e.get('art', ''), 'quelle': e.get('quelle', '')} for e in sorted(akte['ereignisse'], key=lambda x: x['datum'])],
            'entwuerfe': [{'id': w['id'], 'titel': w['titel'], 'fassung': w.get('fassung', 1), 'status': w.get('status', '')} for w in akte['entwuerfe']],
            'dokumente': [{'id': d['id'], 'titel': kurz(d['titel'], 90), 'datum': d.get('datum', ''), 'stand': d.get('stand', ''), 'anlage': d.get('anlage', ''), 'bereich': d.get('gruppe', '')} for d in liste],
            'nicht_erfasst': abweichungen['nicht_erfasst'], 'verschoben': abweichungen['verschoben'],
            'hinweis': 'Dokumentdatum ist kein Zugangsnachweis. Inhalte mit dokument_text lesen. ' + ABGLEICH_HINWEIS}

@werkzeug('dokument_text', 'Textauszug eines Dokuments (Word, E-Mail, PDF, Text, HTML). Fotos haben keinen Text.',
          {'fall': {'type': 'string'}, 'dokument': {'type': 'string', 'description': 'D-Kennung wie D0038'}}, pflicht=['fall', 'dokument'])
def dokument_text(fall, dokument):
    akte, _ = store.lese_akte(fall); ordner = store.fall_ordner(fall); dokument = (dokument or '').strip().upper()
    d = akte['dokumente'].get(dokument)
    if not d: raise ValueError('Unbekannte Dokumentkennung. ' + ABGLEICH_HINWEIS)
    p = store.sicher(d['pfad'], ordner)
    if not p.is_file(): raise ValueError('Datei fehlt am registrierten Ort. Falls sie verschoben wurde: bestand_abgleichen ausführen.')
    t, hinweis = dokumente.text(p)
    return {'dokument': dokument, 'titel': d['titel'], 'pfad': d['pfad'], 'text': t, 'hinweis': hinweis}

@werkzeug('dokumente_suchen', 'Volltextsuche in Titeln, Ordnungsangaben und Dokumentinhalten eines Falls.',
          {'fall': {'type': 'string'}, 'frage': {'type': 'string', 'description': 'Suchbegriff, mindestens zwei Zeichen'}}, pflicht=['fall', 'frage'])
def dokumente_suchen(fall, frage):
    akte, _ = store.lese_akte(fall)
    return {'treffer': dokumente.suche(fall, akte, frage)}

@werkzeug('frist_berechnen', 'Fristende nach §§ 187, 188, 193 BGB mit den landesweiten Feiertagen eines Bundeslands berechnen (Standard: Einstellung der Mappe). Liefert die Rechnung als Text. Entscheidet nicht, welche Frist gilt.',
          {'start': {'type': 'string', 'description': 'Ereignistag (Zugang) als JJJJ-MM-TT'},
           'menge': {'type': 'integer'}, 'einheit': {'type': 'string', 'enum': ['tage', 'wochen', 'monate', 'jahre']},
           'ereignisfrist': {'type': 'boolean', 'description': 'true: Ereignistag zählt nicht mit (§ 187 Abs. 1 BGB), Regelfall'},
           'werktagsregel': {'type': 'boolean', 'description': 'true: Ende auf Sa, So, Feiertag verschiebt sich auf den nächsten Werktag (§ 193 BGB)'},
           'land': {'type': 'string', 'enum': list(fristen.LAENDER), 'description': 'Bundesland des Leistungsorts (§ 193 BGB), Kürzel wie BW, BY, NW; leer: Einstellung der Mappe'}},
          pflicht=['start', 'menge', 'einheit'])
def frist_berechnen(start, menge, einheit, ereignisfrist=True, werktagsregel=True, land=''):
    return fristen.berechne(start, menge, einheit, ereignisfrist, werktagsregel, (land or store.feiertagsland()).upper())

@werkzeug('beispiel_laden', 'Die mitgelieferte Beispielakte (erfundener Fall) als neuen Fall anlegen, zum Ausprobieren. Der Fall bekommt die nächste freie Kennung.', {}, schreibend=True)
def beispiel_laden():
    return store.beispiel_laden()

@werkzeug('bestand_pruefen', 'Prüfsummen aller registrierten Dateien eines Falls mit dem ersten Stand vergleichen; meldet auch nicht erfasste und verschobene Dateien. Schreibt nichts.',
          {'fall': {'type': 'string'}}, pflicht=['fall'])
def bestand_pruefen(fall):
    ordner = store.fall_ordner(fall); _, abweichungen = bestand.abgleich(ordner)
    return {'fall': fall, **bestand.pruefen(ordner), 'nicht_erfasst': abweichungen['nicht_erfasst'], 'verschoben_erkannt': abweichungen['verschoben']}

@werkzeug('journal_lesen', 'Verlauf eines Falls aus JOURNAL.md, neueste Einträge zuletzt.',
          {'fall': {'type': 'string'}}, pflicht=['fall'])
def journal_lesen(fall):
    return {'eintraege': store.journal_lesen(fall)}

@werkzeug('quellen_katalog', 'Gemeinsamer Zugangskatalog amtlicher Rechtsquellen aus 04 Rechtsquellen/Quellen.md.', {})
def quellen_katalog():
    p = store.sicher('04 Rechtsquellen/Quellen.md')
    if not p.exists(): return {'quellen': [], 'text': ''}
    text = p.read_text('utf-8')
    if '<!-- RECHT:ANFANG -->' in text:
        teil = text.split('<!-- RECHT:ANFANG -->', 1)[1].split('<!-- RECHT:ENDE -->', 1)[0].strip()
        liste = json.loads(teil.removeprefix('```json').removesuffix('```').strip())
        return {'quellen': liste, 'text': text.split('<!-- RECHT:ANFANG -->', 1)[0].strip()}
    return {'quellen': [], 'text': text}

def _oeffnen_befehl(p, zeigen):
    """Befehl für den Dateimanager des Systems: macOS Finder, Linux xdg-open, Windows Explorer.
    zeigen=True hebt die Datei im Ordner hervor; wo das nicht geht, öffnet sich der Ordner."""
    import sys
    if sys.platform == 'darwin': return ['/usr/bin/open', '-R', str(p)] if zeigen else ['/usr/bin/open', str(p)]
    if sys.platform.startswith('win'): return ['explorer', '/select,' + str(p)] if zeigen else ['explorer', str(p)]
    return ['xdg-open', str(p.parent if zeigen else p)]

def oeffnen(fall=None, dokument=None, bereich=None, zeigen=False):
    """Datei oder Ordner mit dem Dateimanager öffnen. Nicht für die KI, nur für die Oberfläche. Schreibt nichts."""
    import subprocess
    if fall and dokument:
        akte, _ = store.lese_akte(fall); d = akte['dokumente'].get(dokument)
        if not d: raise ValueError('Unbekannte Dokumentkennung. ' + ABGLEICH_HINWEIS)
        p = store.sicher(d['pfad'], store.fall_ordner(fall))
        if not p.exists(): raise ValueError('Datei fehlt am registrierten Ort.')
        if not zeigen and p.suffix.lower() in ('.py', '.sh', '.json', '.html'): zeigen = True
        args = _oeffnen_befehl(p, zeigen)
    elif fall:
        basis = store.fall_ordner(fall)
        if bereich and bereich not in store.GRUPPEN: raise ValueError('Unbekannter Bereich.')
        args = _oeffnen_befehl(store.sicher(bereich, basis) if bereich else basis, False)
    else:
        orte = {'projekt': '.', 'eingang': '01 Eingang', 'vertraege': '03 Verträge und Vorsorge', 'quellen': '04 Rechtsquellen', 'vorlagen': '05 Vorlagen', 'doku': 'DOKU'}
        if bereich not in orte: raise ValueError('Unbekannter Ort.')
        args = _oeffnen_befehl(store.sicher(orte[bereich]), False)
    try: subprocess.run(args, check=True, timeout=8, capture_output=True)
    except FileNotFoundError: raise ValueError('Kein Dateimanager gefunden (' + args[0] + ').')
    return {'ok': True}

# ---------------------------------------------------------------- schreibend
@werkzeug('fall_anlegen', 'Neuen Fall mit fester Kennung und Ordnerstruktur anlegen.',
          {'titel': {'type': 'string'}, 'bereich': {'type': 'string', 'enum': akte_schema.BEREICHE},
           'rolle': {'type': 'string', 'description': 'eigene Rolle, z. B. Betroffener, Mieter, Arbeitnehmer'}, 'ziel': {'type': 'string'}},
          schreibend=True, pflicht=['titel'])
def fall_anlegen(titel, bereich='Allgemein', rolle='', ziel=''):
    return store.neuer_fall(titel, bereich, rolle, ziel)

@werkzeug('fall_status_setzen', 'Fallstatus auf offen, ruhend oder abgeschlossen setzen. Der Fall bleibt am gleichen Ort.',
          {'fall': {'type': 'string'}, 'status': {'type': 'string', 'enum': akte_schema.FALL_STATUS}}, schreibend=True, pflicht=['fall', 'status'])
def fall_status_setzen(fall, status):
    rev = store.fall_status(fall, status)
    store.journal_anhaengen(fall, 'Entscheidung', f'Status {status}', f'Fallstatus auf „{status}“ gesetzt.')
    return {'revision': rev}

@werkzeug('akte_speichern', 'Vollständige Akte speichern. Nur mit der Revision, die beim Lesen geliefert wurde. Wird vor dem Speichern geprüft.',
          {'fall': {'type': 'string'}, 'akte': {'type': 'object'}, 'revision': {'type': 'string'}}, schreibend=True, pflicht=['fall', 'akte', 'revision'], ki=False)
def akte_speichern(fall, akte, revision):
    return {'revision': store.speichere_akte(fall, akte, revision)}

def _quelle(fall, quelle, detail=''):
    """Quelle muss eine D-Kennung sein. Freitext (z. B. von Sprachmodellen) wandert in den Text."""
    quelle = (quelle or '').strip()
    if not quelle: return '', detail
    if re.fullmatch(r'D\d{4,}', quelle.upper()):
        akte, _ = _akte_mit_dokument(fall, quelle)
        if quelle.upper() in akte['dokumente']: return quelle.upper(), detail
        raise ValueError(f'Dokumentkennung {quelle} gibt es in diesem Fall nicht.')
    return '', (detail + ' ' if detail else '') + f'[Quelle laut Angabe: {quelle}; keine Dokumentkennung]'

def _naechste(akte, block):
    """Nächste Kennung über den Zähler der Akte (akte_schema.naechste_kennung): entfernte Kennungen kommen nie wieder (F11)."""
    return akte_schema.naechste_kennung(akte, block)

@werkzeug('aufgabe_anlegen', 'Aufgabe in einem Fall anlegen.',
          {'fall': {'type': 'string'}, 'titel': {'type': 'string'}, 'detail': {'type': 'string'},
           'faellig': {'type': 'string', 'description': 'JJJJ-MM-TT oder leer'}, 'quelle': {'type': 'string', 'description': 'Dokumentkennung wie D0001 aus der Fallübersicht, sonst leer lassen; kein Freitext'}},
          schreibend=True, pflicht=['fall', 'titel'])
def aufgabe_anlegen(fall, titel, detail='', faellig='', quelle=''):
    quelle, detail = _quelle(fall, quelle, detail)
    akte, rev = store.lese_akte(fall)
    eintrag = {'id': _naechste(akte, 'aufgaben'), 'titel': titel, 'detail': detail, 'faellig': faellig, 'erledigt': False, 'quelle': quelle}
    akte['aufgaben'].append(eintrag); rev = store.speichere_akte(fall, akte, rev)
    return {'aufgabe': eintrag, 'revision': rev}

@werkzeug('aufgabe_setzen', 'Aufgabe als erledigt oder wieder offen setzen, optional Fälligkeit oder Detail ändern.',
          {'fall': {'type': 'string'}, 'aufgabe': {'type': 'string', 'description': 'A-Kennung wie A01'}, 'erledigt': {'type': 'boolean'},
           'faellig': {'type': 'string'}, 'detail': {'type': 'string'}}, schreibend=True, pflicht=['fall', 'aufgabe'])
def aufgabe_setzen(fall, aufgabe, erledigt=None, faellig=None, detail=None):
    akte, rev = store.lese_akte(fall)
    a = next((x for x in akte['aufgaben'] if x['id'] == aufgabe), None)
    if not a: raise ValueError('Unbekannte Aufgabenkennung.')
    if erledigt is not None: a['erledigt'] = bool(erledigt)
    if faellig is not None: a['faellig'] = faellig
    if detail is not None: a['detail'] = detail
    rev = store.speichere_akte(fall, akte, rev)
    return {'aufgabe': a, 'revision': rev}

@werkzeug('frist_eintragen', 'Frist oder Termin in einem Fall eintragen. Bestätigt nur, wenn die Rechnung das Fristende nennt, Auslöser, Rechtsgrundlage und Quelle da sind und kein Marker [PRÜFEN], [QUELLE], [BELEG] offen ist; die Bestätigung bekommt Prüfdatum und Prüfer.',
          {'fall': {'type': 'string'}, 'datum': {'type': 'string'}, 'titel': {'type': 'string'},
           'art': {'type': 'string', 'enum': akte_schema.FRIST_ART}, 'ausloeser': {'type': 'string'}, 'rechtsgrundlage': {'type': 'string'},
           'berechnung': {'type': 'string'}, 'pruefstatus': {'type': 'string', 'enum': akte_schema.FRIST_STATUS}, 'quelle': {'type': 'string', 'description': 'Dokumentkennung wie D0001, sonst leer; kein Freitext'},
           'geprueft_von': {'type': 'string', 'description': 'Wer die Bestätigung geprüft hat (Name oder Assistent); nur bei pruefstatus bestätigt'}},
          schreibend=True, pflicht=['fall', 'datum', 'titel', 'art'])
def frist_eintragen(fall, datum, titel, art, ausloeser='', rechtsgrundlage='', berechnung='', pruefstatus='offen', quelle='', geprueft_von=''):
    quelle, berechnung = _quelle(fall, quelle, berechnung)
    akte, rev = store.lese_akte(fall)
    eintrag = {'id': _naechste(akte, 'fristen'), 'datum': datum, 'titel': titel, 'art': art, 'ausloeser': ausloeser,
               'rechtsgrundlage': rechtsgrundlage, 'berechnung': berechnung, 'pruefstatus': pruefstatus, 'quelle': quelle}
    if pruefstatus == 'bestätigt':   # F12: eine Bestätigung trägt Prüfdatum und Prüfer; das Schema prüft Rechnung, Beleg und Marker
        eintrag['geprueft_am'] = date.today().isoformat(); eintrag['geprueft_von'] = (geprueft_von or '').strip()
    akte['fristen'].append(eintrag); rev = store.speichere_akte(fall, akte, rev)
    return {'frist': eintrag, 'eigenschaften': akte_schema.frist_eigenschaften(eintrag), 'revision': rev}

@werkzeug('ereignis_eintragen', 'Ereignis in die Chronologie eines Falls eintragen.',
          {'fall': {'type': 'string'}, 'datum': {'type': 'string'}, 'titel': {'type': 'string'},
           'art': {'type': 'string', 'enum': akte_schema.EREIGNIS_ART_VORSCHLAG}, 'quelle': {'type': 'string', 'description': 'Dokumentkennung wie D0001, sonst leer; kein Freitext'}, 'detail': {'type': 'string'}},
          schreibend=True, pflicht=['fall', 'datum', 'titel'])
def ereignis_eintragen(fall, datum, titel, art='Vermerk', quelle='', detail=''):
    quelle, detail = _quelle(fall, quelle, detail)
    akte, rev = store.lese_akte(fall)
    eintrag = {'id': _naechste(akte, 'ereignisse'), 'datum': datum, 'titel': titel, 'art': art, 'quelle': quelle, 'detail': detail}
    akte['ereignisse'].append(eintrag); rev = store.speichere_akte(fall, akte, rev)
    return {'ereignis': eintrag, 'revision': rev}

@werkzeug('notiz_anlegen', 'Ordnungsnotiz in einem Fall anlegen.',
          {'fall': {'type': 'string'}, 'titel': {'type': 'string'}, 'text': {'type': 'string'}}, schreibend=True, pflicht=['fall', 'titel', 'text'])
def notiz_anlegen(fall, titel, text):
    from datetime import date
    akte, rev = store.lese_akte(fall)
    eintrag = {'id': _naechste(akte, 'notizen'), 'titel': titel, 'text': text, 'datum': date.today().isoformat()}
    akte['notizen'].append(eintrag); rev = store.speichere_akte(fall, akte, rev)
    return {'notiz': eintrag, 'revision': rev}

@werkzeug('entwurf_erfassen', 'Entwurf in der Akte erfassen oder fortschreiben (Titel, Datei, Fassung, Status). Gleicher Titel = neue Fassung. Bei Status „geprüft“ oder „versandt“ wird die Datei (und eine gleichnamige .docx) als unveränderliche Kopie unter 06 Entwürfe/Fassungen eingefroren, mit Prüfsumme in der Akte; die Kopie bekommt eine eigene D-Kennung.',
          {'fall': {'type': 'string'}, 'titel': {'type': 'string'}, 'datei': {'type': 'string', 'description': 'Pfad im Fallordner, z. B. 06 Entwürfe/Einspruch_ENTWURF.md'},
           'status': {'type': 'string', 'enum': akte_schema.ENTWURF_STATUS}, 'versandt_als': {'type': 'string', 'description': 'D-Kennung des Versandbelegs bei Status versandt'}},
          schreibend=True, pflicht=['fall', 'titel', 'datei'])
def entwurf_erfassen(fall, titel, datei, status='in Arbeit', versandt_als=''):
    from datetime import datetime
    akte, rev = _akte_mit_dokument(fall, versandt_als); ordner = store.fall_ordner(fall)
    quelle = store.sicher(datei, ordner)
    if not quelle.is_file(): raise ValueError(f'Entwurfsdatei fehlt: {datei}')
    e = next((x for x in akte['entwuerfe'] if x['titel'] == titel), None)
    if e: e.update({'datei': datei, 'fassung': e.get('fassung', 1) + 1, 'status': status, 'versandt_als': versandt_als})
    else: e = {'id': _naechste(akte, 'entwuerfe'), 'titel': titel, 'datei': datei, 'fassung': 1, 'status': status, 'versandt_als': versandt_als}; akte['entwuerfe'].append(e)
    # Jede erfasste Fassung mit Prüfsumme; freigegebene und versandte Fassungen als Kopie einfrieren (Prüfbericht F28)
    sha = bestand.sha_datei(quelle); fassungen = e.setdefault('fassungen', []); hinweise = []
    stand = {'fassung': e['fassung'], 'datei': datei, 'sha256': sha, 'zeit': datetime.now().isoformat(timespec='seconds'), 'status': status}
    if status == 'versandt':
        geprueft = [x for x in fassungen if x.get('status') == 'geprüft']
        if not geprueft: hinweise.append('Vor dem Versand wurde keine Fassung als „geprüft“ erfasst.')
        elif geprueft[-1]['sha256'] != sha: hinweise.append(f'Der Sendetext weicht von der zuletzt geprüften Fassung {geprueft[-1]["fassung"]} ab; die versandte Fassung wird trotzdem eingefroren.')
    if status in ('geprüft', 'versandt'):
        kopien = {}; zielordner = ordner / '06 Entwürfe' / 'Fassungen'; zielordner.mkdir(parents=True, exist_ok=True)
        dateien = [quelle] + ([quelle.with_suffix('.docx')] if quelle.suffix.lower() != '.docx' and quelle.with_suffix('.docx').is_file() else [])
        for q in dateien:
            ziel = zielordner / f'{q.stem}_Fassung{e["fassung"]:02d}_{status}{q.suffix}'
            if ziel.exists():
                if bestand.sha_datei(ziel) != bestand.sha_datei(q): raise ValueError(f'Eingefrorene Kopie {ziel.name} gibt es schon mit anderem Inhalt. Nichts wird überschrieben.')
            else: shutil.copyfile(q, ziel); ziel.chmod(0o444)   # nur lesbar: die Kopie ist das Original dieser Fassung
            kopien[q.suffix.lower().lstrip('.')] = str(ziel.relative_to(ordner))
        stand['kopien'] = kopien
        bestand.abgleichen(ordner, weg='Fassung eingefroren'); dokumente.katalog(fall, akte)
        pfad_zu_id = {d['pfad']: k for k, d in akte['dokumente'].items()}
        for rel in kopien.values():
            k = pfad_zu_id.get(rel)
            if k: akte['dokumente'][k].update({'titel': f'{titel}, Fassung {e["fassung"]} ({status})', 'art': 'Entwurf', 'stand': 'Versandt' if status == 'versandt' else 'Entwurf', 'notiz': f'Eingefrorene Kopie von {datei}, Prüfsumme in {e["id"]}.'})
        stand['kopie_dokument'] = pfad_zu_id.get(kopien.get(quelle.suffix.lower().lstrip('.')), '')
    fassungen.append(stand)
    rev = store.speichere_akte(fall, akte, rev)
    return {'entwurf': e, 'revision': rev, 'hinweise': hinweise}

def _akte_mit_dokument(fall, dokument=''):
    """Akte lesen, nur für schreibende Werkzeuge. Ist die Dokumentkennung unbekannt, den Bestand abgleichen
    und den Katalog nachziehen (neu zugeordnete oder im Finder abgelegte Dateien bekommen so ihren
    Eintrag), erst dann gilt sie als unbekannt."""
    akte, rev = store.lese_akte(fall)
    dokument = (dokument or '').strip().upper()
    if dokument and dokument not in akte['dokumente']:
        bestand.abgleichen(store.fall_ordner(fall), weg='Abgleich vor Änderung')
        _, ergaenzt, _ = dokumente.katalog(fall, akte)
        if ergaenzt: rev = store.speichere_akte(fall, akte, rev, ohne_sicherung=True)
    return akte, rev

@werkzeug('bestand_abgleichen', 'Bestand eines Falls mit den Dateien abgleichen: neue Dateien in 01 bis 08 bekommen eine Kennung, im Finder verschobene werden über die Prüfsumme wiedergefunden, fehlende Ordnungsangaben werden in der Akte ergänzt. Der einzige Weg, auf dem neue Dateien registriert werden.',
          {'fall': {'type': 'string'}}, schreibend=True, pflicht=['fall'])
def bestand_abgleichen(fall):
    ordner = store.fall_ordner(fall)
    _, bericht = bestand.abgleichen(ordner)
    akte, rev = store.lese_akte(fall)
    _, ergaenzt, _ = dokumente.katalog(fall, akte)
    if ergaenzt: rev = store.speichere_akte(fall, akte, rev, ohne_sicherung=True)
    return {'fall': fall, 'neu': bericht['neu'], 'verschoben': bericht['verschoben'], 'fehlend': bericht['fehlend'],
            'in_akte_ergaenzt': ergaenzt, 'revision': rev}


@werkzeug('dokument_ordnen', 'Ordnungsangaben eines Dokuments ändern (Titel, Datum, Art, Stand, Themen, Anlage, Personen, Verweise, Notiz). Die Datei selbst bleibt unverändert.',
          {'fall': {'type': 'string'}, 'dokument': {'type': 'string'}, 'felder': {'type': 'object', 'description': 'nur die zu ändernden Felder'}},
          schreibend=True, pflicht=['fall', 'dokument', 'felder'])
def dokument_ordnen(fall, dokument, felder):
    akte, rev = _akte_mit_dokument(fall, dokument)
    d = akte['dokumente'].get(dokument)
    if not d: raise ValueError('Unbekannte Dokumentkennung.')
    erlaubt = {'titel', 'datum', 'art', 'stand', 'themen', 'anlage', 'personen', 'verweise', 'notiz'}
    fremd = set(felder) - erlaubt
    if fremd: raise ValueError('Nur Ordnungsangaben sind änderbar, nicht: ' + ', '.join(sorted(fremd)))
    d.update(felder); rev = store.speichere_akte(fall, akte, rev)
    return {'dokument': dokument, 'revision': rev}

@werkzeug('dokument_verschieben', 'Datei in einen anderen Aktenbereich einsortieren. Kennung und Inhalt bleiben, nichts wird überschrieben.',
          {'fall': {'type': 'string'}, 'dokument': {'type': 'string'}, 'bereich': {'type': 'string', 'enum': store.GRUPPEN},
           'unterordner': {'type': 'string', 'description': 'optional, z. B. An Vorstand'}},
          schreibend=True, pflicht=['fall', 'dokument', 'bereich'])
def dokument_verschieben(fall, dokument, bereich, unterordner=''):
    ordner = store.fall_ordner(fall)
    neu = bestand.verschieben(ordner, dokument, bereich, unterordner)
    akte, rev = _akte_mit_dokument(fall, dokument)
    if dokument in akte['dokumente']:
        akte['dokumente'][dokument]['pfad'] = neu; rev = store.speichere_akte(fall, akte, rev, ohne_sicherung=True)
    return {'dokument': dokument, 'pfad': neu, 'revision': rev}

@werkzeug('journal_schreiben', 'Eintrag an das Journal eines Falls anhängen.',
          {'fall': {'type': 'string'}, 'art': {'type': 'string', 'enum': store.JOURNAL_ARTEN}, 'titel': {'type': 'string'}, 'text': {'type': 'string'}},
          schreibend=True, pflicht=['fall', 'art', 'titel', 'text'])
def journal_schreiben(fall, art, titel, text):
    return store.journal_anhaengen(fall, art, titel, text)

@werkzeug('sicherung_erstellen', 'Geprüfte ZIP-Sicherung des ganzen Projekts erstellen, mit Kopie an das zweite Ziel.', {}, schreibend=True)
def sicherung_erstellen():
    return sicherung.erstellen()

@werkzeug('sicherung_probe', 'Wiederherstellungsprobe: die letzte Sicherung in einem Zwischenordner entpacken, Akten gegen das Schema und alle Dateien gegen die Prüfsummen prüfen, Zwischenordner wieder entfernen. Die Mappe bleibt unberührt.',
          {'archiv': {'type': 'string', 'description': 'Pfad eines Archivs; leer: die letzte Sicherung'}}, schreibend=True)
def sicherung_probe(archiv=''):
    return sicherung.probe(archiv or None)

def fuer_agenten():
    """Werkzeuge, die eine angebundene KI sehen soll (ohne die großen Ganz-Akte-Werkzeuge)."""
    return [w for w in KATALOG if w.get('ki', True)]
