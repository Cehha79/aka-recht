#!/usr/bin/env python3
"""Erzeugt aus einem Entwurf (.md oder .txt) eine Word-Datei (.docx), ohne Fremdpaket.

Aufruf:  python3 docx_erzeugen.py <Entwurf.md|.txt> [Ziel.docx]
         python3 docx_erzeugen.py --pruefen <Entwurf.md|.txt>   nur der Vorabbericht, keine Datei (Exit 1 bei Befunden)
Regeln:
  - Alles VOR der ersten Trennlinie (Zeile aus mindestens drei „---“ oder 20 „-“)
    sind interne Hinweise und werden nicht übernommen. Fehlt die Trennlinie,
    wird der ganze Text übernommen.
  - Überschriften: „# “ und „## “; Aufzählung: „- “; fett: **Text**.
  - Kopfzeilen (Von:, An:, Cc:, Betreff:, Datum:) werden fett gesetzt.
  - Marker wie [PRÜFEN: …], [BELEG: …], [QUELLE: …] bleiben sichtbar, damit
    nichts Ungeprüftes unbemerkt versandt wird.
  - Vorabbericht (seit 17.09.2026, Prüfbericht F29): vor dem Schreiben wird der
    Sendetext geprüft auf offene Marker (mit und ohne Doppelpunkt), Platzhalter
    【…】, fehlende Trennlinie, interne Notizen im Sendetext, Kopfzeilen (Von, An,
    Datum, Betreff), Anlagenliste und Anträge. Der Bericht wird immer ausgegeben.
    Eine erzeugte Datei ist kein Nachweis der Versandfertigkeit; die Freigabe
    trifft der Nutzer bewusst (entwurf_erfassen status=geprüft), nie das Skript.
Ein .docx ist eine ZIP-Datei mit XML; hier wird sie direkt geschrieben.
"""
import sys

# Ein- und Ausgabe immer UTF-8, auch unter Windows (Konsole dort cp1252); Ausgaben für Assistenten und Tests müssen UTF-8 sein (Stufe 9, 17.09.2026).
for _strom in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
import re, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

SCHRIFT, GROESSE = 'Arial', 22  # Größe in halben Punkten: 22 = 11 pt

def laeufe(text):
    """Text mit **fett** in Word-Runs zerlegen."""
    teile = re.split(r'(\*\*[^*]+\*\*)', text); xml = ''
    for t in teile:
        if not t: continue
        fett = t.startswith('**') and t.endswith('**')
        inhalt = t[2:-2] if fett else t
        xml += f'<w:r><w:rPr><w:rFonts w:ascii="{SCHRIFT}" w:hAnsi="{SCHRIFT}"/>{"<w:b/>" if fett else ""}<w:sz w:val="{GROESSE}"/></w:rPr><w:t xml:space="preserve">{escape(inhalt)}</w:t></w:r>'
    return xml

def absatz(text, art='', fett=False, nach=120):
    ppr = f'<w:pPr>{f"<w:pStyle w:val=\"{art}\"/>" if art else ""}<w:spacing w:after="{nach}"/></w:pPr>'
    if fett: text = f'**{text}**'
    return f'<w:p>{ppr}{laeufe(text)}</w:p>'

def sendetext(quelle):
    return zerlegen(Path(quelle).read_text('utf-8'))[1]

def zerlegen(text):
    """(interne Hinweise, Sendetext, Trennlinie gefunden?)"""
    teile = re.split(r'\n(?:-{20,}|---)\s*\n', text, maxsplit=1)
    if len(teile) == 2: return teile[0], teile[1], True
    return '', text, False

MARKER = re.compile(r'\[(PRÜFEN|BELEG|QUELLE)\b[^\]]*\]?')
PLATZHALTER = re.compile(r'【[^】]*】|\{\{[^}]*\}\}|<<[^>]*>>|\[\.\.\.\]|\[…\]')
INTERN = re.compile(r'(?im)^(?:interne?\s+(?:hinweise?|notiz|anmerkung|vermerk)|hinweis an|notiz|todo|prüfnotiz)\b|nicht im sendetext')
KOPF = ('Von', 'An', 'Datum', 'Betreff')

