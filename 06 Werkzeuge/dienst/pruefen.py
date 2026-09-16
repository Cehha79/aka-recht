#!/usr/bin/env python3
"""Funktionstest des Dienstes mit künstlichen Akten außerhalb des Projekts.

Aufruf: python3 "06 Werkzeuge/dienst/pruefen.py"
Kopiert Vorlagen und Werkzeuge in einen Temp-Ordner, startet dort einen eigenen
Dienst, prüft die Schnittstelle Punkt für Punkt und beendet den Dienst wieder.
Es werden keine echten Akten berührt. Nur Standardbibliothek.
"""
import sys
sys.dont_write_bytecode = True
import base64, hashlib, json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request, zipfile
from pathlib import Path

QUELLE = Path(__file__).resolve().parents[2]

def vorbereiten(base):
    root = base / 'Recht'; root.mkdir()
    for o in ['01 Eingang', '02 Fälle', 'DOKU']: (root / o).mkdir()
    shutil.copytree(QUELLE / '05 Vorlagen', root / '05 Vorlagen', ignore=shutil.ignore_patterns('.DS_Store'))
    (root / '06 Werkzeuge').mkdir()
    shutil.copy2(QUELLE / '06 Werkzeuge/akte_schema.py', root / '06 Werkzeuge/akte_schema.py')
    shutil.copytree(QUELLE / '06 Werkzeuge/dienst', root / '06 Werkzeuge/dienst', ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'))
    (base / 'iCloud').mkdir()
    z = {'schema': 1, 'app': 'AKA Recht', 'faelle': [],
         'sicherung': {'ziel': str(base / 'Sicherungen'), 'zweites_ziel': str(base / 'iCloud' / 'AKA Recht Sicherungen'), 'letzte': None},
         'verbindungen': {}}
    (root / 'zentrale.json').write_text(json.dumps(z, ensure_ascii=False, indent=2))
    return root

def run():
    base = Path(tempfile.mkdtemp(prefix='aka-recht-pruefung-', dir='/private/tmp' if Path('/private/tmp').is_dir() else None)).resolve(); root = vorbereiten(base)
    instanz = hashlib.sha256(str(root).encode()).hexdigest()[:14]
    laufzeit = Path(tempfile.gettempdir()) / f'aka-recht-dienst-{instanz}.json'
    if laufzeit.exists(): laufzeit.unlink()
    bestanden = []; server = None
    def ok(name): bestanden.append(name); print('ok ', name)
    try:
        with (base / 'server.log').open('wb') as log:
            server = subprocess.Popen([sys.executable, str(root / '06 Werkzeuge/dienst/server.py'), '--root', str(root), '--serve'], stdout=log, stderr=log)
        for _ in range(80):
            if laufzeit.exists(): break
            if server.poll() is not None: raise RuntimeError((base / 'server.log').read_text())
            time.sleep(.1)
        d = json.loads(laufzeit.read_text()); url = f'http://127.0.0.1:{d["port"]}'; cookie = f'aka_{instanz}={d["key"]}'; csrf = d['csrf']
        def anfrage(pfad, daten=None, erwartet=200, kopf=None, roh=False):
            k = {'Cookie': cookie, **(kopf or {})}
            if daten is not None: k = {'Content-Type': 'application/json', 'X-AKA-CSRF': csrf, 'Origin': url, **k}
            r = urllib.request.Request(url + pfad, data=json.dumps(daten).encode() if daten is not None else None, headers=k, method='POST' if daten is not None else 'GET')
            try:
                with urllib.request.urlopen(r, timeout=60) as a: code, body = a.status, a.read()
            except urllib.error.HTTPError as e: code, body = e.code, e.read()
            assert code == erwartet, f'{pfad}: HTTP {code} statt {erwartet}: {body[:300]!r}'
            if roh: return body
            try: return json.loads(body)
            except json.JSONDecodeError: return body.decode('utf-8', 'replace')

        # 1 Zugang
        r = urllib.request.Request(url + '/api/zentrale')
        try: urllib.request.urlopen(r); raise AssertionError('ohne Cookie durchgelassen')
        except urllib.error.HTTPError as e: assert e.code == 403
        ok('Nicht angemeldeten Zugriff abgewiesen')
        anfrage('/api/werkzeug', {'name': 'faelle_auflisten', 'parameter': {}}, erwartet=403, kopf={'Origin': 'http://böse.example'})
        ok('Schreibanfrage von fremdem Ursprung abgewiesen')
        z = anfrage('/api/zentrale'); assert z['faelle'] == [] and z['csrf'] == csrf and z['app'] == 'AKA Recht'
        ok('Zentrale mit leerer Fallliste und Sitzungsdaten')
        html = anfrage('/', roh=True).decode(); assert 'Stufe 4' in html
        ok('Startseite liefert Platzhalter, solange die Oberfläche fehlt')
        kat = anfrage('/api/werkzeuge'); assert len(kat) >= 18 and not any(w['name'] in ('loeschen', 'versenden') for w in kat)
        ok(f'Werkzeugkatalog mit {len(kat)} Werkzeugen, ohne Löschen und Versand')

        # 2 Fälle. Die Fallvorlage kommt aus git ohne ihre leeren Ordner (F09): hier ebenso, die Ordner müssen trotzdem entstehen.
        for g in ['01 Eingang', '02 Grundlagen', '03 Schriftverkehr', '04 Verfahren', '05 Beweise', '06 Entwürfe', '07 Recherche', '08 Archiv']:
            shutil.rmtree(root / '05 Vorlagen/Fallvorlage' / g, ignore_errors=True)
        assert sorted(p.name for p in (root / '05 Vorlagen/Fallvorlage').iterdir() if not p.name.startswith('.')) == ['JOURNAL.md', 'akte.json', 'bestand.json']
        f1 = anfrage('/api/fall', {'titel': 'Bußgeld Parkverstoß', 'bereich': 'Verkehr und Bußgeld', 'rolle': 'Betroffener', 'ziel': 'Einspruch prüfen'})
        f2 = anfrage('/api/fall', {'titel': 'Miete Nebenkosten 2025', 'bereich': 'Wohnen und Miete'})
        assert f1['id'] == 'R-0001' and f2['id'] == 'R-0002'
        for g in ['01 Eingang', '02 Grundlagen', '03 Schriftverkehr', '04 Verfahren', '05 Beweise', '06 Entwürfe', '07 Recherche', '08 Archiv']: assert (root / f1['ordner'] / g).is_dir(), g
        assert 'Fall angelegt' in (root / f1['ordner'] / 'JOURNAL.md').read_text()
        ok('Zwei Fälle aus verschiedenen Rechtsgebieten mit festen Kennungen, allen acht Bereichen (auch ohne Ordner in der Vorlage) und Journal angelegt')
        anfrage('/api/fall', {'titel': ''}, erwartet=400); ok('Fall ohne Titel abgewiesen')

        # 3 Dokumente
        inhalt = 'Anhörungsbogen\nZugestellt am 05.09.2026\nMessgerät Traffistar\n'.encode()
        r = anfrage('/api/fall/R-0001/eingang', {'name': 'Anhoerung.txt', 'inhalt': base64.b64encode(inhalt).decode()})
        assert r['dokument'] == 'D0001'
        r2 = anfrage('/api/fall/R-0001/eingang', {'name': 'Anhoerung.txt', 'inhalt': base64.b64encode(b'zweite Datei').decode()})
        assert r2['name'] == 'Anhoerung (2).txt' and r2['dokument'] == 'D0002'
        ok('Import vergibt Kennungen und überschreibt keine gleichnamige Datei')
        anfrage('/api/fall/R-0001/eingang', {'name': '../ausbruch.txt', 'inhalt': base64.b64encode(b'x').decode()}, erwartet=400)
        ok('Pfadausbruch beim Import abgewiesen')
        akte_roh = (root / f1['ordner'] / 'akte.json').read_bytes()
        fall = anfrage('/api/fall/R-0001')
        assert 'D0001' in fall['akte']['dokumente'] and any(x['id'] == 'D0001' for x in fall['dokumente']) and set(fall['ergaenzt']) == {'D0001', 'D0002'}
        assert (root / f1['ordner'] / 'akte.json').read_bytes() == akte_roh, 'Lesen der Akte hat akte.json geschrieben'
        r = anfrage('/api/werkzeug', {'name': 'bestand_abgleichen', 'parameter': {'fall': 'R-0001'}, 'bestaetigt': True})
        assert set(r['in_akte_ergaenzt']) == {'D0001', 'D0002'} and 'D0001' in json.loads((root / f1['ordner'] / 'akte.json').read_text())['dokumente']
        fall = anfrage('/api/fall/R-0001'); rev = fall['revision']; assert not fall['ergaenzt'] and not fall['abweichungen']['nicht_erfasst']
        ok('Importierte Dateien: Lesen zeigt sie als ergänzt, ohne zu schreiben; bestand_abgleichen trägt sie in die Akte ein')
        t = anfrage('/api/fall/R-0001/text/D0001'); assert 'Traffistar' in t['text']
        s = anfrage('/api/fall/R-0001/suche?q=traffistar'); assert s['treffer'] == ['D0001']
        ok('Textauszug und Volltextsuche')
        anfrage('/api/fall/R-0002/text/D0001', erwartet=400); ok('Dokumentkennungen bleiben je Fall getrennt')

        # 4 Verschieben, Finder-Verschiebung, Bestand
        r = anfrage('/api/werkzeug', {'name': 'dokument_verschieben', 'parameter': {'fall': 'R-0001', 'dokument': 'D0001', 'bereich': '02 Grundlagen', 'unterordner': 'Bescheide'}})
        assert r.get('bestaetigung_noetig'); ok('Schreibendes Werkzeug ohne Bestätigung hält an')
        # F05: nur der JSON-Wahrheitswert true ist eine Bestätigung
        for wert in ('false', 'true', 'ja', 1, 0, None, [True], {'x': 1}):
            a = anfrage('/api/werkzeug', {'name': 'dokument_verschieben', 'parameter': {'fall': 'R-0001', 'dokument': 'D0001', 'bereich': '02 Grundlagen'}, 'bestaetigt': wert}, erwartet=400)
            assert 'bestaetigt' in a['fehler'], (wert, a)
        assert anfrage('/api/werkzeug', {'name': 'dokument_verschieben', 'parameter': {'fall': 'R-0001', 'dokument': 'D0001', 'bereich': '02 Grundlagen'}, 'bestaetigt': False}).get('bestaetigung_noetig')
        assert (root / f1['ordner'] / '01 Eingang' / 'Anhoerung.txt').is_file(), 'ein abgewiesener Wert hat verschoben'
        ok('Bestätigung: „false“, „true“, 1, null und andere Typen werden abgewiesen, nur JSON true oder false gelten')
        r = anfrage('/api/werkzeug', {'name': 'dokument_verschieben', 'parameter': {'fall': 'R-0001', 'dokument': 'D0001', 'bereich': '02 Grundlagen', 'unterordner': 'Bescheide'}, 'bestaetigt': True})
        assert r['pfad'] == '02 Grundlagen/Bescheide/Anhoerung.txt' and (root / f1['ordner'] / r['pfad']).is_file()
        b = json.loads((root / f1['ordner'] / 'bestand.json').read_text()); assert b['dateien']['D0001']['pfad'] == r['pfad'] and b['verschiebungen'][-1]['id'] == 'D0001'
        ok('Einsortieren behält Kennung und protokolliert die Verschiebung')
        os.rename(root / f1['ordner'] / r['pfad'], root / f1['ordner'] / '05 Beweise' / 'Anhoerung.txt')
        bestand_roh = (root / f1['ordner'] / 'bestand.json').read_bytes()
        fall = anfrage('/api/fall/R-0001')
        assert fall['akte']['dokumente']['D0001']['pfad'] == '05 Beweise/Anhoerung.txt' and fall['abweichungen']['verschoben'] == [{'id': 'D0001', 'von': '02 Grundlagen/Bescheide/Anhoerung.txt', 'nach': '05 Beweise/Anhoerung.txt'}]
        assert (root / f1['ordner'] / 'bestand.json').read_bytes() == bestand_roh, 'Lesen hat bestand.json geschrieben'
        r = anfrage('/api/werkzeug', {'name': 'bestand_abgleichen', 'parameter': {'fall': 'R-0001'}, 'bestaetigt': True}); assert r['verschoben'][0]['nach'] == '05 Beweise/Anhoerung.txt' and r['in_akte_ergaenzt'] == ['D0001']
        b = json.loads((root / f1['ordner'] / 'bestand.json').read_text()); assert b['dateien']['D0001']['pfad'] == '05 Beweise/Anhoerung.txt' and 'Prüfsumme' in b['verschiebungen'][-1]['weg']
        fall = anfrage('/api/fall/R-0001'); rev = fall['revision']; assert not fall['abweichungen']['verschoben']
        ok('Im Finder verschobene Datei über Prüfsumme wiedererkannt: Lesen meldet sie, der Abgleich übernimmt sie, Kennung bleibt')
        p = root / f1['ordner'] / '05 Beweise' / 'Anhoerung.txt'; p.write_bytes(inhalt + b'geaendert')
        bp = anfrage('/api/werkzeug', {'name': 'bestand_pruefen', 'parameter': {'fall': 'R-0001'}})
        assert [x['id'] for x in bp['veraendert']] == ['D0001'] and bp['geprueft'] == 1
        p.write_bytes(inhalt); bp = anfrage('/api/werkzeug', {'name': 'bestand_pruefen', 'parameter': {'fall': 'R-0001'}}); assert not bp['veraendert']
        ok('Bestandsprüfung erkennt geänderten Inhalt trotz gleichem Namen')

        # 4b Lesen schreibt nichts (Prüfbericht 16.09.2026, F03): Dateistand vor und nach jedem lesenden Weg vergleichen
        def zustand():
            return {str(p.relative_to(root)): (p.stat().st_mtime_ns, p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()) for p in root.rglob('*') if p.is_file()}
        (root / f1['ordner'] / '05 Beweise' / 'Finder-Ablage.txt').write_text('im Finder abgelegt\n')
        vorher = zustand()
        for pfad in ('/api/zentrale', '/api/bestand', '/api/fall/R-0001', '/api/fall/R-0001/text/D0001', '/api/fall/R-0001/suche?q=finder', '/api/fall/R-0001/journal', '/api/quellen', '/api/einstellungen'): anfrage(pfad)
        for name, par in [('faelle_auflisten', {}), ('fall_uebersicht', {'fall': 'R-0001'}), ('bestand_pruefen', {'fall': 'R-0001'}), ('dokument_text', {'fall': 'R-0001', 'dokument': 'D0001'}),
                          ('dokumente_suchen', {'fall': 'R-0001', 'frage': 'finder'}), ('journal_lesen', {'fall': 'R-0001'}), ('quellen_katalog', {}), ('frist_berechnen', {'start': '2026-01-31', 'menge': 1, 'einheit': 'monate'})]:
            anfrage('/api/werkzeug', {'name': name, 'parameter': par})
        anfrage('/api/fall/R-0001/text/D0099', erwartet=400)
        nachher = zustand(); geaendert = sorted(k for k in set(nachher) | set(vorher) if nachher.get(k) != vorher.get(k))
        assert not geaendert, 'ein lesender Aufruf hat Dateien geändert: ' + ', '.join(geaendert)
        u = anfrage('/api/werkzeug', {'name': 'fall_uebersicht', 'parameter': {'fall': 'R-0001'}})
        assert u['nicht_erfasst'] == ['05 Beweise/Finder-Ablage.txt'] and not any(d['titel'].startswith('Finder') for d in u['dokumente'])
        assert anfrage('/api/werkzeug', {'name': 'bestand_pruefen', 'parameter': {'fall': 'R-0001'}})['nicht_erfasst'] == ['05 Beweise/Finder-Ablage.txt']
        assert next(f for f in anfrage('/api/zentrale')['faelle'] if f['id'] == 'R-0001')['nicht_erfasst'] == 1
        zp = root / 'zentrale.json'; zk = zp.read_bytes(); zp.unlink()
        try: assert anfrage('/api/zentrale')['faelle'] == [] and not zp.exists(), 'Lesen ohne zentrale.json hat sie angelegt'
        finally: zp.write_bytes(zk)
        ok('Lesende Werkzeuge und Routen ändern keine Datei, auch nicht bei neuer Finder-Datei oder fehlender zentrale.json; Abweichungen werden gemeldet')
        r = anfrage('/api/werkzeug', {'name': 'bestand_abgleichen', 'parameter': {'fall': 'R-0001'}, 'bestaetigt': True})
        assert r['neu'] == [{'id': 'D0003', 'pfad': '05 Beweise/Finder-Ablage.txt'}] and r['in_akte_ergaenzt'] == ['D0003'] and not r['verschoben']
        assert anfrage('/api/fall/R-0001/text/D0003')['text'].startswith('im Finder')
        assert anfrage('/api/werkzeug', {'name': 'bestand_abgleichen', 'parameter': {'fall': 'R-0001'}}).get('bestaetigung_noetig')
        ok('bestand_abgleichen registriert die Finder-Datei mit der nächsten Kennung, ergänzt die Akte und braucht die Bestätigung')

        # 5 Speichern, Revision, Schema
        fall = anfrage('/api/fall/R-0001'); rev = fall['revision']; akte = fall['akte']
        akte['fall']['ziel'] = 'Einspruch prüfen, Messung anzweifeln'
        r = anfrage('/api/fall/R-0001', {'akte': akte, 'revision': rev}); rev2 = r['revision']; assert rev2 != rev
        anfrage('/api/fall/R-0001', {'akte': akte, 'revision': rev}, erwartet=409)
        ok('Speichern mit Revision; veralteter Stand wird abgewiesen')
        kaputt = json.loads(json.dumps(akte)); kaputt['fristen'].append({'id': 'F01', 'datum': '2026-09-19', 'titel': 'Einspruch', 'art': 'gesetzlich', 'pruefstatus': 'bestätigt'})
        anfrage('/api/fall/R-0001', {'akte': kaputt, 'revision': rev2}, erwartet=400)
        # F10: unmögliche Kalendertage und falsche Typen geben Fehlerlisten, keinen Absturz, und kein Speichern
        sys.path.insert(0, str(root / '06 Werkzeuge')); import akte_schema
        def kaputte(aenderung):
            k = json.loads(json.dumps(akte)); aenderung(k); return k
        proben = [
            ('31. Februar', kaputte(lambda k: k['ereignisse'].append({'id': 'E01', 'datum': '2026-02-31', 'titel': 'x'})), 'Kalender'),
            ('Monat 13', kaputte(lambda k: k['fall'].__setitem__('angelegt', '2026-13-01')), 'Kalender'),
            ('fall=null', kaputte(lambda k: k.__setitem__('fall', None)), 'fall muss ein Objekt'),
            ('Liste statt Objekt', kaputte(lambda k: k.__setitem__('fall', [])), 'fall muss ein Objekt'),
            ('Zahl statt Eintrag', kaputte(lambda k: k.__setitem__('beteiligte', [5])), 'Kennung'),
            ('Text in kosten', kaputte(lambda k: k.__setitem__('kosten', ['x'])), 'kein Objekt'),
            ('angeheftet=5', kaputte(lambda k: k['fall'].__setitem__('angeheftet', 5)), 'angeheftet'),
            ('fassung=true', kaputte(lambda k: k['entwuerfe'].append({'id': 'W01', 'titel': 'x', 'status': 'in Arbeit', 'fassung': True})), 'fassung'),
            ('betrag=true', kaputte(lambda k: k['kosten'].append({'datum': '2026-09-01', 'posten': 'x', 'betrag': True})), 'betrag'),
            ('unbekannte Kennung', kaputte(lambda k: k['aufgaben'].append({'id': 'A09', 'titel': 'x', 'erledigt': False, 'quelle': 'D9999'})), 'D9999'),
        ]
        for name, probe, erwartet in proben:
            fehler, _ = akte_schema.validate(probe)
            assert fehler and any(erwartet in s for s in fehler), (name, fehler)
        assert akte_schema.validate(None)[0] and akte_schema.validate('x')[0]
        assert not akte_schema.validate(kaputte(lambda k: k['ereignisse'].append({'id': 'E01', 'datum': '2028-02-29', 'titel': 'Schalttag'})))[0]
        anfrage('/api/fall/R-0001', {'akte': proben[0][1], 'revision': rev2}, erwartet=400)
        assert '2026-02-31' not in (root / f1['ordner'] / 'akte.json').read_text()
        ok('Schema: 31. Februar, Monat 13, fall=null, Liste statt Objekt, Zahl statt Eintrag, true statt Zahl geben Fehler statt Absturz; Schalttag gilt')
        ok('Bestätigte Frist ohne Grundlage wird nicht gespeichert')
        staende = sorted((base / 'Sicherungen' / 'Ordnungsstände' / 'R-0001').glob('*_akte.json')); assert staende
        ok('Vorfassung der Ordnungsdaten außerhalb des Projekts gesichert')

        # 6 Fristen, Aufgaben, Journal
        sys.path.insert(0, str(root / '06 Werkzeuge/dienst')); import fristen
        # Grenzfälle der §§ 187, 188 BGB ohne § 193 BGB. Erwartungswerte von Hand aus dem Gesetzestext abgeleitet,
        # nicht aus dem Rechner (Prüfbericht 16.09.2026, F02: Beginnfrist am Monatsende endete einen Tag zu früh).
        # (Start, Menge, Einheit, Ereignisfrist?, erwartetes Ende, § 188 Abs. 3 erwartet?)
        grenzfaelle = [
            ('2026-01-31', 1, 'monate', False, '2026-02-28', True),    # 31.02. fehlt: letzter Tag des Monats
            ('2026-01-30', 1, 'monate', False, '2026-02-28', True),
            ('2026-01-29', 1, 'monate', False, '2026-02-28', True),    # 29.02. fehlt 2026
            ('2026-01-28', 1, 'monate', False, '2026-02-27', False),   # 28.02. vorhanden, also der Vortag
            ('2028-01-30', 1, 'monate', False, '2028-02-29', True),    # Schaltjahr
            ('2028-01-29', 1, 'monate', False, '2028-02-28', False),
            ('2026-03-01', 1, 'monate', False, '2026-03-31', False),   # Vortag des 01.04.
            ('2026-03-31', 1, 'monate', False, '2026-04-30', True),
            ('2026-08-31', 6, 'monate', False, '2027-02-28', True),
            ('2028-02-29', 1, 'jahre', False, '2029-02-28', True),
            ('2028-03-01', 1, 'jahre', False, '2029-02-28', False),
            ('2026-03-02', 2, 'wochen', False, '2026-03-15', False),   # Montag bis Sonntag
            ('2026-02-05', 10, 'tage', False, '2026-02-14', False),
            ('2026-01-31', 1, 'monate', True, '2026-02-28', True),     # Ereignisfrist, § 188 Abs. 3
            ('2026-05-31', 1, 'monate', True, '2026-06-30', True),
            ('2026-03-31', 1, 'monate', True, '2026-04-30', True),
            ('2028-02-29', 1, 'jahre', True, '2029-02-28', True),
            ('2026-01-15', 1, 'monate', True, '2026-02-15', False),
            ('2026-02-05', 2, 'wochen', True, '2026-02-19', False),
            ('2026-02-05', 10, 'tage', True, '2026-02-15', False),
        ]
        for start, menge, einheit, ereignis, erwartet, abs3 in grenzfaelle:
            r = fristen.berechne(start, menge, einheit, ereignisfrist=ereignis, werktagsregel=False)
            art = 'Ereignisfrist' if ereignis else 'Beginnfrist'
            assert r['ende'] == erwartet, f'{start} + {menge} {einheit} ({art}): {r["ende"]} statt {erwartet}'
            assert ('§ 188 Abs. 3 BGB' in r['grundlagen']) == abs3, f'{start} + {menge} {einheit} ({art}): § 188 Abs. 3 {"fehlt" if abs3 else "zu viel"}'
            assert r['ende_text'] in ' '.join(r['rechnung']), f'{start}: Rechnung nennt nicht das Ergebnis'
        ok(f'Fristenrechner: {len(grenzfaelle)} Grenzfälle der §§ 187, 188 BGB (Monatsende, Schaltjahr, Jahresfrist, Beginn- und Ereignisfrist)')
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-08-21', 'menge': 3, 'einheit': 'wochen'}); assert fr['ende'] == '2026-09-11'
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-09-05', 'menge': 2, 'einheit': 'wochen'}); assert fr['ende'] == '2026-09-21' and fr['verschoben']
        ok('Fristenrechner über die Schnittstelle, mit § 193 BGB')
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-06-03', 'menge': 1, 'einheit': 'tage', 'land': 'BW'}); assert fr['ende'] == '2026-06-05' and 'Fronleichnam' in ' '.join(fr['rechnung'])
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-06-03', 'menge': 1, 'einheit': 'tage', 'land': 'BE'}); assert fr['ende'] == '2026-06-04'
        fr = anfrage('/api/fristen/berechnen', {'start': '2025-05-07', 'menge': 1, 'einheit': 'tage', 'land': 'BE'}); assert fr['ende'] == '2025-05-09', fr   # 08.05.2025 (Donnerstag) in Berlin einmalig Feiertag, GVBl. Berlin 2024 S. 460
        fr = anfrage('/api/fristen/berechnen', {'start': '2025-05-07', 'menge': 1, 'einheit': 'tage', 'land': 'BB'}); assert fr['ende'] == '2025-05-08', fr
        anfrage('/api/einstellungen', {'einstellungen': {'feiertagsland': 'NW'}}); assert anfrage('/api/einstellungen')['einstellungen']['feiertagsland'] == 'NW'
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-10-30', 'menge': 2, 'einheit': 'tage'}); assert fr['ende'] == '2026-11-02' and fr['feiertagsland'] == 'NW'
        anfrage('/api/fristen/berechnen', {'start': '2026-06-03', 'menge': 1, 'einheit': 'tage', 'land': 'XX'}, erwartet=400)
        ok('Feiertage je Bundesland (Fronleichnam BW, nicht BE), Einstellung Bundesland, unbekanntes Land abgewiesen')
        r = anfrage('/api/werkzeug', {'name': 'beispiel_laden', 'parameter': {}, 'bestaetigt': True}); beispiel = r['id']
        b = anfrage('/api/fall/' + beispiel); assert b['akte']['fall']['id'] == beispiel and b['akte']['fall']['bereich'] == 'Arbeit'
        assert set(b['akte']['dokumente']) == {d['id'] for d in b['dokumente']}
        d4 = next(d for d in b['dokumente'] if d['id'] == 'D0004'); assert any(isinstance(v, str) and v.endswith('Kuendigungsschutzklage_ENTWURF.md') for v in d4.values())
        assert anfrage('/api/werkzeug', {'name': 'bestand_pruefen', 'parameter': {'fall': beispiel}})['geprueft'] == 4
        ok('Beispielfall laden: Kennungen wie in akte.json, Bestand 4 geprüft')
        r = anfrage('/api/werkzeug', {'name': 'frist_eintragen', 'parameter': {'fall': 'R-0001', 'datum': '2026-09-21', 'titel': 'Einspruchsfrist', 'art': 'gesetzlich', 'ausloeser': 'Zustellung 05.09.2026', 'rechtsgrundlage': '§ 67 Abs. 1 OWiG', 'berechnung': '\n'.join(fr['rechnung']), 'pruefstatus': 'offen', 'quelle': 'D0001'}, 'bestaetigt': True})
        assert r['frist']['id'] == 'F01'
        r = anfrage('/api/werkzeug', {'name': 'aufgabe_anlegen', 'parameter': {'fall': 'R-0001', 'titel': 'Zustellurkunde anfordern', 'quelle': 'D0001'}, 'bestaetigt': True}); assert r['aufgabe']['id'] == 'A01'
        anfrage('/api/werkzeug', {'name': 'aufgabe_anlegen', 'parameter': {'fall': 'R-0001', 'titel': 'x', 'quelle': 'D9999'}, 'bestaetigt': True}, erwartet=400)
        r = anfrage('/api/werkzeug', {'name': 'aufgabe_anlegen', 'parameter': {'fall': 'R-0001', 'titel': 'Freitext-Quelle', 'quelle': 'Zustellung laut Bescheid'}, 'bestaetigt': True})
        assert r['aufgabe']['quelle'] == '' and 'Zustellung laut Bescheid' in r['aufgabe']['detail']
        ok('Frist und Aufgabe eingetragen; unbekannte Kennung abgewiesen, Freitext-Quelle in den Text verschoben')
        anfrage('/api/werkzeug', {'name': 'journal_schreiben', 'parameter': {'fall': 'R-0001', 'art': 'Eingang', 'titel': 'Anhörungsbogen', 'text': 'Eingang D0001 gelesen.'}, 'bestaetigt': True})
        j = anfrage('/api/fall/R-0001/journal')['eintraege']; assert j[-1]['art'] == 'Eingang' and j[-1]['titel'] == 'Anhörungsbogen' and j[0]['titel'] == 'Fall angelegt'
        ok('Journal anhängen und lesen')
        anfrage('/api/werkzeug', {'name': 'loeschen', 'parameter': {}}, erwartet=400); ok('Unbekanntes Werkzeug abgewiesen')

        q = anfrage('/api/quellen'); assert isinstance(q['quellen'], list)
        anfrage('/api/oeffnen', {'bereich': 'unbekannt'}, erwartet=400)
        z = anfrage('/api/zentrale'); assert any(f['id'] == 'R-0001' and f['fristen'] and f['fristen'][0]['id'] == 'F01' for f in z['faelle'])
        ok('Quellenkatalog, Öffnen mit unbekanntem Ort abgewiesen, Fristen in der Fallübersicht')

        # 7 Gemeinsamer Eingang
        anfrage('/api/eingang', {'name': 'Brief.pdf', 'inhalt': base64.b64encode(b'%PDF-1.4 test').decode()})
        assert anfrage('/api/zentrale')['eingang'][0]['name'] == 'Brief.pdf'
        r = anfrage('/api/eingang/zuordnen', {'name': 'Brief.pdf', 'fall': 'R-0002'}); assert r['dokument'] == 'D0001' and (root / f2['ordner'] / '01 Eingang/Brief.pdf').is_file()
        ok('Gemeinsamen Eingang einem Fall zugeordnet')
        r = anfrage('/api/werkzeug', {'name': 'dokument_ordnen', 'parameter': {'fall': 'R-0002', 'dokument': 'D0001', 'felder': {'titel': 'Brief', 'stand': 'Zugegangen'}}, 'bestaetigt': True})
        assert r['dokument'] == 'D0001'
        r = anfrage('/api/werkzeug', {'name': 'entwurf_erfassen', 'parameter': {'fall': 'R-0002', 'titel': 'Antwort', 'datei': '06 Entwürfe/Antwort_ENTWURF.md', 'status': 'versandt', 'versandt_als': 'D0001'}, 'bestaetigt': True})
        assert r['entwurf']['versandt_als'] == 'D0001'
        a2 = json.loads((root / f2['ordner'] / 'akte.json').read_text()); assert a2['dokumente']['D0001']['stand'] == 'Zugegangen'
        ok('Neu zugeordnetes Dokument sofort ordnen und als Versandbeleg verweisen, ohne vorheriges Lesen der Akte')

        # 8 Sicherung
        s = anfrage('/api/sicherung', {}); zp = Path(s['pfad']); assert zp.is_file() and s['zweites_ziel'] and Path(s['zweites_ziel']).is_file()
        assert hashlib.sha256(zp.read_bytes()).hexdigest() == s['sha256'] == zp.with_suffix('.zip.sha256').read_text().split()[0]
        with zipfile.ZipFile(zp) as zf: assert zf.testzip() is None and f"{f1['ordner']}/akte.json" in zf.namelist()
        assert anfrage('/api/sicherung/status')['unveraendert']
        ok('Geprüfte Sicherung mit Prüfsumme und Kopie am zweiten Ziel')

        # 9 MCP-Server über die Standardeingabe
        mcp = subprocess.Popen([sys.executable, str(root / '06 Werkzeuge/dienst/mcp_server.py'), '--root', str(root)],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8')
        def rpc(obj):
            mcp.stdin.write(json.dumps(obj, ensure_ascii=False) + '\n'); mcp.stdin.flush()
            zeile = mcp.stdout.readline(); assert zeile, 'MCP-Server antwortet nicht'
            return json.loads(zeile)
        try:
            a = rpc({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'Test', 'version': '0'}}})
            assert a['id'] == 1 and a['result']['protocolVersion'] == '2025-06-18' and 'tools' in a['result']['capabilities'] and a['result']['serverInfo']['name'] == 'aka-recht' and 'resultType' not in a['result']
            mcp.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n'); mcp.stdin.flush()
            a = rpc({'jsonrpc': '2.0', 'id': 2, 'method': 'ping', 'params': {}}); assert a['id'] == 2 and a['result'] == {}
            ok('MCP: Handshake der älteren Fassung (initialize, initialized ohne Antwort, ping)')
            a = rpc({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/list', 'params': {}}); tools = a['result']['tools']; namen = {t['name'] for t in tools}
            assert len(tools) >= 18 and 'fall_uebersicht' in namen and 'fall_lesen' not in namen and 'akte_speichern' not in namen
            assert all(t['inputSchema']['type'] == 'object' for t in tools)
            schreibend = [t for t in tools if not t['annotations']['readOnlyHint']]; lesend = [t for t in tools if t['annotations']['readOnlyHint']]
            assert schreibend and lesend and all('bestaetigt' in t['inputSchema']['properties'] for t in schreibend) and not any('bestaetigt' in t['inputSchema']['properties'] for t in lesend)
            ok(f'MCP: tools/list mit {len(tools)} Werkzeugen, ohne Ganz-Akte-Werkzeuge; schreibende mit Parameter bestaetigt')
            a = rpc({'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call', 'params': {'name': 'faelle_auflisten', 'arguments': {}}})
            assert not a['result']['isError'] and [f['id'] for f in a['result']['structuredContent']['ergebnis']][:2] == ['R-0001', 'R-0002'] and 'R-0001' in a['result']['content'][0]['text']
            a = rpc({'jsonrpc': '2.0', 'id': 5, 'method': 'tools/call', 'params': {'name': 'fall_uebersicht', 'arguments': {'fall': 'R-0001'}}})
            assert a['result']['structuredContent']['fristen'][0]['id'] == 'F01' and a['result']['structuredContent']['dokumente']
            ok('MCP: lesende Aufrufe liefern Text und strukturiertes Ergebnis')
            a = rpc({'jsonrpc': '2.0', 'id': 6, 'method': 'tools/call', 'params': {'name': 'notiz_anlegen', 'arguments': {'fall': 'R-0001', 'titel': 'MCP-Probe', 'text': 'ohne Bestätigung'}}})
            assert a['result']['structuredContent'].get('bestaetigung_noetig') and 'Rückfrage' in a['result']['content'][0]['text']
            assert not anfrage('/api/fall/R-0001')['akte']['notizen']
            for wert in ('true', 'false', 1, None):
                a = rpc({'jsonrpc': '2.0', 'id': 60, 'method': 'tools/call', 'params': {'name': 'notiz_anlegen', 'arguments': {'fall': 'R-0001', 'titel': 'MCP-Probe', 'text': 'Typprobe', 'bestaetigt': wert}}})
                assert a['result']['isError'] and 'bestaetigt' in a['result']['content'][0]['text'], (wert, a)
            assert not anfrage('/api/fall/R-0001')['akte']['notizen']
            a = rpc({'jsonrpc': '2.0', 'id': 7, 'method': 'tools/call', 'params': {'name': 'notiz_anlegen', 'arguments': {'fall': 'R-0001', 'titel': 'MCP-Probe', 'text': 'mit Bestätigung', 'bestaetigt': True}}})
            assert a['result']['structuredContent']['notiz']['id'] == 'N01' and anfrage('/api/fall/R-0001')['akte']['notizen'][0]['titel'] == 'MCP-Probe'
            ok('MCP: schreibendes Werkzeug hält ohne bestaetigt an und schreibt mit bestaetigt')
            a = rpc({'jsonrpc': '2.0', 'id': 8, 'method': 'tools/call', 'params': {'name': 'loeschen', 'arguments': {}}}); assert a['error']['code'] == -32602
            a = rpc({'jsonrpc': '2.0', 'id': 9, 'method': 'tools/call', 'params': {'name': 'fall_uebersicht', 'arguments': {'fall': 'R-9999'}}}); assert a['result']['isError'] and 'R-9999' in a['result']['content'][0]['text']
            a = rpc({'jsonrpc': '2.0', 'id': 10, 'method': 'gibt/es/nicht', 'params': {}}); assert a['error']['code'] == -32601
            mcp.stdin.write('das ist kein json\n'); mcp.stdin.flush(); a = json.loads(mcp.stdout.readline()); assert a['error']['code'] == -32700
            ok('MCP: unbekanntes Werkzeug und unbekannte Methode als Protokollfehler, Werkzeugfehler als isError, kaputtes JSON gemeldet')
            meta = {'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientCapabilities': {}}
            a = rpc({'jsonrpc': '2.0', 'id': 'd1', 'method': 'server/discover', 'params': {'_meta': meta}})
            assert a['id'] == 'd1' and a['result']['resultType'] == 'complete' and '2026-07-28' in a['result']['supportedVersions'] and a['result']['_meta']['io.modelcontextprotocol/serverInfo']['name'] == 'aka-recht'
            a = rpc({'jsonrpc': '2.0', 'id': 'd2', 'method': 'tools/call', 'params': {'name': 'frist_berechnen', 'arguments': {'start': '2026-08-21', 'menge': 3, 'einheit': 'wochen'}, '_meta': meta}})
            assert a['result']['resultType'] == 'complete' and a['result']['structuredContent']['ende'] == '2026-09-11'
            a = rpc({'jsonrpc': '2.0', 'id': 'd3', 'method': 'tools/list', 'params': {'_meta': {**meta, 'io.modelcontextprotocol/protocolVersion': '1900-01-01'}}}); assert a['error']['code'] == -32022 and '2026-07-28' in a['error']['data']['supported']
            ok('MCP: neue Fassung 2026-07-28 (server/discover, Version je Anfrage, unbekannte Version abgewiesen)')
            mcp.stdin.close(); assert mcp.wait(timeout=10) == 0; ok('MCP: Server beendet sich beim Schließen der Eingabe')
        finally:
            if mcp.poll() is None: mcp.kill(); mcp.wait()

        # 10 Wiederanlauf
        subprocess.run([sys.executable, str(root / '06 Werkzeuge/dienst/server.py'), '--root', str(root), '--no-open'], check=True, capture_output=True, timeout=15)
        assert json.loads(laufzeit.read_text())['pid'] == server.pid; ok('Wiederholter Start verwendet denselben Dienst')
        r = subprocess.run([sys.executable, str(root / '06 Werkzeuge/dienst/server.py'), '--root', str(root), '--check'], capture_output=True, timeout=30)
        assert r.returncode == 0 and 'R-0002' in r.stdout.decode(); ok('Bestandsprüfung über die Befehlszeile')

        ergebnis = {'bestanden': len(bestanden), 'punkte': bestanden, 'ordner': str(base)}
        (base / 'Ergebnis.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2))
        print(f'\n{len(bestanden)} Prüfpunkte bestanden. Testordner: {base}')
        return ergebnis
    finally:
        if server and server.poll() is None:
            server.terminate()
            try: server.wait(timeout=10)
            except subprocess.TimeoutExpired: server.kill(); server.wait()
        if laufzeit.exists(): laufzeit.unlink()

if __name__ == '__main__':
    run()
