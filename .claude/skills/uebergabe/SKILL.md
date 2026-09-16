---
name: uebergabe
description: Übergabepaket für Anwalt, Behörde, Gericht oder Beratungsstelle zusammenstellen: Inhaltsverzeichnis, Chronologie, Fristen, Anlagenverzeichnis, Journal und Originale als ZIP außerhalb des Projekts, mit kurzem Begleitvermerk.
arguments: [fall, empfaenger]
---

# Übergabe für $fall an $empfaenger

Lies `CLAUDE.md` und die Akte (`cli.py fall_lesen fall=$fall`).

## Vorgehen

1. Mit dem Nutzer klären, was der Empfänger braucht: alles, nur Originale,
   nur bestimmte Dokumente (D-Kennungen), mit oder ohne Entwürfe.
   Vertrauliches, das nicht hin soll (Notizen, interne Bewertungen), bleibt draußen.
2. Bestand prüfen: `cli.py bestand_pruefen fall=$fall` (liest nur). Fehlende,
   veränderte oder nicht erfasste Dateien dem Nutzer nennen, bevor etwas
   verschickt wird; nicht erfasste erst nach Freigabe mit
   `cli.py bestand_abgleichen fall=$fall` registrieren.
3. Paket erzeugen:
   `python3 ".claude/recht/werkzeuge/uebergabe_paket.py" $fall [--nur D0001,D0002] [--mit-entwuerfen] [--ziel "~/Desktop/…zip"]`
   Standardziel: Schreibtisch, Name mit Fall und Datum.
4. Begleitvermerk für den Empfänger (Markdown, 1 Seite): Wer ich bin, worum es
   geht, was ich will, welche Fristen laufen (mit Prüfstatus), welche Fragen
   offen sind, was im Paket ist. Als `06 Entwürfe/JJJJ-MM-TT_Begleitvermerk_<Empfänger>_ENTWURF.md`,
   Word-Datei mit `docx_erzeugen.py`.
5. Journal: `cli.py journal_schreiben fall=$fall art=Arbeit titel="Übergabepaket …" text=…`.

## Grenzen

Das Paket wird nicht verschickt. Der Nutzer entscheidet über Empfänger und
Weg. Das Inhaltsverzeichnis ist eine Zusammenstellung, kein Nachweis von
Zugang oder Einreichung.
