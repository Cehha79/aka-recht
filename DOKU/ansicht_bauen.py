#!/usr/bin/env python3
"""Erzeugt aus DOKU/md/*.md die HTML-Ansichten in DOKU/.

Aufruf:  python3 DOKU/ansicht_bauen.py
Nur Standardbibliothek. Die .md ist die Quelle, die .html wird überschrieben.
Jede Seite: Seitenleiste links (alle Seiten, Abschnitte der Seite),
Inhalt rechts, beide Bereiche scrollen für sich.
"""
import html, re, sys
from pathlib import Path
from datetime import datetime

DOKU = Path(__file__).resolve().parent
MD = DOKU / 'md'
REIHENFOLGE = ['Live-Dokumentation', 'STRUKTUR', 'REGELN', 'TODO', 'WICHTIG',
               'Fahrplan', 'Tests-Qualitaet']
CSS_VERSION = 1

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    return t

def anker(text):
    a = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return re.sub(r'[\s_]+', '-', a) or 'abschnitt'

def render(text):
    out, abschnitte = [], []
    # HTML-Kommentarzeilen (etwa die Produkt-Markierungen <!-- produkt:aus -->) erscheinen nicht in der Ansicht
    zeilen = [z for z in text.split('\n') if not (z.strip().startswith('<!--') and z.strip().endswith('-->'))]; i = 0; para = []
    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    while i < len(zeilen):
        z = zeilen[i]
        if z.startswith('```'):
            flush(); j = i + 1; block = []
            while j < len(zeilen) and not zeilen[j].startswith('```'):
                block.append(zeilen[j]); j += 1
            out.append('<pre><code>' + html.escape('\n'.join(block)) + '</code></pre>')
            i = j + 1; continue
        m = re.match(r'^(#{1,3}) (.+)$', z)
        if m:
            flush(); stufe = len(m.group(1)); titel = m.group(2).strip()
            if stufe == 1: out.append('<h1>' + inline(titel) + '</h1>')
            else:
                a = anker(titel)
                if stufe == 2: abschnitte.append((a, titel))
                out.append(f'<h{stufe} id="{a}">' + inline(titel) + f'</h{stufe}>')
            i += 1; continue
        if z.startswith('|'):
            flush(); rows = []
            while i < len(zeilen) and zeilen[i].startswith('|'):
                rows.append([c.strip() for c in zeilen[i].strip().strip('|').split('|')]); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c) for c in r)]
            t = '<table><thead><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in rows[0]) + '</tr></thead><tbody>'
            for r in rows[1:]: t += '<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in r) + '</tr>'
            out.append(t + '</tbody></table>'); continue
        m = re.match(r'^(\s*)([-*]|\d+\.) (.*)$', z)
        if m:
            flush(); tag = 'ol' if m.group(2)[0].isdigit() else 'ul'; items = []
            while i < len(zeilen):
                m2 = re.match(r'^(\s*)([-*]|\d+\.) (.*)$', zeilen[i])
                if m2 and len(m2.group(1)) == len(m.group(1)):
                    items.append(m2.group(3)); i += 1
                elif zeilen[i].startswith(' ' * (len(m.group(1)) + 2)) and zeilen[i].strip() and items:
                    items[-1] += ' ' + zeilen[i].strip(); i += 1
                else: break
            li = []
            for it in items:
                cb = re.match(r'^\[([ x~])\] (.*)$', it)
                if cb:
                    kl = {' ': 'offen', 'x': 'erledigt', '~': 'arbeit'}[cb.group(1)]
                    li.append(f'<li class="{kl}"><span class="kasten">{html.escape(cb.group(1))}</span>' + inline(cb.group(2)) + '</li>')
                else: li.append('<li>' + inline(it) + '</li>')
            out.append(f'<{tag}>' + ''.join(li) + f'</{tag}>'); continue
        if z.startswith('> '):
            flush(); out.append('<blockquote>' + inline(z[2:]) + '</blockquote>'); i += 1; continue
        if re.fullmatch(r'\s*-{3,}\s*', z):
            flush(); out.append('<hr>'); i += 1; continue
        if not z.strip(): flush(); i += 1; continue
        para.append(z.strip()); i += 1
    flush()
    return '\n'.join(out), abschnitte

