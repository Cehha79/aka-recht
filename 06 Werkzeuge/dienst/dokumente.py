#!/usr/bin/env python3
"""Dokumente eines Falls: Katalog, Textauszug, Suche. Liest nur.

Textauszug für txt, md, json, xml, html, docx (Word), eml (E-Mail) und pdf
(über das vorhandene Programm pdftotext, wenn installiert). Fotos haben
keinen Text; sie sind über Titel und Ordnungsangaben auffindbar.
Nur Standardbibliothek.
"""
import re, shutil, subprocess, unicodedata, zipfile
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET
import bestand, store

TEXT_EXT = {'.md', '.txt', '.json', '.xml', '.py', '.sh', '.csv'}
BILD_EXT = {'.jpg', '.jpeg', '.png', '.heic', '.gif'}
TEXT_CACHE = {}

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

def text(pfad):
    """Liefert (text, hinweis) für eine Datei. Ergebnis wird je Dateistand zwischengespeichert."""
    p = Path(pfad); s = p.stat(); k = (str(p), s.st_mtime_ns, s.st_size)
    if k in TEXT_CACHE: return TEXT_CACHE[k]
    ext = p.suffix.lower(); t = ''; hinweis = ''
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
            if len(t.strip()) < 25: hinweis = 'Kein Textinhalt gefunden (Bildscan oder pdftotext fehlt). Inhalt in der PDF-Ansicht lesen.'
        elif ext in BILD_EXT: hinweis = 'Foto oder Bildschirmaufnahme. Auffindbar über Titel und Ordnungsangaben.'
        else: hinweis = 'Für dieses Dateiformat gibt es keine Textvorschau.'
    except Exception:
        hinweis = 'Textvorschau konnte nicht erstellt werden. Das Original bleibt verfügbar.'
    TEXT_CACHE[k] = (t, hinweis)
    return TEXT_CACHE[k]

def katalog(fall_id, akte):
    """Dokumentliste: Bestand plus Ordnungsangaben aus der Akte. Ergänzt fehlende Einträge in der Akte (im Speicher)."""
    ordner = store.fall_ordner(fall_id); vorhanden = bestand.aktualisieren(ordner)
    liste = []; ergaenzt = []
    for kennung, rel in vorhanden.items():
        d = akte['dokumente'].get(kennung)
        if not d:
            name = Path(rel)
            d = {'pfad': rel, 'titel': re.sub(r'_+', ' ', name.stem), 'datum': (re.search(r'20\d\d-\d\d-\d\d', name.name) or [''])[0],
                 'art': '', 'stand': 'Entwurf' if rel.startswith('06 ') else 'Historisch' if rel.startswith('08 ') else 'Original',
                 'themen': [], 'anlage': '', 'personen': [], 'verweise': [], 'notiz': ''}
            akte['dokumente'][kennung] = d; ergaenzt.append(kennung)
        elif d['pfad'] != rel: d['pfad'] = rel; ergaenzt.append(kennung)
        p = ordner / rel
        liste.append({'id': kennung, **d, 'name': p.name, 'gruppe': rel.split('/')[0], 'typ': p.suffix.lower().lstrip('.').upper(),
                      'groesse': p.stat().st_size, 'fehlt': False})
    for kennung, d in akte['dokumente'].items():
        if kennung not in vorhanden:
            liste.append({'id': kennung, **d, 'name': Path(d['pfad']).name, 'gruppe': d['pfad'].split('/')[0], 'typ': '', 'groesse': 0, 'fehlt': True})
    liste.sort(key=lambda x: (x['gruppe'], x['pfad']))
    return liste, ergaenzt

def suche(fall_id, akte, frage):
    q = normalisieren(frage).strip()
    if len(q) < 2: return []
    ordner = store.fall_ordner(fall_id); treffer = []
    liste, _ = katalog(fall_id, akte)
    for d in liste:
        heu = normalisieren(' '.join([d['titel'], d['pfad'], d.get('notiz', ''), ' '.join(d.get('themen', [])), d.get('anlage', '')]))
        if q in heu: treffer.append(d['id']); continue
        if not d['fehlt'] and q in normalisieren(text(ordner / d['pfad'])[0]): treffer.append(d['id'])
    return treffer
