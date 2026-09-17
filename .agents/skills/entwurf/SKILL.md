---
name: entwurf
description: Schreiben oder Schriftsatz als Entwurf verfassen (Einspruch, Widerspruch, Fristsetzung, Auskunft, Klage, Brief), aus den Vorlagen, mit Belegen aus der Akte, als Markdown und Word-Datei. Versand nur nach Freigabe des Nutzers.
arguments: [fall, art]
---

<!-- Erzeugt von „06 Werkzeuge/verteilen.py“ aus .claude/skills/entwurf/SKILL.md.
     Nicht von Hand ändern: die Quelle pflegen, dann das Skript laufen lassen. -->

# Entwurf für $fall: $art

Lies `AGENTS.md` und die Akte (`cli.py fall_lesen fall=$fall`). Vorlagen liegen
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
3. Entwurf aus der Vorlage anlegen: `cli.py vorlage_fuellen fall=$fall vorlage=<Name> [ziel=…]`
   (Namen: `cli.py vorlagen_auflisten`). Das Werkzeug kopiert die Vorlage nach
   `06 Entwürfe/JJJJ-MM-TT_<Vorlage>_ENTWURF.md`, setzt Absender (Einstellungen
   oder Beteiligter mit Rolle „Ich“), Unterschrift, Datum und Fallkennung ein
   und überschreibt nie; meldet es „Kein Absender“, den Nutzer auf die
   Einstellungen hinweisen. Dann die übrigen Platzhalter 【…】 im Sendetext
   ausfüllen. Aufbau der Datei: oben interne Hinweise (Frist, Versandweg,
   offene Punkte), dann `---`, dann der Sendetext. Neue Arbeitsfassung: Datei überschreiben. Die
   eingefrorenen Kopien unter `06 Entwürfe/Fassungen/` nie anfassen.
4. In der Akte erfassen (Pfad relativ zum Fallordner):
   `cli.py entwurf_erfassen fall=$fall titel="…" datei="06 Entwürfe/…_ENTWURF.md" status="in Arbeit"`
   Gleicher Titel = Fassung zählt hoch, jede Fassung mit Prüfsumme. Danach
   `cli.py bestand_abgleichen fall=$fall` (schreibend, nach Freigabe): erst
   der Abgleich gibt der neuen Datei ihre D-Kennung; Lesen allein
   registriert nichts.
   Freigabe durch den Nutzer: `status=geprüft` friert die Datei und eine
   gleichnamige .docx als nur lesbare Kopie unter `06 Entwürfe/Fassungen/`
   ein (eigene D-Kennung, Prüfsumme in der Akte). Nach dem Versand durch
   den Nutzer: `status=versandt versandt_als=D…` (Versandbeleg); weicht
   der Sendetext von der geprüften Fassung ab, meldet das Werkzeug es im
   Feld `hinweise`, das dem Nutzer nennen.
5. Word-Datei erzeugen (Pfad vom Projektordner aus):
   `python3 ".claude/recht/werkzeuge/docx_erzeugen.py" "02 Fälle/<Fallordner>/06 Entwürfe/<Datei>.md"`
   Das Skript gibt einen Vorabbericht aus (offene Marker, Platzhalter 【…】,
   interne Notizen im Sendetext, fehlende Kopfzeilen Von, An, Datum, Betreff,
   Aktenzeichen, Anlagenliste, Antragssatz, fehlende Trennlinie); mit
   `--pruefen` nur der Bericht ohne Datei. Jeden Befund dem Nutzer nennen.
   Eine erzeugte Datei ist kein Nachweis der Versandfertigkeit; die Freigabe
   trifft der Nutzer (Schritt 4, `status=geprüft`).
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

Nicht der Skill versendet. Wenn der Nutzer den Versand meldet
(Prüfbericht 16.09.2026, S06), den Versand nachvollziehbar nachbereiten:

1. Versandweg, Zeitpunkt, Empfänger, Anlagen und die konkrete Fassung
   erfragen; eine erzeugte Word-Datei belegt keinen Versand.
2. Beleg (E-Mail als .eml, Sendebericht, Einlieferungsbeleg, Portalquittung)
   in `01 Eingang/` ablegen lassen, mit `cli.py dokument_verschieben` nach
   `03 Schriftverkehr/Versandnachweise`, Stand „Versandt“.
3. Entwurf auf `status=versandt versandt_als=D…` setzen (friert die Fassung
   ein; weicht der Text von der geprüften Fassung ab, meldet es das Werkzeug).
4. Ereignis „Versand“ mit Quelle des Belegs; fehlt ein Beleg, Ereignis mit
   `detail="Angabe des Nutzers, kein Beleg"` und Aufgabe „Versandbeleg ablegen“.
5. Zugang ist ein eigenes Ereignis (Empfangsbestätigung, Antwort der
   Gegenseite, Zustellnachweis). Versand und Zugang nie gleichsetzen.
6. Eine Frist, die dieses Schreiben wahren sollte, erst dann `erledigt`, wenn
   der vereinbarte Nachweis vorliegt (Eingangsbestätigung des Gerichts, der
   Behörde oder des Empfängers); sonst bleibt sie `bestätigt` oder `offen`
   mit dem Vermerk „Versand laut Nutzerangabe am …, Zugang offen“.

## Grenzen

Kein Versand, keine Einreichung. Keine Zusicherung über Erfolgsaussichten.
Bei Klagen, Kündigungsschutz, Strafanzeigen, Vergleichen: fachanwaltliche
Prüfung empfehlen und die Vorarbeit dafür aufbereiten.
