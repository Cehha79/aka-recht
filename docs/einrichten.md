<p align="center">
<a href="../README.md"><img src="../bilder/reiter-start.svg" alt="Start"></a>
<a href="einrichten.md"><img src="../bilder/reiter-einrichten-aktiv.svg" alt="Einrichten (diese Seite)"></a>
<a href="ki.md"><img src="../bilder/reiter-ki.svg" alt="Mit der KI arbeiten"></a>
<a href="inhalt.md"><img src="../bilder/reiter-inhalt.svg" alt="Inhalt der Mappe"></a>
<a href="sicherheit.md"><img src="../bilder/reiter-sicherheit.svg" alt="Sicherheit und Grenzen"></a>
<a href="mitmachen.md"><img src="../bilder/reiter-mitmachen.svg" alt="Mitmachen und Lizenz"></a>
</p>

<p align="center"><b>Deutsch</b> · <a href="einrichten.en.md">English</a></p>

<img src="../bilder/seite-einrichten.svg" width="100%" alt="2 · Einrichten: Voraussetzungen · Erster Start · KI anbinden · Aktualisieren · Fragen">

## Voraussetzungen

- Python 3, geprüft mit 3.14.7 (`python3 --version`); ältere Fassungen
  sind ungeprüft. Keine weiteren Pakete.
- Geprüft am 17.09.2026 auf macOS, auf Ubuntu 24.04 mit Python 3.12 und auf
  Windows 11 mit Python 3.14: jeweils Funktionstest, Dienst über das
  Startskript, MCP-Server, Beispielfall in einem Ordner mit Umlauten.
- Für Textauszüge aus PDF optional das Programm `pdftotext` (Paket poppler).
  Scans ohne Textschicht liest die Mappe nicht; dafür braucht es
  Texterkennung (OCR) außerhalb der Mappe.

<details>
<summary><b>macOS</b></summary>

- Start mit `Start.command` (Doppelklick).
- Den Ordner nicht mit dem Befehl `zip` oder `ditto` neu packen: Diese
  Archive tragen keine UTF-8-Kennung, und je nach Entpackprogramm wird aus
  „06 Entwürfe“ ein kaputter Ordnername (am 17.09.2026 mit Python geprüft;
  den Finder nicht getestet, also auch nicht verwenden). Das ZIP von GitHub
  ist sauber.

</details>

<details>
<summary><b>Linux</b></summary>

- Start mit `Start.sh`.
- Geprüft auf Ubuntu 24.04 mit Python 3.12; als Dateimanager dient `xdg-open`.

</details>

<details>
<summary><b>Windows</b></summary>

- Start mit `Start.bat` (Doppelklick).
- Unter Windows heißt der Befehl `python` statt `python3`; `python3.exe` ist
  dort nur ein Verweis auf den Microsoft Store. `Start.bat` stellt deshalb bei
  jedem Start `.mcp.json`, `.claude/settings.json` und `.codex/config.toml` auf
  `python` um (`06 Werkzeuge/einrichten_windows.py`, ändert nur diesen einen
  Wert und nichts, wenn schon eingerichtet). Also einmal `Start.bat` starten,
  bevor Claude Code oder Codex im Ordner laufen. Wer mit git arbeitet, sieht
  diese drei Dateien danach als geändert.
- Windows bringt `pdftotext` nicht mit (auf der Testmaschine Windows 11 fehlte
  es); ohne das Programm zeigt die Mappe bei PDFs die Textquelle
  „werkzeug-fehlt“ und liest keinen Text aus.

</details>

## Erster Start

1. Holen: `git clone https://github.com/Cehha79/aka-recht` oder auf GitHub „Code“, „Download ZIP“ und
   entpacken; den Ordner an einen Ort deiner Wahl legen. Zum Weitergeben den
   GitHub-Link teilen, den Ordner nicht selbst neu packen (siehe macOS oben).
2. Starten: macOS `Start.command`, Linux `Start.sh`, Windows `Start.bat`. Der
   Dienst läuft nur auf 127.0.0.1, der Standardbrowser öffnet die Oberfläche.
   Beim ersten Start entsteht `zentrale.json`.
3. Unter „Einstellungen“ deinen Absender eintragen (Name, Anschrift,
   Kontakt); er landet in `zentrale.json` auf deinem Rechner und füllt später
   „Von:“ und Unterschrift in Entwürfen aus den Vorlagen.
4. In der Oberfläche „Neuer Fall“ anlegen, Post nach `01 Eingang` legen oder
   in „Dokumente“ hinzufügen, ordnen, Fristen rechnen, Journal führen.
5. Seite „Anleitung“ in der Oberfläche lesen, dort steht auch, wie du eine KI
   anbindest.

## KI anbinden

<details open>
<summary><b>Claude Code</b></summary>

Sitzung im Ordner starten; `.mcp.json` liegt bei; Dialog bestätigen; mit
`/mcp` prüfen. Skills unter `.claude/skills/` (`/fallaufnahme`,
`/fristencheck`, `/entwurf` …), Hooks aus `.claude/settings.json`.

</details>

<details>
<summary><b>Codex</b></summary>

- Weg A: einmalig `codex mcp add aka-recht -- python3 "<voller Pfad>/06 Werkzeuge/dienst/mcp_server.py"`.
- Weg B ohne diesen Eintrag: den Projektordner in `~/.codex/config.toml` als
  vertraut eintragen (`[projects."<voller Pfad zum Projektordner>"]` mit
  `trust_level = "trusted"`), dann lädt Codex die mitgelieferte
  `.codex/config.toml`; ein Eintrag für einen übergeordneten Ordner genügt nicht.
