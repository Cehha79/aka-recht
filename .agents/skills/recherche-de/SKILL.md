---
name: recherche-de
description: Konkrete deutsche Rechtsfrage am Originalvolltext recherchieren: Vorschriften mit Fassung und Geltungszeitraum, Entscheidungen mit Gericht, Datum, Aktenzeichen, Gegenargumente. Für jedes Rechtsgebiet.
arguments: [fall, frage]
---

<!-- Erzeugt von „06 Werkzeuge/verteilen.py“ aus .claude/skills/recherche-de/SKILL.md.
     Nicht von Hand ändern: die Quelle pflegen, dann das Skript laufen lassen. -->

# Deutsche Rechtsrecherche für $fall: $frage

Lies `AGENTS.md` und den Zugangskatalog `04 Rechtsquellen/Quellen.md`.
Vor der Suche festhalten: Rechtsfrage, Fall, maßgeblicher Zeitraum, gesicherte
Tatsachen (aus der Akte, `cli.py fall_lesen fall=$fall`). Bei ausländischer
Rechtsordnung deutsche Regeln nicht übertragen, sondern den Bedarf benennen.

## Quellenprüfung

1. Primärquellen: Bundesrecht (gesetze-im-internet.de), Landesrecht
   (landesrecht-bw.de oder das Portal des Landes), EU-Recht (EUR-Lex),
   Rechtsprechung (rechtsprechung-im-internet.de, bundesarbeitsgericht.de,
   Landesportale). Suchanfragen ohne Namen, Anschriften und Aktenzeichen des Falls.
2. Originalvolltext öffnen (WebFetch). Bei Normen: Gesetz, Paragraph, Absatz,
   Satz, Fassung, Geltungszeitraum, Übergangsregeln. Heutige und für das
   Ereignis maßgebliche Fassung können abweichen.
3. Bei Entscheidungen: Gericht, Datum, Aktenzeichen, tragende Randnummer,
   Vergleichbarkeit von Sachverhalt und Verfahren. Ein Aktenzeichen mit
   ähnlichem Thema ist kein Beleg.
4. Existenz, Inhalt und Übertragbarkeit einer Quelle getrennt bewerten.
   Nicht abrufbar oder nur als Suchtreffer gesehen heißt „nicht verifiziert“
   und wird als `[QUELLE: …]` markiert, nie als Zitat ausgegeben.
5. Stärkste Gegenansicht, fehlende Tatsachen, alternative Wege benennen.

## Ergebnis

Rechtsfrage; belegte Ausgangstatsachen; geprüfte Quellen mit URL, Abrufdatum,
Rechtsstand, Fundstelle; Anwendung auf den Fall; Gegenargumente; offene
Punkte; nächster Schritt. Nicht verifizierte Quellen getrennt aufführen.

## Ablage

- Vermerk unter `07 Recherche/Prüfvermerke/JJJJ-MM-TT_Recherche_<Thema>.md`,
  vorhandenen Vermerk fortführen.
- Gelesene Quellen in die Akte (`quellen`-Block über `cli.py fall_lesen` und
  `cli.py akte_speichern`): titel, url, geprueft, verwendung.
- Fristen aus der Recherche nur über `/fristencheck`.
- Journal: `cli.py journal_schreiben fall=$fall art=Arbeit titel="Recherche: …" text=…`
Keine gemeinsame Gesetzesbibliothek mit vermeintlich dauerhaft aktuellen Texten aufbauen.
