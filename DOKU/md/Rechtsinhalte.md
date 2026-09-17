# Rechtsinhalte

*Stand: 17.09.2026*

## Aufgabe dieser Datei

Verzeichnis aller Rechtsinhalte, die die Mappe selbst mitbringt: was sie
sind, woher sie stammen, welchen Stand sie haben, wann und wie sie zu prüfen
sind. Fallbezogene Recherchen stehen nicht hier, sondern in der jeweiligen
Akte unter 07 Recherche. Grundsatz aus REGELN Nr. 12: Ein Rechtsinhalt gilt
nur so lange als geprüft, wie sein Prüfdatum reicht; danach ist er ein
Kandidat, bis jemand ihn erneut am amtlichen Volltext liest.

## 1. Was es gibt

| Inhalt | Ort | Was es ist | Wer es nutzt |
|---|---|---|---|
| Feiertagstabelle | `06 Werkzeuge/dienst/fristen.py`, Funktion `feiertage()` | landesweite gesetzliche Feiertage aller 16 Länder, regionale nur als Hinweis, einmalige Feiertage gesondert | Fristenrechner (`frist_berechnen`, `land=`), Oberfläche, Skills |
| Fristenregeln | `fristen.py`, Funktion `berechne()` | §§ 187, 188, 193 BGB als Rechenregeln, mit Text der Rechnung | Fristenrechner |
| Merkblätter je Verfahrensart | `04 Rechtsquellen/Verfahren/*.md` | Rechtsbehelf, Frist mit Norm, Form, Pflichtinhalt, Adressat, Wirkung, Quellen mit Prüfdatum | `/fallaufnahme` (Rechtsbehelf nennen), `/entwurf` (Pflichtinhalt prüfen), Nutzer |
| Schreibvorlagen | `05 Vorlagen/Schreiben/*.md` | Textbausteine mit Platzhaltern und internen Hinweisen; Normen darin sind Beispiele | `/entwurf`, Nutzer |
| Zugangskatalog | `04 Rechtsquellen/Quellen.md` | Adressen amtlicher Angebote (Gesetze, Rechtsprechung, Landesportale), keine Gesetzestexte | Oberfläche (Seite Rechtsquellen), `/recherche-de` |
| Beispielakte | `05 Vorlagen/Beispielakte/` | erfundener Kündigungsfall mit § 4 KSchG und § 38 SGB III als Beispiel | „Beispielfall laden“ |

## 2. Stand je Inhalt

### 2.1 Feiertagstabelle (geprüft 16.09.2026)

„Volltext“ heißt: der Paragraf des Landesgesetzes wurde auf dem amtlichen
Portal oder im Gesetzblatt gelesen. Stand 16.09.2026 spät: 15 von 16 Ländern
am Volltext (HE, NW, RP, SL, ST, TH, BE am Abend im Browser nachgelesen; die
frühere Stütze „Übersicht BMI 2018“ ist damit überall abgelöst). Nur Bremen
stützt sich noch auf eine alte Fassung des Portals.

