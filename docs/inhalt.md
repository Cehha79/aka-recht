<p align="center">
<a href="../README.md"><img src="../bilder/reiter-start.svg" alt="Start"></a>
<a href="einrichten.md"><img src="../bilder/reiter-einrichten.svg" alt="Einrichten"></a>
<a href="ki.md"><img src="../bilder/reiter-ki.svg" alt="Mit der KI arbeiten"></a>
<a href="inhalt.md"><img src="../bilder/reiter-inhalt-aktiv.svg" alt="Inhalt der Mappe (diese Seite)"></a>
<a href="sicherheit.md"><img src="../bilder/reiter-sicherheit.svg" alt="Sicherheit und Grenzen"></a>
<a href="mitmachen.md"><img src="../bilder/reiter-mitmachen.svg" alt="Mitmachen und Lizenz"></a>
</p>

<p align="center"><b>Deutsch</b> · <a href="inhalt.en.md">English</a></p>

<img src="../bilder/seite-inhalt.svg" width="100%" alt="4 · Inhalt der Mappe: Fallordner · Werkzeuge · Vorlagen · Merkblätter · Befehle">

## Ordner eines Falls

Jeder Fall bekommt dieselben Ordner, damit Verweise stabil bleiben:

```text
02 Fälle/R-0001 Beispiel/
├─ akte.json          Ordnungsdaten: Beteiligte, Dokumente, Fristen, Aufgaben, Entwürfe
├─ bestand.json       Prüfsummen jeder Datei (schreibt nur der Dienst)
├─ JOURNAL.md         Verlauf, nur anhängen
├─ 01 Eingang/        neue Post
├─ 02 Grundlagen/     Verträge, Bescheide, Vollmachten
├─ 03 Schriftverkehr/ je Beteiligter ein Ordner, dazu Versandnachweise/
├─ 04 Verfahren/      je Verfahren ein Ordner (Klage, Bußgeld, Widerspruch …)
├─ 05 Beweise/        Fotos, Listen, Quittungen
├─ 06 Entwürfe/       noch nicht versandte Texte, Name endet auf _ENTWURF
├─ 07 Recherche/      Prüfvermerke, fallbezogene Rechtsquellen
└─ 08 Archiv/         alte Übersichten, unverändert
```

Originale in 02 bis 05 und 08 werden nie verändert, umbenannt oder gelöscht;
ein Hook sperrt das für die KI. Neue Texte entstehen in 06, Vermerke in 07.

## Werkzeuge

<img src="../bilder/kapitel-werkzeuge.svg" alt="Werkzeuge: MCP und Befehlszeile">

Dieselben 26 Werkzeuge erreicht die KI über MCP (`06 Werkzeuge/dienst/mcp_server.py`)
oder über die Befehlszeile (`python3 "06 Werkzeuge/dienst/cli.py" <werkzeug> feld=wert`).
Schreibende Werkzeuge laufen über MCP nur mit deiner Bestätigung (es zählt
allein der JSON-Wert `true`); über die Befehlszeile soll die KI vorher
fragen. Lesende Werkzeuge ändern keine Datei: Eine neue oder im Dateimanager
verschobene Datei melden sie nur, ihre Kennung bekommt sie erst durch
`bestand_abgleichen`; die Oberfläche macht das beim Öffnen eines Falls
selbst. Jede Änderung an `akte.json` wird gegen das Datenmodell geprüft
und mit Revision gespeichert.

<details>
<summary><b>Alle 26 Werkzeuge</b></summary>

