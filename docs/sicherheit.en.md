<p align="center">
<a href="../README.en.md"><img src="../bilder/reiter-start-en.svg" alt="Start"></a>
<a href="einrichten.en.md"><img src="../bilder/reiter-einrichten-en.svg" alt="Setup"></a>
<a href="ki.en.md"><img src="../bilder/reiter-ki-en.svg" alt="Working with your AI"></a>
<a href="inhalt.en.md"><img src="../bilder/reiter-inhalt-en.svg" alt="What is inside"></a>
<a href="sicherheit.en.md"><img src="../bilder/reiter-sicherheit-aktiv-en.svg" alt="Safety and limits (this page)"></a>
<a href="mitmachen.en.md"><img src="../bilder/reiter-mitmachen-en.svg" alt="Contributing and licence"></a>
</p>

<p align="center"><a href="sicherheit.md">Deutsch</a> · <b>English</b></p>

<img src="../bilder/seite-sicherheit-en.svg" width="100%" alt="5 · Safety and limits: Guarantees · Backup · Scope · Limits">

## What you can rely on

A legal file needs more than folders. The folder enforces these rules in
code and checks them in the test suite:

- **Reading stays reading.** No reading tool touches `akte.json`,
  `bestand.json` or `zentrale.json`. New files are registered only by the
  sync tool.
- **IDs never come back.** A counter per ID type remembers the highest
  number ever issued; a removed entry is never replaced by a new one with
  the same ID, so journal references stay unambiguous.
- **Reviewed and sent versions are frozen.** With status "geprüft" or
  "versandt" the folder stores a read-only copy under
  `06 Entwürfe/Fassungen/` with checksum and its own ID. The working file
  may change, the copy never does.
- **Deadlines are recalculated.** §§ 187, 188, 193 BGB with the calculation
  shown; month ends, leap years and one-year periods are covered by 20 edge
  cases. Whether a deadline applies is not decided by the calculator.
- **Confirmed means checked.** A deadline is only "bestätigt" when the
  calculation names the end date, evidence and trigger are present and no
  `[PRÜFEN]`, `[QUELLE]` or `[BELEG]` marker is open; the confirmation carries
  review date and reviewer, and an appointment needs the summons as source.
- **Foreign attachments do not run.** "Öffnen" calls the system program only
  for known document formats (PDF, text, office, images, e-mail, audio,
  video); scripts, programs, web pages, archives and unknown types are only
  shown in the file manager, with a note.
- **Uncertainty stays visible.** An event can be "approximate", "period" or
  "unknown" instead of carrying an invented day; a deadline names its
  proceeding and its triggering event, and it is not confirmed on an
  uncertain event.
- **Hand-overs contain only what should go out.** The package is built for a
  named recipient, previews every file, aborts on unknown IDs and is read
  back against its manifest.
- **Backups are provably usable.** Every ZIP is read back after writing;
  "Wiederherstellung prüfen" extracts it into a scratch folder and checks
  case files and checksums.
- **Data stays where you put it.** No AI inside the folder, no network in
  the service. What you back up to a cloud folder is uploaded by your
  system; what your AI reads is processed by its provider.

## Backup

"Geprüfte Sicherung erstellen" in the UI writes a ZIP outside the folder
and reads it back. Target and second target are in the settings and are
shown before the first backup. "Wiederherstellung prüfen" extracts the last
backup into a scratch folder, checks case files and checksums, then removes
the scratch folder. A real restore always goes into a new folder, never over
the running one: `python3 "06 Werkzeuge/dienst/server.py" --restore <ZIP> <new folder>`.
Without the UI: `--check` verifies the inventory, `--backup` backs up,
`--probe` tests the last backup.

Three levels that are not the same: the folder lives on your computer. If a
backup target is in iCloud Drive or another cloud folder, the operating
system uploads the unencrypted ZIP there. And whatever your AI reads is
processed by its provider under its terms; a local MCP server does not change that.

## Scope

This edition is built for German law: deadline calculator under §§ 187, 188,
193 BGB with the state-wide public holidays of all 16 federal states (choose
the state in the settings; regional holidays of single municipalities do not
count, one-off holidays such as Berlin 2025 and 2028 are included), a
catalogue of official German sources, letter templates and fact sheets for
German procedures.

Further jurisdictions are planned, in this order: Austria, Switzerland,
Turkey, then England and Wales, France, USA, China, Russia and more. Until
then the folder can be used elsewhere to organise documents, but deadlines
and templates apply to Germany only.

The UI, templates, manual and skills are currently German only. Further
languages are planned, Turkish first, then English.

## Limits

> [!WARNING]
> The folder is not a lawyer and gives no legal advice. It helps you to
> organise, check and formulate: it files documents, calculates deadlines
> under §§ 187, 188, 193 BGB with a visible calculation, records what is
> proven and what is not, and gives your AI guides for facts, research,
> drafts and adversarial review. Whether a deadline applies, whether a letter
> can go out like this and what to do is for you or a qualified lawyer to
> decide. The author does not know or review any user's matter; everything
> runs on your machine, and what your AI makes of the guides happens in your
> own matter and on your own responsibility.

---

<p align="center">
← <a href="inhalt.en.md">4 · What is inside</a> · <a href="mitmachen.en.md">6 · Contributing and licence</a> →<br>
<sub><a href="../README.en.md#legal-notice-impressum">Legal notice</a> · <a href="../LICENSE">Licence AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Contribute</a></sub>
</p>
