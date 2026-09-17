<p align="center"><img src="bilder/banner.svg" alt="AKA Recht" width="100%"></p>

<p align="center">
<img src="bilder/abzeichen-preis.svg" alt="free">
<img src="bilder/abzeichen-lizenz.svg" alt="licence AGPL-3.0">
<img src="bilder/abzeichen-python.svg" alt="Python 3, no third-party packages">
<img src="bilder/abzeichen-lokal.svg" alt="runs locally, no network">
<img src="bilder/abzeichen-recht.svg" alt="law: Germany">
</p>

<p align="center">
<a href="README.en.md"><img src="bilder/reiter-start-aktiv-en.svg" alt="Start (this page)"></a>
<a href="docs/einrichten.en.md"><img src="bilder/reiter-einrichten-en.svg" alt="Setup"></a>
<a href="docs/ki.en.md"><img src="bilder/reiter-ki-en.svg" alt="Working with your AI"></a>
<a href="docs/inhalt.en.md"><img src="bilder/reiter-inhalt-en.svg" alt="What is inside"></a>
<a href="docs/sicherheit.en.md"><img src="bilder/reiter-sicherheit-en.svg" alt="Safety and limits"></a>
<a href="docs/mitmachen.en.md"><img src="bilder/reiter-mitmachen-en.svg" alt="Contributing and licence"></a>
</p>

<p align="center"><a href="README.md">Deutsch</a> · <b>English</b> · <a href="CONTRIBUTING.md">Contribute</a> · <a href="https://github.com/sponsors/Cehha79">Support</a></p>

# AKA Recht

A parking ticket, a dismissal, a service-charge statement, a notice from the
authorities: sooner or later everyone has a legal matter, and then letters,
photos, e-mails and deadlines are scattered everywhere. **AKA Recht** is the
folder where all of it has its place, and the set of guides with which your
AI helps you to organise, check and formulate.

- **Every matter is a case** with a fixed id, fixed folders, structured data in
  `akte.json` and a journal. Originals are never changed.
- **Deadlines with a calculation:** every deadline shows trigger, legal basis and
  the calculation under §§ 187, 188, 193 BGB with the holidays of your state.
- **Your AI works with it:** Claude Code, Claude Desktop, Codex or any other
  that speaks MCP (Model Context Protocol) or can run commands. 7 guides
  take it from case intake to a reviewed draft, 26 tools let it read
  the case and, after your confirmation, write to it.
- **Everything stays with you:** no AI inside the app, no account, no key, no
  network. The service runs only on your machine.

> [!TIP]
> To try it out there is a fictional sample case (dismissal by the employer).
> Click **"Beispielfall laden"** in the UI, then browse case, documents,
> deadlines and draft. Delete it whenever you like.

Product version 0.2 of 17.09.2026 · data format `akte.json` schema 1 · MCP protocol 2026-07-28 and 2025-11-25 · tested with Python 3.14.7 on macOS 26.7, Ubuntu 24.04 (Python 3.12) and Windows 11 (Python 3.14) · Author: Hasan Tepegöz

## Download

| Way | How |
|---|---|
| Fixed version | On the [release page](https://github.com/Cehha79/aka-recht/releases/latest) download "Source code (zip)" and extract it. |
| Latest state | `git clone https://github.com/Cehha79/aka-recht` or on GitHub "Code", "Download ZIP". |

Then continue with **[Setup](docs/einrichten.en.md)**: requirements, first start
per system, connecting an AI. To pass it on, share the GitHub link and do not
re-pack the folder yourself (the reason is under Setup).

## What it looks like

Click to enlarge. All pictures show the fictional sample case ("Max Muster"
v. "Muster Logistik GmbH"), no real persons. The UI is in German.

<table>
<tr>
<td width="50%"><a href="bilder/01-zentrale.jpg"><img src="bilder/01-zentrale.jpg" alt="Dashboard"></a><br><sub><b>Dashboard:</b> all cases, next deadlines, inbox</sub></td>
<td width="50%"><a href="bilder/02-fallakte.jpg"><img src="bilder/02-fallakte.jpg" alt="Case file"></a><br><sub><b>Case file:</b> role, goal, proceedings, deadlines, tasks</sub></td>
</tr>
<tr>
<td width="50%"><a href="bilder/03-dokumente.jpg"><img src="bilder/03-dokumente.jpg" alt="Documents"></a><br><sub><b>Documents:</b> preview, id, exhibit number, filing</sub></td>
<td width="50%"><a href="bilder/04-fristen.jpg"><img src="bilder/04-fristen.jpg" alt="Deadlines"></a><br><sub><b>Deadlines:</b> legal basis, calculation, check status</sub></td>
</tr>
</table>

The UI has a **dashboard** (overview, all cases, inbox, deadlines of all
cases, legal sources, inventory and backup, settings, manual) and per case a
**case file** (overview, documents with preview, parties, proceedings,
timeline, deadlines with calculator, tasks, drafts, evidence and exhibits,
journal). It is plain HTML, CSS and JavaScript without a framework and needs
no outside access.

> [!WARNING]
> **Not a lawyer, no legal advice.** What the folder does and does not do is
> described under [Safety and limits](docs/sicherheit.en.md#limits).


---

<p align="center">
<a href="docs/einrichten.en.md">2 · Setup</a> →<br>
<sub><a href="README.en.md#legal-notice-impressum">Legal notice</a> · <a href="LICENSE">Licence AGPL-3.0</a> · <a href="CONTRIBUTING.md">Contribute</a></sub>
</p>

## Legal notice (Impressum)

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