| Werkzeug | Art | Zweck |
|---|---|---|
| `faelle_auflisten` | lesend | Alle Fälle mit Kennung, Titel, Bereich, Status, Zahl der Dokumente, nicht erfassten Dateien und offenen Aufgaben. |
| `fall_uebersicht` | lesend | Kompakte Übersicht eines Falls: Fall, Beteiligte, Verfahren, offene Fristen und Aufgaben, Ereignisse, Dokumentliste mit Kennung, Titel, Datum, Stand, dazu nicht erfasste Dateien. Dokumentinhalte über dokument_text. |
| `dokument_text` | lesend | Textauszug eines Dokuments (Word, E-Mail, PDF, Text, HTML) mit Herkunft: textquelle sagt, ob der Text direkt, aus der PDF-Textschicht oder gar nicht gelesen wurde (Bildscan, Foto); textstand ist die in der Akte vermerkte Lesequalität. Der Auszug ist eine Ableitung, Zahlen und Fristen am Original prüfen. |
| `dokumente_suchen` | lesend | Volltextsuche in Titeln, Ordnungsangaben und Dokumentinhalten eines Falls. |
| `frist_berechnen` | lesend | Fristende nach §§ 187, 188, 193 BGB mit den landesweiten Feiertagen eines Bundeslands berechnen (Standard: Einstellung der Mappe). Liefert die Rechnung als Text. Entscheidet nicht, welche Frist gilt. |
| `beispiel_laden` | schreibend | Die mitgelieferte Beispielakte (erfundener Fall) als neuen Fall anlegen, zum Ausprobieren. Der Fall bekommt die nächste freie Kennung. |
| `bestand_pruefen` | lesend | Prüfsummen aller registrierten Dateien eines Falls mit dem ersten Stand vergleichen; meldet auch nicht erfasste und verschobene Dateien. Schreibt nichts. |
| `journal_lesen` | lesend | Verlauf eines Falls aus JOURNAL.md, neueste Einträge zuletzt. |
| `quellen_katalog` | lesend | Gemeinsamer Zugangskatalog amtlicher Rechtsquellen aus 04 Rechtsquellen/Quellen.md. |
| `rechtsinhalte_pruefen` | lesend | Meldet, welche mitgelieferten Rechtsinhalte wieder am amtlichen Volltext zu prüfen sind: Merkblätter (zwölf Monate nach „Letzte vollständige Prüfung“), Feiertagstabelle (ab 1. Dezember fürs Folgejahr), Quellenkatalog (sechs Monate). Status je Eintrag: fällig, bald fällig (30 Tage), unbekannt, in Ordnung. Schreibt nichts, ohne Netz. |
| `fall_anlegen` | schreibend | Neuen Fall mit fester Kennung und Ordnerstruktur anlegen. |
| `fall_status_setzen` | schreibend | Fallstatus auf offen, ruhend oder abgeschlossen setzen. Der Fall bleibt am gleichen Ort. |
| `aufgabe_anlegen` | schreibend | Aufgabe in einem Fall anlegen. |
| `aufgabe_setzen` | schreibend | Aufgabe als erledigt oder wieder offen setzen, optional Fälligkeit oder Detail ändern. |
| `frist_eintragen` | schreibend | Frist oder Termin in einem Fall eintragen. Bestätigt nur, wenn die Rechnung das Fristende nennt, Auslöser, Rechtsgrundlage und Quelle da sind und kein Marker [PRÜFEN], [QUELLE], [BELEG] offen ist; die Bestätigung bekommt Prüfdatum und Prüfer. |
| `vorlagen_auflisten` | lesend | Schreibvorlagen unter 05 Vorlagen/Schreiben mit erster Zeile (interne Hinweise, Merkblatt). |
| `vorlage_fuellen` | schreibend | Entwurf aus einer Schreibvorlage anlegen: kopiert die Vorlage nach 06 Entwürfe des Falls und setzt Absender (Einstellungen oder Beteiligter mit Rolle Ich), Unterschrift, Datum und Fallkennung ein (Platzhalter 【ABSENDER】, 【ABSENDER_NAME】, 【DATUM】, 【R-0000】). Überschreibt nie. Alle anderen Platzhalter bleiben zum Ausfüllen. |
| `ereignis_eintragen` | schreibend | Ereignis in die Chronologie eines Falls eintragen. |
| `notiz_anlegen` | schreibend | Ordnungsnotiz in einem Fall anlegen. |
| `entwurf_erfassen` | schreibend | Entwurf in der Akte erfassen oder fortschreiben (Titel, Datei, Fassung, Status). Gleicher Titel = neue Fassung. Bei Status „geprüft“ oder „versandt“ wird die Datei (und eine gleichnamige .docx) als unveränderliche Kopie unter 06 Entwürfe/Fassungen eingefroren, mit Prüfsumme in der Akte; die Kopie bekommt eine eigene D-Kennung. |
| `bestand_abgleichen` | schreibend | Bestand eines Falls mit den Dateien abgleichen: neue Dateien in 01 bis 08 bekommen eine Kennung, im Finder verschobene werden über die Prüfsumme wiedergefunden, fehlende Ordnungsangaben werden in der Akte ergänzt. Der einzige Weg, auf dem neue Dateien registriert werden. |
| `dokument_ordnen` | schreibend | Ordnungsangaben eines Dokuments ändern (Titel, Datum, Art, Stand, Themen, Anlage, Personen, Verweise, Notiz, Textstand: direkt ausgelesen, OCR-erkannt, visuell geprüft, teilweise lesbar, nicht lesbar). Die Datei selbst bleibt unverändert. |
| `dokument_verschieben` | schreibend | Datei in einen anderen Aktenbereich einsortieren. Kennung und Inhalt bleiben, nichts wird überschrieben. |
| `journal_schreiben` | schreibend | Eintrag an das Journal eines Falls anhängen. |
| `sicherung_erstellen` | schreibend | Geprüfte ZIP-Sicherung des ganzen Projekts erstellen, mit Kopie an das zweite Ziel. |
| `sicherung_probe` | schreibend | Wiederherstellungsprobe: die letzte Sicherung in einem Zwischenordner entpacken, Akten gegen das Schema und alle Dateien gegen die Prüfsummen prüfen, Zwischenordner wieder entfernen. Die Mappe bleibt unberührt. |

