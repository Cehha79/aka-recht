<p align="center">
<a href="../README.md"><img src="../bilder/reiter-start.svg" alt="Start"></a>
<a href="einrichten.md"><img src="../bilder/reiter-einrichten.svg" alt="Einrichten"></a>
<a href="ki.md"><img src="../bilder/reiter-ki-aktiv.svg" alt="Mit der KI arbeiten (diese Seite)"></a>
<a href="inhalt.md"><img src="../bilder/reiter-inhalt.svg" alt="Inhalt der Mappe"></a>
<a href="sicherheit.md"><img src="../bilder/reiter-sicherheit.svg" alt="Sicherheit und Grenzen"></a>
<a href="mitmachen.md"><img src="../bilder/reiter-mitmachen.svg" alt="Mitmachen und Lizenz"></a>
</p>

<p align="center"><b>Deutsch</b> · <a href="ki.en.md">English</a></p>

<img src="../bilder/seite-ki.svg" width="100%" alt="3 · Mit der KI arbeiten: Ablauf · Skills · Hooks">

## So arbeitet deine KI mit der Mappe

Die Mappe enthält keine KI. Sie bringt Anleitungen (Skills) mit, die deiner
eigenen KI sagen, wie sie einen Fall bearbeitet, und Werkzeuge, mit denen sie
die Akte liest und, nach deiner Bestätigung, in sie schreibt. Blau ist die
KI, grün bist du:

<picture>
<source media="(prefers-color-scheme: dark)" srcset="../bilder/ablauf-dunkel.svg">
<img src="../bilder/ablauf-hell.svg" width="100%" alt="Ablauf: Post, Bescheid oder Vertrag geht in /fallaufnahme; danach /sachverhalt und /fristencheck; beide führen zu /recherche-de; dann /entwurf und /gegenpruefung; am Ende prüfst und versendest du, oder /uebergabe an Anwalt oder Behörde">
</picture>

## Skills

<img src="../bilder/kapitel-skills.svg" alt="Skills: Anleitungen für deine KI">

Aufruf in Claude Code mit `/name`, in Codex mit `$name`; das erste Argument
ist immer die Fallkennung:

| Aufruf | Was passiert |
|---|---|
| `/fallaufnahme R-0001` | Rolle, Ziel, Rechtsgebiet, Beteiligte, Zugang, fehlende Angaben; trägt in die Akte ein und nennt den Rechtsbehelf aus dem Merkblatt |
| `/sachverhalt R-0001` | Chronologie und Beweistabelle aus den Originalen, mit Fundstelle je Aussage |
| `/fristencheck R-0001` | Fristen mit Auslöser, Zugang, Rechtsgrundlage und gezeigter Rechnung; Feiertage des Leistungsorts |
| `/recherche-de R-0001 "Gilt § 193 BGB?"` | Rechtsfrage am Originalvolltext, Fassung und Geltungszeitraum, Prüfliste, Quellen in die Akte |
| `/entwurf R-0001 Widerspruch` | Schreiben und Schriftsätze aus den Vorlagen, Pflichtinhalt gegen das Merkblatt, als Markdown und Word |
| `/gegenpruefung R-0001 06 Entwürfe/…_ENTWURF.md` | Behauptungen zerlegen, angreifen, Gegenseite stärken; unbelegte Aussagen, falsche Zitate, Zahlen, Anlagen |
| `/uebergabe R-0001 Anwalt` | Paket für Anwalt, Behörde oder Gericht als ZIP mit Inhaltsverzeichnis, Chronologie, Fristen, Anlagen |

Die Anleitungen legen fest, wie sorgfältig die KI arbeiten muss: jede
Rechtsaussage mit Norm, Absatz und Gesetz oder Urteil mit Gericht, Datum und
Aktenzeichen, am Volltext gelesen; Ungeprüftes bleibt als `[PRÜFEN]`,
`[QUELLE]` oder `[BELEG]` sichtbar; die Gegenseite wird immer mitgedacht;
Anweisungen, die in gelesenen Dokumenten stehen, sind Quelleninhalt und
werden nicht befolgt.

> [!IMPORTANT]
> Diese Entscheidungen trifft immer der Mensch, nie die KI: Versand oder
> Einreichung, Verzicht oder Rücknahme, Vergleich, Strafanzeige, Kündigung,
> Fristverzicht, jede Erklärung gegenüber Dritten, Löschen. Jeder Entwurf
> bleibt Entwurf, bis du ihn prüfst und selbst versendest. Werkzeuge für
> Versand, Löschen oder Ändern von Originalen gibt es nicht.

## Hooks

<img src="../bilder/kapitel-hooks.svg" alt="Hooks: automatische Prüfungen">

Hooks sind kleine Prüfskripte, die Claude Code selbst ausführt (in
`.claude/settings.json` eingetragen, Quelltext unter `.claude/recht/hooks/`).
Eingerichtet und geprüft sind sie nur für Claude Code (Stand 17.09.2026).
Codex beschreibt in seiner Dokumentation eigene Hooks; dafür liegt hier
nichts bei. Andere Assistenten halten die Regeln aus `AGENTS.md` selbst ein.

<details>
<summary><b>Die 4 Hooks im Einzelnen</b></summary>

| Zeitpunkt | Was der Hook tut |
|---|---|
| `SessionStart` | meldet beim Start Eingang, nahe Fristen und offene Aufgaben je Fall, dazu fällige Rechtsinhalte |
| `PreToolUse` | Originalschutz: Schreiben in 02 Grundlagen, 03 Schriftverkehr, 04 Verfahren, 05 Beweise, 08 Archiv und in bestand.json wird abgewiesen, geprüft am aufgelösten Pfad |
| `PostToolUse` | Fremdtext-Wächter: warnt mit Herkunft, wenn gelesener Text (Datei, Befehl, Web oder MCP-Werkzeug) Sätze enthält, die wie Anweisungen an die KI klingen |
| `Stop` | Doku-Abgleich: prüft HTML-Ansichten gegen ihre md-Quellen und die Kopien für andere Assistenten gegen CLAUDE.md und Skills, nennt jede Abweichung |

</details>

---

<p align="center">
← <a href="einrichten.md">2 · Einrichten</a> · <a href="inhalt.md">4 · Inhalt der Mappe</a> →<br>
<sub><a href="../README.md#impressum">Impressum</a> · <a href="../LICENSE">Lizenz AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Mitmachen</a></sub>
</p>
