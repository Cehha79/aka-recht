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
Am 17.09.2026 abends die Rechtsprechung mit Fristfolge im Volltext auf amtlichen Seiten gelesen
und in sieben Merkblätter eingearbeitet: Fax (GmS-OGB 1/98, BGH IV ZB 20/05), E-Mail-Einspruch
(BFH III R 26/14, OLG Karlsruhe 2 ORbs 35 Ss 4/23 mit BVerfG 2 BvR 1402/23), „demnächst“
(BGH VII ZR 240/23), Zugang im Briefkasten (BAG 2 AZR 111/19, 2 AZR 213/23), Belehrungsmangel
(BGH 1 StR 51/25, AG Köln 582 OWi 65/23), Form des Strafantrags (BGH 3 StR 97/24, 5 StR 398/21,
BGBl. 2024 I Nr. 234).
Danach die übrige Rechtsprechung dieser Listen im Volltext gelesen und eingearbeitet:
Messunterlagen (BVerfG 2 BvR 1616/18), Beschränkung des Einspruchs (OLG Düsseldorf 2 ORbs 83/24),
Widerspruch als signiertes PDF per E-Mail (BVerwG 6 C 12.15), Sperrzeit beim Aufhebungsvertrag
(BSG B 11 AL 6/11 R), Kostenvorschuss und Drei-Wochen-Regel (BGH V ZR 203/14), Individualisierung
im Mahnbescheid (BGH VII ZR 255/21), Unterschrift beim Steuer-Einspruch (BFH III R 26/14).
Zuletzt Gruppe D, Verwaltungsanweisungen und Sonderfälle: Anwendungserlass zur Abgabenordnung
zu §§ 172 und 357 (BMF-Handbuch 2025), Fachliche Weisungen der Bundesagentur zu § 159 SGB III,
Kostenverzeichnisse zum GKG (Bußgeld, Nebenklage) und zum JVKostG (Dokumentenpauschale),
Vergütungsverzeichnis zum RVG mit § 13 und Anlage 2, §§ 28a und 29 StVG, § 78 ArbGG,
§§ 1, 10, 11, 13 und 112 SGB XIV.
Zuletzt das Landesrecht: Die Frage, ob es ein Widerspruchsverfahren gibt, ist am 17.09.2026 abends
für alle 16 Länder am jeweiligen Landesportal gelesen und im Merkblatt Widerspruch je Land
eingetragen. Am 17.09.2026 abends (vierzehnte Sitzung) folgte das erste Thema der übrigen
Landesarbeit: Landes-Zustellungsrecht und Bekanntgabefiktion, und zwar für alle 16 Länder am
Volltext. Die Übersicht steht im Merkblatt Widerspruch (Abschnitt 2), kurz auch im Merkblatt
Bußgeld. Ergebnis: Die Vier-Tage-Regel beim Einschreiben gilt in allen 16 Ländern; eigenen
Wortlaut haben BW, BY, NW, MV und SH, auf das Bundes-VwZG verweisen BE, BB, HB, HH, HE, NI, RP,
SL, SN und ST, Thüringen mischt beides. Befunde mit Fristfolge: Hessen hat in § 41 Abs. 2 HVwVfG
die Drei-Tage-Fiktion behalten (Bund und die übrigen 14 Länder: vier Tage); Brandenburg schließt
in § 7 VwVfGBbg die Fiktion bei nachweisbar früherem Zugang aus; beim Abruf aus einem OZG-Postfach
gilt nach § 9 Abs. 1 OZG der vierte Tag nach der Bereitstellung (Hamburg § 41 Abs. 2b HmbVwVfG,
Schleswig-Holstein § 110 Abs. 2b LVwG, Sachsen über § 2a SächsVwVfZG); Art. 41 BayVwVfG hat keinen
Absatz 2a; Rheinland-Pfalz nimmt § 80 VwVfG (Kosten im Vorverfahren) aus. Offen geblieben und
markiert: ob § 1 ThürVwZVG, § 1 Vw ZG-LSA und § 1 VwVfG LSA auch die Gemeinden erfassen. Danach Thema 2, erster Teil:
die zentralen Mahngerichte. Die Zuordnung aller 16 Länder steht jetzt im Merkblatt Mahnverfahren und
ist seit dem 17.09.2026 nachts für alle 16 Länder am Volltext belegt (Verordnungen der Länder und
vier Staatsverträge). Befund: § 689 Abs. 2
Satz 2 ZPO weist Antragsteller ohne inländischen Gerichtsstand dem Amtsgericht Wedding zu; der
Mahngerichtsvertrag von 2005 nennt dafür noch das Amtsgericht Schöneberg und ist insoweit überholt.
Befunde des zweiten Durchgangs (17.09.2026 nachts, die sieben zuletzt offenen Stellen):
(1) Der Staatsvertrag Hamburg/Mecklenburg-Vorpommern datiert vom 17.08.2005, nicht vom 10.10.2005
(das ist das Zustimmungsgesetz von Mecklenburg-Vorpommern); seine Artikel 1 und 2 sind durch
Änderungsstaatsvertrag vom 11./17.11.2015 neu gefasst und gelten seit dem 01.07.2016.
(2) Niedersachsen hat in § 20 Abs. 3 ZustVO-Justiz seit dem 01.10.2025 auch das arbeitsgerichtliche
Mahnverfahren gebündelt: Arbeitsgericht Hannover für die Bezirke aller Arbeitsgerichte.
(3) Die maschinelle Bearbeitung steht nicht überall in derselben Norm: Bremen, Niedersachsen und die
beiden Staatsverträge regeln sie mit, Schleswig-Holstein in einer eigenen Verordnung
(§ 1 MaschMahnEV), Hessen gar nicht in § 48 JuZuV. Danach Thema 2, zweiter Teil: die Bußgeldbehörden je Land. Zwölf Länder sind am Volltext belegt
(Baden-Württemberg schon vorher, dazu Bayern, Berlin, Brandenburg, Hamburg,
Mecklenburg-Vorpommern, Niedersachsen, Nordrhein-Westfalen, Rheinland-Pfalz, Saarland,
Sachsen und Schleswig-Holstein); die Übersicht steht im Merkblatt Einspruch Bußgeldbescheid,
Abschnitt 1. Ein zweiter Befund: Sechs Länder haben die Verkehrsordnungswidrigkeiten bei einer
Landesbehörde gebündelt (Bayern Polizeiverwaltungsamt, Brandenburg Zentraldienst der Polizei,
Berlin Polizei Berlin, Hamburg Behörde für Inneres und Sport, Rheinland-Pfalz Polizeipräsidium
Rheinpfalz, Saarland Landesverwaltungsamt); die übrigen lassen Landkreise und kreisfreie Städte
entscheiden, der ruhende Verkehr bleibt fast überall bei den Gemeinden. Befund: Das Thema ist nicht wie die vorigen in einem Zug zu erledigen, weil die Länder
ganz unterschiedlich regeln — eigene Verkehrs-Bußgeldverordnung (Brandenburg), ein Abschnitt in
einer großen Zuständigkeitsverordnung (Bayern, Niedersachsen, Sachsen) oder gar keine ausdrückliche
Norm, sodass die Zuständigkeit nur über die Straßenverkehrsbehörden und einen Runderlass greifbar
ist (Nordrhein-Westfalen; für Bremen ist geprüft, dass keine Verkehrs-Verordnung besteht). Offen
sind Sachsen-Anhalt und Thüringen sowie die Verkehrszuständigkeit in Bremen; für Hessen ist
geprüft und im Merkblatt festgehalten, dass die Verordnung vom 12.11.2007 Ordnungswidrigkeiten nur
im Gefahrgutrecht regelt und am Landesportal keine Norm zur Verkehrs-Bußgeldzuständigkeit zu
finden war.
Die übrigen Landesthemen (Verwaltungsverfahrens-, Zustellungs-, Informationsfreiheits-,
Petitions- und Gemeindegesetze, Schiedsstellen) bleiben außerhalb
Baden-Württembergs offen.
Fassungen seit 17.09.2026 nach dem Vollzitat des Portals (Abschnitt 4,
Nr. 2).

