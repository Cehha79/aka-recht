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

### 2.1 Feiertagstabelle (geprüft 16.09.2026, Bremen 17.09.2026)

„Volltext“ heißt: der Paragraf des Landesgesetzes wurde auf dem amtlichen
Portal oder im Gesetzblatt gelesen. Stand 17.09.2026: alle 16 Länder am
Volltext (HE, NW, RP, SL, ST, TH, BE am 16.09.2026 abends, Bremen am
17.09.2026 im Browser nachgelesen; die frühere Stütze „Übersicht BMI 2018“
ist damit überall abgelöst). Keine Abweichung von der Tabelle in `fristen.py`.

| Land | Zusätzliche Feiertage in der Tabelle | Beleg | Offen |
|---|---|---|---|
| BW | Heilige Drei Könige, Fronleichnam, Allerheiligen | Volltext FTG BW (16.09.2026) | – |
| BY | Heilige Drei Könige, Fronleichnam, Allerheiligen; regional Mariä Himmelfahrt, Friedensfest | Volltext FTG BY Art. 1 (16.09.2026) | – |
| BE | Frauentag (8. März) seit 2019; einmalig 08.05.2025 und 17.06.2028 | Volltext § 1 FeiertG BE, gesetze.berlin.de (Fassung vom 10.07.2024, gültig 09.05.2025 bis 17.06.2028; Nr. 11 nennt den 17.06.2028; der 08.05.2025 stand in der Fassung 21.07.2024 bis 08.05.2025); GVBl. Berlin 2024 S. 460 | – |
| BB | Reformationstag | Volltext § 2 FTG, bravors.brandenburg.de (Gesetz vom 21.03.1991, geändert 30.04.2015) | – |
| HB | Reformationstag seit 2018 | Volltext § 2 Abs. 1 Buchst. j FeiertG BR (Gesetz über die Sonn-, Gedenk- und Feiertage vom 12.11.1954, SaBremR 113-c-1), transparenz.bremen.de, aktuelle Gesamtausgabe gültig ab 30.06.2025; § 2 in dieser Fassung seit 29.06.2018; Änderungshistorie Nr. 18: „§§ 2 und 14 geändert durch Gesetz vom 26.06.2018 (Brem.GBl. S. 302)“; Vorfassung 21.11.2017 bis 28.06.2018 (17.09.2026) | – |
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
eingearbeitet. Landesrecht war per Skript nicht prüfbar. Am 17.09.2026
danach die „Nicht gelesen“-Listen nachgelesen: 60 Bundesnormen am Rohtext
(VwZG §§ 1 bis 10, ZPO §§ 177 bis 182, § 78 bis 78c StGB, Prozesskostenhilfe,
Gerichtsstände, Verjährung je Vertragsart, Vollstreckungseinstellung,
Nebenklage, Adhäsion, Privatklage, Aufsicht u. a.) und im Browser § 15
AGVwGO BW, § 41 LVwVfG BW (zweite Lesung) sowie §§ 2 bis 4 LVwZG BW. Befund
der zweiten Lesung: Die ab 01.01.2026 gültige Fassung des § 15 AGVwGO heißt
in der Fassungsliste des Portals „vom 02.07.2024“, nicht „vom 18.03.2025“;
der Wortlaut war richtig wiedergegeben. Was offen bleibt, steht je
Merkblatt in der Liste „Nicht gelesen“ (vor allem Rechtsprechung,
Landesrecht außer BW, Verwaltungsanweisungen). Am 17.09.2026 abends die übrigen Bundesnormen dieser Listen am Rohtext gelesen
und eingearbeitet (rund 70 Paragrafen: Prozesskostenhilfe, Privatklage, Nebenklage,
Adhäsion, Punkte und Regelsätze, Auslandszustellung, § 9a OZG, § 87a AO u. a.);
zwei Vorlagen nachgezogen (Klage_Zivilgericht, Einspruch_Bussgeldbescheid).
Am 17.09.2026 abends Landesrecht Baden-Württemberg im Browser am Landesportal gelesen und
in neun Merkblätter eingearbeitet (LVwVfG, LIFG, Landesverfassung, Petitionsausschuss,
Bürgerbeauftragte, Gemeindeordnung, KAG, Zuständigkeitsverordnung Justiz, OWiZuVO, AGGVG;
Schlichtungsgesetz außer Kraft), dazu zwei Entscheidungen des Landesportals (OLG Stuttgart,
LG Mannheim). Andere Länder bleiben als `[QUELLE]` markiert.
Fassungen seit 17.09.2026 nach dem Vollzitat des Portals (Abschnitt 4,
Nr. 2).

