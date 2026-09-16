#!/usr/bin/env python3
"""Stop-Hook: erinnert an den Doku-Abgleich, wenn Code jünger ist als die Doku
oder die HTML-Ansichten älter als die md-Quellen. Blockiert nicht (Exit 0)."""
import sys
sys.dont_write_bytecode = True
import os
from pathlib import Path

def juengste(pfad, muster='*'):
    p = Path(pfad)
    if not p.exists(): return 0
    return max((f.stat().st_mtime for f in p.rglob(muster) if f.is_file() and '__pycache__' not in f.parts), default=0)

def main():
    root = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[3])
    if not (root / 'zentrale.json').exists(): return 0
    code = max(juengste(root / '06 Werkzeuge'), juengste(root / '.claude/recht'))
    md = juengste(root / 'DOKU/md', '*.md'); html = juengste(root / 'DOKU', '*.html')
    hinweise = []
    if code and md and code > md + 60: hinweise.append('Code wurde nach der letzten Doku-Änderung geändert: DOKU/md/Live-Dokumentation.md und TODO.md prüfen.')
    if md and html and md > html + 5: hinweise.append('md-Quellen sind jünger als die HTML-Ansichten: python3 DOKU/ansicht_bauen.py ausführen.')
    if hinweise: print('AKA Recht, Doku-Abgleich: ' + ' '.join(hinweise))
    return 0

if __name__ == '__main__':
    sys.exit(main())
