---
name: uebergabe
description: Übergabepaket für Anwalt, Behörde, Gericht oder Beratungsstelle zusammenstellen: Inhaltsverzeichnis, Chronologie, Fristen, Anlagenverzeichnis, Journal und Originale als ZIP außerhalb des Projekts, mit kurzem Begleitvermerk.
arguments: [fall, empfaenger]
---

<!-- Erzeugt von „06 Werkzeuge/verteilen.py“ aus .claude/skills/uebergabe/SKILL.md.
     Nicht von Hand ändern: die Quelle pflegen, dann das Skript laufen lassen. -->

# Übergabe für $fall an $empfaenger

Lies `AGENTS.md` und die Akte (`cli.py fall_lesen fall=$fall`).

## Vorgehen

1. Mit dem Nutzer Empfänger und Umfang festlegen, bevor etwas gebaut wird:
   `--empfaenger anwalt` ergibt den Umfang „voll“ (Verzeichnis mit Beteiligten,
   Verfahren, Chronologie, Fristen, offenen Aufgaben, Journal, alle Originale
   aus 02 bis 05; Entwürfe nur mit `--mit-entwuerfen`). `behoerde`, `gericht`,
   `gegenseite`, `beratung` ergeben „dokumente“: nur die mit `--nur D0001,D0002`
   gewählten Dokumente und deren Verzeichnis, keine Chronologie, keine
   Fristen, kein Journal, keine internen Angaben (`--mit-journal`,
   `--mit-chronologie` nur auf ausdrücklichen Wunsch). Notizen und interne
   Bewertungen sind nie im Paket.
2. Bestand prüfen: `cli.py bestand_pruefen fall=$fall` (liest nur). Fehlende,
   veränderte oder nicht erfasste Dateien dem Nutzer nennen, bevor etwas
   verschickt wird; nicht erfasste erst nach Freigabe mit
   `cli.py bestand_abgleichen fall=$fall` registrieren.
3. Erst die Vorschau, dann das Paket:
   `python3 ".claude/recht/werkzeuge/uebergabe_paket.py" $fall --empfaenger <…> [--nur D0001,D0002] [--mit-entwuerfen] --vorschau`
   zeigt jede Datei, die hinein käme; dem Nutzer zeigen, dann denselben
   Aufruf ohne `--vorschau` [--ziel "~/Desktop/…zip"]. Unbekannte oder
   fehlende Kennungen brechen ab, es entsteht kein Paket. Das Skript schreibt
   erst eine vorläufige Datei, liest sie zurück, prüft jede Datei gegen das
   Manifest (`00 Manifest.json` im Paket) und benennt erst dann um.
   Standardziel: Schreibtisch, Name mit Fall, Empfänger und Datum.
4. Begleitvermerk für den Empfänger (Markdown, 1 Seite): Wer ich bin, worum es
   geht, was ich will, welche Fristen laufen (mit Prüfstatus), welche Fragen
   offen sind, was im Paket ist. Als `06 Entwürfe/JJJJ-MM-TT_Begleitvermerk_<Empfänger>_ENTWURF.md`,
   Word-Datei mit `docx_erzeugen.py`.
5. Journal: `cli.py journal_schreiben fall=$fall art=Arbeit titel="Übergabepaket …" text=…`.

## Datensparsamkeit vor der Übergabe

Nur, was Empfänger und Zweck brauchen (Prüfbericht 16.09.2026, S05). Vor
dem Bau der Vorschau prüfen und dem Nutzer die Ausschlüsse mit Grund nennen:

- Dokumente: jedes gewählte Dokument einzeln begründen; Gesundheitsdaten,
  Daten Dritter (Kollegen, Zeugen, Familie), interne Notizen, Entwürfe und
  Gedächtnisprotokolle nur, wenn der Zweck es verlangt. Bei Gericht und
  Behörde nur die Anlagen, die im Schriftsatz genannt sind.
- Ordnungsangaben: Titel, Notizfelder und Dateinamen im Verzeichnis
  können Bewertungen oder Namen Dritter tragen („Lügner“, Klarnamen von
  Zeugen); vorher lesen, nötigenfalls Titel neutral fassen (nur
  Ordnungsangabe, nie die Datei).
- Journal und Chronologie sind intern; nur mit `--mit-journal`,
  `--mit-chronologie` und nur an die eigene Anwältin oder den eigenen Anwalt.
- Schwärzungen: die Mappe schwärzt nicht. Wird eine geschwärzte Fassung
  gebraucht, entsteht sie als neue Datei außerhalb der Originale (06
  Entwürfe) mit einem geeigneten Programm; danach prüfen, ob der verdeckte
  Text auch im Textauszug (`dokument_text`) und in den Metadaten fehlt. Ein
  schwarzes Rechteck über lesbarem Text reicht nicht.
- Nach der Vorschau: jede Datei der Liste gegen die Ausschlussliste lesen;
  eine ausgeschlossene Angabe darf weder in einer Datei noch im Verzeichnis
  noch im Manifest stehen.

## Grenzen

Das Paket wird nicht verschickt. Der Nutzer entscheidet über Empfänger und
Weg. Das Inhaltsverzeichnis ist eine Zusammenstellung, kein Nachweis von
Zugang oder Einreichung.
