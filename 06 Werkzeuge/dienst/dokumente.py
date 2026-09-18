#!/usr/bin/env python3
"""Dokumente eines Falls: Katalog, Textauszug, Suche. Liest nur.

Textauszug für txt, md, json, xml, html, docx (Word), eml (E-Mail) und pdf
(über das vorhandene Programm pdftotext, wenn installiert). Fotos und Scans
haben keinen Text; das Werkzeug texterkennung legt auf Wunsch eine erkannte
Textfassung unter 07 Recherche/Texterkennung an (Stufe 13).
Nur Standardbibliothek.
"""
import re, shutil, subprocess, unicodedata, zipfile
from datetime import date
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET
import bestand, store

TEXT_EXT = {'.md', '.txt', '.json', '.xml', '.py', '.sh', '.csv'}
BILD_EXT = {'.jpg', '.jpeg', '.png', '.heic', '.gif'}
TEXT_CACHE = {}
OCR_ORDNER = '07 Recherche/Texterkennung'   # Ablage erkannter Texte (Stufe 13)
OCR_TRENNER = '=' * 72                     # trennt den Kopf der Ableitung vom erkannten Text

def normalisieren(s):
    return unicodedata.normalize('NFKD', str(s).casefold()).encode('ascii', 'ignore').decode()

class _NurText(HTMLParser):
    def __init__(self): super().__init__(); self.teile = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'): self.skip += 1
        if tag in ('p', 'div', 'li', 'tr', 'br', 'h1', 'h2', 'h3', 'section'): self.teile.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'): self.skip = max(0, self.skip - 1)
        if tag in ('p', 'div', 'li', 'tr', 'h1', 'h2', 'h3'): self.teile.append('\n')
        if tag in ('td', 'th'): self.teile.append(' | ')
    def handle_data(self, d):
        if not self.skip: self.teile.append(d)
    def text(self): return '\n'.join(re.sub(r'\s+', ' ', z).strip() for z in ''.join(self.teile).splitlines() if z.strip())

def html_zu_text(t):
    h = _NurText(); h.feed(t); return h.text()

TEXTQUELLEN = {   # woher der Auszug stammt (Prüfbericht 16.09.2026, F34): der Leser soll wissen, was er wirklich gelesen hat
    'direkt': 'Text direkt aus der Datei gelesen',
    'pdf-text': 'Text aus der Textschicht der PDF (pdftotext); Spalten und Tabellen können in falscher Reihenfolge stehen',
    'pdf-teiltext': 'PDF mit gemischten Seiten: nur ein Teil hat eine Textschicht, die übrigen Seiten sind Bildscans und nicht ausgelesen',
    'kein-text': 'PDF ohne Textschicht (Bildscan): kein Text ausgelesen, Inhalt nur in der Ansicht lesbar',
    'werkzeug-fehlt': 'PDF, aber pdftotext ist nicht installiert: kein Text ausgelesen',
    'bild': 'Foto oder Bildschirmaufnahme: kein Text ausgelesen; Texterkennung (OCR) mit dem Werkzeug texterkennung möglich',
    'ocr': 'Text aus der Texterkennung (OCR): Ableitung mit möglichen Fehlern, am Original prüfen',
    'kein-auszug': 'Dateiformat ohne Textvorschau',
    'fehler': 'Textvorschau konnte nicht erstellt werden',
}
ABLEITUNG = 'Der Auszug ist eine Ableitung, kein Original: Zahlen, Zugangsdaten, Fristen und Anträge am Original gegenprüfen.'
SEITE_MINDESTZEICHEN = 25   # weniger gilt als Seite ohne Textschicht (Seitenzahl, Kopfzeile, Streuzeichen eines Scans)

def pdf_seiten(pfad, ausgabe):
    """Seitenzahl und die Nummern der Seiten ohne Textschicht (Prüfbericht N06, N07, 18.09.2026).

    pdftotext trennt Seiten mit dem Seitenumbruch \\f und hängt ihn auch hinter die letzte Seite;
    „Umbrüche + 1“ zählte deshalb eine Seite zu viel. Die wirkliche Seitenzahl liefert pdfinfo,
    wenn es da ist (gehört wie pdftotext zu poppler); sonst werden die Abschnitte gezählt."""
    teile = ausgabe.split('\f')
    if teile and not teile[-1].strip(): teile.pop()   # der Umbruch hinter der letzten Seite
    ohne_text = [i for i, s in enumerate(teile, 1) if len(s.strip()) < SEITE_MINDESTZEICHEN]
    seiten = len(teile)
    prog = shutil.which('pdfinfo')
    if prog:
        try:
            r = subprocess.run([prog, str(pfad)], capture_output=True, timeout=15)
            m = re.search(r'^Pages:\s+(\d+)', r.stdout.decode('utf-8', 'replace'), re.M)
            if m:
                echt = int(m.group(1))
                if echt > seiten: ohne_text += list(range(seiten + 1, echt + 1))   # Seiten, die gar keinen Abschnitt lieferten
                seiten = echt
        except Exception:
            pass   # pdfinfo ist freiwillig; ohne es bleibt die Zählung über die Abschnitte
    return seiten, ohne_text

