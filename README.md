<p align="center"><img src="bilder/banner.svg" alt="AKA Recht: Deine Aktenmappe für Rechtssachen" width="100%"></p>

<p align="center">
<img src="bilder/abzeichen-preis.svg" alt="kostenlos">
<img src="bilder/abzeichen-lizenz.svg" alt="Lizenz AGPL-3.0">
<img src="bilder/abzeichen-python.svg" alt="Python 3, keine Fremdpakete">
<img src="bilder/abzeichen-lokal.svg" alt="läuft lokal, ohne Netz">
<img src="bilder/abzeichen-recht.svg" alt="Recht: Deutschland">
</p>

<p align="center"><b>Deutsch</b> · <a href="README.en.md">English</a> · <a href="CONTRIBUTING.md">Mitmachen</a> · <a href="https://github.com/sponsors/Cehha79">Unterstützen</a></p>

# AKA Recht

Ein Strafzettel, eine Kündigung, eine Nebenkostenabrechnung, ein Bescheid
vom Amt: Irgendwann hat jeder eine Rechtssache, und dann liegen Briefe,
Fotos, Mails und Fristen überall. **AKA Recht** ist der Ordner, in dem das
alles seinen Platz findet, und die Anleitung, mit der deine KI dir hilft,
es zu ordnen, zu prüfen und zu formulieren.

- **Jede Sache ist ein Fall** mit fester Kennung, festen Ordnern, Ordnungsdaten
  in `akte.json` und einem Journal. Originale werden nie verändert.
- **Fristen mit Rechnung:** Jede Frist zeigt Auslöser, Rechtsgrundlage und den
  Rechenweg nach §§ 187, 188, 193 BGB, mit den Feiertagen deines Bundeslands.
- **Deine KI arbeitet mit:** Claude Code, Claude Desktop, Codex oder jede andere,
  die MCP (Model Context Protocol) oder Befehle ausführen kann. Sieben
  Anleitungen führen sie von der Fallaufnahme bis zum geprüften Entwurf.
- **Alles bleibt bei dir:** keine KI in der App, kein Konto, kein Schlüssel,
  kein Netz. Der Dienst läuft nur auf deinem Rechner.

> [!TIP]
> Zum Ausprobieren gibt es einen erfundenen Beispielfall (Kündigung durch den
> Arbeitgeber). In der Oberfläche auf **„Beispielfall laden“** klicken, dann
> durch Akte, Dokumente, Fristen und Entwurf klicken. Jederzeit löschbar.

Version 0.1 · Stand 16.09.2026 · Autor: Hasan Tepegöz

## So sieht es aus

Zum Vergrößern anklicken. Alle Bilder zeigen den erfundenen Beispielfall
(„Max Muster“ gegen „Muster Logistik GmbH“), keine echten Personen.

<table>
<tr>
<td width="50%"><a href="bilder/01-zentrale.jpg"><img src="bilder/01-zentrale.jpg" alt="Zentrale: alle Fälle, Fristen, Eingang"></a><br><sub><b>Zentrale:</b> alle Fälle, nächste Fristen, Posteingang</sub></td>
<td width="50%"><a href="bilder/02-fallakte.jpg"><img src="bilder/02-fallakte.jpg" alt="Fallakte: Rolle, Ziel, Verfahren, nächste Fristen und Aufgaben"></a><br><sub><b>Fallakte:</b> Rolle, Ziel, Verfahren, Fristen, Aufgaben</sub></td>
</tr>
<tr>
<td width="50%"><a href="bilder/03-dokumente.jpg"><img src="bilder/03-dokumente.jpg" alt="Dokumente mit Vorschau, Kennung und Anlagennummer"></a><br><sub><b>Dokumente:</b> Vorschau, Kennung, Anlagennummer, Einsortieren</sub></td>
<td width="50%"><a href="bilder/04-fristen.jpg"><img src="bilder/04-fristen.jpg" alt="Fristen mit Rechtsgrundlage, Rechnung und Prüfstatus"></a><br><sub><b>Fristen:</b> Rechtsgrundlage, Rechenweg, Prüfstatus</sub></td>
</tr>
</table>

## Was deine KI damit kann

Die Mappe bringt Anleitungen mit (Skills), die deiner KI sagen, wie sie
einen Fall bearbeitet. Du rufst sie in Claude Code mit `/name` auf, in Codex
mit `$name`:

