#!/usr/bin/env python3
"""Erzeugt aus einem Entwurf (.md oder .txt) eine Word-Datei (.docx), ohne Fremdpaket.

Aufruf:  python3 docx_erzeugen.py <Entwurf.md|.txt> [Ziel.docx]
Regeln:
  - Alles VOR der ersten Trennlinie (Zeile aus mindestens drei „---“ oder 20 „-“)
    sind interne Hinweise und werden nicht übernommen. Fehlt die Trennlinie,
    wird der ganze Text übernommen.
  - Überschriften: „# “ und „## “; Aufzählung: „- “; fett: **Text**.
  - Kopfzeilen (Von:, An:, Cc:, Betreff:, Datum:) werden fett gesetzt.
  - Marker wie [PRÜFEN: …], [BELEG: …], [QUELLE: …] bleiben sichtbar, damit
    nichts Ungeprüftes unbemerkt versandt wird.
Ein .docx ist eine ZIP-Datei mit XML; hier wird sie direkt geschrieben.
"""
import sys
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
    text = Path(quelle).read_text('utf-8')
    teile = re.split(r'\n(?:-{20,}|---)\s*\n', text, maxsplit=1)
    return teile[1] if len(teile) == 2 else text

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
    marker = re.findall(r'\[(PRÜFEN|BELEG|QUELLE):[^\]]*\]', text)
    return ziel, marker

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    ziel, marker = erzeugen(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print('Word-Datei:', ziel)
    if marker: print(f'Achtung: {len(marker)} offene Marker im Sendetext ({", ".join(sorted(set(marker)))}). Vor Versand auflösen.')
