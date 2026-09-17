#!/usr/bin/env python3
"""Texterkennung (OCR) für Fotos und PDF-Scans (Stufe 13, 17.09.2026).

Nutzt das freiwillige Zusatzprogramm tesseract, wie dokumente.py das Programm
pdftotext nutzt: Ist es installiert, geht die Erkennung, sonst kommt eine klare
Meldung und nichts passiert. PDF-Seiten werden vorher mit pdftoppm (Paket
poppler) zu Bildern gerastert, HEIC-Fotos unter macOS mit sips umgewandelt.
Alles läuft auf dem Rechner, ohne Netz, in einem Zwischenordner, der danach
wieder verschwindet. Das Modul liest und schreibt keine Akte; das Ablegen des
Ergebnisses macht das Werkzeug texterkennung in werkzeuge.py.

Erkannter Text ist eine Ableitung. Tesseract verwechselt Zeichen und kann
Zeilen auslassen oder verwürfeln, ohne es zu melden.
Nur Standardbibliothek.
"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path

BILD_EXT = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp'}
HEIC_EXT = {'.heic'}
PDF_DPI = 300                       # Rasterung der PDF-Seiten; tesseract liest um 300 dpi am besten
SPRACHE_STANDARD = 'deu'
SPRACHE_MUSTER = re.compile(r'[a-z][a-z_]{2,}(\+[a-z][a-z_]{2,})*')   # tesseract-Kürzel, mehrere mit +, etwa deu+eng
ZEITLIMIT_SEITE = 180
WARNUNG = ('Texterkennung verwechselt Zeichen und kann ganze Zeilen auslassen oder verwürfeln, ohne es zu melden. '
           'Zahlen, Daten, Fristen, Beträge, Aktenzeichen und Namen immer am Original prüfen; '
           'der Textstand „visuell geprüft“ entsteht erst durch diesen Abgleich.')
INSTALLATION = ('Texterkennung braucht das freiwillige Zusatzprogramm tesseract mit deutscher Sprache '
                '(macOS mit Homebrew: brew install poppler tesseract tesseract-lang; Linux, etwa Ubuntu: '
                'sudo apt install poppler-utils tesseract-ocr tesseract-ocr-deu). Ohne das Programm bleibt alles wie bisher.')


def _lauf(befehl, zeit):
    return subprocess.run(befehl, capture_output=True, timeout=zeit)


def programme():
    """Welche Hilfsprogramme vorhanden sind: tesseract mit Version und Sprachen, pdftoppm, sips (nur macOS)."""
    t = shutil.which('tesseract'); version = ''; sprachen = []
    if t:
        try:
            r = _lauf([t, '--version'], 30)
            m = re.search(r'tesseract\s+v?(\d[\d.]*)', (r.stdout + r.stderr).decode('utf-8', 'replace'))
            version = m[1] if m else ''
            r = _lauf([t, '--list-langs'], 30)
            sprachen = [z.strip() for z in r.stdout.decode('utf-8', 'replace').splitlines()[1:] if z.strip()]
        except (OSError, subprocess.SubprocessError):
            t = None
    return {'tesseract': t, 'version': version, 'sprachen': sprachen, 'pdftoppm': shutil.which('pdftoppm'),
            'sips': shutil.which('sips') if sys.platform == 'darwin' else None}


def _bild_lesen(tesseract, bild, sprache):
    r = _lauf([tesseract, str(bild), 'stdout', '-l', sprache], ZEITLIMIT_SEITE)
    if r.returncode != 0:
        raise ValueError('tesseract meldet einen Fehler: ' + r.stderr.decode('utf-8', 'replace').strip()[-300:])
    return r.stdout.decode('utf-8', 'replace').replace('\f', '').strip()


def erkennen(pfad, sprache=SPRACHE_STANDARD):
    """Text aus einem Bild oder einer PDF erkennen. Liefert text (bei mehreren Seiten mit Trennzeilen
    „--- Seite N ---“, damit Fundstellen nennbar sind), seiten, programm, sprache, dpi (bei PDF).
    Schreibt nur in einen eigenen Zwischenordner."""
    p = Path(pfad); ext = p.suffix.lower()
    if not SPRACHE_MUSTER.fullmatch(sprache or ''):
        raise ValueError('„sprache“ muss ein tesseract-Kürzel sein, etwa deu, eng oder deu+eng.')
    prog = programme()
    if not prog['tesseract']: raise ValueError(INSTALLATION)
    fehlend = [s for s in sprache.split('+') if s not in prog['sprachen']]
    if fehlend:
        raise ValueError(f'Sprache {", ".join(fehlend)} ist für tesseract nicht installiert (vorhanden: {", ".join(prog["sprachen"]) or "keine"}). ' + INSTALLATION)
    ergebnis = {'programm': f'tesseract {prog["version"]}'.strip(), 'sprache': sprache, 'dpi': None}
    with tempfile.TemporaryDirectory(prefix='aka-recht-ocr-') as tmp:
        tmp = Path(tmp)
        if ext == '.pdf':
            if not prog['pdftoppm']: raise ValueError('Für PDF-Scans braucht die Texterkennung zusätzlich das Programm pdftoppm (Paket poppler).')
            r = _lauf([prog['pdftoppm'], '-r', str(PDF_DPI), '-png', str(p), str(tmp / 'seite')], 600)
            if r.returncode != 0: raise ValueError('pdftoppm konnte die PDF nicht rastern: ' + r.stderr.decode('utf-8', 'replace').strip()[-300:])
            bilder = sorted(tmp.glob('seite*.png'), key=lambda b: int(re.search(r'(\d+)$', b.stem)[1]))
            if not bilder: raise ValueError('Die PDF hat keine Seiten, die gerastert werden konnten.')
            ergebnis['dpi'] = PDF_DPI
        elif ext in BILD_EXT:
            bilder = [p]
        elif ext in HEIC_EXT:
            if not prog['sips']: raise ValueError('HEIC-Fotos kann die Texterkennung nur unter macOS umwandeln (sips). Foto vorher als JPG oder PNG speichern.')
            ziel = tmp / 'foto.png'
            r = _lauf([prog['sips'], '-s', 'format', 'png', str(p), '--out', str(ziel)], 120)
            if r.returncode != 0 or not ziel.is_file(): raise ValueError('sips konnte das HEIC-Foto nicht umwandeln.')
            bilder = [ziel]
        else:
            raise ValueError(f'Für den Dateityp „{ext or "ohne Endung"}“ gibt es keine Texterkennung; möglich sind PDF, PNG, JPG, TIFF, BMP und unter macOS HEIC.')
        seiten = [_bild_lesen(prog['tesseract'], b, sprache) for b in bilder]
    text = seiten[0] if len(seiten) == 1 else '\n\n'.join(f'--- Seite {i} ---\n{t}' for i, t in enumerate(seiten, 1))
    ergebnis.update({'text': text, 'seiten': len(seiten)})
    return ergebnis


if __name__ == '__main__':
    import json
    for _strom in (sys.stdout, sys.stderr):   # Konsole unter Windows ist cp1252 (Stufe 9)
        if hasattr(_strom, 'reconfigure'): _strom.reconfigure(encoding='utf-8', errors='replace')
    if len(sys.argv) < 2: print(json.dumps(programme(), ensure_ascii=False, indent=2)); sys.exit(0)
    e = erkennen(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else SPRACHE_STANDARD)
    print(e['text'])