| Merkblatt | Normen | Rechtsstand (Vollzitat) | Geprüft | Offen |
|---|---|---|---|---|
| Einspruch Steuerbescheid | §§ 347, 350, 355, 356, 357, 361, 362, 367, 108, 110, 122, 122a, 172, 87a (Abs. 1 bis 8) AO; Art. 97 § 28 EGAO; § 47 FGO; §§ 187, 188 BGB; § 1 Abs. 2 AO; § 3 KAG BW | AO i. d. F. v. 23.01.2025, zuletzt geändert 03.07.2026; EGAO 29.06.2026; FGO 29.06.2026 (Stand-Zeile 22.12.2025); KAG BW § 3 gültig ab 12.12.2020 | 17.09.2026 (Fristbeispiel berichtigt: § 188 Abs. 2 BGB ergibt den Sonntag, § 108 Abs. 3 AO den Montag) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | AEAO zu §§ 172, 357, Vorfassung § 122a, BFH III R 26/14, Kostenerstattung, Kommunalabgabengesetze außer BW |
| Widerspruch Verwaltungsakt | §§ 57, 58, 60, 68, 69, 70, 72, 73, 74, 79, 80 VwGO; §§ 3a, 29, 31, 41, 80 VwVfG; § 222, §§ 177 bis 181 ZPO; §§ 1 bis 5, 8, 10 VwZG; § 15 AGVwGO BW, § 41 LVwVfG BW, §§ 2 bis 4 LVwZG BW; § 9 VwZG; § 9a OZG; § 80 LVwVfG BW | VwGO 20.05.2026 (Stand-Zeile 23.04.2026); VwVfG 22.07.2026 (Stand-Zeile 15.07.2024); VwZG 03.07.2026 (Stand-Zeile 15.07.2024); AGVwGO BW gültig ab 01.01.2026 (Fassungsliste: vom 02.07.2024); LVwVfG BW gültig ab 07.02.2025; LVwZG BW 03.07.2007; OZG 22.07.2026 (Stand-Zeile 19.07.2024) | 17.09.2026 (De-Mail aus § 3a Abs. 3 gestrichen, § 80 Abs. 6, Fristbeispiel; förmliche Zustellung; BW zweite Lesung, Fassungsangabe § 15 AGVwGO berichtigt) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Landesrecht der übrigen Länder, Gebührengesetze, Rechtsprechung, Onlinezugangsgesetze der Länder |
| Klage Arbeitsgericht | §§ 2, 9, 11, 11a, 12a, 46, 46c, 46g, 48, 54, 59, 61, 61a, 61b, 64, 66 ArbGG; §§ 12, 13, 17, 114, 115, 117, 130, 130a, 167, 222, 253, 269, 330, 496 ZPO; §§ 1, 4, 5, 7, 23 KSchG; §§ 6, 9, 11, 42 GKG, KV 8210, 8211; §§ 17a, 17b GVG; § 15 AGG; § 16 ArbGG; § 130 BGB; § 168 SGB IX; § 17 MuSchG; § 159 SGB III; §§ 116, 118 bis 127 ZPO; § 24 KSchG; § 174 SGB IX | ArbGG 20.05.2026 (Stand-Zeile 27.04.2026); ZPO 20.05.2026 (Stand-Zeile 22.12.2025); KSchG 14.06.2021; GKG 20.05.2026; AGG 22.12.2023; BGB 23.07.2026; SGB IX 24.07.2026; MuSchG 22.12.2025; SGB III 24.07.2026 | 17.09.2026 (Fünf-Monats-Grenze § 66 Abs. 1 S. 2, Ausschluss verspäteten Vorbringens § 61a Abs. 5; Klagefrist auch im Kleinbetrieb, Sonderkündigungsschutz, Sperrzeit) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) | Fachliche Weisungen zu § 159 SGB III, Rechtsprechung (Zugang, Fax, „demnächst“, Sperrzeit, Weiterbeschäftigung), § 78 ArbGG |
| Zivilklage | §§ 3, 4, 12, 13, 17, 29, 29a, 29c, 32, 38, 78, 79, 91, 92, 93, 114, 115, 117, 130, 130a, 130d, 139, 167, 222, 233, 234, 253, 269, 271, 275, 276, 278, 330, 331, 338, 339, 495a, 496, 511, 517 ZPO; §§ 23, 71, 72, 119 GVG; §§ 12, 34, 43 GKG, KV 1210, 1211; §§ 195, 199, 204, 269, 270, 288, 438, 548, 634a BGB; § 15a EGZPO; §§ 40, 116, 118 bis 127 ZPO; § 288 Abs. 5, 6 BGB; Schlichtungsgesetz BW (außer Kraft seit 30.04.2013) | ZPO 20.05.2026; GVG 02.07.2026 (Stand-Zeile 09.01.2026); GKG 20.05.2026; BGB 23.07.2026; EGZPO 08.12.2025 (Wertgrenzen: AG 10.000 Euro, § 495a und Berufung 1.000 Euro, am Rohtext bestätigt) | 17.09.2026 (§ 71 Abs. 2 GVG, Auslandsfristen, § 234 Abs. 1 S. 2; Gerichtsstände, Verjährung je Vertragsart, Prozesskostenhilfe) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | RVG, Schlichtungsgesetze außer BW, Aufhebungsgesetz BW im Wortlaut, Rechtsprechung |
| Mahnverfahren | §§ 167, 222, 338, 339, 688 bis 697, 699 bis 703d, 707, 719, 750, 794 ZPO; § 12 Abs. 3, § 34 GKG, KV 1100 mit Anm. zu 1210; § 204 BGB; §§ 751, 765a ZPO; §§ 1 bis 3 MahnVordrV; § 2 ZuVOJu BW | ZPO 20.05.2026; GKG 20.05.2026; BGB 23.07.2026 (Mindestgebühr KV 1100: 38 Euro, am Rohtext bestätigt); MahnVordrV 05.10.2021; ZuVOJu BW § 2 gültig ab 01.11.2023 | 17.09.2026 (Ende der Verjährungshemmung § 204 Abs. 2 BGB, Online-Antrag ohne Unterschrift; Einstellung der Vollstreckung nach Einspruch) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Landesverordnungen zum Mahngericht außer BW, Rechtsprechung zur Individualisierung; keine Vorlage (Formularzwang), §§ 752 ff. ZPO, Vorgaben für maschinelle Mahnanträge |
| Strafanzeige | §§ 153, 153a, 158, 160, 163, 170, 171, 172, 374, 376 bis 383, 395, 403, 406d, 406e, 406h, 406i, 471 StPO; §§ 77, 77b, 77d, 78 bis 78c, 123, 145d, 164, 185, 194, 223, 230, 247, 303, 303c StGB; § 78b Abs. 1 bis 6 StGB; §§ 200, 384 bis 394, 396 bis 402, 404 bis 406c StPO; §§ 37, 38, 40 AGGVG BW; LG Mannheim 30.11.2021, 4 Qs 48/21 | StPO 03.07.2026 (Stand-Zeile 23.02.2026); StGB 20.03.2026 | 17.09.2026 („Sachbeschädigung unter Angehörigen“ berichtigt, Klageerzwingung, Kostenrisiko Privatklage; Verjährung, Nebenklage, Adhäsion) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Schiedsstellenrecht außer BW und Online-Wachen, SGB XIV, Gebühren von Adhäsion und Nebenklage |
| Akteneinsicht | § 29 VwVfG; § 25 SGB X; § 364 AO; § 49 OWiG; §§ 32f, 147, 406e StPO; § 299 ZPO; § 83 BetrVG; § 44a VwGO; § 241 BGB; Art. 12, 15, 77, 79 DSGVO; §§ 1, 7, 9 IFG; § 12 GBO; § 9 HGB; § 32f Abs. 1 bis 6, § 403 StPO; § 29 LVwVfG BW; §§ 1, 2, 3, 7, 9, 10, 12 LIFG BW | VwVfG 22.07.2026 (Stand-Zeile 15.07.2024); SGB X 21.07.2026; AO 03.07.2026; StPO 03.07.2026; ZPO 20.05.2026; BetrVG 19.07.2024; IFG 19.06.2020; GBO 22.06.2026; HGB 04.02.2026; DSGVO EUR-Lex; LIFG BW zuletzt geändert 10.02.2026 | 17.09.2026 (§ 406e Abs. 3, Verweis auf einen nicht vorhandenen Abs. 6 entfernt, IFG-Frist als Soll-Frist) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Landes-VwVfG und Informationsfreiheitsgesetze außer BW, JVKostG, Rechtsprechung BFH und BAG, Erben als Einsichtsberechtigte nach § 406e Abs. 4 StPO |
| Dienstaufsichtsbeschwerde | Art. 17, 45c GG; § 26 DRiG; §§ 73, 191f BRAO; § 62 OWiG; §§ 164, 185 StGB; §§ 146, 147 GVG; § 92 BNotO; §§ 42, 766 ZPO; §§ 24, 98 StPO; § 43 VwGO; § 87 SGB IV; § 50 BeamtStG; § 106 BBG; § 90 SGB IV; § 193 StGB; §§ 1 bis 9 Gesetz nach Art. 45c GG; Art. 2, 35a LV BW; §§ 1, 2 PetAusschG BW; §§ 1, 2, 3, 16, 17, 19 BürgBG BW; §§ 118, 119 GemO BW | GG 22.03.2025; DRiG 22.10.2024; BRAO 22.12.2025; GVG 02.07.2026; BNotO 16.07.2026; SGB IV 24.07.2026; BeamtStG 20.12.2023; BBG 03.07.2026; Gesetz nach Art. 45c GG 05.05.2004; BürgBG BW vom 23.02.2016; PetAusschG BW vom 20.02.1979 | 17.09.2026 (§ 73 Abs. 3 und 5 BRAO, Marker zu E-Mail und anonymen Beschwerden) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | BVerfG zur Bescheidungspflicht, Petitionsgesetze außer BW, Disziplinarrecht, Gerichtsvollzieherordnungen, Kammergesetze |
| Zuständigkeit finden | § 52 Nr. 1 bis 5 VwGO; § 57 SGG; § 38 FGO; §§ 36, 50, 52, 68 OWiG; § 143, §§ 17a, 17b, § 71 GVG; §§ 7, 8 StPO; §§ 29a, 281 ZPO; Verweise auf die anderen Merkblätter; sieben amtliche Verzeichnisse (Abruf geprüft); § 2 ZuVOJu BW; §§ 2, 4, 5 OWiZuVO BW | VwGO 20.05.2026; SGG 20.05.2026; FGO 29.06.2026; OWiG 22.12.2025; GVG 02.07.2026; StPO 03.07.2026 | 17.09.2026 (Jahresfrist bei fehlender Belehrung gilt nicht für Bußgeldbescheide, Verweisung nur beim Rechtsweg von Amts wegen) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Landesverordnungen außer BW, Behördenfinder des Bundes (nicht erreichbar) |
| Einspruch Bußgeldbescheid | §§ 18, 31, 33, 46, 49, 50, 51, 52, 55, 56, 62, 66 bis 74, 79, 80, 89, 105, 107, 109, 110c, 111 OWiG; §§ 32a, 32d, 35a, 43, 44, 45, 297, 298, 300, 302, 303, 341, 344, 345, 410, 411 StPO; §§ 25, 25a, 26 StVG; §§ 2 bis 8, 10 VwZG; §§ 177 bis 182 ZPO; §§ 2 bis 4 LVwZG BW; § 9 VwZG; §§ 4, 28 StVG; §§ 1 bis 4 BKatV; §§ 2, 4, 5 OWiZuVO BW; OLG Stuttgart 09.11.2017, 4 Rb 25 Ss 833/17 | OWiG 22.12.2025; StPO 03.07.2026 (Stand-Zeile 23.02.2026); VwZG 03.07.2026 (Stand-Zeile 15.07.2024); StVG 12.05.2026 (§ 26 Abs. 3 StVG: sechs Monate, Übergangsrecht offen); BKatV 12.08.2026; OWiZuVO BW §§ 2, 4 gültig ab 30.07.2026 | 17.09.2026 (Zustellung an den Verteidiger, § 52 OWiG, Fahrverbotsbeginn § 25 Abs. 3 StVG; Zustellungsarten, Gebühren, Rechtsbeschwerde) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Landes-Zustellungsgesetze außer BW, GKG-Kostenverzeichnis, Änderungshistorie § 26 Abs. 3 StVG, Rechtsprechung (Fax, E-Mail, Messunterlagen, Beschränkung des Einspruchs), Anlage zur BKatV, §§ 28a, 29 StVG, Verordnungen nach § 68 Abs. 3 OWiG, § 15 LVwG BW |

