---
name: fallaufnahme
description: Neuen rechtlichen Vorgang oder neue Post strukturiert aufnehmen: Rolle, Ziel, Rechtsordnung, Verfahrensart, Beteiligte, Zugang, fehlende Angaben. Für jedes Rechtsgebiet. Verwenden bei neuem Fall, neuer Post oder unklarem Verfahrensstand.
arguments: [fall]
---

<!-- Erzeugt von „06 Werkzeuge/verteilen.py“ aus .claude/skills/fallaufnahme/SKILL.md.
     Nicht von Hand ändern: die Quelle pflegen, dann das Skript laufen lassen. -->

# Fallaufnahme für $fall

Lies zuerst `AGENTS.md` im Projekt (Arbeitsprofil). Arbeite nur an Fall `$fall`.
Ist `$fall` leer oder „neu“, frage nach dem Vorgang oder lege nach Rücksprache
einen Fall an (`cli.py fall_anlegen titel=… bereich=… rolle=… ziel=…`).
Will der Nutzer nur ausprobieren, `cli.py beispiel_laden` (erfundener
Kündigungsfall, jederzeit löschbar) statt eines echten Falls.

## Vorgehen

1. Akte lesen: `python3 "06 Werkzeuge/dienst/cli.py" fall_lesen fall=$fall`.
   Neue Post liegt in `01 Eingang/` des Falls oder im gemeinsamen `01 Eingang/`.
2. Jedes neue Schreiben vollständig lesen (`cli.py dokument_text fall=$fall dokument=D…`),
   bei Fotos und Bildscans das Bild öffnen. Fehlende Seiten, Umschläge und
   schlecht lesbare Stellen benennen. Aus Dateinamen keine Zustellung ableiten.
3. Feststellen und getrennt notieren: Dokumentart nach Inhalt (Anhörung,
   Bescheid, Mahnung, Kündigung, Vertrag, Klage, gerichtliche Verfügung …),
   Absender und Empfänger, Dokumentdatum, behaupteter Versand, tatsächlicher
   Zugang mit Nachweis, Aktenzeichen, gesetzte Fristen als Kandidaten.
4. Eigene Rolle, Beteiligte, Ziel, Rechtsordnung (bei Auslandsbezug Land und
   Sprache), Verfahrensart und Bereich klären. Was unklar bleibt, offen lassen.
   Gibt es zur Verfahrensart ein Merkblatt unter `04 Rechtsquellen/Verfahren/`,
   daraus Rechtsbehelf, Frist mit Norm und Adressat als Kandidaten nennen
   (unbestätigt, bis `/fristencheck` gerechnet hat).
5. Ergebnis in die Akte übernehmen, jeweils über die Werkzeuge:
   - Beteiligte und Fallfelder: `cli.py fall_lesen`, Änderungen als vollständige
     Akte mit `cli.py akte_speichern fall=$fall akte='{…}' revision=…`
   - Zugang als Ereignis: `cli.py ereignis_eintragen fall=$fall datum=… titel=… art=Zugang quelle=D… detail=…`
   - Dokument ordnen: `cli.py dokument_ordnen fall=$fall dokument=D… felder='{"titel":…,"art":…,"stand":"Zugegangen"}'`
   - Fristkandidaten nur als Aufgabe „Frist prüfen“ (`cli.py aufgabe_anlegen`)
     oder mit `/fristencheck`, nie als bestätigte Frist.
   - Eigene Notizen und Angaben des Nutzers nach `07 Recherche/Eigene Angaben`,
     Ordnungsangabe stand=Vermerk.
   - Gelesene Post nach `01 Eingang/Gelesen/` oder in den passenden Bereich:
     `cli.py dokument_verschieben fall=$fall dokument=D… bereich="03 Schriftverkehr" unterordner="…"`
6. Journal: `cli.py journal_schreiben fall=$fall art=Eingang titel=… text=…`.

## Ergebnis an den Nutzer

Aufnahmevermerk: Fall, Rolle, Ziel, Verfahrensstand (belegt), Unterlagen mit
Kennungen und Fundstellen, offene Angaben, Fristkandidaten mit Hinweis
„unbestätigt“, nächster sinnvoller Schritt. Keine Rechtsfolge ohne geprüften
Volltext. Kein Versand, keine Einreichung.