| Merkblatt | Normen | Rechtsstand (Vollzitat) | Geprüft | Offen |
|---|---|---|---|---|
| Einspruch Steuerbescheid | §§ 347, 350, 355, 356, 357, 361, 362, 367, 108, 110, 122, 122a, 172, 87a (Abs. 1 bis 8) AO; Art. 97 § 28 EGAO; § 47 FGO; §§ 187, 188 BGB; § 1 Abs. 2 AO; § 3 KAG BW; BFH 13.05.2015, III R 26/14; BFH III R 26/14 (auch zur Unterschrift); AEAO zu §§ 172, 357 | AO i. d. F. v. 23.01.2025, zuletzt geändert 03.07.2026; EGAO 29.06.2026; FGO 29.06.2026 (Stand-Zeile 22.12.2025); KAG BW § 3 gültig ab 12.12.2020 | 17.09.2026 (Fristbeispiel berichtigt: § 188 Abs. 2 BGB ergibt den Sonntag, § 108 Abs. 3 AO den Montag) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: übrige Rechtsprechung der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Verwaltungsanweisungen und Kostenverzeichnisse ergänzt) | Vorfassung § 122a AO, Kostenerstattung, Kommunalabgabengesetze außer BW |
| Widerspruch Verwaltungsakt | §§ 57, 58, 60, 68, 69, 70, 72, 73, 74, 79, 80 VwGO; §§ 3a, 29, 31, 41, 80 VwVfG; § 222, §§ 177 bis 181 ZPO; §§ 1 bis 5, 8, 10 VwZG; § 15 AGVwGO BW, § 41 LVwVfG BW, §§ 2 bis 4 LVwZG BW; § 9 VwZG; § 9a OZG; § 80 LVwVfG BW; GmS-OGB 05.04.2000, GmS-OGB 1/98; BVerwG 07.12.2016, 6 C 12.15; Vorverfahren aller 16 Länder (u. a. Art. 12 AGVwGO BY, § 80 NJG, § 16a HessAGVwGO, § 6 AGVwGO RP, § 110 JustG NRW, § 63 JustG Bln, § 6 AGVwGO HH, Art. 8 AGVwGO HB, § 119 LVwG SH, §§ 13a, 13b GerStrukGAG MV, § 8a AG VwGO LSA, §§ 8a bis 9 ThürAGVwGO, § 8 AGVwGO SL) | VwGO 20.05.2026 (Stand-Zeile 23.04.2026); VwVfG 22.07.2026 (Stand-Zeile 15.07.2024); VwZG 03.07.2026 (Stand-Zeile 15.07.2024); AGVwGO BW gültig ab 01.01.2026 (Fassungsliste: vom 02.07.2024); LVwVfG BW gültig ab 07.02.2025; LVwZG BW 03.07.2007; OZG 22.07.2026 (Stand-Zeile 19.07.2024) | 17.09.2026 (De-Mail aus § 3a Abs. 3 gestrichen, § 80 Abs. 6, Fristbeispiel; förmliche Zustellung; BW zweite Lesung, Fassungsangabe § 15 AGVwGO berichtigt) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: übrige Rechtsprechung der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Vorverfahren aller Länder an den Landesportalen gelesen) (17.09.2026 abends: Landes-Zustellungsrecht und Bekanntgabefiktion aller 16 Länder am Volltext gelesen, Übersicht in Abschnitt 2 des Merkblatts) | Landes-VwVfG im Übrigen (Akteneinsicht, Kosten im Vorverfahren) außer BW und RP; Gebührengesetze der Länder; Rechtsprechung (Fax an Behörden, reformatio in peius); Onlinezugangsgesetze der Länder |
| Klage Arbeitsgericht | §§ 2, 9, 11, 11a, 12a, 46, 46c, 46g, 48, 54, 59, 61, 61a, 61b, 64, 66 ArbGG; §§ 12, 13, 17, 114, 115, 117, 130, 130a, 167, 222, 253, 269, 330, 496 ZPO; §§ 1, 4, 5, 7, 23 KSchG; §§ 6, 9, 11, 42 GKG, KV 8210, 8211; §§ 17a, 17b GVG; § 15 AGG; § 16 ArbGG; § 130 BGB; § 168 SGB IX; § 17 MuSchG; § 159 SGB III; §§ 116, 118 bis 127 ZPO; § 24 KSchG; § 174 SGB IX; BAG 22.08.2019, 2 AZR 111/19; BAG 20.06.2024, 2 AZR 213/23; BGH 10.10.2024, VII ZR 240/23; GmS-OGB 1/98; BGH 25.04.2006, IV ZB 20/05; BSG 02.05.2012, B 11 AL 6/11 R; BGH 25.09.2015, V ZR 203/14; § 1a KSchG; § 78 ArbGG; Fachliche Weisungen der BA zu § 159 SGB III | ArbGG 20.05.2026 (Stand-Zeile 27.04.2026); ZPO 20.05.2026 (Stand-Zeile 22.12.2025); KSchG 14.06.2021; GKG 20.05.2026; AGG 22.12.2023; BGB 23.07.2026; SGB IX 24.07.2026; MuSchG 22.12.2025; SGB III 24.07.2026 | 17.09.2026 (Fünf-Monats-Grenze § 66 Abs. 1 S. 2, Ausschluss verspäteten Vorbringens § 61a Abs. 5; Klagefrist auch im Kleinbetrieb, Sonderkündigungsschutz, Sperrzeit) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: übrige Rechtsprechung der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Verwaltungsanweisungen und Kostenverzeichnisse ergänzt) | Rechtsprechung (Unterschrift, Einwurf-Einschreiben, Weiterbeschäftigung), GKG-Kostenverzeichnis außer Nr. 8210, 8211 |
| Zivilklage | §§ 3, 4, 12, 13, 17, 29, 29a, 29c, 32, 38, 78, 79, 91, 92, 93, 114, 115, 117, 130, 130a, 130d, 139, 167, 222, 233, 234, 253, 269, 271, 275, 276, 278, 330, 331, 338, 339, 495a, 496, 511, 517 ZPO; §§ 23, 71, 72, 119 GVG; §§ 12, 34, 43 GKG, KV 1210, 1211; §§ 195, 199, 204, 269, 270, 288, 438, 548, 634a BGB; § 15a EGZPO; §§ 40, 116, 118 bis 127 ZPO; § 288 Abs. 5, 6 BGB; Schlichtungsgesetz BW (außer Kraft seit 30.04.2013); BGH 10.10.2024, VII ZR 240/23; GmS-OGB 1/98; BGH 25.04.2006, IV ZB 20/05; BGH 25.09.2015, V ZR 203/14; § 13 RVG mit Anlage 2, VV 1000, 1003, 3100, 3104, 7002, 7008 | ZPO 20.05.2026; GVG 02.07.2026 (Stand-Zeile 09.01.2026); GKG 20.05.2026; BGB 23.07.2026; EGZPO 08.12.2025 (Wertgrenzen: AG 10.000 Euro, § 495a und Berufung 1.000 Euro, am Rohtext bestätigt) | 17.09.2026 (§ 71 Abs. 2 GVG, Auslandsfristen, § 234 Abs. 1 S. 2; Gerichtsstände, Verjährung je Vertragsart, Prozesskostenhilfe) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: übrige Rechtsprechung der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Verwaltungsanweisungen und Kostenverzeichnisse ergänzt) | RVG im Übrigen, Schlichtungsgesetze außer BW, Aufhebungsgesetz BW im Wortlaut, Rechtsprechung zur Nachholung der Klagebegründung |
| Mahnverfahren | §§ 167, 222, 338, 339, 688 bis 697, 699 bis 703d, 707, 719, 750, 794 ZPO; § 12 Abs. 3, § 34 GKG, KV 1100 mit Anm. zu 1210; § 204 BGB; §§ 751, 765a ZPO; §§ 1 bis 3 MahnVordrV; § 2 ZuVOJu BW; BGH 10.10.2024, VII ZR 240/23; BGH 14.07.2022, VII ZR 255/21; § 690 ZPO | ZPO 20.05.2026; GKG 20.05.2026; BGB 23.07.2026 (Mindestgebühr KV 1100: 38 Euro, am Rohtext bestätigt); MahnVordrV 05.10.2021; ZuVOJu BW § 2 gültig ab 01.11.2023 | 17.09.2026 (Ende der Verjährungshemmung § 204 Abs. 2 BGB, Online-Antrag ohne Unterschrift; Einstellung der Vollstreckung nach Einspruch) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: übrige Rechtsprechung der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: zentrale Mahngerichte aller Länder aufgenommen, acht Länder mit Landesnorm am Volltext) (17.09.2026 nachts: die übrigen acht Länder am Volltext, damit alle 16 belegt) | Keine Vorlage (Formularzwang), §§ 752 ff. ZPO, Vorgaben für maschinelle Mahnanträge |
| Strafanzeige | §§ 153, 153a, 158, 160, 163, 170, 171, 172, 374, 376 bis 383, 395, 403, 406d, 406e, 406h, 406i, 471 StPO; §§ 77, 77b, 77d, 78 bis 78c, 123, 145d, 164, 185, 194, 223, 230, 247, 303, 303c StGB; § 78b Abs. 1 bis 6 StGB; §§ 200, 384 bis 394, 396 bis 402, 404 bis 406c StPO; §§ 37, 38, 40 AGGVG BW; LG Mannheim 30.11.2021, 4 Qs 48/21; § 158 Abs. 2 StPO i. d. F. v. 12.07.2024 (BGBl. 2024 I Nr. 234); BGH 21.08.2024, 3 StR 97/24; BGH 12.05.2022, 5 StR 398/21; §§ 1, 10, 11, 13, 112 SGB XIV; KV GKG Teil 3 Hauptabschnitt 5; VV RVG Nr. 4143, 4144 | StPO 03.07.2026 (Stand-Zeile 23.02.2026); StGB 20.03.2026 | 17.09.2026 („Sachbeschädigung unter Angehörigen“ berichtigt, Klageerzwingung, Kostenrisiko Privatklage; Verjährung, Nebenklage, Adhäsion) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: Verwaltungsanweisungen und Kostenverzeichnisse ergänzt) | Schiedsstellenrecht außer BW und Online-Wachen, SGB XIV im Übrigen, Instanzrechtsprechung zu § 158 Abs. 2 StPO neue Fassung |
| Akteneinsicht | § 29 VwVfG; § 25 SGB X; § 364 AO; § 49 OWiG; §§ 32f, 147, 406e StPO; § 299 ZPO; § 83 BetrVG; § 44a VwGO; § 241 BGB; Art. 12, 15, 77, 79 DSGVO; §§ 1, 7, 9 IFG; § 12 GBO; § 9 HGB; § 32f Abs. 1 bis 6, § 403 StPO; § 29 LVwVfG BW; §§ 1, 2, 3, 7, 9, 10, 12 LIFG BW; KV JVKostG Nr. 2000 | VwVfG 22.07.2026 (Stand-Zeile 15.07.2024); SGB X 21.07.2026; AO 03.07.2026; StPO 03.07.2026; ZPO 20.05.2026; BetrVG 19.07.2024; IFG 19.06.2020; GBO 22.06.2026; HGB 04.02.2026; DSGVO EUR-Lex; LIFG BW zuletzt geändert 10.02.2026 | 17.09.2026 (§ 406e Abs. 3, Verweis auf einen nicht vorhandenen Abs. 6 entfernt, IFG-Frist als Soll-Frist) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Verwaltungsanweisungen und Kostenverzeichnisse ergänzt) | Landes-VwVfG und Informationsfreiheitsgesetze außer BW, JVKostG, Rechtsprechung BFH und BAG, Erben als Einsichtsberechtigte nach § 406e Abs. 4 StPO; JVKostG im Übrigen |
| Dienstaufsichtsbeschwerde | Art. 17, 45c GG; § 26 DRiG; §§ 73, 191f BRAO; § 62 OWiG; §§ 164, 185 StGB; §§ 146, 147 GVG; § 92 BNotO; §§ 42, 766 ZPO; §§ 24, 98 StPO; § 43 VwGO; § 87 SGB IV; § 50 BeamtStG; § 106 BBG; § 90 SGB IV; § 193 StGB; §§ 1 bis 9 Gesetz nach Art. 45c GG; Art. 2, 35a LV BW; §§ 1, 2 PetAusschG BW; §§ 1, 2, 3, 16, 17, 19 BürgBG BW; §§ 118, 119 GemO BW | GG 22.03.2025; DRiG 22.10.2024; BRAO 22.12.2025; GVG 02.07.2026; BNotO 16.07.2026; SGB IV 24.07.2026; BeamtStG 20.12.2023; BBG 03.07.2026; Gesetz nach Art. 45c GG 05.05.2004; BürgBG BW vom 23.02.2016; PetAusschG BW vom 20.02.1979 | 17.09.2026 (§ 73 Abs. 3 und 5 BRAO, Marker zu E-Mail und anonymen Beschwerden) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | BVerfG zur Bescheidungspflicht, Petitionsgesetze außer BW, Disziplinarrecht, Gerichtsvollzieherordnungen, Kammergesetze |
| Zuständigkeit finden | § 52 Nr. 1 bis 5 VwGO; § 57 SGG; § 38 FGO; §§ 36, 50, 52, 68 OWiG; § 143, §§ 17a, 17b, § 71 GVG; §§ 7, 8 StPO; §§ 29a, 281 ZPO; Verweise auf die anderen Merkblätter; sieben amtliche Verzeichnisse (Abruf geprüft); § 2 ZuVOJu BW; §§ 2, 4, 5 OWiZuVO BW | VwGO 20.05.2026; SGG 20.05.2026; FGO 29.06.2026; OWiG 22.12.2025; GVG 02.07.2026; StPO 03.07.2026 | 17.09.2026 (Jahresfrist bei fehlender Belehrung gilt nicht für Bußgeldbescheide, Verweisung nur beim Rechtsweg von Amts wegen) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) | Landesverordnungen außer BW, Behördenfinder des Bundes (nicht erreichbar) |
| Einspruch Bußgeldbescheid | §§ 18, 31, 33, 46, 49, 50, 51, 52, 55, 56, 62, 66 bis 74, 79, 80, 89, 105, 107, 109, 110c, 111 OWiG; §§ 32a, 32d, 35a, 43, 44, 45, 297, 298, 300, 302, 303, 341, 344, 345, 410, 411 StPO; §§ 25, 25a, 26 StVG; §§ 2 bis 8, 10 VwZG; §§ 177 bis 182 ZPO; §§ 2 bis 4 LVwZG BW; § 9 VwZG; §§ 4, 28 StVG; §§ 1 bis 4 BKatV; §§ 2, 4, 5 OWiZuVO BW; OLG Stuttgart 09.11.2017, 4 Rb 25 Ss 833/17; OLG Karlsruhe 16.02.2023, 2 ORbs 35 Ss 4/23; BVerfG 11.02.2026, 2 BvR 1402/23; BGH 29.04.2026, 1 StR 51/25; AG Köln 16.11.2023, 582 OWi 65/23; GmS-OGB 1/98; BGH 25.04.2006, IV ZB 20/05; BVerfG 12.11.2020, 2 BvR 1616/18; OLG Düsseldorf 27.08.2024, 2 ORbs 83/24; §§ 28a, 29 StVG; KV GKG Nr. 4110 bis 4112; VV RVG Nr. 5100 bis 5110, 7002, 7008 | OWiG 22.12.2025; StPO 03.07.2026 (Stand-Zeile 23.02.2026); VwZG 03.07.2026 (Stand-Zeile 15.07.2024); StVG 12.05.2026 (§ 26 Abs. 3 StVG: sechs Monate, Übergangsrecht offen); BKatV 12.08.2026; OWiZuVO BW §§ 2, 4 gültig ab 30.07.2026 | 17.09.2026 (Zustellung an den Verteidiger, § 52 OWiG, Fahrverbotsbeginn § 25 Abs. 3 StVG; Zustellungsarten, Gebühren, Rechtsbeschwerde) (17.09.2026 abends: Bundesnormen der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Landesrecht Baden-Württemberg im Browser ergänzt) (17.09.2026 abends: Rechtsprechung mit Fristfolge im Volltext ergänzt) (17.09.2026 abends: übrige Rechtsprechung der Liste „Nicht gelesen“ ergänzt) (17.09.2026 abends: Verwaltungsanweisungen und Kostenverzeichnisse ergänzt) (17.09.2026 abends: Landes-Zustellungsrecht aller 16 Länder gelesen) | Verordnungen zu den Bußgeldbehörden von ST und TH, Verkehrszuständigkeit in HB, Gliederungsnummer des Zuständigkeitsverzeichnisses SH; Wortlaut der nordrhein-westfälischen Verordnung vom 25.09.1979; Änderungshistorie § 26 Abs. 3 StVG, Rechtsprechung (Fax an Behörden, Verfahrensgang nach OLG Karlsruhe 2 ORbs 35 Ss 4/23, obergerichtlich zu § 44 Satz 2 StPO, Umfang der Messunterlagen im Einzelfall), Anlage zur BKatV, Verordnungen nach § 68 Abs. 3 OWiG, § 15 LVwG BW |

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
- Portale, Nachtrag 17.09.2026 abends (Landes-Zustellungsrecht):
  gesetze-bayern.de liefert den Volltext per curl, die Gesamtansicht mit
  `…/Content/Document/<Kürzel>?all=true`. recht.nrw.de: die Suche ist JavaScript und per curl leer,
  ein Treffer öffnet sich nur durch Klick auf die Titel-Koordinaten, die Gesetzesseite
  (`/lrgv/gesetz/<datum>-<titel>/`) ist danach per curl vollständig lesbar. BRAVORS (Brandenburg):
  Schnellsuche und erweiterte Suche waren im Browser nicht bedienbar (Formular wird beim Absenden
  zurückgesetzt), die Gesetzesseiten (`/de/gesetze-<Nummer>`, `/gesetze/<kürzel>`) sind per curl
  lesbar; die Adresse eines gesuchten Gesetzes über eine Suchmaschine mit Domainfilter finden und
  dann am Volltext lesen. Niedersachsen: voris läuft jetzt unter
  `voris.wolterskluwer-online.de` (Wolters Kluwer, nicht mehr juris), Suche über `/search?query=…`,
  Volltext über „Gesamte Quelle anzeigen“, je Paragraf ein eigenes Dokument; alte jportal-Adressen
  liefern 404. Transparenzportal Bremen: Metaseiten der Gesetze sind per curl lesbar. juris-Portale
  (Hamburg, Berlin, Hessen, M-V, Rheinland-Pfalz, Saarland, Sachsen-Anhalt, Schleswig-Holstein,
  Thüringen): nur im Browser; direkte Dokumentadressen führen zur Suche zurück, der Weg ist die
  Schnellsuche (Feld anklicken, tippen, Lupe klicken, nicht Enter) und dann „Gesamtausgabe“ oder
  „Einzelnorm“. In Hessen führt `perma?j=<Kürzel>_!_<Paragraf>` zuverlässig zu einer
  JURISLINK-Trefferliste mit allen Fassungen; in Hamburg und M-V nicht. REVOSax (Sachsen): Suche nur
  über das Formular, die Vorschrift dann per curl (`/vorschrift/<Nummer>-<Kürzel>`).
- Das BMF-Portal zum Anwendungserlass AO (ao.bundesfinanzministerium.de)
  blockiert Skriptabrufe; juris.bundesfinanzhof.de war nicht erreichbar.
