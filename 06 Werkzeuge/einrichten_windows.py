#!/usr/bin/env python3
"""Windows einrichten: Befehl `python3` in den KI-Konfigurationen durch `python` ersetzen.

Unter Windows ist `python3.exe` nur ein Verweis auf den Microsoft Store; der
echte Interpreter von python.org heißt `python`. Die mitgelieferten
Konfigurationen nennen `python3` (richtig für macOS und Linux). Dieses Skript
ändert in genau drei Dateien nur den Wert des Befehls, sonst nichts:

  .mcp.json               MCP-Server für Claude Code
  .claude/settings.json   Hooks für Claude Code (Exec-Form, Pfade über ${CLAUDE_PROJECT_DIR})
  .codex/config.toml      MCP-Server für Codex

Start.bat ruft es bei jedem Start auf; ist alles eingerichtet, ändert es nichts.
Eine lokale Datei kann die Hooks nicht ersetzen (Claude Code legt Hooks aus
settings.json und settings.local.json zusammen), deshalb wird settings.json
selbst angepasst.

Aufruf:
  python "06 Werkzeuge/einrichten_windows.py"              einrichten (nur unter Windows)
  python "06 Werkzeuge/einrichten_windows.py" --pruefen    nur melden; Exit 1, wenn noch python3 steht
  --root <Ordner>   anderer Projektordner (für Tests)
  --erzwingen       auch außerhalb von Windows ändern (nur für Tests)
Exit 0 eingerichtet oder nichts zu tun, 1 noch python3 (bei --pruefen) oder
Fehler, 2 außerhalb von Windows ohne --erzwingen. Nur Standardbibliothek.
"""
import sys

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); Ausgaben für Assistenten und Tests müssen UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
import argparse, json, os, tempfile
from pathlib import Path

# (Datei, alter Text, neuer Text): genau der Befehlswert, in JSON und TOML jeweils in der Schreibweise der Datei.
ERSETZUNGEN = [
    ('.mcp.json', '"command": "python3"', '"command": "python"'),
    ('.claude/settings.json', '"command": "python3"', '"command": "python"'),
    ('.codex/config.toml', 'command = "python3"', 'command = "python"'),
]

def befehle(datei, text):
    """Alle Befehlswerte der Datei, nach dem Einlesen als JSON oder TOML (prüft zugleich, dass die Datei gültig ist)."""
    if datei.endswith('.toml'):
        import tomllib
        return [s.get('command') for s in tomllib.loads(text).get('mcp_servers', {}).values()]
    daten = json.loads(text)
    if datei == '.mcp.json':
        return [s.get('command') for s in daten.get('mcpServers', {}).values()]
    return [h.get('command') for gruppen in daten.get('hooks', {}).values() for g in gruppen for h in g.get('hooks', [])]

def schreiben(pfad, text):
    """Atomar schreiben: erst Zwischendatei im selben Ordner, dann ersetzen; Zeilenenden bleiben, wie sie sind."""
    fd, tmp = tempfile.mkstemp(dir=pfad.parent, prefix='.' + pfad.name + '.')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as fh: fh.write(text)
        os.replace(tmp, pfad)
    except BaseException:
        if os.path.exists(tmp): os.unlink(tmp)
        raise

def main():
    ap = argparse.ArgumentParser(description='python3 durch python in den KI-Konfigurationen ersetzen (Windows).')
    ap.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--pruefen', action='store_true')
    ap.add_argument('--erzwingen', action='store_true')
    a = ap.parse_args()
    root = Path(a.root).resolve()
    if os.name != 'nt' and not a.pruefen and not a.erzwingen:
        print('Nicht Windows: nichts geändert. Unter macOS und Linux bleibt python3 richtig.')
        return 2
    offen = geaendert = 0
    for datei, alt, neu in ERSETZUNGEN:
        pfad = root / datei
        if not pfad.is_file():
            print(f'{datei}: fehlt, übersprungen.'); continue
        text = pfad.read_bytes().decode('utf-8')   # als Bytes lesen: read_text() machte aus CRLF stillschweigend LF (Windows-Test 17.09.2026)
        try: vorher = befehle(datei, text)
        except Exception as e:
            print(f'{datei}: nicht lesbar ({e}), nichts geändert.'); offen += 1; continue
        anzahl = vorher.count('python3')
        if not anzahl:
            print(f'{datei}: bereits eingerichtet.'); continue
        if a.pruefen:
            print(f'{datei}: {anzahl}× python3.'); offen += 1; continue
        neu_text = text.replace(alt, neu)
        nachher = befehle(datei, neu_text)
        if 'python3' in nachher or len(nachher) != len(vorher):
            print(f'{datei}: Schreibweise unerwartet, nichts geändert. Bitte python3 von Hand durch python ersetzen.'); offen += 1; continue
        schreiben(pfad, neu_text); geaendert += 1
        print(f'{datei}: {anzahl}× python3 durch python ersetzt.')
    if geaendert:
        print('Claude Code und Codex neu starten, damit die Änderung wirkt.')
    return 1 if offen else 0

if __name__ == '__main__':
    sys.exit(main())
