# STRUKTUR

*Stand: 16.09.2026*

## Aufgabe dieser Datei

Hier steht, wie die Rechts-App aufgebaut ist und aufgebaut werden soll.
Keine Aufgabenliste, keine Arbeitsregeln.

## Zielbild in einem Satz

Ein Ordner, in dem jede Rechtssache (Arbeit, Verkehr, Miete, Verträge,
Behörden, Strafsachen und mehr) als eigene Fallakte liegt, bedient durch eine
lokale Oberfläche im Browser und später als Desktop-App, mit einer getrennten
Claude-Schicht für Prüfabläufe.

## Zwei Schichten

```text
Schicht 2  Claude-Schicht      .claude/recht/  Skills, Hooks, Vorlagen
               │  liest und schreibt akte.json, JOURNAL.md, Entwürfe
               ▼
Schicht 1  Aktenkern           02 Fälle/R-XXXX …/  festes Datenformat
               ▲
               │  liest und schreibt dasselbe Format
           Dienst + Oberfläche   06 Werkzeuge/   Python-Standardbibliothek,
                                                 HTML/CSS/JS, nur 127.0.0.1
```

Beide Schichten arbeiten auf denselben Dateien. Damit sie sich nicht in die
Quere kommen, gilt: Der Dienst schreibt nur mit Revisionsprüfung (Prüfsumme
der Datei vor dem Speichern), und Claude schreibt nur, wenn der Dienst nicht
gerade dieselbe Datei hält (Sperrdatei im temporären Ordner).

## Projektordner

```text
Recht/
├─ Start.command              startet den Dienst und öffnet den Browser (macOS)
├─ Start.sh, Start.bat        dasselbe für Linux (Ubuntu 24.04) und Windows (Windows 11), beide geprüft 17.09.2026
├─ CLAUDE.md                  Arbeitsprofil, Quelle (Stufe 5)
├─ AGENTS.md                  erzeugt aus CLAUDE.md für Codex, Cursor, Gemini CLI (Stufe 7)
├─ .agents/skills/            erzeugte Kopien der Skills für Codex (Stufe 7)
├─ .mcp.json                  MCP-Server für Claude Code (Stufe 7)
├─ .codex/config.toml         MCP-Server für Codex, projektbezogen (lädt nur, wenn genau dieser Ordner in ~/.codex/config.toml vertraut ist)
├─ zentrale.json              Fallliste, Sicherungsziel, Einstellungen (Bundesland, Absender für Entwürfe; bleibt lokal)
├─ 01 Eingang/                gemeinsame Post ohne Fallzuordnung
├─ 02 Fälle/                  eine Fallakte je Vorgang, feste Kennung R-0001 …
├─ 03 Verträge und Vorsorge/  Unterlagen ohne Streit (Finder-Ablage)
├─ 04 Rechtsquellen/          Quellen.md (Zugangskatalog), Verfahren/ (Merkblätter je Rechtsbehelf, Stufe 10)
├─ 05 Vorlagen/               Fallvorlage, Beispielakte (vollständiger erfundener Fall Kündigung, „Beispielfall laden“)
├─ 06 Werkzeuge/
│  ├─ dienst/                 server.py, store.py, dokumente.py, fristen.py,
│  │                          bestand.py, sicherung.py, werkzeuge.py, cli.py
│  ├─ oberflaeche/            index.html, app.js, style.css
│  ├─ verteilen.py            AGENTS.md und .agents/skills/ aus den Quellen erzeugen
│  └─ pruefen.py              Funktionstest mit künstlichen Akten
├─ .claude/recht/      Claude-Schicht als Plugin „recht“ (Stufe 5): Skills,
│                             Hooks, Vorlagen, Werkzeuge; lädt automatisch im Projekt
└─ DOKU/                      md/ als Quelle, HTML-Ansichten daneben; Rechtsinhalte.md = Stand und Pflege der mitgelieferten Rechtsinhalte
```

## Fallakte: feste Ordnerstruktur

Jeder Fall bekommt dieselben Ordner. Leere Ordner sind erlaubt. Die Nummern
sind fest, damit Verweise stabil bleiben.

