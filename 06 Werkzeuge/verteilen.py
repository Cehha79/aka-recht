#!/usr/bin/env python3
"""Verteilen: eine Quelle, erzeugte Kopien für andere KI-Assistenten.

Claude Code liest CLAUDE.md und .claude/skills/. Codex, Cursor, Gemini CLI
und andere lesen AGENTS.md und .agents/skills/. Damit nichts doppelt gepflegt
wird, ist CLAUDE.md die Quelle und dieses Skript erzeugt daraus:

  AGENTS.md                 aus CLAUDE.md, mit wenigen benannten Ersetzungen
  .agents/skills/<name>/    Spiegel von .claude/skills/<name>/ (Datei für Datei)

Vorlagen und Werkzeuge bleiben, wo sie sind; die Skills verweisen auf Pfade
im Projekt, die für jeden Assistenten gleich sind.

Aufruf:
  python3 "06 Werkzeuge/verteilen.py"            erzeugen oder aktualisieren
  python3 "06 Werkzeuge/verteilen.py" --pruefen  nur vergleichen, nichts schreiben
                                                 (Exit 1, wenn eine Kopie fehlt oder veraltet ist)
Das Skript löscht nichts. Verwaiste Kopien werden nur gemeldet.
Nur Standardbibliothek.
"""
import sys

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); Ausgaben für Assistenten und Tests müssen UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUELLE_PROFIL = ROOT / 'CLAUDE.md'
ZIEL_PROFIL = ROOT / 'AGENTS.md'
QUELLE_SKILLS = ROOT / '.claude' / 'skills'
ZIEL_SKILLS = ROOT / '.agents' / 'skills'

KOPF_PROFIL = ('<!-- Erzeugt von „06 Werkzeuge/verteilen.py“ aus CLAUDE.md. Nicht von Hand ändern:\n'
               '     CLAUDE.md pflegen, dann das Skript laufen lassen. -->\n\n')
KOPF_SKILL = ('<!-- Erzeugt von „06 Werkzeuge/verteilen.py“ aus .claude/skills/{name}/SKILL.md.\n'
              '     Nicht von Hand ändern: die Quelle pflegen, dann das Skript laufen lassen. -->\n\n')

# Benannte Ersetzungen. Jede Quellstelle muss genau einmal in CLAUDE.md
# vorkommen, sonst meldet das Skript den Fund und bricht ab. So fällt auf,
# wenn CLAUDE.md umformuliert wurde und die Ersetzung nicht mehr greift.
ERSETZUNGEN = [
    ('# CLAUDE.md – AKA Recht',
     '# AGENTS.md – AKA Recht'),
    ('Arbeitsprofil für Claude in diesem Projekt.',
     'Arbeitsprofil für jeden KI-Assistenten, der diese Datei lädt (geprüft mit\n'
     'Codex; Claude Code liest dasselbe Profil als CLAUDE.md, andere nur wenn sie\n'
     'so eingestellt sind — siehe README, Abschnitt „KI anbinden“).'),
    ('Die Regeln aus `~/.claude/CLAUDE.md` gelten weiter.',
     'Persönliche Regeln des Nutzers gelten zusätzlich, soweit der Assistent sie lädt.'),
    ('3. Der SessionStart-Hook meldet Eingang und Fristen der Fälle.',
     '3. Zum Sitzungsstart `python3 "06 Werkzeuge/dienst/cli.py" faelle_auflisten`\n'
     '   aufrufen: Eingang, Fristen und offene Aufgaben je Fall.'),
    ('08 Archiv nie ändern. Ein Hook sperrt das. Neue Texte nach 06 Entwürfe,',
     '08 Archiv nie ändern, auch nicht umbenennen. Neue Texte nach 06 Entwürfe,'),
    ('## Prüfabläufe (Plugin `.claude/recht`)',
     '## Prüfabläufe (Skills unter `.agents/skills/`)'),
    ('Hooks in `.claude/settings.json`:\n'
     'SessionStart (Eingang, Fristen), PreToolUse (Originalschutz), PostToolUse\n'
     '(Fremdtext-Wächter), Stop (Doku-Abgleich). Hook-Änderungen wirken nach\n'
     'Neustart der Sitzung.',
     'Hooks (automatische Prüfungen) sind in dieser Mappe nur für Claude Code\n'
     'eingerichtet (Stand 17.09.2026). Codex beschreibt in seiner Dokumentation\n'
     'eigene Hooks; dafür ist hier nichts konfiguriert und nichts geprüft. Andere\n'
     'Assistenten halten die Regeln selbst ein: zum Sitzungsstart\n'
     '`python3 "06 Werkzeuge/dienst/cli.py" faelle_auflisten` aufrufen (Eingang,\n'
     'Fristen, Aufgaben), nie in die Originalbereiche 02 bis 05 und 08 einer\n'
     'Fallakte schreiben, nie bestand.json anfassen, nach Änderungen die Doku\n'
     'in `DOKU/md/` mitpflegen.'),
]

