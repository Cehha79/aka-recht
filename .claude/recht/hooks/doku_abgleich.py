#!/usr/bin/env python3
"""Stop-Hook: prüft am Ende einer Antwort, ob erzeugte Dateien zu ihren Quellen passen, und nennt
konkret, was nachzuziehen ist. Blockiert nicht (Exit 0).
Seit 17.09.2026 (Prüfbericht F26) inhaltlich statt nach Zeitstempel:
1. Jede HTML-Ansicht in DOKU/ wird aus ihrer md-Quelle neu erzeugt (im Speicher, mit ansicht_bauen.py)
   und mit der gespeicherten Datei verglichen; jede abweichende oder fehlende Ansicht wird einzeln genannt.
2. AGENTS.md und .agents/skills/ werden über `verteilen.py --pruefen` gegen CLAUDE.md und .claude/skills/
   verglichen; jede fehlende oder veraltete Kopie wird genannt.
3. Nur als Hinweis bleibt der Zeitvergleich: Code- oder Skill-Dateien, die jünger sind als
   DOKU/md/Live-Dokumentation.md, werden mit Namen aufgezählt (fehlt die Live-Doku wie im Produkt, entfällt das).
Läuft auch ohne zentrale.json (Entwicklung ohne eingerichtete Akte)."""
import sys

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); Ausgaben für Assistenten und Tests müssen UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
import importlib.util, os, subprocess
from pathlib import Path


def ansichten_pruefen(root):
    """Jede md-Quelle neu rendern und mit der HTML-Datei vergleichen. Liefert Namen abweichender Ansichten."""
    skript = root / 'DOKU' / 'ansicht_bauen.py'
    if not skript.is_file() or not (root / 'DOKU' / 'md').is_dir(): return []
    spec = importlib.util.spec_from_file_location('ansicht_bauen', skript); modul = importlib.util.module_from_spec(spec); spec.loader.exec_module(modul)
    vorhanden = [n for n in modul.REIHENFOLGE if (modul.MD / f'{n}.md').exists()]
    vorhanden += sorted(p.stem for p in modul.MD.glob('*.md') if p.stem not in vorhanden)
    lokal = modul.nur_lokal()   # N09: veröffentlichte Seiten verlinken nur veröffentlichte
    oeffentlich = [n for n in vorhanden if n not in lokal]
    abweichend = []
    for n in vorhanden:
        quelle = modul.MD / f'{n}.md'; ziel = modul.DOKU / f'{n}.html'
        text = quelle.read_text('utf-8'); inhalt, abschnitte = modul.render(text)
        soll = modul.seite(n, inhalt, abschnitte, vorhanden if n in lokal else oeffentlich, modul.stand(text))   # Stempel aus der Stand-Zeile, nicht aus der Dateizeit
        ist = ziel.read_text('utf-8') if ziel.is_file() else None
        if ist != soll: abweichend.append(f'DOKU/{n}.html' + ('' if ist is not None else ' (fehlt)'))
    return abweichend


def verteilung_pruefen(root):
    """AGENTS.md und .agents/skills/ gegen die Quellen: Zeilen „fehlt“ und „veraltet“ aus verteilen.py --pruefen."""
    skript = root / '06 Werkzeuge' / 'verteilen.py'
    if not skript.is_file() or not (root / 'CLAUDE.md').is_file(): return []
    try: r = subprocess.run([sys.executable, str(skript), '--pruefen'], capture_output=True, text=True, timeout=30, cwd=root)
    except Exception as e: return [f'verteilen.py --pruefen nicht ausführbar ({e})']
    return [z.strip() for z in r.stdout.splitlines() if z.startswith(('fehlt', 'veraltet'))]


def juengere_als_doku(root):
    doku = root / 'DOKU' / 'md' / 'Live-Dokumentation.md'
    if not doku.is_file(): return []
    grenze = doku.stat().st_mtime + 60; treffer = []
    for ordner in ('06 Werkzeuge', '.claude/recht', '.claude/skills'):
        p = root / ordner
        if not p.exists(): continue
        for f in p.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts and not f.name.startswith('.') and f.stat().st_mtime > grenze: treffer.append(str(f.relative_to(root)))
    for f in (root / 'CLAUDE.md',):
        if f.is_file() and f.stat().st_mtime > grenze: treffer.append(f.name)
    return sorted(treffer)


def main():
    root = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[3]).resolve()
    hinweise = []
    try: a = ansichten_pruefen(root)
    except Exception as e: a = [f'Ansichten nicht prüfbar ({e})']
    if a: hinweise.append('HTML-Ansichten weichen von ihrer md-Quelle ab: ' + ', '.join(a) + '. python3 DOKU/ansicht_bauen.py ausführen.')
    v = verteilung_pruefen(root)
    if v: hinweise.append('Erzeugte Kopien für andere Assistenten sind nicht aktuell: ' + '; '.join(v) + '. python3 "06 Werkzeuge/verteilen.py" ausführen.')
    j = juengere_als_doku(root)
    if j: hinweise.append('Jünger als DOKU/md/Live-Dokumentation.md: ' + ', '.join(j[:8]) + (f' und {len(j) - 8} weitere' if len(j) > 8 else '') + '. Live-Dokumentation.md und TODO.md prüfen.')
    if hinweise: print('AKA Recht, Doku-Abgleich: ' + ' '.join(hinweise))
    return 0


if __name__ == '__main__':
    sys.exit(main())
