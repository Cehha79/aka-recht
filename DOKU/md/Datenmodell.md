# Datenmodell

*Stand: 16.09.2026*

## Aufgabe dieser Datei

Feldgenaue Beschreibung von `akte.json`, `bestand.json` und `JOURNAL.md`
(Schema-Version 1). STRUKTUR.md gibt den Überblick, hier stehen die Details.
Prüfbar mit `python3 "06 Werkzeuge/akte_schema.py" <akte.json>`.

## Grundsätze

- Eine `akte.json` je Fall, UTF-8, eingerückt, lesbar im Editor.
- Datumsfelder immer `JJJJ-MM-TT`. Die Oberfläche zeigt `TT.MM.JJJJ`.
- Kennungen sind stabil und werden nie neu vergeben: D0001 (Dokument),
  P01 (Beteiligter), V01 (Verfahren), E01 (Ereignis), F01 (Frist),
  A01 (Aufgabe), W01 (Entwurf), N01 (Notiz). Anlagenkennungen wie `K 13`
  oder `B 2` sind Text im Feld `anlage` und bleiben, wie sie im Schriftsatz
  stehen.
- Verweise gehen immer auf Kennungen, nie auf Dateipfade. Ein Verweis auf
  eine unbekannte Kennung ist ein Fehler.
- Feste Werte (Fehler bei Abweichung) und vorgeschlagene Werte (nur Warnung)
  sind unten je Feld markiert.
- Marker in Textfeldern: `[BELEG: …]`, `[PRÜFEN: …]`, `[QUELLE: …]`.

## fall

| Feld | Inhalt | Regel |
|---|---|---|
| id | R-0001 | fest: `R-` und mindestens vier Ziffern |
| titel | Kurzbezeichnung | Pflicht |
| untertitel | Beteiligte oder Zusatz | frei |
| bereich | Hauptbereich | vorgeschlagen: die neun Bereiche aus STRUKTUR.md plus Allgemein |
| themen | Liste von Stichworten | frei, wird aus den Dokumenten gesammelt |
| rolle | eigene Rolle, z. B. Arbeitnehmer, Betroffener, Mieter | Warnung wenn leer |
| ziel | was erreicht werden soll | Warnung wenn leer |
| rechtsordnung | DE | frei, bei Auslandsbezug Land und Sprache |
| status | offen, ruhend, abgeschlossen | fest |
| angelegt | Datum | Datum |
| angeheftet | Liste von D-Kennungen | Verweise |

## beteiligte

| Feld | Inhalt | Regel |
|---|---|---|
| id | P01 | fest |
| name | Name oder Stelle | Pflicht |
| rolle | Ich, Gegner, Gericht, Behörde, Anwalt, Zeuge, Stelle, Versicherung, Sonstige | vorgeschlagen |
| anschrift, kontakt | Text | frei |
| aktenzeichen | Zeichen dieser Stelle | frei |

## dokumente

Objekt mit D-Kennung als Schlüssel. Jede Datei im Bestand hat einen Eintrag,
Ordnungsangaben sind optional.

| Feld | Inhalt | Regel |
|---|---|---|
| pfad | relativ zum Fallordner | Pflicht, kein `/` am Anfang, kein `..` |
| titel | Anzeigetitel | frei, sonst Dateiname |
| datum | Dokumentdatum | Datum; ist kein Zugangsdatum |
| art | Schreiben, E-Mail, Foto, Vertrag, Bescheid, Urteil, Entwurf, Beleg, Übersicht, Gesetz, Sonstiges | vorgeschlagen |
| stand | Original, Entwurf, Versandt, Zugegangen, Historisch, Vermerk | fest |
| themen | Liste | frei |
| anlage | K 8, B 1 | frei |
| personen | Liste von P-Kennungen | Verweise |
| verweise | Liste von D-Kennungen | Verweise |
| notiz | Ordnungsnotiz | frei |

## verfahren

| Feld | Inhalt | Regel |
|---|---|---|
| id | V01 | fest |
| art | Arbeitsgericht, Bußgeldverfahren, Widerspruch, Mahnverfahren, Strafanzeige … | Pflicht, frei |
| stelle | P-Kennung des Gerichts oder der Behörde | Verweis |
| aktenzeichen | Zeichen der Stelle | frei |
| stand | Verfahrensstand in einem Satz | frei |
| ordner | Unterordner in 04 Verfahren | frei |

## ereignisse

| Feld | Inhalt | Regel |
|---|---|---|
| id | E01 | fest |
| datum | Datum | Pflicht |
| titel | Kurztitel | Pflicht |
| art | Zugang, Versand, Termin, Gespräch, Vorfall, Entscheidung, Vermerk, Arbeitsstand | vorgeschlagen |
| quelle | D-Kennung | Verweis |
| detail | Text | frei |

## fristen

