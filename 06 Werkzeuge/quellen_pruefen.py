#!/usr/bin/env python3
"""Prüft die Quellenangaben der mitgelieferten Rechtsinhalte.

REGELN Nr. 12 verlangt, dass jede Rechtsaussage am amtlichen Volltext geprüft ist.
Bisher war das eine Frage der Sorgfalt; dieses Skript macht drei Teile davon nachprüfbar:

1. **Nur amtliche Quellen.** Jede verlinkte Adresse in den Merkblättern, im Quellenkatalog
   und in den Schreibvorlagen muss zu einer amtlichen Stelle gehören (AMTLICH unten).
   Ein Link auf einen Verlag, ein Forum oder eine Zusammenfassung ist ein Fehler — auch
   wenn der Inhalt stimmt, denn er belegt nichts.
2. **Keine Reste aus einer KI-Sitzung.** Zeichenfolgen wie `turn0search`, `oaicite` oder
   „nicht quellenhart verifiziert“ entstehen, wenn eine Antwort aus einem Chat übernommen
   wurde, statt am Volltext zu lesen. Sie sind ein sicheres Zeichen dafür, dass eine
   Fundstelle nicht geprüft ist.
3. **Kopfzeile mit Prüfdatum.** Jedes Merkblatt muss sagen, wann es zuletzt vollständig
   geprüft wurde (das wertet `pflege.py` aus).

Der Gedanke stammt aus `check_legal_anchors.py` von Klotzkette
(github.com/Klotzkette/bautraegervertragspruefer-skill, Apache-2.0 OR MIT, gesehen
18.09.2026); geschrieben ist dieses Skript eigenständig für AKA Recht. Herkunft siehe
`DRITTE.md`.

Aufruf:
    python3 "06 Werkzeuge/quellen_pruefen.py"            nur lesen, kein Netz
    python3 "06 Werkzeuge/quellen_pruefen.py" --netz     zusätzlich jede Adresse abrufen
    python3 "06 Werkzeuge/quellen_pruefen.py" --root ..  anderer Projektordner

Exit 0, wenn alles in Ordnung ist, sonst 1. Schreibt nichts. Nur Standardbibliothek.
"""
import argparse
import re
import sys
from pathlib import Path

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]

