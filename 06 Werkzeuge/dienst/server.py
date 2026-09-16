#!/usr/bin/env python3
"""AKA Recht, lokaler Dienst. Ausschließlich 127.0.0.1, Python-Standardbibliothek.

Aufruf:
  python3 server.py                 Dienst starten oder wiederverwenden, Browser öffnen
  python3 server.py --fall R-0001   direkt eine Fallakte öffnen
  python3 server.py --check         Bestand aller Fälle prüfen (ohne Dienst)
  python3 server.py --backup        geprüfte Sicherung erstellen (ohne Dienst)
  python3 server.py --probe [ZIP]   Wiederherstellungsprobe der letzten (oder genannten) Sicherung
  python3 server.py --restore ZIP ORDNER   Sicherung in einen neuen, leeren Ordner außerhalb entpacken und prüfen
  python3 server.py --serve         nur der Dienstprozess (intern)

Zugriff braucht das Sitzungscookie aus dem Startlink; Änderungen zusätzlich die
Schreibkennung im Kopf X-AKA-CSRF und einen Ursprung von 127.0.0.1.
"""
import sys
sys.dont_write_bytecode = True
import argparse, base64, json, mimetypes, os, re, secrets, signal, subprocess, tempfile, threading, time, urllib.request
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bestand, dokumente, fristen, sicherung, store, werkzeuge
OBERFLAECHE = Path(__file__).resolve().parent.parent / 'oberflaeche'
CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-src 'self'; object-src 'none'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"
CSP_ROH = "sandbox allow-scripts; default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; script-src 'unsafe-inline'; frame-ancestors 'self'"
PLATZHALTER = '<!doctype html><html lang="de"><meta charset="utf-8"><title>AKA Recht</title><body style="font-family:-apple-system,sans-serif;padding:40px"><h1>AKA Recht, Dienst läuft</h1><p>Die Oberfläche (Stufe 4) ist noch nicht gebaut. Die Schnittstelle ist unter /api/… erreichbar, der Werkzeugkatalog unter /api/werkzeuge.</p></body></html>'

def laufzeitdatei(): return Path(tempfile.gettempdir()) / f'aka-recht-dienst-{store.instanz()}.json'
def cookie_name(): return 'aka_' + store.instanz()

