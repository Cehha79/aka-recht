<p align="center"><img src="bilder/banner.svg" alt="AKA Recht: Deine Aktenmappe für Rechtssachen" width="100%"></p>

<p align="center">
<img src="bilder/abzeichen-preis.svg" alt="kostenlos">
<img src="bilder/abzeichen-lizenz.svg" alt="Lizenz AGPL-3.0">
<img src="bilder/abzeichen-python.svg" alt="Python 3, keine Fremdpakete">
<img src="bilder/abzeichen-lokal.svg" alt="läuft lokal, ohne Netz">
<img src="bilder/abzeichen-recht.svg" alt="Recht: Deutschland">
</p>

<p align="center">
<a href="README.md"><img src="bilder/reiter-start-aktiv.svg" alt="Start (diese Seite)"></a>
<a href="docs/einrichten.md"><img src="bilder/reiter-einrichten.svg" alt="Einrichten"></a>
<a href="docs/ki.md"><img src="bilder/reiter-ki.svg" alt="Mit der KI arbeiten"></a>
<a href="docs/inhalt.md"><img src="bilder/reiter-inhalt.svg" alt="Inhalt der Mappe"></a>
<a href="docs/sicherheit.md"><img src="bilder/reiter-sicherheit.svg" alt="Sicherheit und Grenzen"></a>
<a href="docs/mitmachen.md"><img src="bilder/reiter-mitmachen.svg" alt="Mitmachen und Lizenz"></a>
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
  die MCP (Model Context Protocol) oder Befehle ausführen kann. 7 Anleitungen
  führen sie von der Fallaufnahme bis zum geprüften Entwurf, 26 Werkzeuge
  lassen sie in der Akte lesen und, nach deiner Bestätigung, schreiben.
- **Alles bleibt bei dir:** keine KI in der App, kein Konto, kein Schlüssel,
  kein Netz. Der Dienst läuft nur auf deinem Rechner.

> [!TIP]
> Zum Ausprobieren gibt es einen erfundenen Beispielfall (Kündigung durch den
> Arbeitgeber). In der Oberfläche auf **„Beispielfall laden“** klicken, dann
> durch Akte, Dokumente, Fristen und Entwurf klicken. Jederzeit löschbar.

Produkt Version 0.2 vom 17.09.2026 · Datenformat `akte.json` Schema 1 · MCP-Protokoll 2026-07-28 und 2025-11-25 · geprüft mit Python 3.14.7 auf macOS 26.7, Ubuntu 24.04 (Python 3.12) und Windows 11 (Python 3.14) · Autor: Hasan Tepegöz

## Herunterladen

| Weg | So geht es |
|---|---|
| Feste Version | Auf der [Release-Seite](https://github.com/Cehha79/aka-recht/releases/latest) das Archiv „Source code (zip)“ laden und entpacken. |
| Neuester Stand | `git clone https://github.com/Cehha79/aka-recht` oder oben auf GitHub „Code“, „Download ZIP“. |

Danach weiter mit **[Einrichten](docs/einrichten.md)**: Voraussetzungen, erster
Start je System, KI anbinden. Zum Weitergeben den GitHub-Link teilen und den
Ordner nicht selbst neu packen (warum, steht unter Einrichten).

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

Die Oberfläche hat eine **Zentrale** (Übersicht, alle Fälle, Posteingang,
Fristen aller Fälle, Rechtsquellen, Bestand und Sicherung, Einstellungen,
Anleitung) und je Fall eine **Fallakte** (Übersicht, Dokumente mit Vorschau,
Beteiligte, Verfahren, Chronologie, Fristen mit Rechner, Aufgaben, Entwürfe,
Beweise und Anlagen, Journal). Sie ist reines HTML, CSS und JavaScript ohne
Framework und braucht keinen Zugang nach außen.

> [!WARNING]
> **Kein Rechtsanwalt, keine Rechtsberatung.** Was die Mappe kann und was
> nicht, steht unter [Sicherheit und Grenzen](docs/sicherheit.md#grenzen).


---

<p align="center">
<a href="docs/einrichten.md">2 · Einrichten</a> →<br>
<sub><a href="README.md#impressum">Impressum</a> · <a href="LICENSE">Lizenz AGPL-3.0</a> · <a href="CONTRIBUTING.md">Mitmachen</a></sub>
</p>

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
