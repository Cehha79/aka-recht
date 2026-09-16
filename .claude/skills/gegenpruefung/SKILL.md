---
name: gegenpruefung
description: Entwurf oder Bewertung kritisch gegen Originalbelege und Rechtsquellen prüfen: Gegenargumente, unbelegte Aussagen, unpassende Zitate, Zahlen, Anlagen, Fristen. Keine stillen Änderungen am geprüften Text.
arguments: [fall, ziel]
---

# Gegenprüfung für $fall: $ziel

Lies `CLAUDE.md`, die Akte (`cli.py fall_lesen fall=$fall`) und den zu prüfenden
Text `$ziel` (Pfad im Fallordner oder D-Kennung). Prüfe ihn als Behauptung,
auch wenn er von einer KI stammt. Ein zweiter KI-Durchgang ist keine
anwaltliche Bestätigung.

## Prüfmethode

1. Zentrale Behauptungen auf Beleg und Fundstelle zurückführen. Trägt das
   Dokument die Behauptung oder gibt es sie nur wieder? Schlüsse aus
   Dateinamen, Kopien oder bloßen Entwürfen markieren.
2. Rechtszitate am Originalvolltext lesen: Gericht, Aktenzeichen, Datum,
   Gesetzesfassung, Anwendbarkeit auf den Zeitraum. Eine formal plausible
   Fundstelle kann erfunden oder unpassend sein.
3. Stärkstes sachliches Gegenargument aus Sicht der anderen Seite. Fehlende
   Nachweise, alternative Erklärungen, Ausschlussfristen, Zugang, Beweislast.
4. Anträge und Ergebnis mit dem belegten Sachverhalt vergleichen. Zahlen,
   Daten, Anlagenverweise, Platzhalter 【 】 und Marker `[PRÜFEN]`, `[BELEG]`,
   `[QUELLE]` auflisten.
5. Fristangaben: Auslöser, Zugang, Grundlage, Rechnung gesondert prüfen
   (`cli.py frist_berechnen`). Ohne Voraussetzung keine Freigabe behaupten.
6. Angriff in drei Schritten: (a) den Text in einzelne, prüfbare Behauptungen
   zerlegen (Tatsache, Rechtssatz, Schluss); (b) jede Behauptung einzeln
   angreifen, so wie es ein gegnerischer Anwalt täte; (c) die Gegenseite
   in ihrer stärksten Form aufschreiben (nicht die schwache Fassung), dann
   erst die eigene Antwort darauf. Befunde nach Schwere ordnen: verliert
   den Anspruch, schwächt ihn, Schönheitsfehler.

## Ergebnis

Befunde nach Bedeutung: Stelle; Problem; Beleg oder Quelle; Auswirkung;
Korrekturvorschlag. Unbekanntes getrennt von nachgewiesenen Fehlern.
Keine Aussage „rechtssicher“ oder „alles korrekt“. Den Text nur bei
ausdrücklichem Änderungsauftrag bearbeiten, sonst Prüfbericht liefern.

## Ablage

Bericht unter `07 Recherche/Prüfvermerke/JJJJ-MM-TT_Gegenpruefung_<Thema>.md`;
Journal-Eintrag mit `cli.py journal_schreiben fall=$fall art=Arbeit titel="Gegenprüfung: …" text=…`.