```text
02 Fälle/R-0001 Beispiel/
├─ akte.json          Ordnungsdaten des Falls (fachlich, siehe unten)
├─ bestand.json       Prüfsummen und Verschiebungen (technisch, nur der Dienst)
├─ JOURNAL.md         Verlauf des Falls als Markdown, nur anhängen, ersetzt das alte TODO.md
├─ 01 Eingang/        neue Post; Unterordner Gelesen/ nach Bearbeitung
├─ 02 Grundlagen/     Verträge, Vollmachten, Bescheide, Policen, Mietvertrag
├─ 03 Schriftverkehr/ je Beteiligter ein Unterordner, dazu Versandnachweise/
├─ 04 Verfahren/      je Verfahren ein nummerierter Unterordner
├─ 05 Beweise/        Fotos, Zeugenlisten, Dienstpläne, Quittungen
├─ 06 Entwürfe/       noch nicht versandte Texte, Dateiname endet auf _ENTWURF; Fassungen/ mit eingefrorenen Kopien geprüfter und versandter Fassungen
├─ 07 Recherche/      Prüfvermerke (md plus html), Gesetzessammlung des Falls
└─ 08 Archiv/         alte Übersichten, frühere Arbeitsumgebung, unverändert
```

Ein Verfahren ist alles, was eine eigene Stelle und ein eigenes Aktenzeichen
hat: Klage beim Arbeitsgericht, Bußgeldbescheid, Widerspruch gegen einen
Bescheid, Mahnverfahren, Strafanzeige. Mehrere Verfahren in einem Konflikt
bekommen getrennte Unterordner und getrennte Fristen.

## Themenbereiche

Ein Fall hat einen Hauptbereich und beliebig viele Themen. Die Bereiche sind
Filter und Vorlagen, keine Ordner.

Seit 16.09.2026 abends 18 Bereiche plus „Allgemein“;
ältere Bereichsnamen in bestehenden Akten bleiben gültig, das Schema warnt nur.

| Bereich | Beispiele |
|---|---|
| Arbeit | Kündigung, Lohn, Zeugnis, Abmahnung, Arbeitsgericht |
| Verkehr und Bußgeld | Blitzer, Parken, Fahrverbot, Unfall, Führerschein |
| Steuern und Abgaben | Steuerbescheid, Einspruch, Finanzamt, Gebühren, Rundfunkbeitrag |
| Behörden und Bescheide | Verwaltungsakt, Widerspruch, Antrag, Gemeinde, Zulassung |
| Sozialleistungen und Rente | Bürgergeld, Arbeitslosengeld, Rente, Kindergeld, Wohngeld |
| Gesundheit und Pflege | Krankenkasse, Pflegegrad, Behandlungsfehler, Reha, Betreuung |
| Wohnen und Miete | Mietvertrag, Nebenkosten, Kaution, Wohnungskündigung, Eigentum |
| Bauen und Nachbarn | Bauantrag, Handwerker, Lärm, Grenze, Grundstück |
| Verträge und Verbraucher | Kauf, Reparatur, Abo, Reise, Handy, Internet, Widerruf |
| Forderungen und Inkasso | Rechnung, Mahnung, Mahnbescheid, Schulden, Vollstreckung |
| Versicherungen | Haftpflicht, Kfz, Hausrat, Unfall, Berufsunfähigkeit, Deckung |
| Familie und Unterhalt | Trennung, Scheidung, Unterhalt, Sorgerecht, Umgang |
| Erbe und Vorsorge | Testament, Nachlass, Vollmacht, Patientenverfügung |
| Strafsachen und Anzeigen | Anzeige, Vorladung, Strafbefehl, eigene Rolle zuerst klären |
| Schule, Ausbildung und Studium | Zeugnis, BAföG, Prüfung, Ausbildungsvertrag |
| Aufenthalt und Staatsangehörigkeit | Aufenthaltstitel, Einbürgerung, Visum, Ausländerbehörde |
| Geschäft, Datenschutz und Internet | Geschäftsvertrag, Abmahnung, Urheberrecht, DSGVO, Marke |
| Vereine und Ehrenamt | Satzung, Mitgliedschaft, Vorstand |
| Allgemein | passt nirgends |

## Datenmodell: akte.json

Eine Datei je Fall, UTF-8, lesbar eingerückt. Kennungen sind stabil und
werden nie wiederverwendet.

