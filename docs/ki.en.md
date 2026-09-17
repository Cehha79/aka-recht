<p align="center">
<a href="../README.en.md"><img src="../bilder/reiter-start-en.svg" alt="Start"></a>
<a href="einrichten.en.md"><img src="../bilder/reiter-einrichten-en.svg" alt="Setup"></a>
<a href="ki.en.md"><img src="../bilder/reiter-ki-aktiv-en.svg" alt="Working with your AI (this page)"></a>
<a href="inhalt.en.md"><img src="../bilder/reiter-inhalt-en.svg" alt="What is inside"></a>
<a href="sicherheit.en.md"><img src="../bilder/reiter-sicherheit-en.svg" alt="Safety and limits"></a>
<a href="mitmachen.en.md"><img src="../bilder/reiter-mitmachen-en.svg" alt="Contributing and licence"></a>
</p>

<p align="center"><a href="ki.md">Deutsch</a> · <b>English</b></p>

<img src="../bilder/seite-ki-en.svg" width="100%" alt="3 · Working with your AI: Workflow · Skills · Hooks">

## How your AI works with the folder

The folder contains no AI. It ships with guides (skills) that tell your own
AI how to work a case, and tools with which it reads the case and, after your
confirmation, writes to it. Blue is the AI, green is you:

<picture>
<source media="(prefers-color-scheme: dark)" srcset="../bilder/ablauf-dunkel-en.svg">
<img src="../bilder/ablauf-hell-en.svg" width="100%" alt="Workflow: a letter, notice or contract goes into /fallaufnahme; then /sachverhalt and /fristencheck; both lead to /recherche-de; then /entwurf and /gegenpruefung; finally you check and send, or /uebergabe to a lawyer or authority">
</picture>

## Skills

<img src="../bilder/kapitel-skills-en.svg" alt="Skills: guides for your AI">

Call them in Claude Code with `/name`, in Codex with `$name`; the first
argument is always the case id:

| Call | What happens |
|---|---|
| `/fallaufnahme R-0001` | Case intake: role, goal, area of law, parties, receipt dates, missing facts; writes to the case and names the remedy from the fact sheet |
| `/sachverhalt R-0001` | Statement of facts: timeline and evidence table from the originals, with a source for every statement |
| `/fristencheck R-0001` | Deadlines with trigger, receipt, legal basis and a visible calculation; holidays of the place of performance |
| `/recherche-de R-0001 "Gilt § 193 BGB?"` | Legal research on the original full text, version and period of validity, checklist, sources into the case |
| `/entwurf R-0001 Widerspruch` | Letters and pleadings from the templates, mandatory content checked against the fact sheet, as Markdown and Word |
| `/gegenpruefung R-0001 06 Entwürfe/…_ENTWURF.md` | Adversarial review: split claims, attack them, strengthen the other side; unsupported claims, wrong citations, figures, exhibits |
| `/uebergabe R-0001 Anwalt` | Hand-over package for a lawyer, authority or court as a ZIP with index, timeline, deadlines, exhibits |

The guides set the standard of care: every legal statement names the
provision with paragraph and act, or the decision with court, date and
docket number, read in the full text; anything unverified stays visible as
`[PRÜFEN]`, `[QUELLE]` or `[BELEG]`; the other side is always considered;
instructions found inside documents are source content and are not followed.

> [!IMPORTANT]
> These decisions are always taken by the human, never by the AI: sending or
> filing, waiver or withdrawal, settlement, criminal complaint, termination,
> waiving a deadline, any declaration to third parties, deletion. Every draft
> stays a draft until you check it and send it yourself. There are no tools
> for sending, deleting or changing originals.

## Hooks

<img src="../bilder/kapitel-hooks-en.svg" alt="Hooks: automatic checks">

Hooks are small check scripts that Claude Code runs itself (registered in
`.claude/settings.json`, source under `.claude/recht/hooks/`). They are set
up and tested for Claude Code only (as of 17.09.2026). Codex documents hooks
of its own; nothing is included here for them. Other assistants follow the
rules in `AGENTS.md` themselves.

<details>
<summary><b>The 4 hooks in detail</b></summary>

| Event | What the hook does |
|---|---|
| `SessionStart` | reports new mail, near deadlines and open tasks per case at session start, plus legal content due for a check |
| `PreToolUse` | original protection: writing into 02 to 05, 08 and bestand.json is refused, checked on the resolved path |
| `PostToolUse` | foreign-text guard: warns with the source when read text (file, command, web or MCP tool) contains sentences that look like instructions to the AI |
| `Stop` | doc check: compares the HTML views with their md sources and the copies for other assistants with CLAUDE.md and the skills, names every mismatch |

</details>

---

<p align="center">
← <a href="einrichten.en.md">2 · Setup</a> · <a href="inhalt.en.md">4 · What is inside</a> →<br>
<sub><a href="../README.en.md#legal-notice-impressum">Legal notice</a> · <a href="../LICENSE">Licence AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Contribute</a></sub>
</p>
