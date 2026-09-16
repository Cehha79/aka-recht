# AKA Recht

A local case folder for legal matters of every kind (employment, traffic,
tenancy, contracts, public authorities, criminal matters and more). Every
matter is a case with a fixed ID, fixed folders, structured data in
`akte.json` and a journal. You work with it through a browser interface and
through the AI you already have: Claude Code, Claude Desktop, Codex or any
other assistant that speaks MCP (Model Context Protocol) or can run commands.
The folder itself contains no AI, needs no account, no API key and no
network.

Version 0.1 · as of 16.09.2026 · Author: Hasan Tepegöz · Deutsch: [README.md](README.md)

Note: the interface, templates, guides and skills are in German, and the
folder is built for German law (see Scope). This file only translates the
overview.

## What it looks like

All pictures show the invented sample case R-9001 (speeding fine, "Max
Muster"). No real persons.

![Home: all cases, deadlines, inbox](bilder/01-zentrale.jpg)

![Case file: role, goal, proceedings, next deadlines and tasks](bilder/02-fallakte.jpg)

![Documents with preview, ID and exhibit number](bilder/03-dokumente.jpg)

![Deadlines with legal basis, calculation and check status](bilder/04-fristen.jpg)

## What your AI can do with it

The folder ships with guides (skills) that tell your AI how to work a case.
In Claude Code you call them with `/name`, in Codex with `$name`:

| Call | What happens |
|---|---|
| `fallaufnahme` | Case intake: role, goal, area of law, parties, receipt dates, missing facts; writes to the case file |
| `sachverhalt` | Statement of facts: timeline and evidence table from the originals, with a source for every statement |
| `recherche-de` | Legal research on the original full text, version and period of validity, sources into the case |
| `fristencheck` | Deadlines with trigger, receipt, legal basis and a visible calculation |
| `entwurf` | Letters and pleadings from the templates, with evidence from the case, as Markdown and Word |
| `gegenpruefung` | Adversarial review: counter-arguments, unsupported claims, wrong citations, figures, exhibits |
| `uebergabe` | Hand-over package for a lawyer, authority or court as a ZIP |

The guides set the standard of care: every legal statement names the
provision with paragraph and act, or the decision with court, date and
docket number, read in the full text; anything unverified stays visible as
`[PRÜFEN]`, `[QUELLE]` or `[BELEG]`; the other side is always considered.
Every draft stays a draft until you check it and send it yourself.

## Scope

This version is built for German law: deadline calculator under §§ 187,
188, 193 BGB with the public holidays of Baden-Württemberg, a catalogue of
official German legal sources, templates for German proceedings. Other
jurisdictions are planned, in this order: Austria, Switzerland, France,
England and Wales, Turkey, USA, China, Russia and more. Until then you can
use the folder elsewhere to organise documents, but deadlines and templates
apply to Germany only. Further languages are planned along with the
countries.

## Requirements

- Python 3 (`python3 --version`), no other packages.
- Built and tested on macOS. Linux and Windows: start scripts are included
  and the service uses only the standard library, but it has not been
  tested there yet. On Windows the command is usually `python`, not
  `python3`; then replace `python3` with `python` in `.mcp.json` and
  `.claude/settings.json`.
- Optional for text extraction from PDF: `pdftotext` (package poppler).

## First start

1. Put the folder wherever you like.
2. Start it: macOS double-click `Start.command`, Linux run `Start.sh`,
   Windows double-click `Start.bat`. The service binds to 127.0.0.1 only
   and your default browser opens the interface. `zentrale.json` is created
   on first start.
3. In the interface: "Neuer Fall" (new case), put mail into `01 Eingang` or
   add it under "Dokumente", sort it, calculate deadlines, keep the journal.
4. Read the "Anleitung" page in the interface; it also explains how to
   connect an AI.

## Connecting an AI

| Assistant | What to do |
|---|---|
| Claude Code | Start a session in the folder; `.mcp.json` is included; confirm the dialog; check with `/mcp`. Skills live in `.claude/skills/`. |
| Codex | Once: `codex mcp add aka-recht -- python3 "<full path>/06 Werkzeuge/dienst/mcp_server.py"`; skills in `.agents/skills/` (`$fristencheck` …). |
| Claude Desktop | Settings, Developer, Edit Config: entry `aka-recht` with `command` `python3` and `args` `["<full path>/06 Werkzeuge/dienst/mcp_server.py"]`; restart Claude Desktop. |
| others with MCP | same call in the assistant's configuration file. |
| without MCP, with commands | `python3 "06 Werkzeuge/dienst/cli.py" liste` |

Writing tools run only after you confirm the call. There are no tools for
sending, deleting or changing originals.

## Limits

The folder is not a lawyer and gives no legal advice. It helps you organise,
check and draft: it sorts documents, calculates deadlines with a visible
calculation, records what is proven and what is not, and guides your AI
through facts, research, drafts and review. Whether a deadline applies,
whether a letter can go out and what to do is for you or a qualified
lawyer to decide. The author does not know or review any user's matter;
everything runs on your machine, and what your AI makes of the guides
happens in your own matter and on your own responsibility.

## Backup

"Geprüfte Sicherung erstellen" in the interface writes a ZIP outside the
folder and reads it back. Target and second target are in the settings.
Check without the interface: `python3 "06 Werkzeuge/dienst/server.py" --check`.

## Licence

Copyright 2026 Hasan Tepegöz. Free software under the GNU Affero
General Public License, version 3 (AGPL-3.0), full text in `LICENSE`.
In plain words: use, copy, change and share it freely, privately or at
work; if you distribute a changed version or offer it as a network service,
you must provide the complete source under the same licence; keep the
licence text and copyright notices; no warranty, no liability as far as the
law allows. The English text in `LICENSE` is the only binding one.

## Contributing and supporting

The folder is free and developed in the open. Bug reports, suggestions,
public holidays of other German states, translations, templates and later
whole country packages are welcome. Please never submit real case files,
names or docket numbers. Contributions are licensed under AGPL-3.0. How to
contribute: `CONTRIBUTING.md` (German).

Issues and discussions are for the software only. Questions about a real
case ("does this deadline apply to me?") will not be answered there; that
would be legal advice, which only admitted persons may give. Please turn to
a lawyer or an advice centre.

If the folder helped you and you want to give something back, the author
welcomes voluntary support unter https://github.com/sponsors/Cehha79. Contact: info@mika-tec.com.

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
