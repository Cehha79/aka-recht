#!/usr/bin/env python3
"""SessionStart-Hook: meldet neue Post, nahe Fristen und offene Aufgaben aller Fälle.
Liest nur. Gibt Kontext für Claude als JSON aus. Bei Fehlern still (Exit 0)."""
import sys
sys.dont_write_bytecode = True
import json, os
from datetime import date
from pathlib import Path

def main():
    root = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[3])
    if not (root / 'zentrale.json').exists(): return 0  # kein AKA-Recht-Projekt, nichts melden
    sys.path.insert(0, str(root / '06 Werkzeuge/dienst'))
    try:
        import store, werkzeuge
        store.konfigurieren(root)
        zeilen = [f'AKA Recht, Sitzungsstart {date.today():%d.%m.%Y}. Arbeitsprofil: CLAUDE.md im Projekt; Übergabe: DOKU/md/Live-Dokumentation.md.']
        eingang = [p.name for p in (root / '01 Eingang').iterdir() if p.is_file() and not p.name.startswith('.')] if (root / '01 Eingang').exists() else []
        zeilen.append('Gemeinsamer Eingang: ' + (', '.join(eingang) if eingang else 'leer') + '.')
        heute = date.today().isoformat()
        for f in werkzeuge.faelle_auflisten():
            if f.get('fehler'): zeilen.append(f'{f["id"]}: Fehler beim Lesen: {f["fehler"]}'); continue
            ordner = store.fall_ordner(f['id']); post = [p.name for p in (ordner / '01 Eingang').iterdir() if p.is_file() and not p.name.startswith('.')] if (ordner / '01 Eingang').exists() else []
            nah = [x for x in f['fristen'] if x['datum'] and (x['datum'] < heute or (date.fromisoformat(x['datum']) - date.today()).days <= 21)]
            teile = [f'{f["id"]} {f["titel"]} ({f["bereich"]}, {f["status"]})']
            teile.append('neue Post: ' + (', '.join(post) if post else 'keine'))
            if f.get('nicht_erfasst'): teile.append(f'{f["nicht_erfasst"]} Datei(en) ohne Kennung (bestand_abgleichen nach Freigabe)')
            if nah: teile.append('Fristen: ' + '; '.join(f'{x["datum"]} {x["titel"]} [{x["pruefstatus"]}' + (', ohne Prüfdatum' if x['pruefstatus'] == 'bestätigt' and not x.get('eigenschaften', {}).get('geprueft') else '') + (', offener Marker' if x.get('eigenschaften', {}).get('offene_marker') else '') + ']' + (' ÜBERSCHRITTEN' if x['datum'] < heute else '') for x in nah))
            teile.append(f'offene Aufgaben: {f["offene_aufgaben"]}')
            zeilen.append(' · '.join(teile))
        if not werkzeuge.faelle_auflisten(): zeilen.append('Noch kein Fall im neuen Format eingetragen (zentrale.json).')
        zeilen.append('Regeln: Originale nie ändern; Fristen nur mit Auslöser, Grundlage, Rechnung; nichts versenden; Werkzeuge über 06 Werkzeuge/dienst/cli.py.')
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': '\n'.join(zeilen)}}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': f'AKA Recht: Sitzungsstart-Hook konnte die Akten nicht lesen ({e}).'}}, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    sys.exit(main())
