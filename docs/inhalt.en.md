<p align="center">
<a href="../README.en.md"><img src="../bilder/reiter-start-en.svg" alt="Start"></a>
<a href="einrichten.en.md"><img src="../bilder/reiter-einrichten-en.svg" alt="Setup"></a>
<a href="ki.en.md"><img src="../bilder/reiter-ki-en.svg" alt="Working with your AI"></a>
<a href="inhalt.en.md"><img src="../bilder/reiter-inhalt-aktiv-en.svg" alt="What is inside (this page)"></a>
<a href="sicherheit.en.md"><img src="../bilder/reiter-sicherheit-en.svg" alt="Safety and limits"></a>
<a href="mitmachen.en.md"><img src="../bilder/reiter-mitmachen-en.svg" alt="Contributing and licence"></a>
</p>

<p align="center"><a href="inhalt.md">Deutsch</a> · <b>English</b></p>

<img src="../bilder/seite-inhalt-en.svg" width="100%" alt="4 · What is inside: Case folders · Tools · Templates · Fact sheets · Commands">

## Case folders

Every case gets the same folders so that references stay stable:

```text
02 Fälle/R-0001 Beispiel/
├─ akte.json          structured data: parties, documents, deadlines, tasks, drafts
├─ bestand.json       checksums of every file (written only by the service)
├─ JOURNAL.md         history, append only
├─ 01 Eingang/        new mail
├─ 02 Grundlagen/     contracts, notices, powers of attorney
├─ 03 Schriftverkehr/ one folder per party, plus proof of dispatch
├─ 04 Verfahren/      one folder per proceeding (action, fine, appeal …)
├─ 05 Beweise/        photos, lists, receipts
├─ 06 Entwürfe/       unsent texts, name ends with _ENTWURF
├─ 07 Recherche/      review memos, case-related legal sources
└─ 08 Archiv/         old overviews, unchanged
```

Originals in 02 to 05 and 08 are never changed, renamed or deleted; a hook
blocks that for the AI. New texts go to 06, memos to 07.

## Tools

<img src="../bilder/kapitel-werkzeuge-en.svg" alt="Tools: MCP and command line">

The same 26 tools are available over MCP (`06 Werkzeuge/dienst/mcp_server.py`)
and on the command line (`python3 "06 Werkzeuge/dienst/cli.py" <tool> field=value`).
Over MCP, writing tools run only with your confirmation (only the JSON value
`true` counts); on the command line the AI is told to ask first. Reading tools
never change a file: a new or moved file is only reported, it gets its ID
through `bestand_abgleichen`; the UI does that when you open a case. Every
change to `akte.json` is validated against the data model and saved with a revision.

<details>
<summary><b>All 26 tools</b></summary>