- Prüfen im Projektordner mit `codex mcp list`. Unter Windows `python` statt
  `python3`. Skills unter `.agents/skills/` (`$fristencheck` …).

</details>

<details>
<summary><b>Claude Desktop</b></summary>

Einstellungen, Entwickler, Konfiguration bearbeiten: Eintrag `aka-recht` mit
`command` `python3` (unter Windows `python`) und `args`
`["<voller Pfad>/06 Werkzeuge/dienst/mcp_server.py"]`; Claude Desktop neu starten.

</details>

<details>
<summary><b>Andere Assistenten</b></summary>

- Mit MCP: gleicher Aufruf in der Konfigurationsdatei des Assistenten;
  Arbeitsprofil in `AGENTS.md`.
- Ohne MCP, mit Befehlen: `python3 "06 Werkzeuge/dienst/cli.py" liste`.
- ChatGPT im Browser oder in der App startet keinen lokalen Server; es
  verlangt eine öffentliche HTTPS-Adresse oder einen Tunnel über OpenAI. Das
  ist für AKA Recht nicht vorgesehen.

</details>

Schreibende Werkzeuge laufen nur, wenn du den Aufruf bestätigst. Werkzeuge
für Versand, Löschen oder Ändern von Originalen gibt es nicht.

## Aktualisieren

Deine eigenen Daten liegen in `01 Eingang`, `02 Fälle`,
`03 Verträge und Vorsorge` und `zentrale.json`. Vor jeder Aktualisierung
eine Sicherung anlegen („Geprüfte Sicherung erstellen“ in der Oberfläche).

<details open>
<summary><b>Mit git</b></summary>

Im Ordner der Mappe `git pull`. Die vier Orte mit deinen Daten stehen in der
mitgelieferten `.gitignore`; git lässt sie unberührt. Unter Windows hat
`Start.bat` drei Konfigurationsdateien geändert; bricht `git pull` deshalb ab,
vorher `git checkout -- .mcp.json .claude/settings.json .codex/config.toml`
ausführen (verwirft nur diese Umstellung, `Start.bat` setzt sie beim nächsten
Start wieder).

</details>

<details>
<summary><b>Mit einem neuen ZIP</b></summary>

1. Neue Version in einen neuen Ordner entpacken.
2. Den laufenden Dienst beenden. Einen Knopf dafür gibt es nicht: den Rechner
   neu starten, oder unter macOS und Linux im Terminal
   `pkill -f "06 Werkzeuge/dienst/server.py"` (beendet jeden laufenden Dienst
   einer Mappe auf diesem Rechner).
3. Aus dem alten Ordner `01 Eingang`, `02 Fälle`, `03 Verträge und Vorsorge`
   und `zentrale.json` in den neuen Ordner verschieben; die leeren Ordner des
   neuen Ordners vorher entfernen.
4. Im neuen Ordner starten. Fälle und Einstellungen sind wieder da; die Pfade
   in `zentrale.json` sind relativ zum Ordner.
5. Hast du Codex oder Claude Desktop mit dem vollen Pfad zu
   `mcp_server.py` eingerichtet, den Pfad auf den neuen Ordner ändern.

</details>

## Häufige Fragen

<details>
<summary><b>Brauche ich ein Konto oder Internet?</b></summary>

Für die Mappe nicht: Der Dienst läuft nur auf 127.0.0.1 und ruft keine fremden
Adressen auf. Deine KI (Claude, Codex oder eine andere) braucht ihr eigenes
Konto und ihren eigenen Zugang; was sie liest, verarbeitet ihr Anbieter.

</details>

<details>
<summary><b>Welche KI kann ich benutzen?</b></summary>

Geprüft sind Claude Code, Claude Desktop und Codex (siehe „KI anbinden“).
Jede andere KI, die MCP spricht oder Befehle ausführen darf, sollte gehen,
ist aber nicht geprüft. ChatGPT im Browser oder in der App ist nicht
vorgesehen, weil es keinen lokalen Server startet.

</details>

<details>
<summary><b>Landen meine Fälle auf GitHub?</b></summary>

Nein. Die Mappe lädt nichts hoch. Wer selbst mit git arbeitet: `01 Eingang`,
`02 Fälle`, `03 Verträge und Vorsorge` und `zentrale.json` stehen in der
`.gitignore` und werden nicht erfasst. Liegt ein Sicherungsziel in einem
Cloud-Ordner, lädt dein System die Sicherung dorthin hoch.

</details>

<details>
<summary><b>Kann die Mappe eingescannte Briefe lesen?</b></summary>

Nur, wenn das PDF eine Textschicht hat und `pdftotext` installiert ist. Fotos
und Scans ohne Textschicht liest sie nicht; das Werkzeug `dokument_text`
meldet dann ehrlich, dass kein Text gelesen wurde. Texterkennung ist geplant.

</details>

<details>
<summary><b>Gilt das auch für Österreich, die Schweiz oder die Türkei?</b></summary>

Noch nicht. Fristenrechner, Merkblätter und Vorlagen gelten nur für deutsches
Recht. Weitere Länder sind geplant, siehe
[Geltungsbereich](sicherheit.md#geltungsbereich).

</details>

<details>
<summary><b>Beantwortet hier jemand Fragen zu meinem Fall?</b></summary>

Nein. Issues und Diskussionen sind nur für die Software. Für deinen Fall eine
Fachanwältin, einen Fachanwalt oder eine Beratungsstelle fragen.

</details>

---

<p align="center">
← <a href="../README.md">1 · Start</a> · <a href="ki.md">3 · Mit der KI arbeiten</a> →<br>
<sub><a href="../README.md#impressum">Impressum</a> · <a href="../LICENSE">Lizenz AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Mitmachen</a></sub>
</p>