ANHANG_PROFIL = '''
## Für Assistenten außer Claude Code

- Skills liegen als Kopie unter `.agents/skills/<name>/SKILL.md` (Quelle:
  `.claude/skills/`). Platzhalter wie `$fall` stehen für das Argument des
  Aufrufs, etwa die Fallkennung R-0001.
- Alle Werkzeuge laufen ohne Dienst über `python3 "06 Werkzeuge/dienst/cli.py"`;
  `liste` zeigt Namen, Parameter und ob ein Werkzeug schreibt. Schreibende
  Werkzeuge nur nach Rückfrage beim Nutzer aufrufen.
- Diese Datei wird aus CLAUDE.md erzeugt (`python3 "06 Werkzeuge/verteilen.py"`).
  Änderungen gehören in CLAUDE.md.
'''


def profil_erzeugen():
    text = QUELLE_PROFIL.read_text('utf-8')
    for alt, neu in ERSETZUNGEN:
        n = text.count(alt)
        if n != 1:
            raise SystemExit(f'Ersetzung greift nicht ({n}× gefunden statt 1×): {alt[:60]!r}. CLAUDE.md wurde umformuliert; ERSETZUNGEN im Skript anpassen.')
        text = text.replace(alt, neu)
    return KOPF_PROFIL + text.rstrip('\n') + '\n' + ANHANG_PROFIL


def skill_erzeugen(name, text):
    """Kopfvermerk hinter dem Frontmatter (--- … ---) einfügen, sonst ganz oben.
    „CLAUDE.md“ wird zu „AGENTS.md“: andere Assistenten lesen das erzeugte Profil."""
    text = text.replace('CLAUDE.md', 'AGENTS.md')
    if text.startswith('---\n'):
        ende = text.find('\n---\n', 4)
        if ende != -1:
            ende += len('\n---\n')
            return text[:ende] + '\n' + KOPF_SKILL.format(name=name) + text[ende:].lstrip('\n')
    return KOPF_SKILL.format(name=name) + text


def geplante_dateien():
    """Alle Zieldateien mit ihrem Sollinhalt."""
    plan = {ZIEL_PROFIL: profil_erzeugen()}
    if not QUELLE_SKILLS.is_dir():
        raise SystemExit(f'Skill-Quelle fehlt: {QUELLE_SKILLS}')
    for ordner in sorted(p for p in QUELLE_SKILLS.iterdir() if p.is_dir() and not p.name.startswith('.')):
        for datei in sorted(p for p in ordner.rglob('*') if p.is_file() and not p.name.startswith('.')):
            ziel = ZIEL_SKILLS / datei.relative_to(QUELLE_SKILLS)
            if datei.name == 'SKILL.md':
                plan[ziel] = skill_erzeugen(ordner.name, datei.read_text('utf-8'))
            else:
                plan[ziel] = datei.read_bytes()
    return plan


def verwaiste(plan):
    """Kopien unter .agents/skills, zu denen es keine Quelle mehr gibt."""
    if not ZIEL_SKILLS.is_dir(): return []
    return sorted(p for p in ZIEL_SKILLS.rglob('*') if p.is_file() and not p.name.startswith('.') and p not in plan)


def lesen(pfad):
    return pfad.read_bytes() if pfad.exists() else None


def main(argv):
    pruefen = '--pruefen' in argv
    if any(a not in ('--pruefen',) for a in argv[1:]):
        print(__doc__); return 2
    plan = geplante_dateien()
    neu, geaendert, gleich = [], [], []
    for ziel, soll in plan.items():
        soll_roh = soll if isinstance(soll, bytes) else soll.encode('utf-8')
        ist = lesen(ziel)
        if ist is None: neu.append(ziel)
        elif ist != soll_roh: geaendert.append(ziel)
        else: gleich.append(ziel)
        if not pruefen and ist != soll_roh:
            ziel.parent.mkdir(parents=True, exist_ok=True)
            ziel.write_bytes(soll_roh)
    rel = lambda p: p.relative_to(ROOT).as_posix()   # immer Schrägstrich, auch unter Windows
    wort = 'fehlt' if pruefen else 'neu'
    for p in neu: print(f'{wort:<10} {rel(p)}')
    wort = 'veraltet' if pruefen else 'aktualisiert'
    for p in geaendert: print(f'{wort:<10} {rel(p)}')
    for p in verwaiste(plan): print(f'verwaist   {rel(p)}  (Quelle fehlt; nicht gelöscht, bitte selbst entscheiden)')
    print(f'{len(gleich)} aktuell, {len(neu)} {"fehlend" if pruefen else "neu"}, {len(geaendert)} {"veraltet" if pruefen else "aktualisiert"}. Quelle: CLAUDE.md und .claude/skills/.')
    return 1 if pruefen and (neu or geaendert) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