| Block | Kennung | Felder (Auswahl) |
|---|---|---|
| `fall` | R-0001 | titel, bereich, themen, rolle, ziel, rechtsordnung, status (offen, ruhend, abgeschlossen), angelegt |
| `beteiligte` | P01 … | name, rolle (Gegner, Gericht, Behörde, Anwalt, Zeuge, Stelle), anschrift, kontakt, aktenzeichen |
| `dokumente` | D0001 … | pfad, titel, datum, art (Schreiben, E-Mail, Foto, Vertrag, Bescheid, Urteil, Entwurf), status (Original, Entwurf, Versandt, Zugegangen), themen, anlage (K 1), personen, verweise, notiz |
| `verfahren` | V01 … | art, stelle (P-Kennung), aktenzeichen, stand, ordner |
| `ereignisse` | E01 … | datum (Sortierdatum), zeitpunkt (genau, ungefähr, zeitraum, unbekannt), datum_bis, zeitpunkt_text, titel, art (Zugang, Versand, Termin, Gespräch, Vorfall), quelle (D-Kennung), detail |
| `fristen` | F01 … | datum, titel, art (gesetzlich, selbst gesetzt, vorsorglich, Termin), ausloeser (Text), verfahren (V-Kennung), ausloeser_ereignis (E-Kennung), rechtsgrundlage, berechnung, pruefstatus (offen, bestätigt, erledigt), quelle, geprueft_am, geprueft_von |
| `aufgaben` | A01 … | titel, detail, faellig, erledigt, quelle |
| `entwuerfe` | W01 … | titel, datei, fassung, status (in Arbeit, geprüft, versandt), versandt_als (D-Kennung) |
| `kosten` | | datum, posten, betrag, beleg |
| `notizen` | N01 … | titel, text, datum |
| `quellen` | | titel, url, geprueft, verwendung (fallbezogene Rechtsquellen) |

Regeln im Modell: Eine Frist ohne Auslöser, Rechtsgrundlage und Prüfstatus
darf nicht als bestätigt gespeichert werden; „bestätigt“ verlangt zudem, dass
die Rechnung das Fristende nennt, kein Marker offen ist und ein Prüfdatum
gesetzt wird (drei Eigenschaften gerechnet, belegt, geprüft; Datenmodell.md).
Unsichere Zeitpunkte stehen als Feld am Ereignis (ungefähr, Zeitraum,
unbekannt), das Datum ist dann nur Sortierdatum; eine Frist auf einem solchen
Ereignis bleibt offen oder vorsorglich (F13). Ein Entwurf wird beim Versand
nicht gelöscht, sondern bekommt den Status versandt und einen Verweis auf den
Versandbeleg. Ein Dokument beweist zunächst nur seinen Inhalt.

Die feldgenaue Beschreibung steht in Datenmodell.md.

`bestand.json` führt je D-Kennung den Pfad, die erste Prüfsumme (SHA-256)
und jede Verschiebung mit Zeitpunkt. Das schreibt nur der Dienst, und nur
über schreibende Wege (Import, Zuordnung, Einsortieren, `bestand_abgleichen`).
Lesende Werkzeuge melden neue oder verschobene Dateien als Abweichung und
ändern nichts (seit 17.09.2026, Prüfbericht F03).

## Dienst (Stufe 3)

Python-Standardbibliothek, ein Prozess, nur 127.0.0.1, Sitzungsschlüssel
über Start.command, Schreibkennung gegen fremde Seiten. Kein Netzzugriff nach
außen. Systemabhängig sind nur drei Stellen, je mit Weiche: Browser öffnen
(`webbrowser`), Datei im Dateimanager zeigen (`open`, `xdg-open`,
`explorer`), Sperre (`fcntl` oder unter Windows `msvcrt`); das zweite
Sicherungsziel iCloud Drive wird nur vorgeschlagen, wo es den Ordner gibt. Textauszug aus PDF über das vorhandene `pdftotext`, wenn installiert.