| Tool | Kind | Purpose |
|---|---|---|
| `faelle_auflisten` | reads | List all cases with id, title, area, status, number of documents, unregistered files and open tasks |
| `fall_uebersicht` | reads | Compact overview of one case: parties, proceedings, open deadlines and tasks, events, document list, unregistered files |
| `dokument_text` | reads | Text of one document (Word, e-mail, PDF, text, HTML) with its source: read directly, from the PDF text layer or not at all (scan, photo); the extract is derived, check figures and deadlines against the original |
| `dokumente_suchen` | reads | Full-text search in titles, metadata and document contents of a case |
| `frist_berechnen` | reads | Deadline end under §§ 187, 188, 193 BGB with the public holidays of a federal state; shows the calculation, does not decide which deadline applies |
| `beispiel_laden` | writes | Create the bundled sample case (fictional) as a new case |
| `bestand_pruefen` | reads | Compare checksums of all registered files of a case with their first state; also reports unregistered and moved files; writes nothing |
| `journal_lesen` | reads | Read the case journal, newest entries last |
| `quellen_katalog` | reads | Catalogue of official legal sources from 04 Rechtsquellen/Quellen.md |
| `rechtsinhalte_pruefen` | reads | Reports which bundled legal content is due for a new check against the official full text: fact sheets, holiday table, source catalogue; writes nothing, no network |
| `fall_anlegen` | writes | Create a new case with a fixed id and folder structure |
| `fall_status_setzen` | writes | Set case status to open, dormant or closed |
| `aufgabe_anlegen` | writes | Add a task to a case |
| `aufgabe_setzen` | writes | Mark a task done or open, optionally change due date or detail |
| `frist_eintragen` | writes | Enter a deadline or appointment; "confirmed" only with trigger, legal basis, calculation naming the end date, source and no open marker; confirmation carries review date and reviewer |
| `vorlagen_auflisten` | reads | List the letter templates under 05 Vorlagen/Schreiben with their first line |
| `vorlage_fuellen` | writes | Create a draft from a template in 06 Entwürfe with sender, signature, date and case id filled in; never overwrites; other placeholders stay to be filled |
| `ereignis_eintragen` | writes | Add an event to the case timeline |
| `notiz_anlegen` | writes | Add a note to a case |
| `entwurf_erfassen` | writes | Register a draft or a new version; with status "geprüft" or "versandt" the file is frozen as a read-only copy under 06 Entwürfe/Fassungen with checksum and its own id |
| `bestand_abgleichen` | writes | Sync the inventory of a case with its files: new files get an id, moved files are found by checksum; the only way new files are registered |
| `dokument_ordnen` | writes | Change metadata of a document (title, date, kind, state, topics, exhibit, persons, references, note, reading quality); the file stays untouched |
| `dokument_verschieben` | writes | File a document into another section; id and content stay, nothing is overwritten |
| `journal_schreiben` | writes | Append an entry to the case journal |
| `sicherung_erstellen` | writes | Create a verified ZIP backup of the whole folder, with a copy to the second target |
| `sicherung_probe` | writes | Restore test: extract the last backup into a scratch folder, check case files against the schema and all files against their checksums, remove the scratch folder |

</details>

## Templates

<img src="../bilder/kapitel-vorlagen-en.svg" alt="Templates: letters with placeholders">

Templates under `05 Vorlagen/Schreiben/` (German): internal notes on top
(deadline, form, addressee), the text to send below the separator with
placeholders 【 】. `.claude/recht/werkzeuge/docx_erzeugen.py` turns a draft
into a `.docx` and warns about open placeholders and markers.

<details>
<summary><b>All 10 templates</b></summary>

| Template | Purpose |
|---|---|
| `Akteneinsicht.md` | Request for access to files at an authority, court or employer with selectable legal basis |
| `Auskunft_DSGVO.md` | Data access request under Art. 15 GDPR |
| `Briefkopf.md` | Skeleton for any letter: sender, recipient, date, subject |
| `Einspruch_Bussgeldbescheid.md` | Objection to an administrative fine notice, with request for file access |
| `Einspruch_Steuerbescheid.md` | Objection to a tax assessment, with optional suspension of enforcement |
| `Fristsetzung.md` | Demand with a deadline (performance, payment, reply) |
| `Klage_Arbeitsgericht.md` | Labour court action, skeleton with motions and exhibits |
| `Klage_Zivilgericht.md` | Civil action before the local or regional court, payment claim with interest, default judgment, jurisdiction |
| `Strafanzeige.md` | Criminal complaint with or without formal request for prosecution, facts, evidence, request for confirmation |
| `Widerspruch_Bescheid.md` | Administrative appeal against an authority decision |

</details>

## Fact sheets

<img src="../bilder/kapitel-merkblaetter-en.svg" alt="Fact sheets: procedures, full text">

Fact sheets under `04 Rechtsquellen/Verfahren/` (German) describe per
remedy the deadline, form, mandatory content, addressee and effect, every
item with its provision and a check date. `/fallaufnahme` names the remedy
from them, `/entwurf` checks the mandatory content against them.

<details>
<summary><b>All 10 fact sheets with check date</b></summary>