</details>

## Vorlagen

<img src="../bilder/kapitel-vorlagen.svg" alt="Vorlagen: Schreiben mit Platzhaltern">

Vorlagen unter `05 Vorlagen/Schreiben/`: oben interne Hinweise (Frist,
Form, Adressat), unter der Trennlinie der Sendetext mit Platzhaltern 【 】.
Der Word-Erzeuger `.claude/recht/werkzeuge/docx_erzeugen.py` macht daraus
eine `.docx` und warnt vor offenen Platzhaltern und Markern.

<details>
<summary><b>Alle 10 Vorlagen</b></summary>

| Vorlage | Zweck |
|---|---|
| `Akteneinsicht.md` | Antrag auf Akteneinsicht bei Behörde, Gericht oder Arbeitgeber mit wählbarer Rechtsgrundlage |
| `Auskunft_DSGVO.md` | Auskunftsantrag nach Art. 15 DSGVO |
| `Briefkopf.md` | Grundgerüst für jedes Schreiben: Absender, Empfänger, Datum, Betreff |
| `Einspruch_Bussgeldbescheid.md` | Einspruch gegen einen Bußgeldbescheid, mit Akteneinsicht |
| `Einspruch_Steuerbescheid.md` | Einspruch gegen einen Steuerbescheid, mit Aussetzung der Vollziehung als Option |
| `Fristsetzung.md` | Aufforderung mit Frist (Nacherfüllung, Zahlung, Antwort) |
| `Klage_Arbeitsgericht.md` | Klage zum Arbeitsgericht, Grundgerüst mit Anträgen und Anlagen |
| `Klage_Zivilgericht.md` | Zivilklage zum Amts- oder Landgericht, Zahlungsantrag mit Zinsen, Versäumnisurteil, Zuständigkeit |
| `Strafanzeige.md` | Strafanzeige mit oder ohne Strafantrag, Sachverhalt, Beweismittel, Bitte um Bestätigung |
| `Widerspruch_Bescheid.md` | Widerspruch gegen einen Bescheid einer Behörde |

</details>

## Merkblätter

<img src="../bilder/kapitel-merkblaetter.svg" alt="Merkblätter: Verfahren am Volltext">

Merkblätter unter `04 Rechtsquellen/Verfahren/` beschreiben je Rechtsbehelf
Frist, Form, Pflichtinhalt, Adressat und Wirkung, jede Angabe mit Norm und
Prüfdatum. `/fallaufnahme` nennt daraus den Rechtsbehelf, `/entwurf` prüft
den Pflichtinhalt dagegen.

<details>
<summary><b>Alle 10 Merkblätter mit Prüfdatum</b></summary>

| Merkblatt | Inhalt | Letzte vollständige Prüfung |
|---|---|---|
| `04 Rechtsquellen/Verfahren/Akteneinsicht.md` | Akteneinsicht und Auskunft | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Dienstaufsichtsbeschwerde.md` | Dienstaufsichtsbeschwerde, Fachaufsichtsbeschwerde, Petition | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Einspruch_Bussgeldbescheid.md` | Einspruch gegen einen Bußgeldbescheid | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Einspruch_Steuerbescheid.md` | Einspruch gegen einen Steuerbescheid | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Klage_Arbeitsgericht.md` | Klage zum Arbeitsgericht | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Mahnverfahren.md` | Mahnverfahren (Mahnbescheid und Vollstreckungsbescheid) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Strafanzeige.md` | Strafanzeige und Strafantrag | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Widerspruch_Verwaltungsakt.md` | Widerspruch gegen einen Verwaltungsakt (Bescheid einer Behörde) | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Zivilklage.md` | Zivilklage vor dem Amtsgericht oder Landgericht | 17.09.2026 |
| `04 Rechtsquellen/Verfahren/Zustaendigkeit_finden.md` | Zuständige Stelle finden | 17.09.2026 |