| Land | Zusätzliche Feiertage in der Tabelle | Beleg | Offen |
|---|---|---|---|
| BW | Heilige Drei Könige, Fronleichnam, Allerheiligen | Volltext FTG BW (16.09.2026) | – |
| BY | Heilige Drei Könige, Fronleichnam, Allerheiligen; regional Mariä Himmelfahrt, Friedensfest | Volltext FTG BY Art. 1 (16.09.2026) | – |
| BE | Frauentag (8. März) seit 2019; einmalig 08.05.2025 und 17.06.2028 | Volltext § 1 FeiertG BE, gesetze.berlin.de (Fassung vom 10.07.2024, gültig 09.05.2025 bis 17.06.2028; Nr. 11 nennt den 17.06.2028; der 08.05.2025 stand in der Fassung 21.07.2024 bis 08.05.2025); GVBl. Berlin 2024 S. 460 | – |
| BB | Reformationstag | Volltext § 2 FTG, bravors.brandenburg.de (Gesetz vom 21.03.1991, geändert 30.04.2015) | – |
| HB | Reformationstag seit 2018 | Transparenzportal zeigt nur Fassungen bis 2017 mit „31. Oktober 2017“; Änderungsgesetz Brem.GBl. 2018 S. 302 nur aus Pressemeldungen | `[QUELLE: Brem.GBl. 2018 S. 302 am Volltext lesen]` |
| HH | Reformationstag seit 2018 | Volltext § 1 FeiertG HA, landesrecht-hamburg.de, gültig ab 21.03.2018 | – |
| HE | Fronleichnam | Volltext § 1 HFeiertagsG, rv.hessenrecht.hessen.de (Bek. 29.12.1971, Textnachweis ab 01.01.2004) | – |
| MV | Frauentag (8. März) seit 2023, Reformationstag | Volltext § 2 FTG M-V, landesrecht-mv.de, gültig ab 13.07.2022 | – |
| NI | Reformationstag seit 2018 | Volltext § 2 NFeiertagsG, voris (Fassung ab 29.06.2018) | – |
| NW | Fronleichnam, Allerheiligen | Volltext § 2 Feiertagsgesetz NW, recht.nrw.de (Bek. 23.04.1989, Fassung gültig ab 01.01.2000) | – |
| RP | Fronleichnam, Allerheiligen | Volltext § 2 LFtG, landesrecht.rlp.de (Gesetz vom 15.07.1970, Textnachweis ab 01.10.2001; Abs. 2 erlaubt einmalige Feiertage durch Verordnung) | – |
| SL | Fronleichnam, Mariä Himmelfahrt, Allerheiligen | Volltext § 2 SFG, recht.saarland.de (Fassung vom 18.11.2010, gültig ab 24.12.2010; Abs. 2 erlaubt einmalige Feiertage durch Verordnung) | – |
| SN | Reformationstag, Buß- und Bettag; regional Fronleichnam | Volltext § 1 SächsSFG, revosax (PDF, Fassung vom 21.12.2010; Änderung 23.04.2025 betrifft § 1 nicht `[PRÜFEN]`) | – |
| ST | Heilige Drei Könige, Reformationstag | Volltext § 2 FeiertG LSA, landesrecht.sachsen-anhalt.de (Bek. 25.08.2004, gültig ab 01.01.2004) | – |
| SH | Reformationstag seit 2018 | Volltext § 2 SFTG, gesetze-rechtsprechung.sh.juris.de, gültig ab 30.03.2018 | – |
| TH | Reformationstag, Weltkindertag (20. September) seit 2019; regional Fronleichnam | Volltext § 2 ThürFGtG, landesrecht.thueringen.de (Fassung gültig ab 27.03.2019 mit Weltkindertag; Vorfassung 01.05.2008 bis 26.03.2019; Abs. 2: Fronleichnam durch Verordnung für Gemeinden mit überwiegend katholischer Bevölkerung) | – |

Bundesweit einmalig: 31.10.2017 (Reformationsjubiläum) ist eingetragen.
Länder können nach ihren Gesetzen weitere einmalige Feiertage durch
Verordnung erklären (etwa § 2 Abs. 2 SFTG, § 2 Abs. 3 FTG M-V); solche
Verordnungen sind nicht erfasst.

### 2.2 Merkblätter

Alle zehn am 17.09.2026 von einer zweiten Instanz (drei unabhängige
Prüfer) am Rohtext von gesetze-im-internet.de gegengeprüft, Befunde
eingearbeitet. Landesrecht war per Skript nicht prüfbar.
Fassungen seit 17.09.2026 nach dem Vollzitat des Portals (Abschnitt 4,
Nr. 2).