def datum_aus_name(name):
    """Dokumentdatum aus dem Dateinamen, aber nur als Vorschlag (Prüfbericht N08, 18.09.2026).

    Vorher wurde jedes Muster JJJJ-MM-TT übernommen. „2026-02-31“ ist kein Kalendertag; die Akte
    ließ sich danach nicht mehr speichern, und jeder folgende Bestandsabgleich scheiterte erneut.
    Liefert (datum, hinweis); bei einem unmöglichen Datum bleibt das Feld leer und der Hinweis
    landet in der Ordnungsnotiz."""
    m = re.search(r'20\d\d-\d\d-\d\d', name)
    if not m: return '', ''
    try:
        date.fromisoformat(m.group(0)); return m.group(0), ''
    except ValueError:
        return '', f'Im Dateinamen steht „{m.group(0)}“ — das ist kein Kalendertag. Dokumentdatum bleibt leer, bitte von Hand setzen.'

def text(pfad):
    """Liefert (text, hinweis) für eine Datei; befund() liefert dazu Textquelle, Seiten und Zeichen."""
    b = befund(pfad); return b['text'], b['hinweis']

def befund(pfad):
    """Textauszug mit Herkunft: text, hinweis, textquelle (Schlüssel aus TEXTQUELLEN), seiten (PDF), zeichen. Je Dateistand zwischengespeichert."""
    p = Path(pfad); s = p.stat(); k = (str(p), s.st_mtime_ns, s.st_size)
    if k in TEXT_CACHE: return TEXT_CACHE[k]
    ext = p.suffix.lower(); t = ''; hinweis = ''; quelle = 'direkt'; seiten = None; ohne_text = []
    try:
        if ext in TEXT_EXT: t = p.read_text('utf-8-sig', errors='replace')
        elif ext in ('.html', '.htm'): t = html_zu_text(p.read_text('utf-8', errors='replace'))
        elif ext == '.docx':
            with zipfile.ZipFile(p) as z:
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                for name in z.namelist():
                    if re.match(r'word/(document|header\d+|footer\d+|footnotes|endnotes)\.xml$', name):
                        baum = ET.fromstring(z.read(name))
                        t += '\n'.join(''.join(n.itertext()) for n in baum.findall('.//w:p', ns)) + '\n'
            hinweis = 'Textvorschau. Seitenlayout und Unterschriften im Original prüfen.'
        elif ext == '.eml':
            mail = BytesParser(policy=policy.default).parsebytes(p.read_bytes())
            t = '\n'.join(f'{k}: {mail.get(k, "")}' for k in ('Date', 'From', 'To', 'Cc', 'Subject')) + '\n\n'
            teil = mail.get_body(preferencelist=('plain', 'html'))
            if teil: t += html_zu_text(teil.get_content()) if teil.get_content_type() == 'text/html' else teil.get_content()
            anhaenge = [str(x.get_filename()) for x in mail.walk() if x.get_filename()]
            if anhaenge: t += '\n\nAnhänge in der E-Mail:\n' + '\n'.join(anhaenge)
            hinweis = 'E-Mail-Text mit Kopfzeilen. Anhänge liegen in der Originaldatei.'
        elif ext == '.pdf':
            prog = shutil.which('pdftotext')
            if prog:
                r = subprocess.run([prog, '-layout', str(p), '-'], capture_output=True, timeout=30)
                t = r.stdout.decode('utf-8', 'replace')
                seiten, ohne_text = pdf_seiten(p, t)   # N07: die letzte Seite endet auch mit \f, sie darf nicht doppelt zählen
            if len(t.strip()) < 25:
                quelle = 'kein-text' if prog else 'werkzeug-fehlt'; t = ''
                hinweis = ('Kein Textinhalt gefunden (Bildscan). Inhalt in der PDF-Ansicht lesen oder das Werkzeug texterkennung nutzen; das Dokument gilt als nicht gelesen.' if prog
                           else 'pdftotext ist nicht installiert, kein Text ausgelesen. Inhalt in der PDF-Ansicht lesen.')
            elif ohne_text:   # N06: gemischte PDF, nur ein Teil der Seiten hat eine Textschicht
                quelle = 'pdf-teiltext'
                liste = ', '.join(str(n) for n in ohne_text[:12]) + (' …' if len(ohne_text) > 12 else '')
                hinweis = (f'Gemischte PDF mit {seiten} Seite(n): {len(ohne_text)} davon ohne Textschicht (Seite {liste}). '
                           'Von diesen Seiten wurde nichts ausgelesen — sie in der PDF-Ansicht lesen oder das Werkzeug texterkennung nutzen. '
                           'Das Dokument gilt erst als gelesen, wenn auch diese Seiten geprüft sind. '
                           'Spalten, Tabellen und Stempel können in falscher Reihenfolge stehen; Unterschriften und handschriftliche Vermerke fehlen.')
            else:
                quelle = 'pdf-text'; hinweis = f'Textschicht der PDF, {seiten} Seite(n). Spalten, Tabellen und Stempel können in falscher Reihenfolge stehen; Unterschriften und handschriftliche Vermerke fehlen.'
        elif ext in BILD_EXT: quelle = 'bild'; hinweis = 'Foto oder Bildschirmaufnahme: kein Text ausgelesen. Bild öffnen und ansehen oder das Werkzeug texterkennung nutzen; Textstand „visuell geprüft“ erst nach dem eigenen Abgleich eintragen.'
        else: quelle = 'kein-auszug'; hinweis = 'Für dieses Dateiformat gibt es keine Textvorschau.'
    except Exception:
        quelle = 'fehler'; hinweis = 'Textvorschau konnte nicht erstellt werden. Das Original bleibt verfügbar.'
    TEXT_CACHE[k] = {'text': t, 'hinweis': hinweis, 'textquelle': quelle, 'textquelle_text': TEXTQUELLEN[quelle], 'seiten': seiten,
                     'seiten_ohne_text': ohne_text, 'zeichen': len(t.strip())}   # N06: welche Seiten nicht ausgelesen wurden
    return TEXT_CACHE[k]