| Modul | Aufgabe |
|---|---|
| `server.py` | HTTP-Dienst, Sitzungen, Routen, statische Oberfläche |
| `store.py` | akte.json und zentrale.json lesen und mit Revision schreiben, Sperre |
| `dokumente.py` | Dateien auflisten, Textauszug (txt, md, html, docx, eml, pdf) mit Herkunft (`befund()`: textquelle, Seiten, Zeichen; Bildscan und Foto gelten als nicht gelesen, seit 17.09.2026, F34), Suche |
| `fristen.py` | Fristen rechnen nach §§ 187, 188, 193 BGB, landesweite Feiertage aller 16 Bundesländer (Kürzel, Einstellung `feiertagsland` in zentrale.json, Standard BW), Rechnung als Text |
| `bestand.py` | Prüfsummen, Verschiebungen erkennen, Bestand prüfen |
| `sicherung.py` | geprüfte ZIP-Sicherung außerhalb des Projekts, SHA-256, Kopie an das zweite Ziel (Rechte 0600); Status prüft beide Archive und nennt die Ziele mit Cloud-Hinweis; `wiederherstellen()` entpackt in einen neuen, leeren Ordner außerhalb und prüft Schema und Prüfsummen, `probe()` dasselbe in einem Zwischenordner (seit 17.09.2026, F19, F20) |
| `werkzeuge.py` | Katalog aller Funktionen als beschriebene Werkzeuge (Name, Zweck, Parameter, lesend oder schreibend); Oberfläche und KI rufen dieselben Werkzeuge |
| `cli.py` | alle Werkzeuge über die Befehlszeile, für Claude Code, Codex und andere Assistenten |
| `mcp_server.py` | dieselben Werkzeuge als MCP-Server über die Standardeingabe (JSON-RPC 2.0), für Claude Code, Claude Desktop, Codex, Cursor, Gemini; schreibende nur mit `bestaetigt` |

Schnittstelle, Skizze:

```text
GET  /api/zentrale                    Fälle, Eingang, Sicherungsstand
GET  /api/fall/R-0001                 akte.json plus Dokumentliste
POST /api/fall/R-0001                 akte.json speichern (mit Revision)
GET  /api/fall/R-0001/text/D0038      Textauszug eines Dokuments
GET  /raw/R-0001/D0038                Originaldatei anzeigen
POST /api/fall/R-0001/verschieben     Datei einsortieren
POST /api/fall                        neuen Fall anlegen
POST /api/eingang/zuordnen            gemeinsame Post einem Fall zuordnen
POST /api/fristen/berechnen           Frist rechnen, Ergebnis mit Rechnung
GET  /api/bestand                     Prüfsummen aller Fälle prüfen
POST /api/sicherung                   geprüfte ZIP erstellen
POST /api/sicherung/probe             Wiederherstellungsprobe der letzten (oder genannten) Sicherung
GET  /api/werkzeuge                   Werkzeugkatalog (für Oberfläche und KI)
GET  /api/einstellungen               Sicherungsziele, Bundesland für Feiertage, Absender, Länderliste
POST /api/einstellungen               Sicherungsziele, Bundesland und Absender ändern (nur Text, bleibt lokal)
```

## Aktenmappe für jede KI (Stufe 7)

Grundsatz: Die App enthält keine KI. Sie ist eine
Aktenmappe, die jede KI benutzen kann, die der Nutzer schon hat: Claude Code,
Codex und andere. Dafür gibt es drei Standards, die wir bedienen:

| Standard | Was er ist | Wer ihn liest | Bei uns |
|---|---|---|---|
| `AGENTS.md` und `CLAUDE.md` | Arbeitsanweisung im Projektordner, Klartext | Codex, Cursor, Gemini CLI, viele Agenten (`AGENTS.md`); Claude Code (`CLAUDE.md`) | eine Quelle, beide Dateien daraus erzeugt |
| Agent Skills (`SKILL.md`) | Ordner mit Anleitung, offener Standard von Anthropic, von Codex übernommen | Claude Code (`.claude/skills/`), Codex (`.agents/skills/`) | Skills einmal gepflegt, für Codex kopiert |
| MCP (Model Context Protocol) | offene Schnittstelle, über die eine KI Werkzeuge aufruft; JSON über die Standardeingabe | Claude Desktop, Claude Code, ChatGPT, Codex, Cursor, Gemini | eigener MCP-Server `mcp_server.py` ohne Fremdpaket, stellt die Werkzeuge für Assistenten bereit (Katalog ohne `fall_lesen` und `akte_speichern`; Stand 17.09.2026: 25 Werkzeuge für Assistenten, 27 im Katalog; die Zahl prüft der Produktbau gegen den Katalog, maßgeblich ist `cli.py liste`) |
| Befehlszeile | `cli.py` | jede KI, die Befehle ausführen darf | vorhanden |