# Amtliche Stellen: Gesetzgeber, Gerichte, Behörden und die Landesportale.
# Eine Adresse, die hier nicht steht, gilt als nicht amtlich — im Zweifel lieber melden
# als durchlassen. Neue Portale werden hier eingetragen, mit einem Wort zur Herkunft.
AMTLICH = {
    # Bund
    'www.gesetze-im-internet.de': 'Bundesrecht, BMJ und juris',
    'www.recht.bund.de': 'Verkündungsplattform des Bundes',
    'testphase.rechtsinformationen.bund.de': 'Rechtsinformationsportal des Bundes',
    'www.rechtsprechung-im-internet.de': 'Rechtsprechung des Bundes',
    'service.bund.de': 'Behördensuche des Bundes',
    'verwaltung.bund.de': 'Verwaltungsportal des Bundes',
    'ao.bundesfinanzministerium.de': 'Anwendungserlass zur AO, BMF',
    'www.arbeitsagentur.de': 'Bundesagentur für Arbeit',
    'www.handelsregister.de': 'gemeinsames Registerportal der Länder',
    # Gerichte
    'www.bundesgerichtshof.de': 'BGH', 'www.bundesverfassungsgericht.de': 'BVerfG',
    'www.bverfg.de': 'BVerfG', 'www.bverwg.de': 'BVerwG',
    'www.bundesarbeitsgericht.de': 'BAG', 'www.bundesfinanzhof.de': 'BFH',
    'nrwe.justiz.nrw.de': 'Rechtsprechungsdatenbank NRW',
    'justiz.de': 'Justizportal des Bundes und der Länder',
    'www.justiz.de': 'Justizportal des Bundes und der Länder',
    'service.justiz.de': 'Justizportal, Dienste',
    'www.justizadressen.nrw.de': 'Orts- und Gerichtsverzeichnis',
    'www.mahngerichte.de': 'zentrale Mahngerichte',
    'www.online-mahnantrag.de': 'Mahnantrag der Justiz',
    # Länder
    'www.landesrecht-bw.de': 'Baden-Württemberg', 'www.gesetze-bayern.de': 'Bayern',
    'gesetze.berlin.de': 'Berlin', 'bravors.brandenburg.de': 'Brandenburg',
    'www.transparenz.bremen.de': 'Bremen', 'www.landesrecht-hamburg.de': 'Hamburg',
    'www.rv.hessenrecht.hessen.de': 'Hessen', 'www.landesrecht-mv.de': 'Mecklenburg-Vorpommern',
    'voris.wolterskluwer-online.de': 'Niedersachsen (voris)', 'recht.nrw.de': 'Nordrhein-Westfalen',
    'www.im.nrw': 'Innenministerium NRW', 'landesrecht.rlp.de': 'Rheinland-Pfalz',
    'www.landesrecht.rlp.de': 'Rheinland-Pfalz', 'recht.saarland.de': 'Saarland',
    'www.revosax.sachsen.de': 'Sachsen', 'www.landesrecht.sachsen-anhalt.de': 'Sachsen-Anhalt',
    'www.gesetze-rechtsprechung.sh.juris.de': 'Schleswig-Holstein',
    'landesrecht.thueringen.de': 'Thüringen', 'www.service-bw.de': 'Zuständigkeitsfinder BW',
    'portal.onlinewache.polizei.de': 'Online-Wachen der Länderpolizeien',
    # Europa
    'eur-lex.europa.eu': 'EU-Recht',
}

# Zeichenfolgen, die es in einem geprüften Rechtstext nie geben darf.
VERBOTEN = {
    'turn0search': 'Rest einer Chat-Suche statt einer Fundstelle',
    'turn1search': 'Rest einer Chat-Suche statt einer Fundstelle',
    'oaicite': 'Zitatmarke eines Chatmodells',
    'citeturn': 'Zitatmarke eines Chatmodells',
    '[wordlim': 'Rest einer Chat-Ausgabe',
    'beck-online': 'Verlagsquelle, belegt nichts Amtliches',
    'beckrs': 'Verlagsfundstelle, belegt nichts Amtliches',
    'nicht quellenhart verifiziert': 'Eingeständnis einer ungeprüften Stelle',
    'laut chatgpt': 'keine Quelle',
    'laut claude': 'keine Quelle',
}

URL = re.compile(r'https?://[^\s)\]|,;"\'>]+')
KOPFZEILE = re.compile(r'^\*Letzte vollständige Prüfung:\s*(\d{2}\.\d{2}\.\d{4})\*\s*$', re.M)


def dateien(root):
    """Die Texte, die Rechtsaussagen tragen: Merkblätter, Quellenkatalog, Schreibvorlagen."""
    orte = [root / '04 Rechtsquellen', root / '05 Vorlagen' / 'Schreiben']
    return sorted(p for ort in orte if ort.is_dir() for p in ort.rglob('*.md'))


def pruefe_datei(p, root):
    """Liefert (befunde, adressen) für eine Datei."""
    text = p.read_text('utf-8', errors='replace')
    wo = p.relative_to(root).as_posix()
    befunde = []
    klein = text.lower()
    for muster, grund in VERBOTEN.items():
        if muster in klein:
            zeile = next((i for i, z in enumerate(text.splitlines(), 1) if muster in z.lower()), 0)
            befunde.append((wo, zeile, f'„{muster}“ gefunden — {grund}'))
    adressen = []
    for zeilennr, zeile in enumerate(text.splitlines(), 1):
        for m in URL.finditer(zeile):
            adresse = m.group(0).rstrip('.,;:')
            host = re.sub(r'^https?://', '', adresse).split('/')[0].lower()
            adressen.append((wo, zeilennr, adresse, host))
            if host not in AMTLICH:
                befunde.append((wo, zeilennr, f'nicht amtliche Quelle: {host} (in {adresse[:70]})'))
    # Merkblätter tragen ihr Prüfdatum im Kopf; der Quellenkatalog und die Vorlagen nicht.
    if p.parent.name == 'Verfahren' and not KOPFZEILE.search(text):
        befunde.append((wo, 1, 'Kopfzeile „*Letzte vollständige Prüfung: TT.MM.JJJJ*“ fehlt'))
    return befunde, adressen