| Merkblatt | Normen | Rechtsstand (Vollzitat) | Geprüft | Offen |
|---|---|---|---|---|
| Einspruch Steuerbescheid | §§ 347, 350, 355, 356, 357, 361, 362, 367, 108, 110, 122, 122a, 172, 87a AO; Art. 97 § 28 EGAO; § 47 FGO; §§ 187, 188 BGB | AO i. d. F. v. 23.01.2025, zuletzt geändert 03.07.2026; EGAO 29.06.2026; FGO 29.06.2026 (Stand-Zeile 22.12.2025) | 17.09.2026 (Fristbeispiel berichtigt: § 188 Abs. 2 BGB ergibt den Sonntag, § 108 Abs. 3 AO den Montag) | AEAO zu §§ 172, 357, § 87a Abs. 6 bis 8 AO, Vorfassung § 122a, BFH III R 26/14, Kostenerstattung, Kommunalabgaben |
| Widerspruch Verwaltungsakt | §§ 57, 58, 60, 68, 69, 70, 72, 73, 74, 79, 80 VwGO; §§ 3a, 29, 31, 41, 80 VwVfG; § 222 ZPO; § 15 AGVwGO BW, § 41 LVwVfG BW | VwGO 20.05.2026 (Stand-Zeile 23.04.2026); VwVfG 22.07.2026 (Stand-Zeile 15.07.2024); AGVwGO BW 18.03.2025 (gültig ab 01.01.2026); LVwVfG BW 28.01.2025 | 17.09.2026 (De-Mail aus § 3a Abs. 3 gestrichen, § 80 Abs. 6, Fristbeispiel) | Landesrecht der übrigen Länder und zweite Lesung BW, § 80 LVwVfG BW, VwZG, § 9a OZG, Gebührengesetze, Rechtsprechung |
| Klage Arbeitsgericht | §§ 2, 9, 11, 11a, 12a, 46, 46c, 46g, 48, 54, 59, 61, 61a, 61b, 64, 66 ArbGG; §§ 12, 13, 17, 130, 130a, 167, 222, 253, 330, 496 ZPO; §§ 1, 4, 5, 7 KSchG; §§ 6, 9, 11, 42 GKG, KV 8210, 8211; §§ 17a, 17b GVG; § 15 AGG | ArbGG 20.05.2026 (Stand-Zeile 27.04.2026); ZPO 20.05.2026 (Stand-Zeile 22.12.2025); KSchG 14.06.2021; GKG 20.05.2026; AGG 22.12.2023 | 17.09.2026 (Fünf-Monats-Grenze § 66 Abs. 1 S. 2, Ausschluss verspäteten Vorbringens § 61a Abs. 5) | § 269 ZPO, § 16 ArbGG, § 1 Abs. 1 und § 23 KSchG, § 130 BGB, § 168 SGB IX, § 17 MuSchG, § 159 SGB III, Rechtsprechung |
| Zivilklage | §§ 3, 12, 13, 17, 29, 78, 79, 91, 93, 130, 130a, 130d, 167, 222, 233, 234, 253, 269, 271, 275, 276, 278, 330, 331, 338, 339, 495a, 496, 511, 517 ZPO; §§ 23, 71, 72, 119 GVG; §§ 12, 34 GKG, KV 1210, 1211; §§ 195, 199, 204 BGB; § 15a EGZPO | ZPO 20.05.2026; GVG 02.07.2026 (Stand-Zeile 09.01.2026); GKG 20.05.2026; BGB 23.07.2026; EGZPO 08.12.2025 (Wertgrenzen: AG 10.000 Euro, § 495a und Berufung 1.000 Euro, am Rohtext bestätigt) | 17.09.2026 (§ 71 Abs. 2 GVG, Auslandsfristen, § 234 Abs. 1 S. 2) | §§ 29a, 29c, 32, 38, 92, 114 ff., 139 ZPO, § 43 GKG, §§ 269, 270, 288, 438, 548, 634a BGB, RVG, Landesschlichtungsgesetze |
| Mahnverfahren | §§ 167, 222, 338, 339, 688 bis 697, 699 bis 703c, 794 ZPO; § 12 Abs. 3, § 34 GKG, KV 1100 mit Anm. zu 1210; § 204 BGB | ZPO 20.05.2026; GKG 20.05.2026; BGB 23.07.2026 (Mindestgebühr KV 1100: 38 Euro, am Rohtext bestätigt) | 17.09.2026 (Ende der Verjährungshemmung § 204 Abs. 2 BGB, Online-Antrag ohne Unterschrift) | §§ 703a, 703d, 707, 719, 750 ff. ZPO, Landesverordnung zentrales Mahngericht, MahnVordrV, Rechtsprechung zur Individualisierung; keine Vorlage (Formularzwang) |
| Strafanzeige | §§ 153, 153a, 158, 160, 163, 170, 171, 172, 374, 376, 379, 379a, 380, 406d, 406e, 406h, 406i, 471 StPO; §§ 77, 77b, 77d, 145d, 164, 194, 230, 247, 303c StGB | StPO 03.07.2026 (Stand-Zeile 23.02.2026); StGB 20.03.2026 | 17.09.2026 („Sachbeschädigung unter Angehörigen“ berichtigt, Klageerzwingung, Kostenrisiko Privatklage) | § 78 StGB, § 123 Abs. 2 StGB, §§ 377, 378, 381 ff., 395 ff., 403 ff. StPO, Landesrecht zu Schiedsstellen und Online-Wachen, SGB XIV |
| Akteneinsicht | § 29 VwVfG; § 25 SGB X; § 364 AO; § 49 OWiG; §§ 147, 406e StPO; § 299 ZPO; § 83 BetrVG; Art. 12, 15, 77, 79 DSGVO; §§ 1, 7, 9 IFG; § 12 GBO; § 9 HGB | VwVfG 22.07.2026 (Stand-Zeile 15.07.2024); SGB X 21.07.2026; AO 03.07.2026; StPO 03.07.2026; ZPO 20.05.2026; BetrVG 19.07.2024; IFG 19.06.2020; GBO 22.06.2026; HGB 04.02.2026; DSGVO EUR-Lex | 17.09.2026 (§ 406e Abs. 3, Verweis auf einen nicht vorhandenen Abs. 6 entfernt, IFG-Frist als Soll-Frist) | Landes-VwVfG und LIFG, § 25 Abs. 5 SGB X, § 44a VwGO, § 406e Abs. 4, § 32f StPO, § 241 Abs. 2 BGB, JVKostG, Rechtsprechung BFH und BAG |
| Dienstaufsichtsbeschwerde | Art. 17 GG; § 26 DRiG; § 73 BRAO; § 62 OWiG; § 164 StGB | GG 22.03.2025; DRiG 22.10.2024; BRAO 22.12.2025 | 17.09.2026 (§ 73 Abs. 3 und 5 BRAO, Marker zu E-Mail und anonymen Beschwerden) | BVerfG zur Bescheidungspflicht, Art. 45c GG, Petitionsgesetze, Disziplinarrecht, §§ 146, 147 GVG, § 87 SGB IV, § 191f BRAO, § 98 StPO, § 43 VwGO |
| Zuständigkeit finden | § 52 VwGO; § 57 SGG; § 38 FGO; §§ 36, 50, 52, 68 OWiG; § 143, §§ 17a, 17b, § 71 GVG; §§ 7, 8 StPO; §§ 29a, 281 ZPO; Verweise auf die anderen Merkblätter; sieben amtliche Verzeichnisse (Abruf geprüft) | VwGO 20.05.2026; SGG 20.05.2026; FGO 29.06.2026; OWiG 22.12.2025; GVG 02.07.2026; StPO 03.07.2026 | 17.09.2026 (Jahresfrist bei fehlender Belehrung gilt nicht für Bußgeldbescheide, Verweisung nur beim Rechtsweg von Amts wegen) | § 52 Nr. 4 VwGO, Landesverordnungen, Behördenfinder des Bundes (nicht erreichbar) |
| Einspruch Bußgeldbescheid | §§ 18, 31, 33, 46, 49, 50, 51, 52, 55, 56, 62, 66 bis 74, 79, 80, 89, 105, 109, 110c OWiG; §§ 32a, 32d, 43, 44, 45, 297, 298, 300, 302, 303, 410, 411 StPO; §§ 25, 25a, 26 StVG | OWiG 22.12.2025; StPO 03.07.2026 (Stand-Zeile 23.02.2026); StVG 12.05.2026 (§ 26 Abs. 3 StVG: sechs Monate, Übergangsrecht offen) | 17.09.2026 (Zustellung an den Verteidiger, § 52 OWiG, Fahrverbotsbeginn § 25 Abs. 3 StVG) | VwZG Bund und Länder, § 107, § 111 OWiG, §§ 35a, 341, 344, 345 StPO, GKG-Kostenverzeichnis, BKatV, §§ 4, 28 StVG, Änderungshistorie § 26 Abs. 3 StVG, Rechtsprechung (Fax, E-Mail, Messunterlagen, Beschränkung des Einspruchs) |