Regeln für alle Wege: Lesen frei und wirklich nur lesend (kein Werkzeug mit
`readOnlyHint` fasst akte.json, bestand.json oder zentrale.json an), Schreiben
nur über die Werkzeuge mit Schema und Revision, Originale gesperrt, kein
Versand, kein Löschen. Neue Dateien registriert allein `bestand_abgleichen`;
die Oberfläche ruft es beim Öffnen eines Falls selbst auf, eine KI nur nach
Bestätigung. zentrale.json legt der Dienst beim ersten Start an, nie ein
lesender Aufruf.
Schlüssel oder Konten braucht die Mappe nicht; die KI bringt der Nutzer mit.

Stand 16.09.2026: `06 Werkzeuge/verteilen.py` (Punkt 1) ist gebaut. Es
erzeugt `AGENTS.md` aus `CLAUDE.md` über eine Liste benannter Ersetzungen
(Titel, Zielgruppe, Hook-Hinweise werden zu Handlungsanweisungen; greift eine
Ersetzung nicht mehr, bricht das Skript ab) und hängt einen Abschnitt „Für
Assistenten außer Claude Code“ an. Die Skills werden Datei für Datei nach
`.agents/skills/` kopiert, mit Kopfvermerk „erzeugt“ und `CLAUDE.md` zu
`AGENTS.md`. `--pruefen` vergleicht nur und liefert Exit 1 bei Abweichung.
Verwaiste Kopien werden gemeldet, nie gelöscht.

`06 Werkzeuge/dienst/mcp_server.py` (Punkt 2) ist gebaut. Der Client startet
das Skript als Unterprozess; Nachrichten gehen zeilenweise als JSON-RPC 2.0
über Standardeingabe und -ausgabe, Meldungen auf die Standardfehlerausgabe.
Zwei Protokoll-Zeitalter der Spezifikation (gelesen am 16.09.2026 auf
modelcontextprotocol.io): die Fassungen bis 2025-11-25 mit Handshake
(`initialize`, `notifications/initialized`) und die Fassung 2026-07-28 ohne
Handshake, bei der jede Anfrage ihre Version in `params._meta` trägt und es
`server/discover` gibt. Methoden: `initialize`, `server/discover`, `ping`,
`tools/list`, `tools/call`. Werkzeuge aus `werkzeuge.fuer_agenten()` (Katalog ohne `fall_lesen` und
`akte_speichern`, Zahl siehe oben), jedes mit `inputSchema` und
`annotations.readOnlyHint` (seit 17.09.2026 zutreffend: lesende Werkzeuge
schreiben nichts). Schreibende Werkzeuge tragen im Schema den
Parameter `bestaetigt`; ohne den JSON-Wahrheitswert `true` liefert der Aufruf
nur die Rückfrage, Text wie `"true"` oder Zahlen werden als Fehler abgewiesen
(seit 17.09.2026, F05).
Fehler: unbekanntes Werkzeug oder unbekannte Methode als Protokollfehler
(JSON-RPC `error`), Werkzeugfehler als Ergebnis mit `isError`. Beim Schließen
der Eingabe beendet sich der Server.

### Anbindung je Assistent (Punkt 3, geprüft am 16.09.2026)

