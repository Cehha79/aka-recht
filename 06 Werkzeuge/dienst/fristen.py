#!/usr/bin/env python3
"""Fristenrechner nach §§ 187, 188, 193 BGB mit Feiertagen Baden-Württemberg.

Der Rechner liefert immer die Rechnung als Text mit. Er entscheidet nicht,
welche Frist gilt und ob § 193 BGB (Verschiebung auf den nächsten Werktag)
auf die konkrete Frist anwendbar ist. Das bleibt fachliche Prüfung.
Nur Standardbibliothek.
"""
from datetime import date, timedelta
import calendar, re

WOCHENTAGE = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

def ostersonntag(jahr):
    """Gregorianischer Osteralgorithmus (Meeus/Jones/Butcher)."""
    a = jahr % 19; b, c = divmod(jahr, 100); d, e = divmod(b, 4)
    f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    monat, tag = divmod(h + l - 7 * m + 114, 31)
    return date(jahr, monat, tag + 1)

def feiertage(jahr, land='BW'):
    """Gesetzliche Feiertage. BW: Feiertagsgesetz Baden-Württemberg."""
    o = ostersonntag(jahr)
    fest = {
        date(jahr, 1, 1): 'Neujahr', date(jahr, 5, 1): 'Tag der Arbeit',
        date(jahr, 10, 3): 'Tag der Deutschen Einheit', date(jahr, 12, 25): '1. Weihnachtstag',
        date(jahr, 12, 26): '2. Weihnachtstag',
        o - timedelta(days=2): 'Karfreitag', o + timedelta(days=1): 'Ostermontag',
        o + timedelta(days=39): 'Christi Himmelfahrt', o + timedelta(days=50): 'Pfingstmontag',
    }
    if land == 'BW':
        fest[date(jahr, 1, 6)] = 'Heilige Drei Könige'
        fest[o + timedelta(days=60)] = 'Fronleichnam'
        fest[date(jahr, 11, 1)] = 'Allerheiligen'
    return fest

def ist_werktag(d, land='BW'):
    return d.weekday() < 5 and d not in feiertage(d.year, land)

def _monate_addieren(d, n):
    """Gleicher Tag n Monate später; fehlt der Tag, letzter Tag des Monats (§ 188 Abs. 3 BGB)."""
    jahr = d.year + (d.month - 1 + n) // 12; monat = (d.month - 1 + n) % 12 + 1
    letzter = calendar.monthrange(jahr, monat)[1]
    return date(jahr, monat, min(d.day, letzter)), d.day > letzter

def _datum(wert):
    if isinstance(wert, date): return wert
    m = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', str(wert).strip())
    if m: return date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', str(wert).strip())
    if m: return date(int(m[3]), int(m[2]), int(m[1]))
    raise ValueError(f'Datum „{wert}“ nicht lesbar (JJJJ-MM-TT oder TT.MM.JJJJ).')

def fmt(d): return f'{WOCHENTAGE[d.weekday()]}, {d.day:02d}.{d.month:02d}.{d.year}'

