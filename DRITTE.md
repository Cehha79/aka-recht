# Fremde Anregungen und Bestandteile

AKA Recht steht unter der GNU Affero General Public License, Version 3 (`LICENSE`).
Diese Datei nennt, was von anderen übernommen wurde — auch dann, wenn nur der Gedanke
übernommen und der Code neu geschrieben wurde.

## Klotzkette, „claude-fuer-deutsches-recht“ und Einzel-Skills

**Urheber:** Klotzkette, Copyright 2026
**Quellen:** `github.com/Klotzkette/bautraegervertragspruefer-skill`,
`github.com/Klotzkette/arbeitszeugnispruefer-skill`,
`github.com/Klotzkette/claude-fuer-deutsches-recht`
**Lizenz:** `Apache-2.0 OR MIT`, nach Wahl des Nutzers — mit der AGPL-3.0 vereinbar
**Gesehen am:** 18.09.2026

| Was bei uns | Was dort | Art der Übernahme |
|---|---|---|
| `06 Werkzeuge/quellen_pruefen.py` | `scripts/check_legal_anchors.py` (Bauträgervertragsprüfer) | **Nur der Gedanke:** eine Liste amtlicher Stellen führen, jede verlinkte Quelle dagegen prüfen, und Reste aus einer Chat-Sitzung (`turn0search`, `oaicite`) als Fehler behandeln. Der Code ist eigenständig für AKA Recht geschrieben: eigene Hostliste, eigene Dateiauswahl, eigene Prüfung der Kopfzeile, kein gemeinsamer Quelltext |

Kein Quelltext aus diesen Repositories liegt in AKA Recht. Die Rechtsinhalte
(Merkblätter, Skills, Vorlagen) stammen ausschließlich aus eigener Arbeit am amtlichen
Volltext; sie wurden bewusst **nicht** übernommen, weil die Belegdisziplin dort eine
andere ist (Einzelheiten in `DOKU/md/TODO.md`).

Weiteres Material dieser Repositories liegt zur späteren Prüfung außerhalb des Projekts
unter `~/Projekte/Geplant/AKA Recht Material/` mit einer eigenen `HERKUNFT.md`. Wird
davon etwas übernommen, kommt es hier in die Tabelle.