STYLE = '''
:root{--bg:#eef2f6;--paper:#fbfcfe;--text:#172033;--muted:#5b6472;--line:#cfd8e6;--soft:#e7edf5;--accent:#2f6fed;--code:#dde6f2;--nav:#1d2b44;--navtext:#dbe4f2}
*{box-sizing:border-box}html,body{height:100%;margin:0;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.6;display:grid;grid-template-columns:260px minmax(0,1fr)}
aside{background:var(--nav);color:var(--navtext);overflow-y:auto;min-height:0;padding:26px 16px}
aside .marke{color:#fff;font-weight:700;font-size:15px;letter-spacing:.06em;padding:0 10px 18px}
aside .marke small{display:block;color:#9fb0c9;font-weight:400;letter-spacing:0;margin-top:4px}
aside .titel{font-size:11px;letter-spacing:.14em;color:#9fb0c9;padding:14px 10px 6px;text-transform:uppercase}
aside a{display:block;color:var(--navtext);text-decoration:none;padding:8px 10px;border-radius:6px;font-size:14px}
aside a:hover{background:#ffffff14}aside a.aktiv{background:#e2e9f6;color:#1d2b44;font-weight:600}
aside a.abschnitt{font-size:13px;padding:5px 10px 5px 18px;color:#b9c6da}
main{overflow-y:auto;min-height:0;padding:32px 40px 60px}
article{max-width:960px;margin:0 auto;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:34px 38px;box-shadow:0 18px 45px rgba(23,32,51,.08)}
.stamp{color:var(--muted);font-size:13px;margin:0 0 22px}
h1{font-size:34px;margin:0 0 8px}h2{margin-top:34px;border-top:1px solid var(--line);padding-top:22px;scroll-margin-top:12px}h3{margin-top:22px}
p,li{font-size:16px}blockquote{background:var(--soft);border-left:5px solid var(--accent);margin:16px 0;padding:12px 18px;border-radius:8px}
table{width:100%;border-collapse:separate;border-spacing:0;background:#f8fafd;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:14px 0}
th,td{border-bottom:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top;font-size:15px}th{background:var(--soft)}tr:last-child td{border-bottom:0}
code{background:var(--code);padding:2px 5px;border-radius:5px;font-size:.92em}pre{background:#eef3f8;border:1px solid var(--line);padding:16px;border-radius:10px;overflow:auto;line-height:1.45}pre code{background:transparent;padding:0}
ul,ol{padding-left:26px}li{margin:4px 0}
li.offen,li.erledigt,li.arbeit{list-style:none;margin-left:-22px;padding-left:0}
.kasten{display:inline-block;width:20px;height:20px;line-height:18px;text-align:center;border:1px solid #8a97ab;border-radius:5px;margin-right:8px;font-size:12px;font-family:ui-monospace,Menlo,monospace;background:#fff}
li.erledigt .kasten{background:#2f8f5b;color:#fff;border-color:#2f8f5b}li.arbeit .kasten{background:#e7b23c;color:#fff;border-color:#e7b23c}li.erledigt{color:var(--muted)}
hr{border:0;border-top:1px solid var(--line);margin:24px 0}
@media(max-width:760px){body{grid-template-columns:170px minmax(0,1fr)}main{padding:18px 16px 40px}article{padding:22px 18px}h1{font-size:26px}aside a{font-size:13px}}
@media print{html,body{overflow:visible;display:block}aside{display:none}main{overflow:visible;padding:0}article{border:0;box-shadow:none}}
'''

def seite(name, inhalt, abschnitte, alle, stand):
    nav = ''.join(f'<a href="{n}.html" class="{"aktiv" if n == name else ""}">{html.escape(n)}</a>' for n in alle)
    abs_nav = ''.join(f'<a class="abschnitt" href="#{a}">{html.escape(t)}</a>' for a, t in abschnitte)
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(name)} · Recht DOKU</title>
<style>{STYLE}</style>
</head>
<body>
<aside aria-label="Navigation">
<div class="marke">RECHT<small>DOKU</small></div>
<div class="titel">Seiten</div>
{nav}
<div class="titel">Abschnitte</div>
{abs_nav}
</aside>
<main>
<article>
<div class="stamp">aus md/{html.escape(name)}.md, Stand {stand}</div>
{inhalt}
</article>
</main>
</body>
</html>
'''

def main():
    vorhanden = [n for n in REIHENFOLGE if (MD / f'{n}.md').exists()]
    vorhanden += sorted(p.stem for p in MD.glob('*.md') if p.stem not in vorhanden)
    for n in vorhanden:
        # Stempel ist das Änderungsdatum der Quelle, nicht die Bauzeit: so ändert sich die HTML nur mit dem Inhalt
        stand = datetime.fromtimestamp((MD / f'{n}.md').stat().st_mtime).strftime('%d.%m.%Y %H:%M')
        text = (MD / f'{n}.md').read_text('utf-8')
        inhalt, abschnitte = render(text)
        (DOKU / f'{n}.html').write_text(seite(n, inhalt, abschnitte, vorhanden, stand), 'utf-8')
        print('erzeugt:', f'DOKU/{n}.html')
    return 0

if __name__ == '__main__':
    sys.exit(main())
