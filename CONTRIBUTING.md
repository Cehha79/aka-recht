# Mitmachen bei AKA Recht

AKA Recht ist kostenlos und wird offen entwickelt. Danke, dass du
mithelfen willst. Diese Seite sagt, was hilft, welche Regeln gelten und wie
ein Beitrag abläuft.

## Was hilft

- Fehler melden: Was hast du getan, was ist passiert, was hast du erwartet.
  Bitte mit Version (README) und Betriebssystem, ohne echte Akten.
- Feiertage anderer Bundesländer im Fristenrechner (`06 Werkzeuge/dienst/fristen.py`).
- Schreibvorlagen für weitere Rechtsgebiete (`05 Vorlagen/Schreiben/`), mit
  Quelle je Rechtsaussage.
- Übersetzungen von Oberfläche, Anleitung und Skills.
- Später: Pakete für andere Länder (Fristenregeln, Feiertage, Quellen,
  Vorlagen), nur mit Recherche am Originalvolltext des jeweiligen Landes.
- Prüfung durch Juristinnen und Juristen: Wo ist eine Vorlage, eine
  Anleitung oder ein Rechtssatz falsch oder veraltet?

## Regeln

1. Issues und Diskussionen sind nur für die Software und erfundene
   Beispiele. Keine Fragen und keine Antworten zu echten Fällen:
   Fallberatung ist nicht Gegenstand des Projekts; dafür gibt es
   Fachanwältinnen, Fachanwälte und Beratungsstellen.
2. Keine echten Akten, Namen, Aktenzeichen oder Gesundheitsdaten einreichen,
   auch nicht in Screenshots oder Testdaten. Testfälle sind erfunden.
3. Nur Python-Standardbibliothek, keine Fremdpakete. Oberfläche ohne
   Framework, ohne fremde Schriften, ohne Analysedienste. Der Dienst bleibt
   auf 127.0.0.1 und ruft keine fremden Adressen auf.
4. Jede rechtliche Aussage nennt Norm mit Absatz und Gesetz oder Urteil mit
   Gericht, Datum und Aktenzeichen, am Volltext gelesen. Ungeprüftes bleibt
   als `[QUELLE: …]`, `[PRÜFEN: …]` oder `[BELEG: …]` sichtbar.
5. Die Regeln in `DOKU/md/REGELN.md` gelten für jeden Beitrag. Nach einer
   inhaltlichen Änderung die Doku in `DOKU/md/` im selben Zug mitpflegen.

## Ablauf

1. Repository forken, Zweig anlegen, Änderung machen.
2. Prüfen: `python3 "06 Werkzeuge/dienst/pruefen.py"` (Funktionstest, alle
   Punkte müssen bestehen). Nach Änderungen an `CLAUDE.md` oder einem Skill
   `python3 "06 Werkzeuge/verteilen.py"` laufen lassen. Nach Änderungen an
   CSS oder JS die Versionsnummer im HTML-Link erhöhen.
3. Pull Request mit kurzer Beschreibung: was, warum, wie geprüft.

## Lizenz deiner Beiträge

Mit dem Einreichen bestätigst du, dass du den Beitrag selbst geschrieben hast
oder das Recht hast, ihn beizusteuern, und dass er unter der GNU Affero
General Public License, Version 3 (siehe `LICENSE`), steht. Fremde Texte,
Vorlagen oder Code nur, wenn ihre Lizenz das erlaubt und die Herkunft im
Beitrag steht.

## Sprache

Deutsch ist die Arbeitssprache des Projekts. Beiträge auf Englisch oder
Türkisch sind willkommen; die Anleitung dazu folgt mit den Übersetzungen.

Kontakt: info@mika-tec.com