### 2.3 Schreibvorlagen

Zehn Vorlagen vom 16.09.2026 (Briefkopf, Einspruch Bußgeldbescheid,
Widerspruch Bescheid, Fristsetzung, Auskunft DSGVO, Klage Arbeitsgericht,
Einspruch Steuerbescheid, Klage Zivilgericht, Strafanzeige, Akteneinsicht).
Die Normen darin tragen `[QUELLE]`, wo sie nicht am Volltext gelesen wurden.
Am 17.09.2026 gegen die berichtigten Merkblätter durchgesehen: nur die
Formzeile der Vorlage Widerspruch_Bescheid war zu ergänzen (§ 3a Abs. 3
VwVfG ohne De-Mail, § 9a Abs. 5 OZG über § 70 Abs. 1 VwGO).
Zehn Merkblätter: Einspruch Steuerbescheid, Widerspruch Verwaltungsakt,
Einspruch Bußgeldbescheid, Klage Arbeitsgericht, Zivilklage, Mahnverfahren
(ohne Vorlage, Formularzwang), Strafanzeige, Akteneinsicht,
Dienstaufsichtsbeschwerde (ohne Vorlage, formlos) und Zuständigkeit finden
(Regeln und Verzeichnisse).

## 3. Wann prüfen

| Inhalt | Rhythmus | Auslöser außer der Reihe |
|---|---|---|
| Feiertagstabelle | einmal im Jahr im Dezember für das Folgejahr | Presse zu neuen Feiertagen (etwa 8. Mai, Frauentag, Weltkindertag), Landtagsbeschluss, jede Frist, deren Ende auf einen zweifelhaften Tag fällt |
| Merkblätter | einmal im Jahr, dazu vor jeder Verwendung in einem Fall die Fassung der Norm am Volltext | Änderungsgesetz zur AO, FGO, VwGO, OWiG; neue BFH- oder BGH-Entscheidung zum Verfahren |
| Schreibvorlagen | bei jeder Änderung des zugehörigen Merkblatts | Rückmeldung aus einem Fall, dass ein Baustein nicht passte |
| Zugangskatalog | halbjährlich: jede Adresse einmal aufrufen | Portal antwortet nicht mehr |
| Fristenregeln (§§ 187 ff. BGB) | bei jeder Änderung des BGB-Allgemeinen Teils | Prüfvermerk in einem Fall widerspricht dem Rechner |

