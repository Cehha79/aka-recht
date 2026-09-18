#!/usr/bin/env python3
"""SessionStart-Hook: meldet neue Post, nahe Fristen und offene Aufgaben aller Fälle.
Liest nur. Gibt Kontext für Claude als JSON aus. Bei Fehlern still (Exit 0)."""
import sys

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); Ausgaben für Assistenten und Tests müssen UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
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
        # Die Live-Dokumentation ist interne Entwicklungsdoku und liegt nicht in jeder Mappe;
        # nur nennen, wenn sie da ist (Befund 18.09.2026 beim Trennen von Akte und Entwicklung).
        uebergabe = '; Übergabe: DOKU/md/Live-Dokumentation.md' if (root / 'DOKU' / 'md' / 'Live-Dokumentation.md').exists() else ''
        zeilen = [f'AKA Recht, Sitzungsstart {date.today():%d.%m.%Y}. Arbeitsprofil: CLAUDE.md im Projekt{uebergabe}.']
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
            if nah: teile.append('Fristen: ' + '; '.join(f'{x["datum"]} {x["titel"]} [{x["pruefstatus"]}' + (', ohne Prüfdatum' if x['pruefstatus'] == 'bestätigt' and not x.get('eigenschaften', {}).get('geprueft') else '') + (', offener Marker' if x.get('eigenschaften', {}).get('offene_marker') else '') + (', Auslöser unsicher' if x.get('eigenschaften', {}).get('ausloeser_sicher') is False else '') + ']' + (' ÜBERSCHRITTEN' if x['datum'] < heute else '') for x in nah))
            teile.append(f'offene Aufgaben: {f["offene_aufgaben"]}')
            zeilen.append(' · '.join(teile))
        if not werkzeuge.faelle_auflisten(): zeilen.append('Noch kein Fall im neuen Format eingetragen (zentrale.json).')
        try:   # Stufe 12: Rechtsinhalte, die wieder am Volltext zu prüfen sind; nur melden, wenn etwas ansteht
            r = werkzeuge.rechtsinhalte_pruefen()
            offen = [e for e in r['eintraege'] if e['status'] != 'in Ordnung']
            if offen: zeilen.append(f'Rechtsinhalte: {r["faellig"]} fällig, {r["bald_faellig"]} bald fällig, {r["unbekannt"]} ohne lesbares Prüfdatum (rechtsinhalte_pruefen): ' + '; '.join(f'{e["name"]} {e["status"]}' + (f' ab {e["faellig_ab"]}' if e['faellig_ab'] else '') for e in offen[:6]) + (f' und {len(offen) - 6} weitere' if len(offen) > 6 else '') + '.')
        except Exception as e: zeilen.append(f'Rechtsinhalte: Prüfung nicht möglich ({e}).')
        zeilen.append('Regeln: Originale nie ändern; Fristen nur mit Auslöser, Grundlage, Rechnung; nichts versenden; Werkzeuge über 06 Werkzeuge/dienst/cli.py.')
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': '\n'.join(zeilen)}}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': f'AKA Recht: Sitzungsstart-Hook konnte die Akten nicht lesen ({e}).'}}, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    sys.exit(main())
