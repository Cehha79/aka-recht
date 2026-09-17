<p align="center">
<a href="../README.en.md"><img src="../bilder/reiter-start-en.svg" alt="Start"></a>
<a href="einrichten.en.md"><img src="../bilder/reiter-einrichten-aktiv-en.svg" alt="Setup (this page)"></a>
<a href="ki.en.md"><img src="../bilder/reiter-ki-en.svg" alt="Working with your AI"></a>
<a href="inhalt.en.md"><img src="../bilder/reiter-inhalt-en.svg" alt="What is inside"></a>
<a href="sicherheit.en.md"><img src="../bilder/reiter-sicherheit-en.svg" alt="Safety and limits"></a>
<a href="mitmachen.en.md"><img src="../bilder/reiter-mitmachen-en.svg" alt="Contributing and licence"></a>
</p>

<p align="center"><a href="einrichten.md">Deutsch</a> · <b>English</b></p>

<img src="../bilder/seite-einrichten-en.svg" width="100%" alt="2 · Setup: Requirements · First start · Connecting an AI · Updating · FAQ">

## Requirements

- Python 3, tested with 3.14.7 (`python3 --version`); older versions are
  untested. No other packages.
- Tested on 17 Sep 2026 on macOS, on Ubuntu 24.04 with Python 3.12 and on
  Windows 11 with Python 3.14: test suite, service via the start script, MCP
  server, sample case in a folder with umlauts on each.
- Optional for text extraction from PDF: the program `pdftotext` (poppler).
  Scanned PDFs without a text layer are not read; that needs text recognition
  (OCR) outside the folder.

<details>
<summary><b>macOS</b></summary>

- Start with `Start.command` (double-click).
- Do not re-pack the folder with `zip` or `ditto`: those archives carry no
  UTF-8 flag, and depending on the extractor "06 Entwürfe" turns into a
  broken folder name (tested 17 Sep 2026 with Python; Finder not tested, so
  avoid it too). The GitHub ZIP is clean.

</details>

<details>
<summary><b>Linux</b></summary>

- Start with `Start.sh`.
- Tested on Ubuntu 24.04 with Python 3.12; `xdg-open` serves as file manager.

</details>

<details>
<summary><b>Windows</b></summary>

- Start with `Start.bat` (double-click).
- On Windows the command is `python` instead of `python3`; `python3.exe` there
  is only a Microsoft Store stub. `Start.bat` therefore switches `.mcp.json`,
  `.claude/settings.json` and `.codex/config.toml` to `python` on every start
  (`06 Werkzeuge/einrichten_windows.py`; it changes only that one value and
  nothing once set up). So run `Start.bat` once before using Claude Code or
  Codex in the folder. If you use git, these three files then show as modified.
- Windows does not ship `pdftotext` (it was missing on the Windows 11 test
  machine); without it the folder reports the text source "werkzeug-fehlt"
  for PDFs and extracts no text.

</details>

## First start

1. Get it: `git clone https://github.com/Cehha79/aka-recht` or on GitHub "Code", "Download ZIP" and extract;
   put the folder wherever you like. To pass it on, share the GitHub link and
   do not re-pack the folder yourself (see macOS above).
2. Start: macOS `Start.command`, Linux `Start.sh`, Windows `Start.bat`. The
   service binds to 127.0.0.1 only and your default browser opens the UI.
   `zentrale.json` is created on first start.
3. Under "Einstellungen" enter your sender details (name, address, contact);
   they stay in `zentrale.json` on your computer and later fill "Von:" and
   the signature in drafts made from the templates.
4. In the UI create a new case ("Neuer Fall"), put mail into `01 Eingang` or
   add it under "Dokumente", file it, calculate deadlines, keep the journal.
5. Read the "Anleitung" page in the UI; it also explains how to connect an AI.

## Connecting an AI

<details open>
<summary><b>Claude Code</b></summary>

Start a session in the folder; `.mcp.json` is included; confirm the dialog;
check with `/mcp`. Skills under `.claude/skills/` (`/fallaufnahme`,
`/fristencheck`, `/entwurf` …), hooks from `.claude/settings.json`.

</details>

<details>
<summary><b>Codex</b></summary>

- Option A: once `codex mcp add aka-recht -- python3 "<full path>/06 Werkzeuge/dienst/mcp_server.py"`.
- Option B without that entry: mark the project folder as trusted in
  `~/.codex/config.toml` (`[projects."<full path to the project folder>"]` with
  `trust_level = "trusted"`); Codex then loads the bundled
  `.codex/config.toml`; an entry for a parent folder is not enough.
