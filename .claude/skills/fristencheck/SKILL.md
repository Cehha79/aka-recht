---
name: fristencheck
description: Fristkandidaten eines Falls prüfen und eintragen: Auslöser, Zugang, Rechtsgrundlage, Rechnung nach §§ 187, 188, 193 BGB, Prüfstatus. Bestätigt nur mit Nachweis. Für Bußgeld, Widerspruch, Kündigung, Klage, Zahlung, Auskunft und mehr.
arguments: [fall]
---

# Fristencheck für $fall

Lies `CLAUDE.md` und die Akte (`python3 "06 Werkzeuge/dienst/cli.py" fall_lesen fall=$fall`).

## Vorgehen

1. Kandidaten sammeln: aus Schreiben (Rechtsbehelfsbelehrung, gesetzte Fristen),
   aus dem Rechtsgebiet (Einspruch, Widerspruch, Klage, Verjährung, Ausschluss-
   fristen im Vertrag oder Tarif), aus eigenen Schreiben (selbst gesetzt).
   Kein pauschaler Fristschluss aus Wörtern wie „Bescheid“ oder „Strafzettel“.
2. Je Kandidat drei Dinge belegen: Auslöser (welches Ereignis), Zugang oder
   Bekanntgabe (Datum mit Nachweis, D-Kennung), Rechtsgrundlage (Norm mit
   Absatz, am Volltext gelesen, Fassung und Geltungszeitraum; sonst `[QUELLE: …]`).
3. Rechnen: `cli.py frist_berechnen start=JJJJ-MM-TT menge=… einheit=tage|wochen|monate|jahre ereignisfrist=true werktagsregel=true land=BW`.
   `land` ist das Bundesland des Ortes, an dem die Leistung zu erbringen ist
   (§ 193 BGB: Sitz des Gerichts, der Behörde oder des Empfängers), Kürzel
   wie BW, BY, NW; ohne Angabe gilt die Einstellung der Mappe. Nur
   landesweite Feiertage zählen; meldet die Antwort unter `regional` einen
   Hinweis, den Nutzer fragen, ob der Ort betroffen ist. Die Rechnung
   wörtlich übernehmen, das Bundesland darin nennen. Ob § 193 BGB
   (Verschiebung auf den nächsten Werktag) auf diese Frist anwendbar ist,
   gesondert prüfen und im Text sagen; bei Zweifel den rechnerischen Tag als
   sicheren Tag nennen.
4. Eintragen: `cli.py frist_eintragen fall=$fall datum=… titel=… art=gesetzlich|"selbst gesetzt"|"von Gegenseite gesetzt"|vorsorglich|Termin ausloeser=… rechtsgrundlage=… berechnung=… pruefstatus=offen|bestätigt|abgelaufen quelle=D…`
   - Gesetzliche Frist `bestätigt` nur, wenn Auslöser, Zugang und Grundlage belegt sind.
   - Kalenderfrist aus einem Schreiben (Gegenseite oder eigene): `art` „von
     Gegenseite gesetzt“ oder „selbst gesetzt“, `quelle` das Schreiben,
     `ausloeser` „Fristsetzung im Schreiben vom …“, `rechtsgrundlage` „Datum
     laut Schreiben, keine gesetzliche Frist“, `berechnung` „Kalendertag laut
     Schreiben“ plus Kontrollrechnung, wenn die Frist als Dauer angegeben ist.
     Liegt das Schreiben vor, darf sie `bestätigt` sein; der Zugang des Schreibens
     ist dann als Ereignis mit Annahme zu vermerken.
   - Vergangene, aber weiter relevante Fristen (z. B. Zahlungsziel für die
     Verzugsfrage): `pruefstatus=abgelaufen`. `erledigt` nur, wenn gewahrt oder
     gegenstandslos, mit Begründung im Feld `berechnung` oder im Journal.
   - Fehlt ein Nachweis: `offen` und eine Aufgabe „Nachweis besorgen“
     (`cli.py aufgabe_anlegen`), bei Unsicherheit über die Art zusätzlich eine
     `vorsorglich`e Frist mit dem frühesten denkbaren Datum.
   - Eine bestehende Frist ändern: `cli.py fall_lesen`, Eintrag anpassen,
     `cli.py akte_speichern` mit Revision.
5. Aufgaben „Frist prüfen“ aus der Fallaufnahme mit `cli.py aufgabe_setzen fall=$fall aufgabe=A… erledigt=true` schließen.
6. Journal: `cli.py journal_schreiben fall=$fall art=Arbeit titel="Fristen geprüft" text=…`.

## Ergebnis an den Nutzer

Tabelle: Frist; Datum; Auslöser; Grundlage; Rechnung kurz; Prüfstatus; was
noch fehlt. Nahe oder überschrittene Fristen zuerst und deutlich. Kein
„Frist gewahrt“ ohne Eingangsnachweis der Gegenseite oder des Gerichts.
