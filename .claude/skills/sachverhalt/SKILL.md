---
name: sachverhalt
description: Sachverhalt eines Falls aus den Originalen aufbereiten: Chronologie mit Fundstellen, Beweistabelle, Widersprüche und Beweislücken. Keine Rechtsbewertung, keine Fristen.
arguments: [fall]
---

# Sachverhalt und Belege für $fall

Lies `CLAUDE.md`. Akte lesen mit `python3 "06 Werkzeuge/dienst/cli.py" fall_lesen fall=$fall`.
Dokumentkennungen gelten nur mit der Fallkennung. Quellen anderer Fälle nicht verwenden.

## Dokumentqualität zuerst

Vor jeder Auswertung feststellen, ob das Material lesbar und vollständig ist
(Prüfbericht 16.09.2026, S01). Je Dokument einen Qualitätsstatus vergeben:
vollständig lesbar, teilweise lesbar, nicht lesbar, unvollständig.

- Dateiliste (`cli.py fall_uebersicht`) mit den Anlagen abgleichen, die die
  Schreiben nennen: fehlende Anlagen, fehlende Rückseiten, fehlende Seiten
  (Seitenzahl im Auszug gegen „Seite x von y“ im Text), fehlende Umschläge.
- `textquelle` und `textstand` beachten (siehe unten). Bildscan und Foto
  sind ungelesen, bis der Nutzer den Inhalt gesichtet hat; keine
  Texterkennung (OCR) in der Mappe, eine solche wäre ein eigenes Werkzeug
  außerhalb der Standardbibliothek und läuft nur nach Entscheidung des Nutzers.
- Datums- und Betragsangaben, Aktenzeichen und Namen aus dem Auszug am
  Original prüfen (zweimal lesen, bei PDF-Textschicht auf verdrehte
  Spalten und Tabellen achten). Eine unsichere Zahl bleibt `[PRÜFEN: …]`,
  nie eine sichere Tatsache.
- Mehrere Fassungen desselben Schreibens (Kopie, Scan, Ausdruck mit Vermerk)
  nebeneinander nennen; Abweichungen sind ein Befund.

Ausgabe im Vermerk: Tabelle Dokument; Qualitätsstatus; konkreter Mangel;
nächster Schritt (Sichtprüfung, Nachfordern, Rückseite scannen). Nichts am
Original ändern; ein Textauszug ist eine Ableitung.

## Aufbereitung

- Ereignisse nach belegtem Zeitpunkt ordnen. Unbekannte oder ungefähre
  Zeitpunkte so lassen, keine scheingenauen Daten ergänzen.
- Zu jedem Ereignis: Dokumentkennung und Fundstelle (Seite, Absatz, Kopfzeile).
  Texte mit `cli.py dokument_text`, Bilder öffnen. Die Antwort nennt die
  `textquelle`: nur `direkt` und `pdf-text` sind gelesener Text; bei `bild`,
  `kein-text` (Bildscan) oder `werkzeug-fehlt` gilt das Dokument als nicht
  gelesen, in der Beweistabelle als „nicht lesbar“ führen und den Nutzer um
  Sichtprüfung bitten; danach `cli.py dokument_ordnen … felder='{"textstand":
  "visuell geprüft"}'` (Werte: direkt ausgelesen, OCR-erkannt, visuell
  geprüft, teilweise lesbar, nicht lesbar). Der Auszug ist eine Ableitung:
  Zahlen, Zugangsdaten, Fristen und Anträge am Original gegenprüfen, bei PDF
  können Spalten und Tabellen in falscher Reihenfolge stehen. Mehrere gleiche
  Kopien sind kein mehrfacher Beweis. Eigene Notiz und fremde Bestätigung getrennt gewichten.
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