Der Prüfrhythmus ist eine Vorgabe für die Pflege, keine Garantie. Wer die
Mappe nutzt, prüft die Norm für seinen Fall selbst (README „Grenzen“).

## 4. Wie prüfen und ändern

1. Amtliche Quelle öffnen: Bundesrecht auf gesetze-im-internet.de, Landesrecht
   auf dem Portal des Landes (Adressen in `Quellen.md`), Gesetzblatt für
   Änderungen. Keine Sekundärquelle als Beleg; Wikipedia und Verlagsseiten
   sind nur Hinweise, wo zu suchen ist.
2. Fassung und Geltungszeitraum notieren („gültig ab“, „zuletzt geändert
   durch“). Bei Feiertagen auch einmalige und regionale Tage prüfen.
   gesetze-im-internet.de zeigt zwei Angaben: das Vollzitat (jüngste
   Änderung, auch wenn „textlich nachgewiesen, dokumentarisch noch nicht
   abschließend bearbeitet“) und die Zeile „Stand“ (nur dokumentarisch
   fertig eingearbeitete Änderung). Regel seit 17.09.2026: immer das
   Vollzitat nennen und, wenn die Stand-Zeile älter ist, diese mit dem
   Hinweis „dokumentarisch noch nicht abschließend bearbeitet“ dazusetzen.
   Der Paragraf selbst wird immer am rohen Seitentext (curl) gelesen, nie
   aus einer Zusammenfassung übernommen.
