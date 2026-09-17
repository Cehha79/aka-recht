#!/usr/bin/env python3
"""Befehlszeilen-Zugang zu den Werkzeugen des Dienstes, ohne laufenden Server.

Für Claude in der Sitzung und für Skripte. Dieselben Werkzeuge, dieselben
Prüfungen (Schema, Revision, Sperre) wie in der Oberfläche.

Aufruf:
  python3 "06 Werkzeuge/dienst/cli.py" liste
  python3 "06 Werkzeuge/dienst/cli.py" <werkzeug> '<JSON-Parameter>'
  python3 "06 Werkzeuge/dienst/cli.py" <werkzeug> schluessel=wert schluessel2=wert …

Beispiele:
  cli.py faelle_auflisten
  cli.py fall_lesen fall=R-0001
  cli.py frist_berechnen start=2026-08-21 menge=3 einheit=wochen
  cli.py journal_schreiben fall=R-0001 art=Arbeit titel="Fristen geprüft" text="F01 und F02 gerechnet."
Schreibende Werkzeuge laufen hier als bestätigt: Die Freigabe ist der Aufruf
selbst, den der Nutzer tippt oder in seinem KI-Client je Befehl genehmigt
(Entscheidung 16.09.2026 zu F04). Eine KI ohne solchen Dialog darf cli.py für
schreibende Werkzeuge nur nach ausdrücklicher Zustimmung des Nutzers aufrufen.
"""
import sys
# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); JSON für Assistenten muss UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import store, werkzeuge

def main(argv):
    if len(argv) < 2 or argv[1] in ('-h', '--help'): print(__doc__); return 2
    name = argv[1]
    if name == 'liste':
        for w in werkzeuge.beschreibung():
            print(f"{w['name']:<24} {'schreibend' if w['schreibend'] else 'lesend    '}  {w['beschreibung']}")
            for p, s in w['parameter']['properties'].items():
                print(f"    {p}{'*' if p in w['parameter']['required'] else ''}: {s.get('type', '')} {('= ' + '|'.join(map(str, s['enum']))) if 'enum' in s else ''} {s.get('description', '')}".rstrip())
        return 0
    if len(argv) == 3 and argv[2].strip().startswith('{'): args = json.loads(argv[2])
    else:
        args = {}
        for teil in argv[2:]:
            if '=' not in teil: print(f'Parameter „{teil}“ braucht die Form schluessel=wert.'); return 2
            k, v = teil.split('=', 1)
            if v in ('true', 'false'): v = v == 'true'
            elif v.isdigit(): v = int(v)
            elif v.startswith('[') or v.startswith('{'):
                try: v = json.loads(v)
                except json.JSONDecodeError: pass
            args[k] = v
    if not store.eingerichtet(): print('Hinweis: zentrale.json fehlt, die Mappe ist noch nicht eingerichtet (Start.command einmal ausführen).', file=sys.stderr)
    try:
        erg = werkzeuge.ausfuehren(name, args, bestaetigt=True)
    except Exception as e:
        print(json.dumps({'fehler': str(e)}, ensure_ascii=False)); return 1
    print(json.dumps(erg, ensure_ascii=False, indent=2)); return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