| Assistent | Datei | Stand |
|---|---|---|
| Claude Code 2.1.273 | `.mcp.json` im Projekt: `{"mcpServers":{"aka-recht":{"type":"stdio","command":"python3","args":["06 Werkzeuge/dienst/mcp_server.py"]}}}`. Der Server läuft im Projektordner, deshalb reicht der relative Pfad. Beim ersten interaktiven Start fragt Claude Code, ob es den Projekt-Server laden darf; Status mit `/mcp` oder `claude mcp get aka-recht`. Werkzeugnamen: `mcp__aka-recht__<werkzeug>`. | Geprüft: Testsitzung `claude -p` hat über `mcp__aka-recht__faelle_auflisten` „R-0001“ geliefert. Befund: `${CLAUDE_PROJECT_DIR}` in `.mcp.json` wird in dieser Version nicht ersetzt (Protokoll: Pfad wörtlich mit `${CLAUDE_PROJECT_DIR}`), deshalb kein Platzhalter. |
| Codex CLI 0.154.0 | Skills: `.agents/skills/` wird gelesen. MCP: `.codex/config.toml` im Projekt mit `[mcp_servers.aka-recht]` (command, args, cwd) liegt bei. | Geprüft: Codex nennt alle sieben Skills. Der Server selbst läuft mit Codex (`codex exec -c 'mcp_servers.aka-recht.command="python3"' -c 'mcp_servers.aka-recht.args=["06 Werkzeuge/dienst/mcp_server.py"]'` liefert „R-0001“). Die Projektdatei `.codex/config.toml` hat Codex am 16.09.2026 in drei Läufen nicht geladen; Ausweg war der globale Eintrag `codex mcp add aka-recht -- python3 "/voller/Pfad/06 Werkzeuge/dienst/mcp_server.py"`. Ursache geklärt am 17.09.2026: Codex lädt Projektdateien nur in vertrauten Projekten (Doku: learn.chatgpt.com/docs/config-file/config-advanced, „loads project-scoped config files only when the project is trusted“), und vertraut ist nur der genau eingetragene Ordner `[projects."<Projektordner>"] trust_level = "trusted"` in `~/.codex/config.toml`. Ein Eintrag für einen Elternordner oder `/` genügt nicht; ohne git zählt als Projektordner der Startordner, mit git die Wurzel. Geprüft mit eigenem `CODEX_HOME` in neun Varianten über `codex mcp list --json`; bei gleichem Namen gewinnt die Projektdatei gegen den globalen Eintrag. Nicht geprüft: Start des Servers in einer echten Codex-Sitzung mit der Projektdatei |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json`, unter `mcpServers` ein Eintrag `aka-recht` mit `command` `python3` und `args` `["/voller/Pfad/06 Werkzeuge/dienst/mcp_server.py"]`, Pfade absolut, danach Claude Desktop ganz beenden und neu starten. Protokolle unter `~/Library/Logs/Claude/mcp-server-aka-recht.log`. | Geprüft (16.09.2026): Eintrag von Hand gesetzt, Neustart, Konnektor aka-recht aktiv; Protokoll zeigt `initialize`, `notifications/initialized`, `tools/list`. Claude Desktop hält je Fenster einen eigenen Serverprozess. |
| Cursor, Gemini CLI, andere | Eigene Konfigurationsdatei des Assistenten, gleicher Aufruf (`python3` mit dem Pfad zu `mcp_server.py`, Arbeitsverzeichnis Projektordner oder `--root <Projektordner>`). | Nicht geprüft. |

### Stand je Client (17.09.2026, Prüfbericht F21 bis F23)

Drei Aussagen auseinanderhalten: „der Client kann es laut Doku“,
„in AKA Recht ist es eingerichtet“, „hier praktisch geprüft“.

| Funktion | Claude Code | Codex | Claude Desktop |
|---|---|---|---|
| Hooks (automatische Prüfungen) | dokumentiert, eingerichtet (`.claude/settings.json`), geprüft (Funktionstest Abschnitt 11, Handproben) | in der Codex-Doku beschrieben; hier nichts eingerichtet, nichts geprüft | keine |
| Projektkonfiguration für den MCP-Server | `.mcp.json`, geprüft | `.codex/config.toml` liegt bei; lädt nur, wenn genau der Projektordner in `~/.codex/config.toml` als `trusted` eingetragen ist (Ursache 17.09.2026 geklärt, Codex CLI 0.154.0, geprüft über `codex mcp list`); welche Konfigurationsquelle ein Lauf lädt, im Client prüfen (`codex mcp list --json` zeigt Pfad und `cwd`), nie aus dem globalen Eintrag auf die Projektdatei schließen | Eintrag in `claude_desktop_config.json`, geprüft |
| Skills | `.claude/skills/`, geprüft | `.agents/skills/`, gesehen (sieben Skills gelistet), Ablauf nicht durchgespielt | keine (nur MCP-Werkzeuge) |
| Vollständiger Ablauf nur über MCP | nicht nötig (hat Dateizugriff und cli.py) | nicht nötig (cli.py) | offen: `fall_lesen` und `akte_speichern` sind für Assistenten bewusst nicht freigegeben; Beteiligte und Verfahren ändern, vorhandene Fristen korrigieren, Entwurfstexte schreiben geht über MCP allein nicht (F23). Ein reiner MCP-Client bekommt die Skills auch nicht mit. Abnahme „Fallaufnahme bis Übergabe nur mit MCP“ steht aus (TODO) |

Die Anleitung der Oberfläche (Seite „Anleitung“, Abschnitt „KI anbinden“)
fasst das für Nutzer zusammen.

## Oberfläche (Stufe 4)

Ein Frontend für Zentrale und Fallakte, reines HTML, CSS und JavaScript ohne
Framework, damit es später unverändert in eine Desktop-Hülle passt.
Seitenleiste links, Inhalt rechts, jeder Bereich scrollt für sich. Nach jeder
Änderung an CSS oder JS wird die Versionsnummer im HTML-Link erhöht. Der
Dienst setzt `style-src 'self'`; die Oberfläche erzeugt deshalb keine
Inline-Stile, Abstände und Farben liegen als Hilfsklassen `u-…` in style.css
(seit 17.09.2026, F37).

Bereiche der Zentrale: Übersicht, Alle Fälle, Posteingang, Fristen aller
Fälle, Rechtsquellen, Bestand und Sicherung, Einstellungen, Anleitung.
Bereiche der Fallakte: Übersicht (mit Notizen und Angeheftetem), Dokumente
mit Vorschau (Vorschau, Text, Angaben; Ordnen, Einsortieren, Öffnen, Finder),
Beteiligte, Verfahren, Chronologie, Fristen (mit Rechner im Formular),
Aufgaben, Entwürfe (mit „Entwurf aus Vorlage“: Dialog ruft `vorlage_fuellen`),
Beweise und Anlagen, Journal.

Die Oberfläche schreibt Ordnungsdaten über `/api/fall/<id>` mit Revision und
nutzt für Dateivorgänge die Werkzeuge (Einsortieren, Journal, Fallstatus).
Nach jedem Speichern und jedem Werkzeugaufruf wird die Zentrale neu
eingelesen, beim Zurückkommen nach einem Tageswechsel ebenfalls (seit
17.09.2026, F14). „Öffnen“ startet nur bekannte Dokumentformate (PDF, Text,
Office ohne Makros, Bilder, E-Mail, Ton, Video); Skripte, Programme,
Webseiten, Archive und Unbekanntes werden nur im Dateimanager gezeigt, mit
Hinweis (F36).
Routen im Adressfeld: `#seite=dokumente&fall=R-0001&dok=D0004`.