- Check inside the project folder with `codex mcp list`. On Windows use
  `python` instead of `python3`. Skills under `.agents/skills/` (`$fristencheck` …).

</details>

<details>
<summary><b>Claude Desktop</b></summary>

Settings, Developer, edit config: entry `aka-recht` with `command` `python3`
(on Windows `python`) and `args` `["<full path>/06 Werkzeuge/dienst/mcp_server.py"]`;
restart Claude Desktop.

</details>

<details>
<summary><b>Other assistants</b></summary>

- With MCP: the same call in the assistant's configuration file; work profile
  in `AGENTS.md`.
- Without MCP, with commands: `python3 "06 Werkzeuge/dienst/cli.py" liste`.
- ChatGPT in the browser or app does not start a local server; it requires a
  public HTTPS address or a tunnel through OpenAI. That is not intended for
  AKA Recht.

</details>

Writing tools only run when you confirm the call. There are no tools for
sending, deleting or changing originals.

## Updating

Your own data lives in `01 Eingang`, `02 Fälle`, `03 Verträge und Vorsorge`
and `zentrale.json`. Make a backup before every update ("Geprüfte Sicherung
erstellen" in the UI).

<details open>
<summary><b>With git</b></summary>

Inside the folder run `git pull`. The four places holding your data are listed
in the bundled `.gitignore`; git leaves them alone. On Windows `Start.bat` has
changed three configuration files; if `git pull` stops because of them, first
run `git checkout -- .mcp.json .claude/settings.json .codex/config.toml`
(this only discards that switch; `Start.bat` sets it again on the next start).

</details>

<details>
<summary><b>With a new ZIP</b></summary>

1. Extract the new version into a new folder.
2. Stop the running service. There is no button for it: restart the computer,
   or on macOS and Linux run `pkill -f "06 Werkzeuge/dienst/server.py"` in a terminal
   (this stops every running folder service on this computer).
3. Move `01 Eingang`, `02 Fälle`, `03 Verträge und Vorsorge` and
   `zentrale.json` from the old folder into the new one; remove the empty
   folders of the new one first.
4. Start inside the new folder. Cases and settings are back; the paths in
   `zentrale.json` are relative to the folder.
5. If you set up Codex or Claude Desktop with the full path to
   `mcp_server.py`, change that path to the new folder.

</details>

## FAQ

<details>
<summary><b>Do I need an account or internet access?</b></summary>

Not for the folder: the service binds to 127.0.0.1 only and calls no outside
addresses. Your AI (Claude, Codex or another) needs its own account and
access; whatever it reads is processed by its provider.

</details>

<details>
<summary><b>Which AI can I use?</b></summary>

Tested are Claude Code, Claude Desktop and Codex (see "Connecting an AI").
Any other AI that speaks MCP or may run commands should work but is untested.
ChatGPT in the browser or app is not intended because it starts no local server.

</details>

<details>
<summary><b>Do my cases end up on GitHub?</b></summary>

No. The folder uploads nothing. If you use git yourself: `01 Eingang`,
`02 Fälle`, `03 Verträge und Vorsorge` and `zentrale.json` are in the
`.gitignore` and are not tracked. If a backup target is in a cloud folder,
your system uploads the backup there.

</details>

<details>
<summary><b>Can the folder read scanned letters?</b></summary>

Only if the PDF has a text layer and `pdftotext` is installed. Photos and
scans without a text layer are not read; the tool `dokument_text` then says
honestly that no text was read. Text recognition is planned.

</details>

<details>
<summary><b>Does it work for Austria, Switzerland or Turkey?</b></summary>

Not yet. Deadline calculator, fact sheets and templates apply to German law
only. More countries are planned, see [Scope](sicherheit.en.md#scope).

</details>

<details>
<summary><b>Will anyone here answer questions about my case?</b></summary>

No. Issues and discussions are for the software only. For your case ask a
qualified lawyer or an advice centre.

</details>

---

<p align="center">
← <a href="../README.en.md">1 · Start</a> · <a href="ki.en.md">3 · Working with your AI</a> →<br>
<sub><a href="../README.en.md#legal-notice-impressum">Legal notice</a> · <a href="../LICENSE">Licence AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Contribute</a></sub>
</p>