def katalog(fall_id, akte):
    """Dokumentliste: registrierter Bestand plus Ordnungsangaben aus der Akte. Liest nur.

    Liefert (liste, ergaenzt, abweichungen). Einträge, die im Bestand stehen, aber in der Akte fehlen
    oder einen anderen Pfad haben, werden nur im Speicher ergänzt (Kennungen in `ergaenzt`); gespeichert
    wird das erst durch ein schreibendes Werkzeug (bestand_abgleichen). Dateien ohne Kennung stehen in
    abweichungen['nicht_erfasst'] und erscheinen nicht als Dokument."""
    ordner = store.fall_ordner(fall_id); vorhanden, abweichungen = bestand.abgleich(ordner)
    liste = []; ergaenzt = []
    for kennung, rel in vorhanden.items():
        d = akte['dokumente'].get(kennung)
        if not d:
            name = Path(rel)
            dat, dat_hinweis = datum_aus_name(name.name)   # N08: nur ein echter Kalendertag wird übernommen
            d = {'pfad': rel, 'titel': re.sub(r'_+', ' ', name.stem), 'datum': dat,
                 'art': '', 'stand': 'Entwurf' if rel.startswith('06 ') else 'Historisch' if rel.startswith('08 ') else 'Original',
                 'themen': [], 'anlage': '', 'personen': [], 'verweise': [], 'notiz': dat_hinweis}
            akte['dokumente'][kennung] = d; ergaenzt.append(kennung)
        elif d['pfad'] != rel: d['pfad'] = rel; ergaenzt.append(kennung)
        p = ordner / rel
        liste.append({'id': kennung, **d, 'name': p.name, 'gruppe': rel.split('/')[0], 'typ': p.suffix.lower().lstrip('.').upper(),
                      'groesse': p.stat().st_size, 'fehlt': False})
    for kennung, d in akte['dokumente'].items():
        if kennung not in vorhanden:
            liste.append({'id': kennung, **d, 'name': Path(d['pfad']).name, 'gruppe': d['pfad'].split('/')[0], 'typ': '', 'groesse': 0, 'fehlt': True})
    liste.sort(key=lambda x: (x['gruppe'], x['pfad']))
    return liste, ergaenzt, abweichungen

def suche(fall_id, akte, frage):
    q = normalisieren(frage).strip()
    if len(q) < 2: return []
    ordner = store.fall_ordner(fall_id); treffer = []
    liste, _, _ = katalog(fall_id, akte)
    for d in liste:
        heu = normalisieren(' '.join([d['titel'], d['pfad'], d.get('notiz', ''), ' '.join(d.get('themen', [])), d.get('anlage', '')]))
        if q in heu: treffer.append(d['id']); continue
        if not d['fehlt'] and q in normalisieren(text(ordner / d['pfad'])[0]): treffer.append(d['id'])
    # Trifft die Suche eine Texterkennung, gehört das Original dazu (Stufe 13)
    for d in liste:
        if d['id'] in treffer and d['pfad'].startswith(OCR_ORDNER + '/'):
            treffer += [k for k in d.get('verweise', []) if k not in treffer]
    return treffer