def vorpruefung(text):
    """Vorabbericht zum Sendetext: Liste von Befunden (Sätze) und Zahlen. Leer heißt: nichts gefunden, nicht: versandfertig."""
    intern, send, trennung = zerlegen(text); befunde = []
    if not trennung: befunde.append('Keine Trennlinie („---“) gefunden: der ganze Text gilt als Sendetext, interne Hinweise wären mit drin.')
    marker = MARKER.findall(send)
    if marker:
        zaehl = {m: marker.count(m) for m in sorted(set(marker))}
        befunde.append('Offene Marker im Sendetext: ' + ', '.join(f'{k} ×{v}' for k, v in zaehl.items()) + '. Vor Versand auflösen.')
    ph = PLATZHALTER.findall(send)
    if ph: befunde.append(f'{len(ph)} Platzhalter noch nicht ausgefüllt: ' + ', '.join(dict.fromkeys(p[:40] for p in ph[:6])) + ('…' if len(ph) > 6 else '') + '.')
    m = INTERN.search(send)
    if m: befunde.append('Interne Notiz im Sendetext („' + re.sub(r'\s+', ' ', send[max(0, m.start()-20):m.end()+30]).strip() + '“): gehört über die Trennlinie.')
    for feld in KOPF:
        mm = re.search(rf'(?m)^{feld}:\s*(.*)$', send)
        if not mm: befunde.append(f'Kopfzeile „{feld}:“ fehlt.')
        elif not mm[1].strip() or PLATZHALTER.search(mm[1]) or 'TT.MM.JJJJ' in mm[1]: befunde.append(f'Kopfzeile „{feld}:“ ist noch leer oder Platzhalter.')
    if re.search(r'(?i)\baktenzeichen\b', send) and re.search(r'(?i)aktenzeichen\s*[:：]?\s*(【[^】]*】|…|\.\.\.)', send): befunde.append('Aktenzeichen ist noch Platzhalter.')
    if re.search(r'(?im)^anlagen?:', send):
        liste = re.split(r'(?im)^anlagen?:\s*$', send, maxsplit=1)
        eintraege = [z for z in (liste[1] if len(liste) == 2 else '').split('\n') if z.strip().startswith('- ')]
        if not eintraege: befunde.append('Anlagenliste ohne Einträge.')
        elif all(PLATZHALTER.search(z) for z in eintraege): befunde.append('Anlagenliste besteht nur aus Platzhaltern.')
    elif re.search(r'(?i)\banlage\b|\bbeigefügt\b|\banbei\b', send): befunde.append('Text nennt Anlagen, aber es gibt keine Anlagenliste („Anlagen:“ mit „- “-Zeilen).')
    if re.search(r'(?i)\b(klage|widerspruch|einspruch|antrag)\b', send) and not re.search(r'(?i)\b(beantrage|beantragen|wird beantragt|antrag(e|es)?\b.*?(?:,|:)|lege .{0,40}ein|erhebe)', send):
        befunde.append('Rechtsbehelf oder Antrag genannt, aber kein ausdrücklicher Antragssatz („Ich beantrage …“, „lege … ein“, „erhebe …“) gefunden.')
    return befunde

def dokument_xml(text):
    koerper = []
    for block in re.split(r'\n\s*\n', text.strip()):
        zeilen = block.split('\n')
        if all(z.startswith('- ') for z in zeilen):
            for z in zeilen: koerper.append(f'<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr><w:spacing w:after="60"/></w:pPr>{laeufe(z[2:])}</w:p>')
            continue
        if zeilen[0].startswith('# '): koerper.append(absatz(zeilen[0][2:], 'Ueberschrift1', True, 200)); zeilen = zeilen[1:]
        elif zeilen[0].startswith('## '): koerper.append(absatz(zeilen[0][3:], 'Ueberschrift2', True, 160)); zeilen = zeilen[1:]
        if not zeilen: continue
        runs = ''
        for i, z in enumerate(zeilen):
            if i: runs += '<w:r><w:br/></w:r>'
            m = re.match(r'^(Von|An|Cc|Betreff|Datum|Aktenzeichen|Ihr Zeichen|Unser Zeichen):\s*(.*)$', z)
            runs += laeufe(f'**{m[1]}:** {m[2]}' if m else z)
        koerper.append(f'<w:p><w:pPr><w:spacing w:after="120"/></w:pPr>{runs}</w:p>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + ''.join(koerper) +
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1247" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>')

STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{SCHRIFT}" w:hAnsi="{SCHRIFT}" w:cs="{SCHRIFT}"/><w:sz w:val="{GROESSE}"/><w:lang w:val="de-DE"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
          '<w:style w:type="paragraph" w:styleId="Ueberschrift1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="200"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Ueberschrift2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="160"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style></w:styles>')
NUMBERING = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
             '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="–"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="567" w:hanging="283"/></w:pPr></w:lvl></w:abstractNum>'
             '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')
CONTENT_TYPES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                 '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                 '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
DOC_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>')

def erzeugen(quelle, ziel=None):
    quelle = Path(quelle); ziel = Path(ziel) if ziel else quelle.with_suffix('.docx')
    text = sendetext(quelle)
    with zipfile.ZipFile(ziel, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES); z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', DOC_RELS); z.writestr('word/document.xml', dokument_xml(text))
        z.writestr('word/styles.xml', STYLES); z.writestr('word/numbering.xml', NUMBERING)
    return ziel, vorpruefung(quelle.read_text('utf-8'))

def bericht(befunde):
    if not befunde: return 'Vorabbericht: keine Befunde. Das ist keine Freigabe; Sendetext, Empfänger und Anlagen bleiben Sache des Nutzers.'
    return 'Vorabbericht, vor Versand klären:\n' + '\n'.join(f'  - {b}' for b in befunde)

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--pruefen']
    if not args: sys.exit(__doc__)
    if '--pruefen' in sys.argv:
        befunde = vorpruefung(Path(args[0]).read_text('utf-8')); print(bericht(befunde)); sys.exit(1 if befunde else 0)
    ziel, befunde = erzeugen(args[0], args[1] if len(args) > 1 else None)
    print('Word-Datei:', ziel); print(bericht(befunde))
