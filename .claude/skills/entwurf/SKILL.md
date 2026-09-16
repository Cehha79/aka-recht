---
name: entwurf
description: Schreiben oder Schriftsatz als Entwurf verfassen (Einspruch, Widerspruch, Fristsetzung, Auskunft, Klage, Brief), aus den Vorlagen, mit Belegen aus der Akte, als Markdown und Word-Datei. Versand nur nach Freigabe des Nutzers.
arguments: [fall, art]
---

# Entwurf für $fall: $art

Lies `CLAUDE.md` und die Akte (`cli.py fall_lesen fall=$fall`). Vorlagen liegen
unter `05 Vorlagen/Schreiben/` (LIESMICH.md zuerst). Passende Vorlage
wählen oder Briefkopf.md als Grundlage nehmen. Rechtsgebiet und Rolle aus der
Akte, nicht vorausgesetzt.

## Vorgehen

1. Zweck, Empfänger (P-Kennung), Frist, gewünschte Wirkung klären. Fehlt
   etwas Wesentliches, kurz nachfragen; sonst mit `[PRÜFEN: …]` weiterarbeiten.
2. Sachverhalt aus belegten Tatsachen (D-Kennungen, Fundstellen). Keine
   Behauptung ohne Beleg, sonst `[BELEG: …]`. Rechtsgrundlagen nur nach
   Lesen am Volltext, sonst `[QUELLE: …]`.
   Gibt es zur Verfahrensart ein Merkblatt unter `04 Rechtsquellen/Verfahren/`
   (die Vorlage nennt es), dessen Pflichtinhalt, Adressat und Frist gegen den
   Entwurf prüfen und fehlende Punkte als `[PRÜFEN: …]` markieren. Das
   Merkblatt hat ein Prüfdatum; Fassung der Normen für den Fall erneut prüfen.
3. Datei schreiben: `06 Entwürfe/JJJJ-MM-TT_<Kurzname>_ENTWURF.md` im Fallordner.
   Oben interne Hinweise (Frist, Versandweg, offene Punkte), dann `---`,
   dann der Sendetext. Neue Fassung: Datei überschreiben.
4. In der Akte erfassen (Pfad relativ zum Fallordner):
   `cli.py entwurf_erfassen fall=$fall titel="…" datei="06 Entwürfe/…_ENTWURF.md" status="in Arbeit"`
   Gleicher Titel = Fassung zählt hoch. Danach `cli.py fall_lesen fall=$fall`:
   der Bestand hat der Datei jetzt eine D-Kennung gegeben.
5. Word-Datei erzeugen (Pfad vom Projektordner aus):
   `python3 ".claude/recht/werkzeuge/docx_erzeugen.py" "02 Fälle/<Fallordner>/06 Entwürfe/<Datei>.md"`
   Die Warnung zu offenen Markern dem Nutzer nennen.
6. Setzt der Entwurf selbst eine Frist (Nacherfüllung, Antwort, Zahlung):
   `cli.py frist_eintragen fall=$fall datum=… titel=… art="selbst gesetzt" ausloeser="eigenes Schreiben, Versand offen" rechtsgrundlage="eigene Fristsetzung" berechnung=… pruefstatus=offen quelle=<D-Kennung des Entwurfs>`;
   nach dem Versand auf `bestätigt` setzen und `quelle` auf den Versandbeleg.
7. Vor einer Endfassung `/gegenpruefung` vorschlagen. Journal:
   `cli.py journal_schreiben fall=$fall art=Arbeit titel="Entwurf: …" text=…`.

## Sprache im Sendetext

Kurze Sätze, ein Gedanke je Satz, Aktiv statt Passiv („ich beantrage“, nicht
„es wird beantragt“), bestimmte Angaben statt Umschreibungen (Datum, Betrag,
Kennung statt „kürzlich“, „ein gewisser Betrag“). Keine Drohungen, keine
Wertungen der Person, keine Floskeln („hiermit möchte ich“). Rechtsbegriffe
nur, wo sie tragen; jede Norm mit Absatz. Zuerst das Anliegen, dann die
Begründung, zuletzt Antrag und Frist. Vor der Abgabe einmal laut lesen: Was
ein Sachbearbeiter beim ersten Lesen nicht versteht, wird umformuliert.

## Nach Versand durch den Nutzer

Nicht der Skill versendet. Wenn der Nutzer den Versand meldet: Beleg
(E-Mail als .eml, Sendebericht, Einlieferungsbeleg) in `01 Eingang/` ablegen
lassen, mit `cli.py dokument_verschieben` nach `03 Schriftverkehr/Versandnachweise`,
Entwurf auf `status=versandt versandt_als=D…` setzen, Ereignis „Versand“ und
Journal „Versand“ eintragen.

## Grenzen

Kein Versand, keine Einreichung. Keine Zusicherung über Erfolgsaussichten.
Bei Klagen, Kündigungsschutz, Strafanzeigen, Vergleichen: fachanwaltliche
Prüfung empfehlen und die Vorarbeit dafür aufbereiten.