## Claude-Schicht (Stufe 5)

Projekt-Skills unter `.claude/skills/<name>/SKILL.md`, Hooks in
`.claude/settings.json`, Hilfsskripte unter `.claude/recht/`, Schreibvorlagen
unter `05 Vorlagen/Schreiben/`. Skills heißen `/fallaufnahme`, `/sachverhalt`,
`/recherche-de`, `/gegenpruefung`, `/fristencheck`, `/entwurf`, `/uebergabe`.
Claude Code lädt Projekt-Skills und Projekt-Hooks nach Bestätigung des
Arbeitsbereichs; Hook-Änderungen wirken nach Neustart der Sitzung.

| Teil | Inhalt |
|---|---|
| `skills/fallaufnahme` | Rolle, Ziel, Rechtsordnung, Verfahrensart, Zugang, fehlende Angaben; trägt über die Werkzeuge ein |
| `skills/sachverhalt` | Chronologie und Beweistabelle aus den Originalen, Fundstellen je Aussage, Prüfvermerk in 07 Recherche |
| `skills/recherche-de` | deutsche Rechtsfrage am Originalvolltext, Fassung und Geltungszeitraum, Quellen in die Akte |
| `skills/gegenpruefung` | stärkste Gegenargumente, unbelegte Aussagen, unpassende Zitate, Zahlen, Anlagen, Fristen |
| `skills/fristencheck` | Fristkandidaten mit Auslöser, Zugang, Grundlage, Rechnung über `frist_berechnen`, Prüfstatus |
| `skills/entwurf` | Schreiben und Schriftsätze als Entwurf aus den Vorlagen, Markdown plus Word über `docx_erzeugen.py`, `entwurf_erfassen` |
| `skills/uebergabe` | Übergabepaket als ZIP außerhalb des Projekts über `uebergabe_paket.py`, Begleitvermerk |
| `.claude/settings.json` | SessionStart: Eingang, nahe Fristen, offene Aufgaben je Fall. PreToolUse (Write, Edit, MultiEdit): Schreiben in 02, 03, 04, 05, 08 und bestand.json gesperrt; der Pfad wird gegen den Projektordner aufgelöst („..“ und Verknüpfungen), geprüft werden die Ordnerbestandteile (seit 17.09.2026, F06); Shell und MCP deckt der Hook nicht ab, dort schützt der Dienst. PostToolUse (Read, Bash, WebFetch, WebSearch und die MCP-Werkzeuge `mcp__aka-recht__*`): Fremdtext-Wächter meldet Sätze, die wie Anweisungen an die KI klingen (REGELN Nr. 17), mit Herkunft (Datei, Befehl, Adresse oder Werkzeug mit Fall und Dokumentkennung), blockiert nicht; Ausnahmen nur für aufgelöste Pfade in `.claude`, `.agents`, `DOKU`, `06 Werkzeuge` und den Profil- und README-Dateien (bei Bash nur reines Lesen, nie wenn ein Skript läuft), auch kurze Texte und Dateinamen werden geprüft (seit 17.09.2026, F07). Stop: Doku-Abgleich inhaltlich: jede HTML-Ansicht wird aus ihrer md-Quelle neu erzeugt und verglichen, AGENTS.md und `.agents/skills/` über `verteilen.py --pruefen`, dazu die Namen der Dateien, die jünger sind als die Live-Dokumentation; läuft ohne zentrale.json (seit 17.09.2026, F26) |
| `05 Vorlagen/Schreiben/` | zehn Vorlagen (Briefkopf, Einspruch Bußgeld, Einspruch Steuerbescheid, Widerspruch Bescheid, Fristsetzung, Auskunft DSGVO, Akteneinsicht, Strafanzeige, Klage Arbeitsgericht, Klage Zivilgericht); interne Hinweise über der Trennlinie, Platzhalter 【 】, Marker; feste Platzhalter 【ABSENDER】, 【ABSENDER_NAME】, 【DATUM】, 【R-0000】 füllt das Werkzeug `vorlage_fuellen` aus den Einstellungen (Absender) oder vom Beteiligten mit Rolle „Ich“ des Falls (seit 17.09.2026) |
| `.claude/recht/werkzeuge/docx_erzeugen.py` | Markdown oder Text nach Word ohne Fremdpaket; Vorabbericht zum Sendetext (offene Marker mit und ohne Doppelpunkt, Platzhalter 【…】, interne Notizen, Kopfzeilen Von, An, Datum, Betreff, Aktenzeichen, Anlagenliste, Antragssatz, Trennlinie), `--pruefen` nur Bericht mit Exit 1 bei Befunden; die Datei ist keine Freigabe (seit 17.09.2026, F29) |
| `.claude/recht/werkzeuge/uebergabe_paket.py` | ZIP für einen benannten Empfänger: `--empfaenger anwalt` voll (Verzeichnis mit Chronologie, Fristen, Aufgaben, Journal, Originale 01 bis 05), `behoerde`, `gericht`, `gegenseite`, `beratung` nur die mit `--nur` gewählten Dokumente; `--vorschau`; unbekannte Kennungen brechen ab; Paket wird zurückgelesen und gegen `00 Manifest.json` geprüft (seit 17.09.2026, F08, F27) |

Claude arbeitet in der Sitzung mit denselben Werkzeugen wie die App, über
`06 Werkzeuge/dienst/cli.py` (Schema, Revision, Sperre inklusive). Das
Arbeitsprofil steht in `CLAUDE.md` im Projekt.

Marker in allen Texten der Claude-Schicht: `[BELEG: …]` für fehlende
Fundstelle, `[PRÜFEN: …]` für ungeprüfte Tatsache, `[QUELLE: …]` für eine
noch nicht am Volltext gelesene Rechtsquelle.

## Datenfluss

```text
Neue Post im Finder oder per Oberfläche
  ↓
01 Eingang/               Dienst vergibt D-Kennung und erste Prüfsumme
  ↓
Einsortieren              Pfad wandert, Kennung bleibt, bestand.json protokolliert
  ↓
akte.json                 Titel, Datum, Beteiligte, Verweise, Anlagen-Nummer
  ↓
Claude-Schicht            Fallaufnahme, Sachverhalt, Fristen, Entwürfe
  ↓
06 Entwürfe/ → Versand    Entwurf bekommt Status versandt, Beleg als Dokument
  ↓
JOURNAL.md                jeder Schritt mit Datum, nur anhängen
```
