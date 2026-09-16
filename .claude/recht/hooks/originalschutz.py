#!/usr/bin/env python3
"""PreToolUse-Hook für Write, Edit, MultiEdit: blockiert Schreiben in Originalbereiche
einer Fallakte (02 Grundlagen, 03 Schriftverkehr, 04 Verfahren, 05 Beweise, 08 Archiv)
und in bestand.json. Erlaubt: 06 Entwürfe, 07 Recherche, 01 Eingang, akte.json, JOURNAL.md.
Exit 2 = blockieren, Meldung auf stderr geht an Claude.
Seit 17.09.2026 (Prüfbericht F06, nur Pfadauflösung): Der Pfad wird gegen den Projektordner
(CLAUDE_PROJECT_DIR, sonst Skriptort) aufgelöst, „..“ und Verknüpfungen werden normalisiert,
geprüft werden die Ordnerbestandteile des aufgelösten Pfads statt eines Textmusters.
Shell-Befehle und MCP-Werkzeuge deckt dieser Hook weiterhin nicht ab (Entscheidung 16.09.2026);
dort schützen der Dienst (keine Werkzeuge für Löschen oder Ändern von Originalen) und die
Bestätigung des Nutzers."""
import sys
sys.dont_write_bytecode = True
import json, os, re
from pathlib import Path

PROJEKT = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[3]).resolve()
FAELLE = ('02 Fälle', '02 Faelle')
GESCHUETZT = re.compile(r'^0[2-58] ')   # 02 Grundlagen, 03 Schriftverkehr, 04 Verfahren, 05 Beweise, 08 Archiv


def aufgeloest(p):
    pfad = Path(p).expanduser()
    if not pfad.is_absolute(): pfad = PROJEKT / pfad
    return pfad.resolve()   # folgt Verknüpfungen, entfernt „..“; die Datei muss noch nicht existieren


def befund(pfad):
    """Liefert den Grund für eine Sperre oder None. Prüft die Bestandteile des aufgelösten Pfads:
    …/02 Fälle/<Fall>/<Bereich>/… mit Bereich 02, 03, 04, 05 oder 08, und …/02 Fälle/<Fall>/bestand.json."""
    teile = pfad.parts
    for i, t in enumerate(teile):
        if t in FAELLE and i + 2 < len(teile):
            bereich = teile[i + 2]
            if i + 2 == len(teile) - 1 and bereich == 'bestand.json':
                return 'AKA Recht: bestand.json schreibt nur der Dienst. Neue oder verschobene Dateien mit cli.py bestand_abgleichen (nach Freigabe) registrieren.'
            if i + 3 < len(teile) and GESCHUETZT.match(bereich):
                return f'AKA Recht, Originalschutz: Schreiben in „{bereich}“ ist gesperrt (aufgelöster Pfad: {pfad}). Originale werden nie verändert. Neue Fassungen gehören nach 06 Entwürfe, Vermerke nach 07 Recherche.'
    return None


def main():
    try: daten = json.load(sys.stdin)
    except Exception: return 0
    eingabe = daten.get('tool_input') if isinstance(daten.get('tool_input'), dict) else {}
    roh = str(eingabe.get('file_path') or eingabe.get('notebook_path') or '')
    if not roh: return 0
    try: pfad = aufgeloest(roh)
    except Exception as e:
        print(f'AKA Recht, Originalschutz: Pfad „{roh}“ lässt sich nicht auflösen ({e}). Sicherheitshalber gesperrt.', file=sys.stderr); return 2
    grund = befund(pfad)
    if grund: print(grund, file=sys.stderr); return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
