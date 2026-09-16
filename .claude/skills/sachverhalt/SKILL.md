---
name: sachverhalt
description: Sachverhalt eines Falls aus den Originalen aufbereiten: Chronologie mit Fundstellen, Beweistabelle, Widersprüche und Beweislücken. Keine Rechtsbewertung, keine Fristen.
arguments: [fall]
---

# Sachverhalt und Belege für $fall

Lies `CLAUDE.md`. Akte lesen mit `python3 "06 Werkzeuge/dienst/cli.py" fall_lesen fall=$fall`.
Dokumentkennungen gelten nur mit der Fallkennung. Quellen anderer Fälle nicht verwenden.

## Aufbereitung

- Ereignisse nach belegtem Zeitpunkt ordnen. Unbekannte oder ungefähre
  Zeitpunkte so lassen, keine scheingenauen Daten ergänzen.
- Zu jedem Ereignis: Dokumentkennung und Fundstelle (Seite, Absatz, Kopfzeile).
  Texte mit `cli.py dokument_text`, Bilder öffnen. Mehrere gleiche Kopien sind
  kein mehrfacher Beweis. Eigene Notiz und fremde Bestätigung getrennt gewichten.
- Beweistabelle mit den Spalten: Behauptung; Status (belegt, eigene Angabe,
  Gegenseite, Annahme); Beleg und Fundstelle; was der Beleg tatsächlich zeigt;
  Gegenindiz; fehlender Nachweis. Widersprüche nebeneinander zeigen.
- „Steht im Schreiben“ von „ist passiert“ trennen. Rechtsbegriffe nicht als
  Tatsachen voraussetzen. Unlesbare Beträge, Namen, Daten am Bild prüfen.

## Ablage

- Ereignisse in die Chronologie: `cli.py ereignis_eintragen fall=$fall datum=… titel=… art=… quelle=D… detail=…`
- Prüfvermerk als Markdown unter `07 Recherche/Prüfvermerke/JJJJ-MM-TT_Sachverhalt.md`
  (Beweistabelle als Markdown-Tabelle). Vorhandenen Vermerk fortführen statt
  einen zweiten anzulegen. HTML-Ansicht nur, wenn der Nutzer sie will.
- Journal: `cli.py journal_schreiben fall=$fall art=Arbeit titel="Sachverhalt aufbereitet" text=…`

## Grenzen

Keine Fristen berechnen, keine Originale ändern (Hook sperrt Bereiche 02 bis 05
und 08). Ein Ordnername belegt keine Einreichung.
