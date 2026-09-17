<p align="center">
<a href="../README.md"><img src="../bilder/reiter-start.svg" alt="Start"></a>
<a href="einrichten.md"><img src="../bilder/reiter-einrichten.svg" alt="Einrichten"></a>
<a href="ki.md"><img src="../bilder/reiter-ki.svg" alt="Mit der KI arbeiten"></a>
<a href="inhalt.md"><img src="../bilder/reiter-inhalt.svg" alt="Inhalt der Mappe"></a>
<a href="sicherheit.md"><img src="../bilder/reiter-sicherheit-aktiv.svg" alt="Sicherheit und Grenzen (diese Seite)"></a>
<a href="mitmachen.md"><img src="../bilder/reiter-mitmachen.svg" alt="Mitmachen und Lizenz"></a>
</p>

<p align="center"><b>Deutsch</b> · <a href="sicherheit.en.md">English</a></p>

<img src="../bilder/seite-sicherheit.svg" width="100%" alt="5 · Sicherheit und Grenzen: Zusagen · Sicherung · Geltungsbereich · Grenzen">

## Worauf du dich verlassen kannst

Eine Rechtsakte braucht mehr als Ordner. Diese Regeln setzt die Mappe
technisch durch und prüft sie im Funktionstest:

- **Lesen bleibt Lesen.** Kein lesendes Werkzeug fasst `akte.json`,
  `bestand.json` oder `zentrale.json` an. Neue Dateien registriert nur der
  Abgleich.
- **Kennungen kommen nie wieder.** Ein Zähler je Kennungsart merkt sich die
  höchste je vergebene Nummer; ein entfernter Eintrag wird nie durch einen
  neuen mit derselben Kennung ersetzt, Journalverweise bleiben eindeutig.
- **Geprüfte und versandte Fassungen sind eingefroren.** Beim Status
  „geprüft“ oder „versandt“ legt die Mappe eine nur lesbare Kopie unter
  `06 Entwürfe/Fassungen/` ab, mit Prüfsumme und eigener Kennung. Die
  Arbeitsdatei darf sich ändern, die Kopie nie.
- **Fristen werden nachgerechnet.** §§ 187, 188, 193 BGB mit sichtbarer
  Rechnung; Monatsende, Schaltjahr und Jahresfristen sind mit 20
  Grenzfällen geprüft. Ob eine Frist gilt, entscheidet der Rechner nicht.
- **Bestätigt heißt geprüft.** Eine Frist wird nur „bestätigt“, wenn die
  Rechnung das Fristende nennt, Beleg und Auslöser da sind und kein Marker
  `[PRÜFEN]`, `[QUELLE]` oder `[BELEG]` offen ist; die Bestätigung trägt
  Prüfdatum und Prüfer, ein Termin braucht die Ladung als Quelle.
- **Fremde Anlagen starten nichts.** „Öffnen“ ruft das Systemprogramm nur
  für bekannte Dokumentformate (PDF, Text, Office, Bilder, E-Mail, Ton,
  Video); Skripte, Programme, Webseiten, Archive und Unbekanntes werden nur
  im Dateimanager gezeigt, mit Hinweis.
- **Unsicheres bleibt sichtbar.** Ein Ereignis kann „ungefähr“, „Zeitraum“
  oder „unbekannt“ sein, statt einen erfundenen Tag zu tragen; eine Frist
  nennt ihr Verfahren und ihr Auslöser-Ereignis, und auf einem unsicheren
  Ereignis wird sie nicht bestätigt.
- **Übergaben enthalten nur, was hin soll.** Das Paket wird für einen
  benannten Empfänger gebaut, zeigt vorher jede Datei, bricht bei
  unbekannten Kennungen ab und wird gegen sein Manifest zurückgelesen.
- **Sicherungen sind nachweislich brauchbar.** Jede ZIP wird nach dem
  Schreiben zurückgelesen; „Wiederherstellung prüfen“ entpackt sie in
  einen Zwischenordner und prüft Akten und Prüfsummen.