### 2.3 Schreibvorlagen

Zehn Vorlagen vom 16.09.2026 (Briefkopf, Einspruch Bußgeldbescheid,
Widerspruch Bescheid, Fristsetzung, Auskunft DSGVO, Klage Arbeitsgericht,
Einspruch Steuerbescheid, Klage Zivilgericht, Strafanzeige, Akteneinsicht).
Die Normen darin tragen `[QUELLE]`, wo sie nicht am Volltext gelesen wurden.
Am 17.09.2026 gegen die berichtigten Merkblätter durchgesehen: nur die
Formzeile der Vorlage Widerspruch_Bescheid war zu ergänzen (§ 3a Abs. 3
VwVfG ohne De-Mail, § 9a Abs. 5 OZG über § 70 Abs. 1 VwGO). Nach dem
Nachlesen der „Nicht gelesen“-Listen (17.09.2026) erneut durchgesehen: nur
Klage_Zivilgericht betroffen (§ 288 BGB gelesen, Marker im Antrag auf
`[BELEG: Verzugsbeginn …]` umgestellt, Hinweise zu Zinssatz, Streitwert und
Gerichtsstandsklausel).
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

Das Werkzeug `rechtsinhalte_pruefen` (Befehlszeile: `python3 "06 Werkzeuge/dienst/cli.py" rechtsinhalte_pruefen`, optional `stichtag=JJJJ-MM-TT`) rechnet diese Regeln nach und meldet je Inhalt „fällig“, „bald fällig“ (30 Tage vorher), „unbekannt“ (kein lesbares Prüfdatum) oder „in Ordnung“; der Sitzungsstart meldet es, sobald etwas ansteht. Es liest nur: Merkblätter über die Kopfzeile „Letzte vollständige Prüfung: TT.MM.JJJJ“ (fällig nach zwölf Monaten), Feiertagstabelle über `FEIERTAGE_GEPRUEFT` in `fristen.py` (fällig ab 1. Dezember, wenn das Folgejahr noch nicht geprüft ist), Quellenkatalog über `catalog_checked` je Eintrag (fällig nach sechs Monaten).

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
   Vorlage in den internen Hinweisen. Prüfdatum im Kopf der Datei setzen. Nach einer
   vollständigen Prüfung die eigene Kopfzeile „*Letzte vollständige Prüfung:
   TT.MM.JJJJ*“ erneuern (Feiertage: `FEIERTAGE_GEPRUEFT` in `fristen.py`,
   Quellen: `catalog_checked`); das Nachlesen einzelner Normen ändert sie nicht.
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
- Transparenzportal Bremen (17.09.2026): Die Suchadresse `…/suche?q=` gibt
  es nicht; im Browser unter „Vorschriften“ das Suchfeld per Klick füllen
  (Eingabe über die Element-Referenz geht verloren), Ergebnis
  `vorschriften-72741?…&fulltext=<Suchtext>`. Das Feiertagsgesetz heißt
  „Gesetz über die Sonn-, Gedenk- und Feiertage“; die Metaseite enthält die
  ganze aktuelle Gesamtausgabe und ist per curl lesbar, dazu die Vorlagen
  `template=20_gp_ifg_meta_fassungen_d` (frühere Fassungen) und
  `template=20_gp_ifg_meta_historie_d` (Änderungshistorie mit
  Gesetzblattstelle). Am 16.09.2026 wurde über eine andere Seite nur eine
  Fassung bis 2017 gefunden.
- landesrecht-bw.de, Nachtrag 17.09.2026 abends: Zuverlässig ist `https://www.landesrecht-bw.de/perma?d=<Dokumentkennung>`
  (Kennung `jlr-…` aus dem Link „Dokument ansehen“ der Trefferliste, per Seitenstruktur
  auslesbar); `perma?j=` bleibt oft auf der Trefferliste stehen und leitet erst nach
  10 bis 15 Sekunden um. Suche per Adresse `…/bsbw/search?query=<Text>` funktioniert.
  juris-Kürzel: `InfFrG_BW` (LIFG), `PetAusschG_BW`, `Verf_BW_Artikel_35a` (Artikel mit
  „Artikel_“), `GerZustJuV_BW` (ZuVOJu), `OWiGZustV_BW` (OWiZuVO), `GVGAG_BW` (AGGVG),
  `BürgBG_BW`, `GemO_BW`, `KAG_BW`, `VwVfG_BW`. Das Schlichtungsgesetz BW steht dort als
  außer Kraft (gültig bis 30.04.2013).
- Das BMF-Portal zum Anwendungserlass AO (ao.bundesfinanzministerium.de)
  blockiert Skriptabrufe; juris.bundesfinanzhof.de war nicht erreichbar.