| Fact sheet | Content | Last full check |
|---|---|---|
| `04 Rechtsquellen/Verfahren/Akteneinsicht.md` | Access to files and data: which legal basis applies (VwVfG, SGB X, AO, StPO, OWiG, ZPO, BetrVG, GDPR, IFG) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Dienstaufsichtsbeschwerde.md` | Complaint to a supervisor, supervisory complaint, petition (Art. 17 GG, DRiG, BRAO) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Einspruch_Bussgeldbescheid.md` | Objection to an administrative fine notice (OWiG, StVG) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Einspruch_Steuerbescheid.md` | Objection to a tax assessment (Abgabenordnung) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Klage_Arbeitsgericht.md` | Action before the labour court (ArbGG, ZPO, KSchG, GKG) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Mahnverfahren.md` | Order-for-payment procedure: payment order and enforcement order (ZPO, GKG) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Strafanzeige.md` | Criminal complaint and request for prosecution (StPO, StGB) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Widerspruch_Verwaltungsakt.md` | Administrative appeal against an authority decision (VwGO) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Zivilklage.md` | Civil action before the local or regional court (ZPO, GVG, GKG, BGB) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Zustaendigkeit_finden.md` | Finding the competent court or authority: rules and official directories | 17.09.2026 |

</details>

> [!NOTE]
> Legal content ages. Which holidays, fact sheets and templates ship with
> which status, when and how to check them, is documented in
> [`DOKU/md/Rechtsinhalte.md`](../DOKU/md/Rechtsinhalte.md) (German). Before
> use in a case the provision in the official full text prevails, not the
> fact sheet.

## Commands

<img src="../bilder/kapitel-befehle-en.svg" alt="Commands: without the UI">

<details>
<summary><b>Commands without the UI</b></summary>

| Command (inside the folder) | Purpose |
|---|---|
| `Start.command`, `Start.sh`, `Start.bat` | start the service and open the UI (macOS, Linux, Windows) |
| `python "06 Werkzeuge/einrichten_windows.py"` | Windows only: replace `python3` with `python` in `.mcp.json`, `.claude/settings.json`, `.codex/config.toml` (`Start.bat` does this itself); `--pruefen` report only |
| `python3 "06 Werkzeuge/dienst/server.py" --no-open` | start without a browser; `--check` verify all cases; `--backup` verified backup; `--probe` restore test of the last backup; `--restore <ZIP> <new folder>` extract a backup into a new folder and verify it |
| `python3 "06 Werkzeuge/dienst/cli.py" liste` | list all tools with parameters; then `cli.py <tool> field=value` |
| `python3 "06 Werkzeuge/dienst/cli.py" frist_berechnen start=2026-09-11 menge=1 einheit=monate land=BW` | calculate a deadline, with the calculation shown |
| `python3 "06 Werkzeuge/dienst/cli.py" rechtsinhalte_pruefen` | which fact sheets, holidays and sources are due for a new check against the full text |
| `python3 "06 Werkzeuge/akte_schema.py" "02 Fälle/<case>/akte.json"` | validate a case file against the data model |
| `python3 "06 Werkzeuge/dienst/cli.py" vorlage_fuellen fall=R-0001 vorlage=Widerspruch_Bescheid` | create a draft from a template under 06 Entwürfe, with sender (settings or the party with role "Ich"), signature and date; `vorlagen_auflisten` lists the names |
| `python3 ".claude/recht/werkzeuge/docx_erzeugen.py" <draft.md>` | Word file from a draft, with a pre-check report (open markers, placeholders, header lines, attachments); `--pruefen` report only |
| `python3 ".claude/recht/werkzeuge/uebergabe_paket.py" R-0001 --empfaenger anwalt --vorschau` | hand-over package per recipient (anwalt: everything; gericht, behoerde, gegenseite, beratung: only `--nur D0001,D0002`), preview first, then without `--vorschau` as a verified ZIP with manifest outside the folder |
| `python3 "06 Werkzeuge/verteilen.py"` | generate `AGENTS.md` and `.agents/skills/` from `CLAUDE.md` and `.claude/skills/`; `--pruefen` compare only |
| `python3 "06 Werkzeuge/dienst/pruefen.py"` | functional test with artificial cases in a temp folder |

</details>

---

<p align="center">
← <a href="ki.en.md">3 · Working with your AI</a> · <a href="sicherheit.en.md">5 · Safety and limits</a> →<br>
<sub><a href="../README.en.md#legal-notice-impressum">Legal notice</a> · <a href="../LICENSE">Licence AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Contribute</a></sub>
</p>