| Aufruf | Was passiert |
|---|---|
| `fallaufnahme` | Rolle, Ziel, Rechtsgebiet, Beteiligte, Zugang, fehlende Angaben; trägt in die Akte ein |
| `sachverhalt` | Chronologie und Beweistabelle aus den Originalen, mit Fundstelle je Aussage |
| `recherche-de` | Rechtsfrage am Originalvolltext, Fassung und Geltungszeitraum, Quellen in die Akte |
| `fristencheck` | Fristen mit Auslöser, Zugang, Rechtsgrundlage und gezeigter Rechnung |
| `entwurf` | Schreiben und Schriftsätze aus den Vorlagen, mit Belegen aus der Akte, als Markdown und Word |
| `gegenpruefung` | Gegenargumente, unbelegte Aussagen, falsche Zitate, Zahlen, Anlagen |
| `uebergabe` | Paket für Anwalt, Behörde oder Gericht als ZIP |

Die Anleitungen legen fest, wie sorgfältig die KI arbeiten muss: jede
Rechtsaussage mit Norm, Absatz und Gesetz oder Urteil mit Gericht, Datum und
Aktenzeichen, am Volltext gelesen; Ungeprüftes bleibt als `[PRÜFEN]`,
`[QUELLE]` oder `[BELEG]` sichtbar; die Gegenseite wird immer mitgedacht.
Jeder Entwurf bleibt Entwurf, bis du ihn prüfst und selbst versendest.
Schreibvorlagen liegen unter `05 Vorlagen/Schreiben/`, die Werkzeuge der
Akte (Lesen, Ordnen, Fristen rechnen, Journal) erreicht die KI über MCP
oder `cli.py`.

## Geltungsbereich

Diese Fassung ist für deutsches Recht gebaut: Fristenrechner nach §§ 187,
188, 193 BGB mit den landesweiten Feiertagen aller 16 Bundesländer (Bundesland
in den Einstellungen wählen; regionale Feiertage einzelner Gemeinden zählen
nicht), Quellenkatalog mit deutschen amtlichen Angeboten, Schreibvorlagen für
deutsche Verfahren.

Weitere Rechtsordnungen sind geplant, in dieser Reihenfolge: Österreich,
Schweiz, Frankreich, England und Wales, Türkei, USA, China, Russland und
weitere Länder. Bis dahin lässt sich die Mappe dort zwar zum Ordnen von
Unterlagen nutzen, Fristen und Vorlagen gelten aber nur für Deutschland.

Oberfläche, Vorlagen, Anleitung und Skills sind derzeit nur auf Deutsch.
Weitere Sprachen sind geplant, passend zu den Ländern.

## Voraussetzungen

- Python 3 (`python3 --version`), keine weiteren Pakete.
- Gebaut und geprüft auf macOS. Linux und Windows: Startskripte liegen bei,
  der Dienst nutzt nur die Standardbibliothek, geprüft ist es dort noch
  nicht. Unter Windows heißt der Befehl meist `python` statt `python3`;
  dann in `.mcp.json` und `.claude/settings.json` `python3` durch `python`
  ersetzen.
- Für die Textauszüge aus PDF optional `pdftotext` (Paket poppler).

## Erster Start

1. Ordner an einen Ort deiner Wahl legen.
2. Starten: macOS `Start.command` doppelklicken, Linux `Start.sh`
   ausführen, Windows `Start.bat` doppelklicken. Der Dienst läuft nur auf
   127.0.0.1, der Standardbrowser öffnet die Oberfläche. Beim ersten Start
   entsteht `zentrale.json`.
3. In der Oberfläche „Neuer Fall“ anlegen, Post nach `01 Eingang` legen oder
   in „Dokumente“ hinzufügen, ordnen, Fristen rechnen, Journal führen.
4. Seite „Anleitung“ in der Oberfläche lesen, dort steht auch, wie du eine KI
   anbindest.

## KI anbinden

