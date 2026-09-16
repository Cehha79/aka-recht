# Rechtsinhalte

*Stand: 16.09.2026*

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
Portal oder im Gesetzblatt gelesen. „Übersicht BMI“ heißt: nur die amtliche
Übersicht des Bundesministeriums des Innern (Stand September 2018) bestätigt
den Eintrag; Änderungen nach 2018 sind damit nicht abgedeckt. „Ministerium“
heißt: Seite des zuständigen Landesministeriums.

| Land | Zusätzliche Feiertage in der Tabelle | Beleg | Offen |
|---|---|---|---|
| BW | Heilige Drei Könige, Fronleichnam, Allerheiligen | Volltext FTG BW (16.09.2026) | – |
| BY | Heilige Drei Könige, Fronleichnam, Allerheiligen; regional Mariä Himmelfahrt, Friedensfest | Volltext FTG BY Art. 1 (16.09.2026) | – |
| BE | Frauentag (8. März) seit 2019; einmalig 08.05.2025 und 17.06.2028 | Senatsverwaltung für Inneres (§ 1 FTG, Liste); GVBl. Berlin 2024 S. 460 (Viertes Änderungsgesetz vom 10.07.2024) | Portal gesetze.berlin.de für den Browser freigeben, dann § 1 konsolidiert lesen |
| BB | Reformationstag | Volltext § 2 FTG, bravors.brandenburg.de (Gesetz vom 21.03.1991, geändert 30.04.2015) | – |
| HB | Reformationstag seit 2018 | Transparenzportal zeigt nur Fassungen bis 2017 mit „31. Oktober 2017“; Änderungsgesetz Brem.GBl. 2018 S. 302 nur aus Pressemeldungen | `[QUELLE: Brem.GBl. 2018 S. 302 am Volltext lesen]` |
| HH | Reformationstag seit 2018 | Volltext § 1 FeiertG HA, landesrecht-hamburg.de, gültig ab 21.03.2018 | – |
| HE | Fronleichnam | Übersicht BMI 2018 | Portal rv.hessenrecht.hessen.de freigeben, § 1 HFeiertagsG lesen |
| MV | Frauentag (8. März) seit 2023, Reformationstag | Volltext § 2 FTG M-V, landesrecht-mv.de, gültig ab 13.07.2022 | – |
| NI | Reformationstag seit 2018 | Volltext § 2 NFeiertagsG, voris (Fassung ab 29.06.2018) | – |
| NW | Fronleichnam, Allerheiligen | Übersicht BMI 2018 | recht.nrw.de liefert per Abruf keinen Text; im Browser lesen |
| RP | Fronleichnam, Allerheiligen | Ministerium des Innern RP (Liste der elf Feiertage); Übersicht BMI 2018 | Portal landesrecht.rlp.de freigeben, § 2 LFtG lesen |
| SL | Fronleichnam, Mariä Himmelfahrt, Allerheiligen | Übersicht BMI 2018 | Portal recht.saarland.de freigeben, § 2 SFG lesen |
| SN | Reformationstag, Buß- und Bettag; regional Fronleichnam | Volltext § 1 SächsSFG, revosax (PDF, Fassung vom 21.12.2010; Änderung 23.04.2025 betrifft § 1 nicht `[PRÜFEN]`) | – |
| ST | Heilige Drei Könige, Reformationstag | Übersicht BMI 2018 | Portal landesrecht.sachsen-anhalt.de freigeben, § 2 FeiertG LSA lesen |
| SH | Reformationstag seit 2018 | Volltext § 2 SFTG, gesetze-rechtsprechung.sh.juris.de, gültig ab 30.03.2018 | – |
| TH | Reformationstag, Weltkindertag (20. September) seit 2019; regional Fronleichnam | Reformationstag und Fronleichnam: Übersicht BMI 2018; Weltkindertag nur Presse und Ministerium | Portal landesrecht.thueringen.de freigeben, § 2 ThürFGtG lesen `[QUELLE]` |