3. Änderung an genau einer Stelle: Feiertage in `fristen.py` (Kommentarzeile
   mit Quelle und Datum daneben), Merkblatt im Abschnitt „Geprüfte Quellen“,
   Vorlage in den internen Hinweisen. Prüfdatum im Kopf der Datei setzen.
4. Funktionstest laufen lassen (`pruefen.py`); Feiertage haben eigene
   Prüfpunkte (Fronleichnam BW und BE, 08.05.2025 BE gegen BB).
5. Diese Datei fortschreiben (Tabelle in Abschnitt 2), dann
   `python3 DOKU/ansicht_bauen.py`.
6. Was nicht am Volltext gelesen wurde, bleibt mit `[QUELLE: …]` markiert,
   auch wenn es „allgemein bekannt“ ist.

## 5. Bekannte Eigenheiten der Portale (16.09.2026)

- Die juris-Landesportale (Berlin, Hamburg, Hessen, Mecklenburg-Vorpommern,
  Rheinland-Pfalz, Saarland, Sachsen-Anhalt, Schleswig-Holstein, Thüringen,
  Baden-Württemberg) liefern per Skript nur den Seitentitel. Im Browser
  funktionieren sie über die Suchadresse `…/search?query=<Suchtext>` (Kürzel
  je Portal: bsbw, bsbe, bshe, bsrp, bssl, bsst, bsth) und über den
  Permalink `…/perma?j=<juris-Kürzel>_!_<Paragraf>` (etwa `FeiertG_HE_!_1`,
  `FeiertG_TH_!_2`, `FeiertG_BE_!_1`, `VwGOAG_BW_!_15`); für Rheinland-Pfalz
  griff kein geratenes Kürzel, dort über die Suche gehen. Ein Treffer öffnet
  sich nur durch Klick auf die Koordinaten des Titels, nicht über die
  Element-Referenz. Feste Dokumentadressen leiten auf die Startseite um. Die
  Chrome-Erweiterung braucht je Domain eine Freigabe (seit 16.09.2026 für
  alle genannten erteilt).
- recht.nrw.de (kein juris) hat seit 2026 eine neue Oberfläche: Suche über
  `https://recht.nrw.de/suche/lra/?s=<Suchtext>`, Gesetze unter
  `/lrgv/gesetz/<datum>-<titel>/`, der ganze Gesetzestext auf einer Seite;
  beim ersten Aufruf ein Cookie-Dialog (nur notwendige Cookies wählen).
- bravors.brandenburg.de, voris (Niedersachsen) und revosax (Sachsen, PDF)
  liefern per Abruf den Text; recht.nrw.de nicht.
- landesrecht-bw.de (juris): per Skript nur der Titel. Im Browser führt der
  Permalink `https://www.landesrecht-bw.de/perma?j=<Kürzel>_!_<Paragraf>`
  direkt zur gültigen Fassung (Kürzel wie im Portal, etwa `VwGOAG_BW`,
  `VwVfG_BW`); die Schnellsuche mit dem juris-Kürzel („§ 15 VwGOAG BW“)
  listet alle Fassungen mit Geltungszeitraum, die Suche mit der amtlichen
  Abkürzung („§ 15 AGVwGO“) nur Rechtsprechung.
- Das Transparenzportal Bremen zeigte am 16.09.2026 für das Feiertagsgesetz
  nur Fassungen bis 2017, obwohl es „zuletzt geändert 02.09.2025“ meldet.
- Das BMF-Portal zum Anwendungserlass AO (ao.bundesfinanzministerium.de)
  blockiert Skriptabrufe; juris.bundesfinanzhof.de war nicht erreichbar.
