# Vorlagen für Entwürfe

Jede Vorlage hat zwei Teile: interne Hinweise oberhalb der Trennlinie `---`
(werden nicht in die Word-Datei übernommen) und den Sendetext darunter.
Platzhalter stehen in 【 】 und müssen ersetzt werden. Drei feste Platzhalter füllt
das Werkzeug `vorlage_fuellen` beim Anlegen des Entwurfs: 【ABSENDER】 (Name,
Anschrift, Kontakt aus den Einstellungen oder vom Beteiligten mit Rolle „Ich“
des Falls), 【ABSENDER_NAME】 (Unterschrift) und 【DATUM】 (Tag der Erstellung);
im Briefkopf außerdem 【R-0000】 (Fallkennung). Alle anderen bleiben zum Ausfüllen. Marker `[QUELLE: …]`,
`[PRÜFEN: …]`, `[BELEG: …]` bleiben stehen, bis sie am Original aufgelöst sind.
Der Word-Erzeuger (`werkzeuge/docx_erzeugen.py`) gibt vor dem Schreiben einen Vorabbericht aus: offene Marker (auch ohne Doppelpunkt), Platzhalter 【…】, interne Notizen im Sendetext, fehlende Kopfzeilen, Aktenzeichen, Anlagenliste, Antragssatz, fehlende Trennlinie; `--pruefen` liefert nur den Bericht.

Zu einigen Vorlagen gibt es ein Merkblatt unter `04 Rechtsquellen/Verfahren/`
(Rechtsbehelf, Frist, Form, Pflichtinhalt, Adressat, Quellen mit Stand). Die
Vorlage nennt es in der ersten Zeile; vor dem Entwurf lesen und den Pflichtinhalt
dagegen prüfen. Vorhanden: Einspruch_Steuerbescheid, Widerspruch_Verwaltungsakt,
Einspruch_Bussgeldbescheid, Klage_Arbeitsgericht, Zivilklage (Vorlage
Klage_Zivilgericht), Mahnverfahren (keine Vorlage: Für Mahnantrag,
Widerspruch und Vollstreckungsbescheid gilt Formularzwang, § 703c Abs. 2 ZPO;
das Merkblatt nennt Inhalt und Fristen), Strafanzeige, Akteneinsicht,
Dienstaufsichtsbeschwerde (keine Vorlage; formlos, Aufbau im Merkblatt
Abschnitt 3) und Zustaendigkeit_finden (Regeln und Verzeichnisse, keine
Vorlage).

Die Vorlagen setzen kein Rechtsgebiet voraus. Rechtsgrundlagen sind Beispiele
und immer am Volltext zu prüfen; Fassung und Geltungszeitraum gehören dazu.