| Feld | Inhalt | Regel |
|---|---|---|
| id | F01 | fest |
| datum | Fristende oder Termin | Pflicht |
| titel | Kurztitel | Pflicht |
| art | gesetzlich, selbst gesetzt, von Gegenseite gesetzt, vorsorglich, Termin | fest |
| ausloeser | Ereignis und Zugang, gern mit E-Kennung | Pflicht bei bestätigt |
| rechtsgrundlage | Norm mit Absatz und Gesetz | Pflicht bei bestätigt |
| berechnung | Rechnung als Text, sichtbar | Pflicht bei bestätigt |
| pruefstatus | offen, bestätigt, abgelaufen, erledigt | fest |
| quelle | D-Kennung | Verweis, Pflicht bei bestätigt |

Regel: `bestätigt` nur mit Auslöser, Rechtsgrundlage, Berechnung und Quelle.
Bei `art` Termin genügt ein Datum mit Quelle. Bei Kalenderfristen aus einem
Schreiben (von Gegenseite oder selbst gesetzt) ist das Schreiben die Quelle,
die Rechtsgrundlage lautet „Datum laut Schreiben“. `abgelaufen` ist vorbei,
bleibt aber sichtbar (etwa ein Zahlungsziel für die Verzugsfrage). `erledigt`
bedeutet: gewahrt oder gegenstandslos, mit Begründung in `berechnung` oder
im Journal.

## aufgaben

| Feld | Inhalt | Regel |
|---|---|---|
| id | A01 | fest |
| titel | Kurztitel | Pflicht |
| detail | Text | frei |
| faellig | Datum | Datum, leer erlaubt |
| erledigt | true oder false | fest |
| quelle | D-Kennung | Verweis |

## entwuerfe

| Feld | Inhalt | Regel |
|---|---|---|
| id | W01 | fest |
| titel | Kurztitel | Pflicht |
| datei | Pfad der Quelle (md, txt, html) relativ zum Fallordner | frei; Ausnahme von der Kennungsregel, weil die Datei beim Erfassen oft noch keine D-Kennung hat |
| fassung | 1, 2, 3 … | ganze Zahl ab 1 |
| status | in Arbeit, geprüft, versandt, verworfen | fest |
| versandt_als | D-Kennung des Versandbelegs | Pflicht bei versandt |

## kosten, notizen, quellen

| Block | Felder |
|---|---|
| kosten | datum, posten, betrag (Zahl in Euro), beleg (D-Kennung) |
| notizen | id N01, titel, text, datum |
| quellen | titel, url, geprueft (Datum), verwendung |

`quellen` sind fallbezogene Rechtsquellen mit Abrufdatum. Der gemeinsame
Zugangskatalog bleibt in `04 Rechtsquellen/Quellen.md`.

## bestand.json

Technische Datei, schreibt nur der Dienst.

```json
{
  "schema": 1,
  "dateien": {
    "D0038": {"pfad": "04 Verfahren/01 Teilkündigung/…JPG", "sha256_erst": "…", "sha256": "…", "alt": "alter Pfad", "erfasst": "2026-09-10"}
  },
  "verschiebungen": [
    {"id": "D0038", "von": "01 Eingang/…", "nach": "04 Verfahren/…", "zeit": "2026-09-22T10:00:00", "weg": "Oberfläche"}
  ]
}
```

`sha256_erst` ist die Prüfsumme beim ersten Einlesen und bleibt. `sha256` ist
der zuletzt gesehene Stand. Weichen beide ab, meldet die Bestandsprüfung eine
Änderung. Beim Umzug werden Dateien über `sha256_erst` wiedergefunden, auch
wenn ihr Pfad sich geändert hat.

## JOURNAL.md

Markdown, nur anhängen, neueste Einträge unten. Aufgaben und Fristen gehören
nicht ins Journal.

```text
## JJJJ-MM-TT · Art · Kurztitel
Text mit Bezug auf Kennungen wie D0012, F01, A03.
```

Arten: Eingang, Versand, Entscheidung, Gespräch, Termin, Arbeit, Vermerk.
Die Oberfläche liest die Überschriftzeile und kann danach filtern.

## Werkzeuge

| Werkzeug | Aufgabe |
|---|---|
| `06 Werkzeuge/dienst/cli.py` | alle Werkzeuge ohne laufenden Dienst, für Claude und Skripte |
| `06 Werkzeuge/akte_schema.py` | leere Akte erzeugen, Akte prüfen (Fehler, Warnungen); der Dienst ruft `validate()` vor jedem Speichern |
| `05 Vorlagen/Fallvorlage/` | Ordner 01 bis 08, leere akte.json, bestand.json, JOURNAL.md |
| `05 Vorlagen/Beispielakte/akte.json` | künstlicher Bußgeldfall, alle Blöcke gefüllt, Prüfung ohne Fehler |