class Handler(BaseHTTPRequestHandler):
    server_version = 'AKA-Recht/2.0'
    def log_message(self, *a): pass

    def antwort(self, code, koerper, art='application/json; charset=utf-8', kopf=None):
        if not isinstance(koerper, bytes):
            koerper = json.dumps(koerper, ensure_ascii=False).encode() if art.startswith('application/json') else str(koerper).encode()
        self.send_response(code); self.send_header('Content-Type', art); self.send_header('Content-Length', str(len(koerper)))
        self.send_header('Cache-Control', 'no-store'); self.send_header('X-Content-Type-Options', 'nosniff'); self.send_header('Referrer-Policy', 'no-referrer')
        if not kopf or 'Content-Security-Policy' not in kopf: self.send_header('Content-Security-Policy', CSP)
        for k, v in (kopf or {}).items(): self.send_header(k, v)
        self.end_headers()
        try: self.wfile.write(koerper)
        except (BrokenPipeError, ConnectionResetError): pass

    def angemeldet(self):
        if self.headers.get('Host') != f'127.0.0.1:{self.server.server_port}': return False
        c = SimpleCookie()
        try: c.load(self.headers.get('Cookie', ''))
        except Exception: return False
        t = c.get(cookie_name())
        return bool(t and secrets.compare_digest(t.value, self.server.key))

    def do_GET(self):
        u = urlparse(self.path); pfad = unquote(u.path); q = parse_qs(u.query)
        if pfad == '/' and q.get('key') == [self.server.key] and self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}':
            ziel = '/'
            if q.get('fall'):
                try: store.fall_eintrag(q['fall'][0]); ziel = '/#fall=' + q['fall'][0]
                except ValueError: pass
            self.antwort(303, b'', kopf={'Location': ziel, 'Set-Cookie': f'{cookie_name()}={self.server.key}; HttpOnly; SameSite=Strict; Path=/'}); return
        if not self.angemeldet(): self.antwort(403, 'Bitte AKA Recht über Start.command öffnen.', 'text/plain; charset=utf-8'); return
        try:
            if pfad == '/api/ping': self.antwort(200, {'instanz': store.instanz(), 'pid': os.getpid()}); return
            if pfad == '/favicon.ico': self.antwort(204, b'', 'image/x-icon'); return
            if pfad == '/api/zentrale':
                z = store.lade_zentrale()
                eingang = [{'name': p.name, 'groesse': p.stat().st_size} for p in sorted(store.sicher('01 Eingang').iterdir()) if p.is_file() and not p.name.startswith('.')] if store.sicher('01 Eingang').exists() else []
                self.antwort(200, {'app': z['app'], 'root': str(store.ROOT), 'csrf': self.server.csrf, 'faelle': werkzeuge.faelle_auflisten(), 'eingang': eingang,
                                   'sicherung': sicherung.status(), 'gruppen': store.GRUPPEN}); return
            if pfad == '/api/werkzeuge': self.antwort(200, werkzeuge.beschreibung()); return
            if pfad == '/api/quellen': self.antwort(200, werkzeuge.quellen_katalog()); return
            if pfad == '/api/einstellungen':
                z = store.lade_zentrale(); self.antwort(200, {'sicherung': {k: v for k, v in z['sicherung'].items() if k != 'letzte'}, 'einstellungen': z['einstellungen'], 'laender': fristen.LAENDER}); return
            if pfad == '/api/sicherung/status': self.antwort(200, sicherung.status()); return
            if pfad == '/api/bestand':
                self.antwort(200, {'faelle': [werkzeuge.bestand_pruefen(f['id']) for f in store.faelle()]}); return
            m = re.fullmatch(r'/api/fall/(R-\d{4,})', pfad)
            if m: self.antwort(200, werkzeuge.fall_lesen(m[1])); return
            m = re.fullmatch(r'/api/fall/(R-\d{4,})/text/(D\d{4,})', pfad)
            if m: self.antwort(200, werkzeuge.dokument_text(m[1], m[2])); return
            m = re.fullmatch(r'/api/fall/(R-\d{4,})/suche', pfad)
            if m: self.antwort(200, werkzeuge.dokumente_suchen(m[1], q.get('q', [''])[0])); return
            m = re.fullmatch(r'/api/fall/(R-\d{4,})/journal', pfad)
            if m: self.antwort(200, werkzeuge.journal_lesen(m[1])); return
            m = re.fullmatch(r'/(raw|download)/(R-\d{4,})/(D\d{4,})', pfad)
            if m:
                akte, _ = store.lese_akte(m[2]); d = akte['dokumente'].get(m[3])
                if not d: raise ValueError('Unbekannte Dokumentkennung.')
                p = store.sicher(d['pfad'], store.fall_ordner(m[2]))
                if not p.is_file(): raise ValueError('Datei fehlt am registrierten Ort.')
                art = mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
                if p.suffix.lower() in dokumente.TEXT_EXT: art = 'text/plain; charset=utf-8'
                kopf = {'Content-Security-Policy': CSP_ROH}
                if m[1] == 'download': kopf['Content-Disposition'] = "attachment; filename*=UTF-8''" + urllib.request.quote(p.name)
                self.antwort(200, p.read_bytes(), art, kopf); return
            statisch = {'/': 'index.html', '/index.html': 'index.html', '/style.css': 'style.css', '/app.js': 'app.js'}
            if pfad in statisch:
                p = OBERFLAECHE / statisch[pfad]
                if p.is_file(): self.antwort(200, p.read_bytes(), (mimetypes.guess_type(p.name)[0] or 'text/plain') + '; charset=utf-8'); return
                if pfad in ('/', '/index.html'): self.antwort(200, PLATZHALTER, 'text/html; charset=utf-8'); return
            self.antwort(404, {'fehler': 'Nicht gefunden.'})
        except RuntimeError as e: self.antwort(409, {'fehler': str(e)})
        except Exception as e: self.antwort(400, {'fehler': str(e)})

    def do_POST(self):
        if not self.angemeldet() or not secrets.compare_digest(self.headers.get('X-AKA-CSRF', ''), self.server.csrf): self.antwort(403, {'fehler': 'Ungültige Sitzung.'}); return
        if self.headers.get('Origin') not in (None, f'http://127.0.0.1:{self.server.server_port}'): self.antwort(403, {'fehler': 'Fremder Ursprung.'}); return
        try:
            laenge = int(self.headers.get('Content-Length', '0'))
            if not 0 < laenge <= 40 * 1024 * 1024: raise ValueError('Ungültige Anfragegröße.')
            daten = json.loads(self.rfile.read(laenge)); pfad = urlparse(self.path).path
            if pfad == '/api/werkzeug':
                self.antwort(200, werkzeuge.ausfuehren(daten['name'], daten.get('parameter', {}), bestaetigt=daten.get('bestaetigt', False))); return   # nur JSON true zählt (F05)
            if pfad == '/api/fall': self.antwort(200, werkzeuge.fall_anlegen(**{k: daten.get(k, '') for k in ('titel', 'bereich', 'rolle', 'ziel') if daten.get(k)})); return
            m = re.fullmatch(r'/api/fall/(R-\d{4,})', pfad)
            if m: self.antwort(200, werkzeuge.akte_speichern(m[1], daten['akte'], daten['revision'])); return
            m = re.fullmatch(r'/api/fall/(R-\d{4,})/eingang', pfad)
            if m: self.antwort(200, self.datei_ablegen(store.fall_ordner(m[1]) / '01 Eingang', daten, m[1])); return
            if pfad == '/api/eingang': self.antwort(200, self.datei_ablegen(store.sicher('01 Eingang'), daten)); return
            if pfad == '/api/eingang/zuordnen':
                name = str(daten['name']); fall = daten['fall']
                if name != Path(name).name or name.startswith('.'): raise ValueError('Ungültiger Dateiname.')
                quelle = store.sicher('01 Eingang/' + name)
                if not quelle.is_file(): raise ValueError('Eingangsdatei fehlt.')
                ordner = store.fall_ordner(fall); ziel = store.sicher('01 Eingang/' + name, ordner)
                if ziel.exists(): raise ValueError('Dieser Dateiname existiert im Fall bereits. Es wird nichts überschrieben.')
                ziel.parent.mkdir(exist_ok=True); quelle.rename(ziel)
                vorhanden = bestand.aktualisieren(ordner, weg='Zuordnung aus dem gemeinsamen Eingang')
                kennung = next((k for k, p in vorhanden.items() if p == '01 Eingang/' + name), '')
                self.antwort(200, {'fall': fall, 'dokument': kennung, 'pfad': '01 Eingang/' + name}); return
            if pfad == '/api/fristen/berechnen': self.antwort(200, werkzeuge.frist_berechnen(**daten)); return
            if pfad == '/api/oeffnen': self.antwort(200, werkzeuge.oeffnen(daten.get('fall'), daten.get('dokument'), daten.get('bereich'), bool(daten.get('zeigen')))); return
            if pfad == '/api/sicherung': self.antwort(200, sicherung.erstellen()); return
            if pfad == '/api/sicherung/probe': self.antwort(200, sicherung.probe(daten.get('archiv') or None)); return
            if pfad == '/api/einstellungen':
                z = store.lade_zentrale()
                for k in ('ziel', 'zweites_ziel'):
                    if k in daten.get('sicherung', {}): z['sicherung'][k] = daten['sicherung'][k]
                land = str(daten.get('einstellungen', {}).get('feiertagsland', '') or '').upper()
                if land:
                    if land not in fristen.LAENDER: self.antwort(400, {'fehler': 'Unbekanntes Bundesland.'}); return
                    z['einstellungen']['feiertagsland'] = land
                store.speichere_zentrale(z)
                self.antwort(200, {'ok': True}); return
            self.antwort(404, {'fehler': 'Nicht gefunden.'})
        except RuntimeError as e: self.antwort(409, {'fehler': str(e)})
        except Exception as e: self.antwort(400, {'fehler': str(e)})

    def datei_ablegen(self, ordner, daten, fall=None):
        name = str(daten.get('name', ''))
        if name != Path(name).name or name.startswith('.') or not name or any(c in name for c in '/\\\x00:') or len(name) > 180: raise ValueError('Ungültiger Dateiname.')
        inhalt = base64.b64decode(daten['inhalt'], validate=True)
        if len(inhalt) > 25 * 1024 * 1024: raise ValueError('Über 25 MB: bitte die Datei im Finder ablegen.')
        ordner.mkdir(parents=True, exist_ok=True)
        with store.sperre():
            p = ordner / name; n = 2
            while p.exists(): p = ordner / f'{Path(name).stem} ({n}){Path(name).suffix}'; n += 1
            with p.open('xb') as f: f.write(inhalt)
            p.chmod(0o600)
        erg = {'name': p.name}
        if fall:
            vorhanden = bestand.aktualisieren(store.fall_ordner(fall), weg='Import über die Oberfläche')
            erg['dokument'] = next((k for k, rel in vorhanden.items() if rel == '01 Eingang/' + p.name), ''); erg['fall'] = fall
        return erg