</details>

> [!NOTE]
> Rechtsinhalte altern. Welche Feiertage, Merkblätter und Vorlagen mit
> welchem Stand mitgeliefert sind, wann sie zu prüfen sind und wie, steht in
> [`DOKU/md/Rechtsinhalte.md`](../DOKU/md/Rechtsinhalte.md). Vor der
> Verwendung in einem Fall gilt immer die Norm am amtlichen Volltext, nicht
> das Merkblatt.

## Befehle

<img src="../bilder/kapitel-befehle.svg" alt="Befehle: ohne Oberfläche">

<details>
<summary><b>Befehle ohne Oberfläche</b></summary>

| Befehl (im Ordner der Mappe) | Zweck |
|---|---|
| `Start.command`, `Start.sh`, `Start.bat` | Dienst starten und Oberfläche öffnen (macOS, Linux, Windows) |
| `python "06 Werkzeuge/einrichten_windows.py"` | nur Windows: `python3` in `.mcp.json`, `.claude/settings.json`, `.codex/config.toml` durch `python` ersetzen (macht `Start.bat` selbst); `--pruefen` nur melden |
| `python3 "06 Werkzeuge/dienst/server.py" --no-open` | Dienst ohne Browser starten; `--check` Bestand aller Fälle prüfen; `--backup` geprüfte Sicherung; `--probe` Wiederherstellungsprobe der letzten Sicherung; `--restore <ZIP> <neuer Ordner>` Sicherung in einen neuen Ordner entpacken und prüfen |
| `python3 "06 Werkzeuge/dienst/cli.py" liste` | alle Werkzeuge mit Parametern; danach `cli.py <werkzeug> feld=wert` |
| `python3 "06 Werkzeuge/dienst/cli.py" frist_berechnen start=2026-09-11 menge=1 einheit=monate land=BW` | Frist rechnen, mit Rechenweg |
| `python3 "06 Werkzeuge/dienst/cli.py" rechtsinhalte_pruefen` | welche Merkblätter, Feiertage und Quellen wieder am Volltext zu prüfen sind |
| `python3 "06 Werkzeuge/akte_schema.py" "02 Fälle/<Fall>/akte.json"` | Akte gegen das Datenmodell prüfen |
| `python3 "06 Werkzeuge/dienst/cli.py" vorlage_fuellen fall=R-0001 vorlage=Widerspruch_Bescheid` | Entwurf aus einer Vorlage unter 06 Entwürfe anlegen, mit Absender (Einstellungen oder Beteiligter „Ich“), Unterschrift, Datum; `vorlagen_auflisten` zeigt die Namen |
| `python3 ".claude/recht/werkzeuge/docx_erzeugen.py" <Entwurf.md>` | Word-Datei aus einem Entwurf, mit Vorabbericht (offene Marker, Platzhalter, Kopfzeilen, Anlagen); `--pruefen` nur der Bericht |
| `python3 ".claude/recht/werkzeuge/uebergabe_paket.py" R-0001 --empfaenger anwalt --vorschau` | Übergabepaket je Empfänger (anwalt: alles; gericht, behoerde, gegenseite, beratung: nur `--nur D0001,D0002`), erst Vorschau, dann ohne `--vorschau` als geprüfte ZIP mit Manifest außerhalb der Mappe |
| `python3 "06 Werkzeuge/verteilen.py"` | `AGENTS.md` und `.agents/skills/` aus `CLAUDE.md` und `.claude/skills/` erzeugen; `--pruefen` nur vergleichen |
| `python3 "06 Werkzeuge/dienst/pruefen.py"` | Funktionstest mit künstlichen Akten in einem Temp-Ordner |

</details>

---

<p align="center">
← <a href="ki.md">3 · Mit der KI arbeiten</a> · <a href="sicherheit.md">5 · Sicherheit und Grenzen</a> →<br>
<sub><a href="../README.md#impressum">Impressum</a> · <a href="../LICENSE">Lizenz AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Mitmachen</a></sub>
</p>