Bundesweit einmalig: 31.10.2017 (Reformationsjubiläum) ist eingetragen.
Länder können nach ihren Gesetzen weitere einmalige Feiertage durch
Verordnung erklären (etwa § 2 Abs. 2 SFTG, § 2 Abs. 3 FTG M-V); solche
Verordnungen sind nicht erfasst.

### 2.2 Merkblätter

| Merkblatt | Normen | Rechtsstand | Geprüft | Offen |
|---|---|---|---|---|
| Einspruch Steuerbescheid | §§ 347, 350, 355, 356, 357, 361, 367, 108, 110, 122, 172, 87a AO; § 47 FGO | AO i. d. F. v. 23.01.2025, zuletzt geändert 03.07.2026 | 16.09.2026 | AEAO zu § 357, BFH III R 26/14, Kostenerstattung, Kommunalabgaben |
| Widerspruch Verwaltungsakt | §§ 58, 60, 68, 69, 70, 73, 74, 80 VwGO; §§ 3a, 41, 80 VwVfG | VwGO zuletzt geändert 23.04.2026 | 16.09.2026 | Landes-AGVwGO (Abschaffung je Land), VwZG, § 57 VwGO mit § 222 ZPO, § 72, § 79 VwGO, § 29 VwVfG, Gebührengesetze |

### 2.3 Schreibvorlagen

Sechs Vorlagen vom 16.09.2026 (Briefkopf, Einspruch Bußgeldbescheid,
Widerspruch Bescheid, Fristsetzung, Auskunft DSGVO, Klage Arbeitsgericht) plus
Einspruch Steuerbescheid. Die Normen darin tragen `[QUELLE]`, wo sie nicht
am Volltext gelesen wurden; Merkblätter gibt es für Einspruch Steuerbescheid
und Widerspruch Verwaltungsakt.

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
3. Änderung an genau einer Stelle: Feiertage in `fristen.py` (Kommentarzeile
   mit Quelle und Datum daneben), Merkblatt im Abschnitt „Geprüfte Quellen“,
   Vorlage in den internen Hinweisen. Prüfdatum im Kopf der Datei setzen.
4. Funktionstest laufen lassen (`pruefen.py`); Feiertage haben eigene
   Prüfpunkte (Fronleichnam BW und BE, 08.05.2025 BE gegen BB).
5. Diese Datei fortschreiben (Tabelle in Abschnitt 2), dann
   `python3 DOKU/ansicht_bauen.py`, dann Produkt neu bauen
   (`produkt_bauen.py --ersetzen`), Commit nach Freigabe.
6. Was nicht am Volltext gelesen wurde, bleibt mit `[QUELLE: …]` markiert,
   auch wenn es „allgemein bekannt“ ist.

## 5. Bekannte Eigenheiten der Portale (16.09.2026)

- Die juris-Landesportale (Berlin, Hamburg, Hessen, Mecklenburg-Vorpommern,
  Rheinland-Pfalz, Saarland, Sachsen-Anhalt, Schleswig-Holstein, Thüringen)
  liefern per Skript nur den Seitentitel. Im Browser funktionieren sie, aber
  nur über die Schnellsuche (etwa „§ 1 FeiertG HA“); feste Dokumentadressen
  leiten auf die Startseite um. Die Chrome-Erweiterung braucht je Domain eine
  Freigabe; ohne sie bricht die Steuerung ab.
- bravors.brandenburg.de, voris (Niedersachsen) und revosax (Sachsen, PDF)
  liefern per Abruf den Text; recht.nrw.de nicht.
- Das Transparenzportal Bremen zeigte am 16.09.2026 für das Feiertagsgesetz
  nur Fassungen bis 2017, obwohl es „zuletzt geändert 02.09.2025“ meldet.
- Das BMF-Portal zum Anwendungserlass AO (ao.bundesfinanzministerium.de)
  blockiert Skriptabrufe; juris.bundesfinanzhof.de war nicht erreichbar.