# ---------------------------------------------------------------- Betrieb
def laeuft():
    try:
        d = json.loads(laufzeitdatei().read_text())
        anfrage = urllib.request.Request(f'http://127.0.0.1:{d["port"]}/api/ping', headers={'Cookie': f'{cookie_name()}={d["key"]}'})
        with urllib.request.urlopen(anfrage, timeout=1) as r:
            if json.load(r)['instanz'] == store.instanz(): return d
    except Exception: pass

def dienst(port):
    if store.einrichten(): print('zentrale.json angelegt (erste Einrichtung).', flush=True)
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler); server.daemon_threads = True
    server.key = secrets.token_urlsafe(32); server.csrf = secrets.token_urlsafe(32)
    store.atomar(laufzeitdatei(), json.dumps({'port': server.server_port, 'key': server.key, 'csrf': server.csrf, 'pid': os.getpid(), 'instanz': store.instanz()}))
    laufzeitdatei().chmod(0o600)
    print(f'AKA Recht bereit auf 127.0.0.1:{server.server_port}', flush=True)
    def stop(*a): threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGTERM, stop); signal.signal(signal.SIGINT, stop)
    try: server.serve_forever()
    finally: server.server_close()

def starten(oeffnen=True, fall=None):
    with store.sperre():
        d = laeuft()
        if not d:
            protokoll = Path(tempfile.gettempdir()) / f'aka-recht-dienst-{store.instanz()}.log'
            befehl = [sys.executable, str(Path(__file__).resolve()), '--root', str(store.ROOT), '--serve']
            with protokoll.open('ab') as f: subprocess.Popen(befehl, stdin=subprocess.DEVNULL, stdout=f, stderr=f, start_new_session=True)
            for _ in range(80):
                time.sleep(.1); d = laeuft()
                if d: break
            if not d: raise RuntimeError('Dienst startet nicht. Protokoll: ' + str(protokoll))
    if fall: store.fall_eintrag(fall)
    url = f'http://127.0.0.1:{d["port"]}/?key={d["key"]}' + (f'&fall={fall}' if fall else '')
    if oeffnen:
        import webbrowser   # Standardbrowser auf macOS, Linux und Windows
        if not webbrowser.open(url): print('Browser nicht gefunden. Adresse von Hand öffnen: ' + url)
    print('AKA Recht läuft lokal. Dieses Fenster kann geschlossen werden.\nOrdner: ' + str(store.ROOT)); return d

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=store.ROOT)
    p.add_argument('--serve', action='store_true'); p.add_argument('--port', type=int, default=0)
    p.add_argument('--no-open', action='store_true'); p.add_argument('--fall')
    p.add_argument('--check', action='store_true'); p.add_argument('--backup', action='store_true')
    p.add_argument('--probe', nargs='?', const='', metavar='ZIP'); p.add_argument('--restore', nargs=2, metavar=('ZIP', 'ORDNER'))
    a = p.parse_args(); store.konfigurieren(a.root)
    if a.serve: dienst(a.port)
    elif a.probe is not None:
        b = sicherung.probe(a.probe or None); print(json.dumps(b, ensure_ascii=False, indent=2)); sys.exit(0 if b.get('bestanden') else 1)
    elif a.restore:
        b = sicherung.wiederherstellen(a.restore[0], a.restore[1]); print(json.dumps(b, ensure_ascii=False, indent=2)); sys.exit(0 if b.get('bestanden') else 1)
    elif a.check:
        erg = {'faelle': [werkzeuge.bestand_pruefen(f['id']) for f in store.faelle()]}
        print(json.dumps(erg, ensure_ascii=False, indent=2)); sys.exit(0 if all(not f['veraendert'] and not f['fehlend'] for f in erg['faelle']) else 1)
    elif a.backup: print(json.dumps(sicherung.erstellen(), ensure_ascii=False, indent=2))
    else: starten(not a.no_open, a.fall)