def abruf(adresse):
    """Eine Adresse abrufen; liefert '' oder den Grund. Erst HEAD, dann GET.

    Manche Portale können mit HEAD nichts anfangen und antworten mit 400, 403, 405 oder 501,
    obwohl die Seite da ist (www.recht.bund.de am 18.09.2026: HEAD scheitert, GET leitet mit
    303 weiter). Ein Fehlalarm ist hier schlimmer als kein Alarm: Eine Prüfung, die grundlos
    meckert, wird nicht mehr gelesen."""
    import urllib.error, urllib.request
    kopf = {'User-Agent': 'AKA Recht Quellenpruefung'}
    for verfahren in ('HEAD', 'GET'):
        try:
            with urllib.request.urlopen(urllib.request.Request(adresse, method=verfahren, headers=kopf), timeout=20) as antwort:
                if antwort.status < 400: return ''
                letzter = f'HTTP {antwort.status}'
        except urllib.error.HTTPError as e:
            if e.code < 400: return ''
            letzter = f'HTTP {e.code}'
            if verfahren == 'HEAD' and e.code in (400, 403, 405, 501): continue   # Portal mag HEAD nicht
            if verfahren == 'GET' and e.code in (403, 429): return ''             # Abwehr gegen Skripte, nicht unser Befund
        except Exception as e:
            letzter = f'nicht erreichbar ({type(e).__name__})'
        if verfahren == 'GET': return letzter
    return letzter


def erreichbar(adressen, grenze=None):
    """Nur mit --netz: jede Adresse einmal abrufen. Meldet, was nicht antwortet."""
    befunde = []
    gesehen = {}
    for wo, zeile, adresse, host in adressen:
        if adresse in gesehen:
            if gesehen[adresse]: befunde.append((wo, zeile, f'{gesehen[adresse]}: {adresse[:70]}'))
            continue
        fehler = abruf(adresse)
        gesehen[adresse] = fehler
        if fehler: befunde.append((wo, zeile, f'{fehler}: {adresse[:70]}'))
        if grenze and len(gesehen) >= grenze: break
    return befunde


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--root', type=Path, default=ROOT, help='Projektordner')
    p.add_argument('--netz', action='store_true', help='Adressen zusätzlich abrufen (dauert)')
    p.add_argument('--grenze', type=int, default=0, help='mit --netz: höchstens so viele Adressen prüfen')
    a = p.parse_args()
    root = a.root.resolve()

    liste = dateien(root)
    if not liste:
        print('Keine Rechtsinhalte gefunden. Falscher Ordner?'); return 1
    befunde, adressen = [], []
    for datei in liste:
        b, ad = pruefe_datei(datei, root)
        befunde += b; adressen += ad

    if a.netz:
        print(f'Rufe {len({x[2] for x in adressen})} verschiedene Adressen ab …')
        befunde += erreichbar(adressen, a.grenze or None)

    hosts = {h for _, _, _, h in adressen}
    print(f'{len(liste)} Dateien, {len(adressen)} Verweise, {len(hosts)} verschiedene Stellen.')
    if befunde:
        print(f'\n{len(befunde)} Befund(e):')
        for wo, zeile, text in befunde: print(f'  {wo}:{zeile}: {text}')
        return 1
    print('Alle Quellen amtlich, keine Reste aus einer KI-Sitzung, alle Merkblätter mit Prüfdatum.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
