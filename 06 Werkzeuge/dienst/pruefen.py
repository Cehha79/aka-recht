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

        # 2 Fälle
        f1 = anfrage('/api/fall', {'titel': 'Bußgeld Parkverstoß', 'bereich': 'Verkehr und Bußgeld', 'rolle': 'Betroffener', 'ziel': 'Einspruch prüfen'})
        f2 = anfrage('/api/fall', {'titel': 'Miete Nebenkosten 2025', 'bereich': 'Wohnen und Eigentum'})
        assert f1['id'] == 'R-0001' and f2['id'] == 'R-0002'
        for g in ['01 Eingang', '08 Archiv']: assert (root / f1['ordner'] / g).is_dir()
        assert 'Fall angelegt' in (root / f1['ordner'] / 'JOURNAL.md').read_text()
        ok('Zwei Fälle aus verschiedenen Rechtsgebieten mit festen Kennungen, Ordnern und Journal angelegt')
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
        fall = anfrage('/api/fall/R-0001'); rev = fall['revision']
        assert 'D0001' in fall['akte']['dokumente'] and any(x['id'] == 'D0001' for x in fall['dokumente'])
        ok('Fallakte ergänzt neue Dateien automatisch in den Ordnungsdaten')
        t = anfrage('/api/fall/R-0001/text/D0001'); assert 'Traffistar' in t['text']
        s = anfrage('/api/fall/R-0001/suche?q=traffistar'); assert s['treffer'] == ['D0001']
        ok('Textauszug und Volltextsuche')
        anfrage('/api/fall/R-0002/text/D0001', erwartet=400); ok('Dokumentkennungen bleiben je Fall getrennt')

        # 4 Verschieben, Finder-Verschiebung, Bestand
        r = anfrage('/api/werkzeug', {'name': 'dokument_verschieben', 'parameter': {'fall': 'R-0001', 'dokument': 'D0001', 'bereich': '02 Grundlagen', 'unterordner': 'Bescheide'}})
        assert r.get('bestaetigung_noetig'); ok('Schreibendes Werkzeug ohne Bestätigung hält an')
        r = anfrage('/api/werkzeug', {'name': 'dokument_verschieben', 'parameter': {'fall': 'R-0001', 'dokument': 'D0001', 'bereich': '02 Grundlagen', 'unterordner': 'Bescheide'}, 'bestaetigt': True})
        assert r['pfad'] == '02 Grundlagen/Bescheide/Anhoerung.txt' and (root / f1['ordner'] / r['pfad']).is_file()
        b = json.loads((root / f1['ordner'] / 'bestand.json').read_text()); assert b['dateien']['D0001']['pfad'] == r['pfad'] and b['verschiebungen'][-1]['id'] == 'D0001'
        ok('Einsortieren behält Kennung und protokolliert die Verschiebung')
        os.rename(root / f1['ordner'] / r['pfad'], root / f1['ordner'] / '05 Beweise' / 'Anhoerung.txt')
        fall = anfrage('/api/fall/R-0001'); rev = fall['revision']
        assert fall['akte']['dokumente']['D0001']['pfad'] == '05 Beweise/Anhoerung.txt'
        ok('Im Finder verschobene Datei über Prüfsumme wiedererkannt, Kennung bleibt')
        p = root / f1['ordner'] / '05 Beweise' / 'Anhoerung.txt'; p.write_bytes(inhalt + b'geaendert')
        bp = anfrage('/api/werkzeug', {'name': 'bestand_pruefen', 'parameter': {'fall': 'R-0001'}})
        assert [x['id'] for x in bp['veraendert']] == ['D0001'] and bp['geprueft'] == 1
        p.write_bytes(inhalt); bp = anfrage('/api/werkzeug', {'name': 'bestand_pruefen', 'parameter': {'fall': 'R-0001'}}); assert not bp['veraendert']
        ok('Bestandsprüfung erkennt geänderten Inhalt trotz gleichem Namen')

        # 5 Speichern, Revision, Schema
        fall = anfrage('/api/fall/R-0001'); rev = fall['revision']; akte = fall['akte']
        akte['fall']['ziel'] = 'Einspruch prüfen, Messung anzweifeln'
        r = anfrage('/api/fall/R-0001', {'akte': akte, 'revision': rev}); rev2 = r['revision']; assert rev2 != rev
        anfrage('/api/fall/R-0001', {'akte': akte, 'revision': rev}, erwartet=409)
        ok('Speichern mit Revision; veralteter Stand wird abgewiesen')
        kaputt = json.loads(json.dumps(akte)); kaputt['fristen'].append({'id': 'F01', 'datum': '2026-09-19', 'titel': 'Einspruch', 'art': 'gesetzlich', 'pruefstatus': 'bestätigt'})
        anfrage('/api/fall/R-0001', {'akte': kaputt, 'revision': rev2}, erwartet=400)
        ok('Bestätigte Frist ohne Grundlage wird nicht gespeichert')
        staende = sorted((base / 'Sicherungen' / 'Ordnungsstände' / 'R-0001').glob('*_akte.json')); assert staende
        ok('Vorfassung der Ordnungsdaten außerhalb des Projekts gesichert')

        # 6 Fristen, Aufgaben, Journal
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-08-21', 'menge': 3, 'einheit': 'wochen'}); assert fr['ende'] == '2026-09-11'
        fr = anfrage('/api/fristen/berechnen', {'start': '2026-09-05', 'menge': 2, 'einheit': 'wochen'}); assert fr['ende'] == '2026-09-21' and fr['verschoben']
        ok('Fristenrechner über die Schnittstelle, mit § 193 BGB')
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
            assert not a['result']['isError'] and [f['id'] for f in a['result']['structuredContent']['ergebnis']] == ['R-0001', 'R-0002'] and 'R-0001' in a['result']['content'][0]['text']
            a = rpc({'jsonrpc': '2.0', 'id': 5, 'method': 'tools/call', 'params': {'name': 'fall_uebersicht', 'arguments': {'fall': 'R-0001'}}})
            assert a['result']['structuredContent']['fristen'][0]['id'] == 'F01' and a['result']['structuredContent']['dokumente']
            ok('MCP: lesende Aufrufe liefern Text und strukturiertes Ergebnis')
            a = rpc({'jsonrpc': '2.0', 'id': 6, 'method': 'tools/call', 'params': {'name': 'notiz_anlegen', 'arguments': {'fall': 'R-0001', 'titel': 'MCP-Probe', 'text': 'ohne Bestätigung'}}})
            assert a['result']['structuredContent'].get('bestaetigung_noetig') and 'Rückfrage' in a['result']['content'][0]['text']
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