- **Daten bleiben da, wo du sie legst.** Keine KI in der Mappe, kein Netz
  im Dienst. Was in einen Cloud-Ordner gesichert wird, lädt dein System
  hoch; was deine KI liest, verarbeitet ihr Anbieter.

## Sicherung

„Geprüfte Sicherung erstellen“ in der Oberfläche schreibt eine ZIP außerhalb
des Ordners und liest sie zurück. Ziel und zweites Ziel stehen in den
Einstellungen und werden vor der ersten Sicherung angezeigt.
„Wiederherstellung prüfen“ entpackt die letzte Sicherung in einen
Zwischenordner, prüft Akten und Prüfsummen und räumt ihn wieder ab. Echte
Wiederherstellung immer in einen neuen Ordner, nie über die laufende Mappe:
`python3 "06 Werkzeuge/dienst/server.py" --restore <ZIP> <neuer Ordner>`.
Ohne Oberfläche: `--check` prüft den Bestand, `--backup` sichert, `--probe`
prüft die letzte Sicherung.

Drei Ebenen, die nicht dasselbe sind: Die Mappe liegt auf deinem Rechner.
Liegt ein Sicherungsziel in iCloud Drive oder einem anderen Cloud-Ordner,
lädt das Betriebssystem die unverschlüsselte ZIP dorthin hoch. Und was deine
KI liest, verarbeitet deren Anbieter nach seinen Bedingungen; ein lokaler
MCP-Server ändert daran nichts.

## Geltungsbereich

Diese Fassung ist für deutsches Recht gebaut: Fristenrechner nach §§ 187,
188, 193 BGB mit den landesweiten Feiertagen aller 16 Bundesländer (Bundesland
in den Einstellungen wählen; regionale Feiertage einzelner Gemeinden zählen
nicht, einmalige Feiertage wie in Berlin 2025 und 2028 sind eingetragen),
Quellenkatalog mit deutschen amtlichen Angeboten, Schreibvorlagen und
Merkblätter für deutsche Verfahren.

Weitere Rechtsordnungen sind geplant, in dieser Reihenfolge: Österreich,
Schweiz, Türkei, danach England und Wales, Frankreich, USA, China, Russland
und weitere Länder. Bis dahin lässt sich die Mappe dort zwar zum Ordnen von
Unterlagen nutzen, Fristen und Vorlagen gelten aber nur für Deutschland.

Oberfläche, Vorlagen, Anleitung und Skills sind derzeit nur auf Deutsch.
Weitere Sprachen sind geplant, zuerst Türkisch, dann Englisch.

## Grenzen

> [!WARNING]
> Die Mappe ist kein Rechtsanwalt und gibt keine Rechtsberatung. Sie hilft
> beim Ordnen, Prüfen und Formulieren: Sie ordnet Unterlagen, rechnet Fristen
> nach §§ 187, 188, 193 BGB mit sichtbarer Rechnung, hält fest, was belegt ist
> und was nicht, und gibt deiner KI Anleitungen für Sachverhalt, Recherche,
> Entwürfe und Gegenprüfung. Ob eine Frist gilt, ob ein Schreiben so
> hinausgehen kann und was zu tun ist, prüfst du oder eine Fachanwältin, ein
> Fachanwalt. Der Autor kennt und prüft keine Angelegenheit eines Nutzers;
> alles läuft auf deinem Rechner, und was deine KI aus den Anleitungen macht,
> geschieht in deiner eigenen Sache und Verantwortung.

---

<p align="center">
← <a href="inhalt.md">4 · Inhalt der Mappe</a> · <a href="mitmachen.md">6 · Mitmachen und Lizenz</a> →<br>
<sub><a href="../README.md#impressum">Impressum</a> · <a href="../LICENSE">Lizenz AGPL-3.0</a> · <a href="../CONTRIBUTING.md">Mitmachen</a></sub>
</p>