| Assistent | Was zu tun ist |
|---|---|
| Claude Code | Sitzung im Ordner starten; `.mcp.json` liegt bei; Dialog bestätigen; `/mcp` prüfen. Skills unter `.claude/skills/` (`/fallaufnahme`, `/fristencheck`, `/entwurf` …). |
| Codex | einmalig `codex mcp add aka-recht -- python3 "<voller Pfad>/06 Werkzeuge/dienst/mcp_server.py"`; Skills unter `.agents/skills/` (`$fristencheck` …). |
| Claude Desktop | Einstellungen, Entwickler, Konfiguration bearbeiten: Eintrag `aka-recht` mit `command` `python3` und `args` `["<voller Pfad>/06 Werkzeuge/dienst/mcp_server.py"]`; Claude Desktop neu starten. |
| andere mit MCP | gleicher Aufruf in der Konfigurationsdatei des Assistenten. |
| ohne MCP, mit Befehlen | `python3 "06 Werkzeuge/dienst/cli.py" liste` |

Schreibende Werkzeuge laufen nur, wenn du den Aufruf bestätigst. Werkzeuge
für Versand, Löschen oder Ändern von Originalen gibt es nicht.

## Grenzen

> [!IMPORTANT]
> Die Mappe ist kein Rechtsanwalt und gibt keine Rechtsberatung. Sie hilft
beim Ordnen, Prüfen und Formulieren: Sie ordnet Unterlagen, rechnet Fristen
nach §§ 187, 188, 193 BGB mit sichtbarer Rechnung, hält fest, was belegt ist
und was nicht, und gibt deiner KI Anleitungen für Sachverhalt, Recherche,
Entwürfe und Gegenprüfung. Ob eine Frist gilt, ob ein Schreiben so
hinausgehen kann und was zu tun ist, prüfst du oder eine Fachanwältin, ein
Fachanwalt. Der Autor kennt und
prüft keine Angelegenheit eines Nutzers; alles läuft auf deinem Rechner, und
was deine KI aus den Anleitungen macht, geschieht in deiner eigenen Sache und
Verantwortung.

## Sicherung

„Geprüfte Sicherung erstellen“ in der Oberfläche schreibt eine ZIP außerhalb
des Ordners und liest sie zurück. Ziel und zweites Ziel stehen in den
Einstellungen. Prüfen ohne Oberfläche: `python3 "06 Werkzeuge/dienst/server.py" --check`.

## Lizenz

Copyright 2026 Hasan Tepegöz. Freie Software unter der GNU Affero
General Public License, Version 3 (AGPL-3.0), Wortlaut in `LICENSE`.
In Klartext:

- Du darfst die Mappe kostenlos nutzen, kopieren, ändern und weitergeben,
  privat wie beruflich.
- Wer sie verändert weitergibt oder als Dienst über ein Netz anbietet, muss
  den vollständigen Quelltext unter derselben Lizenz mitliefern.
- Lizenztext und Urheberhinweise bleiben bei jeder Weitergabe dabei.
- Keine Gewährleistung, keine Haftung, soweit das Gesetz das zulässt.

Maßgeblich ist allein der englische Text in `LICENSE`; dieser Abschnitt
erklärt ihn nur.

## Mitmachen und Unterstützen

Die Mappe ist kostenlos und wird offen entwickelt. Fehler, Vorschläge,
Feiertage anderer Bundesländer, Übersetzungen, Vorlagen und später ganze
Länderpakete sind willkommen. Bitte keine echten Akten, Namen oder
Aktenzeichen einreichen. Beiträge stehen unter derselben Lizenz (AGPL-3.0).
Wie ein Beitrag abläuft, steht in `CONTRIBUTING.md`.

Issues und Diskussionen sind nur für die Software da. Fragen zu einem echten
Fall („Gilt bei mir die Frist?“) werden dort nicht beantwortet; das wäre
Rechtsberatung, die nur zugelassene Personen erbringen dürfen. Wende dich
dafür an eine Fachanwältin, einen Fachanwalt oder eine Beratungsstelle.

Wenn dir die Mappe geholfen hat und du etwas zurückgeben willst, freut sich
der Autor über freiwillige Unterstützung unter https://github.com/sponsors/Cehha79. Kontakt: info@mika-tec.com.

## Impressum

Angaben gemäß § 5 DDG und § 18 MStV

Hasan Tepegöz, Einzelunternehmen MikaTec
Pontoiser Straße 54
71034 Böblingen
Deutschland

Telefon: 0173 5904496
E-Mail: info@mika-tec.com
Web: https://www.mika-tec.com

Kleinunternehmer gemäß § 19 UStG; es wird keine Umsatzsteuer ausgewiesen.
Verantwortlich im Sinne des § 18 Abs. 2 MStV: Hasan Tepegöz, Anschrift wie oben.