def berechne(start, menge, einheit, ereignisfrist=True, werktagsregel=True, land='BW'):
    """Fristende berechnen.

    start:          Tag des Ereignisses (Zugang) oder Fristbeginn, Datum oder Text
    menge, einheit: 3 'wochen', 14 'tage', 2 'monate'
    ereignisfrist:  True = Ereignistag zählt nicht mit (§ 187 Abs. 1 BGB, Regelfall bei Zugang)
                    False = Beginn des Tages maßgebend, Tag zählt mit (§ 187 Abs. 2 BGB)
    werktagsregel:  True = fällt das Ende auf Samstag, Sonntag oder Feiertag, gilt der
                    nächste Werktag (§ 193 BGB). Anwendbarkeit auf die konkrete Frist prüfen.
    Rückgabe: dict mit ende, ende_text, rechnung (Liste Sätze), verschoben, grundlagen.
    """
    d0 = _datum(start); menge = int(menge); e = str(einheit).lower().strip()
    einheit = 'tag' if e.startswith('tag') else 'woche' if e.startswith('woch') else 'monat' if e.startswith('monat') else 'jahr' if e.startswith('jahr') else ''
    if menge < 1: raise ValueError('Menge muss mindestens 1 sein.')
    if not einheit: raise ValueError('Einheit: tage, wochen, monate oder jahre.')
    rechnung = []; grundlagen = []
    if ereignisfrist:
        rechnung.append(f'Ereignis am {fmt(d0)}. Der Ereignistag wird nicht mitgerechnet (§ 187 Abs. 1 BGB).')
        grundlagen.append('§ 187 Abs. 1 BGB')
    else:
        rechnung.append(f'Fristbeginn mit Anfang des {fmt(d0)}; dieser Tag wird mitgerechnet (§ 187 Abs. 2 BGB).')
        grundlagen.append('§ 187 Abs. 2 BGB')
    gekuerzt = False
    if einheit == 'tag':
        ende = d0 + timedelta(days=menge - (0 if ereignisfrist else 1))
        rechnung.append(f'Frist von {menge} Tagen endet mit Ablauf des letzten Tages (§ 188 Abs. 1 BGB): {fmt(ende)}.')
        grundlagen.append('§ 188 Abs. 1 BGB')
    else:
        if einheit == 'woche':
            ende = d0 + timedelta(days=7 * menge); wort = f'{menge} Woche{"n" if menge > 1 else ""}'
        elif einheit == 'monat':
            ende, gekuerzt = _monate_addieren(d0, menge); wort = f'{menge} Monat{"e" if menge > 1 else ""}'
        else:
            ende, gekuerzt = _monate_addieren(d0, 12 * menge); wort = f'{menge} Jahr{"e" if menge > 1 else ""}'
        if ereignisfrist:
            rechnung.append(f'Frist von {wort} endet mit Ablauf des Tages der letzten Woche oder des letzten Monats, der dem Ereignistag nach Benennung oder Zahl entspricht (§ 188 Abs. 2 BGB): {fmt(ende)}.')
        else:
            ende -= timedelta(days=1)
            rechnung.append(f'Frist von {wort} endet mit Ablauf des Tages, der dem Beginntag vorangeht (§ 188 Abs. 2 BGB): {fmt(ende)}.')
        grundlagen.append('§ 188 Abs. 2 BGB')
        if gekuerzt:
            rechnung.append('Der entsprechende Tag fehlt im letzten Monat, daher gilt dessen letzter Tag (§ 188 Abs. 3 BGB).')
            grundlagen.append('§ 188 Abs. 3 BGB')
    rechnerisch = ende; verschoben = False
    if werktagsregel and not ist_werktag(ende, land):
        grund = feiertage(ende.year, land).get(ende) or WOCHENTAGE[ende.weekday()]
        while not ist_werktag(ende, land): ende += timedelta(days=1)
        verschoben = True
        rechnung.append(f'Das rechnerische Ende fällt auf {grund}. Es gilt der nächste Werktag (§ 193 BGB): {fmt(ende)}. Ob § 193 BGB auf diese Frist anwendbar ist, fachlich prüfen.')
        grundlagen.append('§ 193 BGB')
    elif werktagsregel:
        rechnung.append(f'{fmt(ende)} ist ein Werktag; keine Verschiebung nach § 193 BGB.')
    else:
        rechnung.append('Verschiebung auf den nächsten Werktag (§ 193 BGB) wurde nicht angewendet.')
    return {'start': d0.isoformat(), 'ende': ende.isoformat(), 'ende_text': fmt(ende),
            'rechnerisch': rechnerisch.isoformat(), 'verschoben': verschoben,
            'rechnung': rechnung, 'grundlagen': grundlagen, 'feiertagsland': land,
            'hinweis': 'Rechnung ohne Gewähr für die Wahl der richtigen Frist. Auslöser, Zugang und Rechtsgrundlage sind gesondert zu belegen.'}

if __name__ == '__main__':
    import json, sys
    if len(sys.argv) < 4: sys.exit('Aufruf: fristen.py <Start> <Menge> <Einheit> [ereignis|beginn] [werktag|ohne]')
    r = berechne(sys.argv[1], sys.argv[2], sys.argv[3], ereignisfrist=(sys.argv[4] if len(sys.argv) > 4 else 'ereignis') == 'ereignis',
                 werktagsregel=(sys.argv[5] if len(sys.argv) > 5 else 'werktag') == 'werktag')
    print(json.dumps(r, ensure_ascii=False, indent=2))
