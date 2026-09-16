#!/usr/bin/env python3
"""PreToolUse-Hook für Write, Edit, MultiEdit: blockiert Schreiben in Originalbereiche
einer Fallakte (02 Grundlagen, 03 Schriftverkehr, 04 Verfahren, 05 Beweise, 08 Archiv)
und in bestand.json. Erlaubt: 06 Entwürfe, 07 Recherche, 01 Eingang, akte.json, JOURNAL.md.
Exit 2 = blockieren, Meldung auf stderr geht an Claude."""
import sys
sys.dont_write_bytecode = True
import json, re

def main():
    try: daten = json.load(sys.stdin)
    except Exception: return 0
    pfad = str((daten.get('tool_input') or {}).get('file_path') or '')
    if not pfad: return 0
    m = re.search(r'02 F[aä]lle/[^/]+/(0[2-58] [^/]+)/', pfad)
    if m:
        print(f'AKA Recht, Originalschutz: Schreiben in „{m[1]}“ ist gesperrt. Originale werden nie verändert. Neue Fassungen gehören nach 06 Entwürfe, Vermerke nach 07 Recherche.', file=sys.stderr); return 2
    if pfad.endswith('/bestand.json'):
        print('AKA Recht: bestand.json schreibt nur der Dienst. Neue oder verschobene Dateien mit cli.py bestand_abgleichen (nach Freigabe) registrieren.', file=sys.stderr); return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
