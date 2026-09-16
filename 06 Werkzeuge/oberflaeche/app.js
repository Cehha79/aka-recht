'use strict';
/* AKA Recht, Oberfläche. Reines JavaScript ohne Bibliotheken.
   Aufbau: Hilfen, Verbindung zum Dienst, Zustand und Routen, Seitenleiste,
   Seiten der Zentrale, Seiten der Fallakte, Vorschau, Dialoge, Ereignisse. */

// ---------------------------------------------------------------- Hilfen
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const datum = iso => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ''); return m ? `${m[3]}.${m[2]}.${m[1]}` : (iso || ''); };
const heute = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
const tageBis = iso => Math.round((new Date(iso + 'T12:00:00') - new Date(heute() + 'T12:00:00')) / 86400000);
const groesse = n => n >= 1048576 ? (n / 1048576).toLocaleString('de-DE', {maximumFractionDigits: 1}) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB';
const badge = (text, ton = '') => text ? `<span class="badge ${ton}">${esc(text)}</span>` : '';
const opt = (liste, wert, leer) => (leer !== undefined ? `<option value="">${esc(leer)}</option>` : '') + liste.map(x => { const [v, t] = Array.isArray(x) ? x : [x, x]; return `<option value="${esc(v)}"${v === wert ? ' selected' : ''}>${esc(t)}</option>`; }).join('');
const naechste = (liste, buchstabe, breite = 2) => buchstabe + String(Math.max(0, ...liste.map(x => parseInt(String(x.id).slice(1), 10) || 0)) + 1).padStart(breite, '0');
const statusTon = s => ({'bestätigt': 'gruen', 'offen': 'gelb', 'abgelaufen': 'rot', 'erledigt': '', 'Original': 'blau', 'Entwurf': 'gelb', 'Versandt': 'gruen', 'Zugegangen': 'blau', 'Historisch': '', 'Vermerk': '', 'offen ': ''}[s] || '');
let toastTimer;
function toast(text, fehler = false) { const t = $('#toast'); clearTimeout(toastTimer); t.textContent = text; t.className = fehler ? 'fehler' : ''; t.hidden = false; toastTimer = setTimeout(() => t.hidden = true, fehler ? 9000 : 5000); }

// ---------------------------------------------------------------- Verbindung zum Dienst
const api = {
  csrf: '',
  async get(url) { return antwort(await fetch(url)); },
  async post(url, daten) { return antwort(await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-AKA-CSRF': api.csrf}, body: JSON.stringify(daten)})); },
  werkzeug(name, parameter, bestaetigt = true) { return api.post('/api/werkzeug', {name, parameter, bestaetigt}); },
};
async function antwort(r) {
  let d; try { d = await r.json(); } catch { throw new Error('Keine Verbindung zum Dienst. Bitte Start.command im Rechtsordner öffnen.'); }
  if (!r.ok) throw new Error(d.fehler || 'Anfrage fehlgeschlagen.');
  return d;
}

// ---------------------------------------------------------------- Zustand und Routen
const S = {zentrale: null, fall: null, route: {}, auswahl: '', tab: 'vorschau', breit: false, filter: {q: '', gruppe: '', typ: '', stand: ''}, treffer: null, quellen: null};
const ZENTRALE_SEITEN = [['home', 'Übersicht'], ['faelle', 'Alle Fälle'], ['eingang', 'Posteingang'], ['fristen', 'Fristen'], ['quellen', 'Rechtsquellen'], ['bestand', 'Bestand und Sicherung'], ['einstellungen', 'Einstellungen'], ['anleitung', 'Anleitung']];
const FALL_SEITEN = [['uebersicht', 'Übersicht'], ['dokumente', 'Dokumente'], ['beteiligte', 'Beteiligte'], ['verfahren', 'Verfahren'], ['chronologie', 'Chronologie'], ['fristen', 'Fristen'], ['aufgaben', 'Aufgaben'], ['entwuerfe', 'Entwürfe'], ['anlagen', 'Beweise und Anlagen'], ['journal', 'Journal']];
const GRUPPEN = ['01 Eingang', '02 Grundlagen', '03 Schriftverkehr', '04 Verfahren', '05 Beweise', '06 Entwürfe', '07 Recherche', '08 Archiv'];
const BEREICHE = ['Allgemein', 'Arbeit', 'Verkehr und Bußgeld', 'Verträge und Verbraucher', 'Wohnen und Eigentum', 'Behörden und Soziales', 'Forderungen und Versicherungen', 'Familie, Vorsorge und Erbe', 'Strafsachen', 'Geschäftliches und Datenschutz'];
const DOK_STAND = ['Original', 'Entwurf', 'Versandt', 'Zugegangen', 'Historisch', 'Vermerk'];
const DOK_ART = ['Schreiben', 'E-Mail', 'Foto', 'Vertrag', 'Bescheid', 'Urteil', 'Entwurf', 'Beleg', 'Übersicht', 'Gesetz', 'Sonstiges'];
const ROLLEN = ['Ich', 'Gegner', 'Gericht', 'Behörde', 'Anwalt', 'Zeuge', 'Stelle', 'Versicherung', 'Sonstige'];
const EREIGNIS_ART = ['Zugang', 'Versand', 'Termin', 'Gespräch', 'Vorfall', 'Entscheidung', 'Vermerk', 'Arbeitsstand'];
const FRIST_ART = ['gesetzlich', 'selbst gesetzt', 'von Gegenseite gesetzt', 'vorsorglich', 'Termin'];
const FRIST_STATUS = ['offen', 'bestätigt', 'abgelaufen', 'erledigt'];
const ENTWURF_STATUS = ['in Arbeit', 'geprüft', 'versandt', 'verworfen'];
const JOURNAL_ARTEN = ['Eingang', 'Versand', 'Entscheidung', 'Gespräch', 'Termin', 'Arbeit', 'Vermerk'];

function routeLesen() { const p = new URLSearchParams(location.hash.slice(1)); return {seite: p.get('seite') || '', fall: p.get('fall') || '', dok: p.get('dok') || ''}; }
function gehe(teile) { const p = new URLSearchParams(); for (const [k, v] of Object.entries(teile)) if (v) p.set(k, v); location.hash = p.toString(); }
const fallLink = (id, seite = 'uebersicht', dok = '') => '#' + new URLSearchParams(Object.assign({seite, fall: id}, dok ? {dok} : {})).toString();

async function ladeZentrale() { S.zentrale = await api.get('/api/zentrale'); api.csrf = S.zentrale.csrf; }
async function ladeFall(id) { S.fall = await api.get('/api/fall/' + id); }
const akte = () => S.fall.akte;
const fallId = () => akte().fall.id;
const dokListe = () => S.fall.dokumente;
const dok = id => dokListe().find(d => d.id === id);
const dokOptionen = (wert, leer = 'Kein Dokument') => opt(dokListe().map(d => [d.id, `${d.id} · ${d.titel}`]), wert, leer);
const personOptionen = (wert, leer = 'Keine Angabe') => opt(akte().beteiligte.map(b => [b.id, `${b.id} · ${b.name}`]), wert, leer);
const personName = id => (akte().beteiligte.find(b => b.id === id) || {}).name || id;

async function render() {
  S.route = routeLesen();
  try {
    if (!S.zentrale) await ladeZentrale();
    if (S.route.fall && (!S.fall || fallId() !== S.route.fall)) { await ladeFall(S.route.fall); S.auswahl = ''; S.treffer = null; }
    if (!S.route.fall) S.fall = null;
  } catch (e) { $('#content').innerHTML = `<div class="leer"><h2>AKA Recht öffnen</h2><p>${esc(e.message)}</p></div>`; return; }
  if (S.route.dok) S.auswahl = S.route.dok;
  seitenleiste();
  const seite = S.route.seite || (S.fall ? 'uebersicht' : 'home');
  const seiten = S.fall ? FALL : ZENTRALE;
  const fn = seiten[seite] || (S.fall ? FALL.uebersicht : ZENTRALE.home);
  $('#brotkrumen').textContent = S.fall ? `${fallId()} · ${akte().fall.bereich}`.toUpperCase() : 'AKA RECHT';
  const [titel, untertitel, inhalt, aktionen] = await fn();
  $('#seitentitel').textContent = titel;
  $('#kopf-aktionen').innerHTML = aktionen || '';
  $('#content').innerHTML = `<div class="seite">${untertitel ? `<p class="untertitel">${esc(untertitel)}</p>` : ''}${inhalt}</div>`;
  $('#content').scrollTop = 0;
  vorschau(seite === 'dokumente' && S.fall && S.auswahl);
}

// ---------------------------------------------------------------- Seitenleiste
function seitenleiste() {
  const aktiv = S.route.seite || (S.fall ? 'uebersicht' : 'home');
  $('#zurueck').hidden = !S.fall;
  $('#marke-unter').textContent = S.fall ? akte().fall.titel : 'Dein Rechtsarbeitsplatz';
  const zahlen = {};
  if (S.fall) {
    const a = akte(); Object.assign(zahlen, {dokumente: dokListe().length, beteiligte: a.beteiligte.length, verfahren: a.verfahren.length, chronologie: a.ereignisse.length,
      fristen: a.fristen.filter(f => f.pruefstatus !== 'erledigt').length, aufgaben: a.aufgaben.filter(x => !x.erledigt).length, entwuerfe: a.entwuerfe.length, journal: S.fall.journal.length});
  } else if (S.zentrale) { zahlen.faelle = S.zentrale.faelle.length; zahlen.eingang = S.zentrale.eingang.length; }
  const liste = S.fall ? FALL_SEITEN : ZENTRALE_SEITEN;
  $('#navigation').innerHTML = `<div class="abschnitt">${S.fall ? 'Fallakte' : 'Überblick'}</div>` + liste.map(([id, name], i) =>
    `<a href="${S.fall ? fallLink(fallId(), id) : '#seite=' + id}" class="${aktiv === id ? 'aktiv' : ''}"${aktiv === id ? ' aria-current="page"' : ''}><span class="nr">${String(i + 1).padStart(2, '0')}</span>${esc(name)}${zahlen[id] !== undefined ? `<span class="zahl">${zahlen[id]}</span>` : ''}</a>`).join('');
}

// ---------------------------------------------------------------- Seiten der Zentrale
function fallKarte(c) {
  if (c.fehler) return `<article class="karte"><span class="kennung">${esc(c.id)}</span><h2>${esc(c.titel)}</h2><p class="hinweis rot">${esc(c.fehler)}</p></article>`;
  return `<article class="karte"><div class="tafel-kopf"><span class="kennung">${esc(c.id)}</span>${badge(c.bereich)}</div><h2>${esc(c.titel)}</h2><p>${esc(c.rolle || 'Rolle noch offen')}</p>
    <p>${c.dokumente} Dokumente · ${c.offene_aufgaben} offene Aufgaben · ${c.fristen_offen} Fristen</p>
    <div class="karte-fuss"><a class="knopf primaer" href="${fallLink(c.id)}">Akte öffnen</a><select data-fallstatus="${esc(c.id)}" aria-label="Status für ${esc(c.titel)}">${opt(['offen', 'ruhend', 'abgeschlossen'], c.status)}</select></div></article>`;
}
function fristenAllerFaelle() {
  return S.zentrale.faelle.flatMap(c => (c.fristen || []).map(f => ({...f, fallId: c.id, fallTitel: c.titel}))).sort((a, b) => a.datum.localeCompare(b.datum));
}
function fristZeile(f, mitFall = true) {
  const t = tageBis(f.datum); const ton = f.pruefstatus === 'erledigt' ? '' : t < 0 ? 'dringend' : t <= 7 ? 'dringend' : t <= 21 ? 'bald' : '';
  const link = mitFall ? fallLink(f.fallId, 'fristen') : fallLink(fallId(), 'fristen');
  return `<div class="zeile"><div class="datumsbox ${ton}"><b>${datum(f.datum).slice(0, 5)}</b>${datum(f.datum).slice(6)}</div><div class="zeile-text"><h3>${esc(f.titel)}</h3>
    <p>${mitFall ? esc(f.fallId + ' · ' + f.fallTitel) + ' · ' : ''}${esc(f.art)} · ${t < 0 ? 'seit ' + (-t) + ' Tagen vorbei' : t === 0 ? 'heute' : 'in ' + t + ' Tagen'}</p>
    <div class="themen">${badge('Prüfstatus: ' + f.pruefstatus, statusTon(f.pruefstatus))}</div></div><div class="aktionen"><a class="knopf klein" href="${link}">Zur Akte</a></div></div>`;
}
const ZENTRALE = {
  async home() {
    const z = S.zentrale, gueltig = z.faelle.filter(c => !c.fehler), offen = gueltig.filter(c => c.status !== 'abgeschlossen');
    const fristen = fristenAllerFaelle().filter(f => f.pruefstatus !== 'erledigt' && f.datum >= heute()).slice(0, 6);
    const inhalt = `<div class="kacheln"><div class="kachel"><strong>${offen.length}</strong><span>offene oder ruhende Fälle</span></div><div class="kachel"><strong>${gueltig.reduce((n, c) => n + c.dokumente, 0)}</strong><span>Dokumente in den Akten</span></div>
      <div class="kachel"><strong>${gueltig.reduce((n, c) => n + c.offene_aufgaben, 0)}</strong><span>offene Aufgaben</span></div><div class="kachel"><strong>${z.eingang.length}</strong><span>neue Dateien im Eingang</span></div></div>
      <div class="tafel-kopf"><h2>Deine Fälle</h2><span><button class="knopf still" data-aktion="beispiel-laden" title="Erfundener Fall zum Ausprobieren, jederzeit löschbar">Beispielfall laden</button> <a href="#seite=faelle">Alle Fälle</a></span></div><div class="raster">${offen.length ? offen.slice(0, 4).map(fallKarte).join('') : '<div class="leer"><h2>Noch kein Fall</h2><p>Lege einen Fall an, sobald du ein rechtliches Anliegen ordnen möchtest. Auch ein Strafzettel oder eine Rechnung ist ein Fall.</p><p style="margin-top:14px"><button class="knopf primaer" data-aktion="neuer-fall">Neuer Fall</button></p></div>'}</div>
      <div class="raster" style="margin-top:18px"><section class="tafel"><h2>Nächste Fristen und Termine</h2><p class="untertitel" style="margin-bottom:8px">Aus allen Akten. Der Prüfstatus bleibt sichtbar.</p>${fristen.length ? fristen.map(f => fristZeile(f)).join('') : '<p class="untertitel">Keine künftigen Fristen eingetragen.</p>'}</section>
      <section class="tafel"><h2>So geht es weiter</h2><p class="untertitel" style="margin-bottom:8px">Neue Post in den Eingang legen, einem Fall zuordnen, dann in der Akte einsortieren und Fristen eintragen.</p><div class="karte-fuss"><a class="knopf" href="#seite=eingang">Posteingang</a><a class="knopf" href="#seite=quellen">Rechtsquellen</a><a class="knopf" href="#seite=bestand">Sicherung</a></div>
      ${z.sicherung.vorhanden ? `<div class="hinweis">Letzte Sicherung: ${esc(datum(z.sicherung.zeit))}${z.sicherung.unveraendert ? '' : ', Datei seither verändert'}.</div>` : '<div class="hinweis gelb">Noch keine Sicherung mit dem neuen Dienst erstellt.</div>'}</section></div>`;
    return ['Alles Rechtliche an einem Ort.', '', inhalt, '<button class="knopf still" data-aktion="neu-laden">Neu einlesen</button><button class="knopf primaer" data-aktion="neuer-fall">Neuer Fall</button>'];
  },
  async faelle() {
    const inhalt = `<div class="filter"><input id="fall-suche" type="search" placeholder="Fall suchen …" aria-label="Fälle suchen"><select id="fall-filter" aria-label="Nach Status filtern">${opt(['Alle', 'offen', 'ruhend', 'abgeschlossen'], 'Alle')}</select></div>
      <div class="raster" id="fall-liste">${S.zentrale.faelle.map(fallKarte).join('') || '<div class="leer"><h2>Noch kein Fall</h2></div>'}</div>
      <section class="tafel" style="margin-top:18px"><h2>Verträge und Vorsorge</h2><p class="untertitel" style="margin-bottom:8px">Unterlagen ohne Streit liegen in der allgemeinen Ablage. Sobald du sie bearbeiten willst, wird daraus ein Fall.</p><button class="knopf klein" data-aktion="finder" data-ort="vertraege">Ablage im Finder</button></section>`;
    return ['Deine Fallakten', 'Ein Vorgang, eine feste Kennung. Abgeschlossene Fälle bleiben am gleichen Ort.', inhalt, '<button class="knopf primaer" data-aktion="neuer-fall">Neuer Fall</button>'];
  },
  async eingang() {
    const e = S.zentrale.eingang;
    const inhalt = `<section class="tafel">${e.length ? e.map(f => `<div class="zeile"><div class="zeile-text"><h3>${esc(f.name)}</h3><p>${groesse(f.groesse)}</p></div><div class="aktionen"><button class="knopf klein" data-aktion="zuordnen" data-name="${esc(f.name)}">Fall zuordnen</button></div></div>`).join('') : '<div class="leer"><h2>Der Eingang ist frei.</h2><p>Neue PDFs, Briefe und E-Mails hier sammeln, wenn der Fall noch nicht feststeht. Ist er bekannt, direkt in der Akte unter Dokumente hinzufügen.</p></div>'}</section>`;
    return ['Gemeinsamer Posteingang', 'Unterlagen sammeln und dem passenden Fall zuordnen. Die Datei wird dabei einmal verschoben, nie überschrieben.', inhalt, '<button class="knopf" data-aktion="finder" data-ort="eingang">Eingang im Finder</button><button class="knopf primaer" data-aktion="hochladen" data-ziel="eingang">Dateien hinzufügen</button>'];
  },
  async fristen() {
    const alle = fristenAllerFaelle();
    const inhalt = alle.length ? `<section class="tafel">${alle.map(f => fristZeile(f)).join('')}</section>` : '<div class="leer"><h2>Keine offenen Fristen</h2><p>Fristen werden in der jeweiligen Akte eingetragen, mit Auslöser, Rechtsgrundlage und Rechnung.</p></div>';
    return ['Fristen und Termine aller Fälle', 'Sortiert nach Datum. Rot: in sieben Tagen oder überschritten. Gelb: in drei Wochen. Ein Kalenderdatum ist keine Bestätigung einer gesetzlichen Frist.', inhalt, ''];
  },
  async quellen() {
    if (!S.quellen) S.quellen = await api.get('/api/quellen');
    const karten = l => l.map(q => `<article class="karte">${badge(q.category || q.kategorie)}<h2><a href="${/^https:\/\//.test(q.url) ? esc(q.url) : '#'}" target="_blank" rel="noopener noreferrer">${esc(q.title || q.titel)} ↗</a></h2><p>${esc(q.use || q.verwendung)}</p><div class="hinweis">${esc(q.limit || q.grenze || '')}</div><span class="pfad">${esc(q.url)}</span><div class="karte-fuss"><button class="knopf klein" data-aktion="kopieren" data-text="${esc(q.url)}">Adresse kopieren</button><small style="color:var(--muted);font-size:.7rem">Katalog geprüft: ${esc(datum(q.catalog_checked || q.geprueft))}</small></div></article>`).join('') || '<div class="leer">Kein passender Zugang.</div>';
    const inhalt = `<div class="filter"><input id="quellen-suche" type="search" placeholder="Zum Beispiel Bundesrecht, Gericht, Bußgeld …" aria-label="Rechtsquellen suchen"></div><div class="raster" id="quellen-liste">${karten(S.quellen.quellen)}</div>`;
    S._quellenKarten = karten;
    return ['Gesetze, Gerichte und Dienste', 'Direkte Zugänge zu amtlichen Angeboten. Die App lädt keine Gesetzestexte nach. Fassung und Geltungszeitraum bei jeder Rechtsfrage am Volltext prüfen.', inhalt, '<button class="knopf" data-aktion="finder" data-ort="quellen">Katalog im Finder</button>'];
  },
  async bestand() {
    const s = S.zentrale.sicherung;
    const inhalt = `<section class="tafel"><div class="tafel-kopf"><h2>Bestand aller Fälle prüfen</h2>${badge('manuell')}</div><p class="untertitel" style="margin-bottom:10px">Vergleicht jede registrierte Datei mit ihrer ersten Prüfsumme. Erkennt geänderte und fehlende Dateien. Bestätigt keine rechtliche Richtigkeit.</p><button class="knopf primaer" data-aktion="bestand-pruefen">Prüfung starten</button><div id="bestand-ergebnis"></div></section>
      <section class="tafel"><h2>Sicherung</h2>${s.vorhanden ? `<p class="pfad">${esc(s.pfad)}</p><p class="untertitel" style="margin:8px 0">Erstellt ${esc(datum(s.zeit))} · ${s.dateien} Dateien · ${groesse(s.groesse)} · ${badge(s.unveraendert ? 'seit Prüfung unverändert' : 'seit Prüfung verändert', s.unveraendert ? 'gruen' : 'rot')}${s.zweites_ziel ? `<br>Kopie: ${esc(s.zweites_ziel)}` : ''}${s.zweites_ziel_hinweis ? `<br>${esc(s.zweites_ziel_hinweis)}` : ''}</p>` : '<div class="hinweis gelb">Noch keine Sicherung mit dem neuen Dienst dokumentiert.</div>'}
      <button class="knopf primaer" data-aktion="sicherung">Geprüfte Sicherung erstellen</button><p class="untertitel" style="margin-top:10px">Die ZIP wird vollständig gelesen und mit dem Arbeitsstand verglichen. Eine Kopie geht an das zweite Ziel (iCloud Drive), wenn es erreichbar ist. Frühere Sicherungen bleiben erhalten.</p></section>`;
    return ['Bestand und Sicherung', '', inhalt, ''];
  },
  async einstellungen() {
    const e = await api.get('/api/einstellungen');
    const inhalt = `<form id="einstellungen" class="tafel"><h2>Sicherung</h2>
      <label class="feld">Sicherungsziel<input name="ziel" value="${esc(e.sicherung.ziel)}"><small>Ordner außerhalb des Projekts. Wird angelegt, wenn er fehlt.</small></label>
      <label class="feld">Zweites Ziel<input name="zweites_ziel" value="${esc(e.sicherung.zweites_ziel || '')}"><small>Zum Beispiel ein Ordner in iCloud Drive. Leer lassen, wenn keins.</small></label>
      <h2>Fristen</h2>
      <label class="feld">Bundesland für Feiertage<select name="feiertagsland">${Object.entries(e.laender || {}).map(([k, n]) => `<option value="${k}"${(e.einstellungen || {}).feiertagsland === k ? ' selected' : ''}>${esc(n)}</option>`).join('')}</select><small>Der Fristenrechner verschiebt ein Fristende nach § 193 BGB nur an landesweiten Feiertagen dieses Landes. Maßgeblich ist der Ort, an dem die Leistung zu erbringen ist (etwa der Sitz des Gerichts oder der Behörde). Regionale Feiertage einzelner Gemeinden zählen nicht.</small></label>
      <button class="knopf primaer" type="submit">Einstellungen speichern</button></form>`;
    return ['Einstellungen', '', inhalt, ''];
  },
  async anleitung() {
    const inhalt = `<article class="tafel anleitung"><h2>Was AKA Recht ist</h2><p>Ein lokaler Ordner mit einer Oberfläche im Browser. Jede Rechtssache ist ein Fall mit fester Kennung (R-0001, R-0002 …), egal ob Arbeitsrecht, Bußgeld, Miete, Vertrag oder Behörde. Alles bleibt auf diesem Mac.</p>
      <h2>Ein Fall entsteht</h2><ul><li>„Neuer Fall“: Bezeichnung, Bereich, eigene Rolle, Ziel.</li><li>Die Akte bekommt feste Ordner 01 Eingang bis 08 Archiv, eine Datei akte.json für alle Ordnungsangaben und ein Journal.</li><li>Post in „Dokumente“ hinzufügen oder im Finder in 01 Eingang legen. Jede Datei bekommt eine Kennung (D0001 …) und eine Prüfsumme.</li></ul>
      <h2>Ordnen ohne Originale zu ändern</h2><ul><li>„Ordnen“ ändert nur Titel, Datum, Art, Stand, Themen, Anlage, Personen und Verweise.</li><li>„Einsortieren“ verschiebt die Datei in einen Aktenbereich. Kennung und Inhalt bleiben.</li><li>Verschiebst du im Finder, findet die App die Datei über ihre Prüfsumme wieder.</li></ul>
      <h2>Fristen</h2><ul><li>Eine Frist braucht Auslöser (Zugang), Rechtsgrundlage, Rechnung und Quelle. Erst dann darf sie „bestätigt“ sein.</li><li>Der Rechner zeigt jede Rechnung nach §§ 187, 188, 193 BGB. Er entscheidet nicht, welche Frist gilt.</li></ul>
      <h2>Sicherung</h2><ul><li>„Geprüfte Sicherung erstellen“ schreibt eine ZIP außerhalb des Projekts, liest sie zurück und vergleicht jede Datei. Eine Kopie geht nach iCloud Drive, wenn eingerichtet.</li><li>Vor jedem Speichern der Ordnungsdaten wird die alte Fassung außerhalb des Projekts abgelegt.</li></ul>
      <h2>Arbeiten mit einer KI</h2><ul><li>Die App enthält keine KI. Sie ist eine Aktenmappe, die jede KI benutzen kann: Claude Code, Codex und andere lesen die Anleitung im Ordner (CLAUDE.md, AGENTS.md) und arbeiten mit denselben Werkzeugen wie diese Oberfläche.</li><li>Schreiben darf eine KI nur über die Werkzeuge; Originale bleiben gesperrt. Schreibende Werkzeuge laufen erst, wenn du den Aufruf bestätigt hast.</li></ul>
      <h2>KI anbinden (MCP)</h2><p>MCP ist die Schnittstelle, über die eine KI die Werkzeuge der Mappe aufruft. Der Server ist die Datei „06 Werkzeuge/dienst/mcp_server.py“; er braucht nur Python 3.</p><ul><li><b>Claude Code:</b> Sitzung im Projektordner starten. Die Datei „.mcp.json“ liegt bei; beim ersten Start fragt Claude Code, ob es den Server aus dem Projekt laden darf. Prüfen mit „/mcp“. Skills wie „/fristencheck R-0001“ liegen unter „.claude/skills/“.</li><li><b>Codex:</b> einmalig im Terminal „codex mcp add aka-recht -- python3 "voller Pfad zu mcp_server.py"“ eingeben, dann Codex im Projektordner starten und mit „/mcp“ prüfen. Die beigelegte „.codex/config.toml“ hat Codex 0.154 noch nicht geladen. Skills liegen unter „.agents/skills/“ und werden mit „$fristencheck“ aufgerufen.</li><li><b>Claude Desktop:</b> Menü Claude, Einstellungen, Entwickler, „Konfiguration bearbeiten“. In der Datei claude_desktop_config.json unter „mcpServers“ einen Eintrag „aka-recht“ mit command „python3“ und args [voller Pfad zu mcp_server.py] eintragen, Pfade absolut. Claude Desktop danach ganz beenden und neu starten.</li><li><b>Ohne MCP:</b> Jede KI, die Befehle ausführen darf, nutzt „python3 06 Werkzeuge/dienst/cli.py liste“.</li></ul>
      <h2>Grenzen</h2><p>Die App ist kein Rechtsanwalt. Prüfsummen belegen Gleichheit, nicht Echtheit. Ein Datum im Kalender ist keine bestätigte gesetzliche Frist. Versand, Einreichung und Löschen macht die App nicht.</p></article>`;
    return ['So arbeitest du mit AKA Recht', '', inhalt, '<button class="knopf" data-aktion="finder" data-ort="doku">Projektdoku im Finder</button>'];
  },
};

// ---------------------------------------------------------------- Seiten der Fallakte
function dokZeile(d) {
  return `<div class="dok-zeile ${S.auswahl === d.id ? 'gewaehlt' : ''}" data-dok="${esc(d.id)}" tabindex="0" role="button"><div class="dok-zelle"><div class="dateisymbol ${esc(d.typ)}">${esc(d.typ || '?')}</div><div style="min-width:0"><div class="dok-titel">${esc(d.titel)}</div><div class="dok-unter">${esc(d.id)}${d.anlage ? ' · ' + esc(d.anlage) : ''} · ${esc(d.pfad)}${d.fehlt ? ' · <b style="color:var(--rot)">Datei fehlt</b>' : ''}</div>${d.themen.length ? `<div class="themen">${d.themen.map(t => `<span class="thema">${esc(t)}</span>`).join('')}</div>` : ''}</div></div>
    <div class="dok-datum">${esc(datum(d.datum))}</div><div class="dok-stand">${badge(d.stand, statusTon(d.stand))}</div></div>`;
}
function gefilterteDoks() {
  const f = S.filter; let l = dokListe();
  if (S.treffer) l = l.filter(d => S.treffer.includes(d.id));
  if (f.gruppe) l = l.filter(d => d.gruppe === f.gruppe);
  if (f.typ) l = l.filter(d => d.typ === f.typ);
  if (f.stand) l = l.filter(d => d.stand === f.stand);
  return l;
}
function zeitstrahl(eintraege, art) {
  return `<div class="zeitstrahl">${eintraege.map(e => `<div class="zs-zeile"><div class="zs-datum">${esc(datum(e.datum))}</div><div class="zs-karte"><div class="zs-inhalt"><div class="tafel-kopf"><span>${badge(e.art)}${e.pruefstatus ? ' ' + badge('Prüfstatus: ' + e.pruefstatus, statusTon(e.pruefstatus)) : ''}</span><button class="knopf klein" data-aktion="bearbeiten" data-art="${art}" data-id="${esc(e.id)}">Bearbeiten</button></div><h3>${esc(e.titel)}</h3><p>${esc(e.detail || e.berechnung || '')}</p>${e.quelle ? `<p style="margin-top:6px"><a href="${fallLink(fallId(), 'dokumente', e.quelle)}">Quelle ${esc(e.quelle)}${dok(e.quelle) ? ' · ' + esc(dok(e.quelle).titel) : ''}</a></p>` : ''}</div></div></div>`).join('')}</div>`;
}
const FALL = {
  async uebersicht() {
    const a = akte(), f = a.fall;
    const fristen = a.fristen.filter(x => x.pruefstatus !== 'erledigt').sort((x, y) => x.datum.localeCompare(y.datum)).slice(0, 5).map(x => ({...x, fallId: f.id, fallTitel: f.titel}));
    const aufgaben = a.aufgaben.filter(x => !x.erledigt).slice(0, 5);
    const gruppen = GRUPPEN.map((g, i) => `<button class="bereich-link" data-aktion="gruppe" data-gruppe="${esc(g)}"><b>${g.slice(0, 2)}</b>${esc(g.slice(3))}<span>${dokListe().filter(d => d.gruppe === g).length}</span></button>`).join('');
    const j = S.fall.journal.slice(-1)[0];
    const inhalt = `<section class="tafel"><div class="tafel-kopf"><div><span class="kennung">${esc(f.id)}</span> ${badge(f.bereich)} ${badge(f.status, f.status === 'offen' ? 'gruen' : '')}</div><button class="knopf klein" data-aktion="fall-bearbeiten">Fall bearbeiten</button></div>
      <div class="raster drei" style="margin-top:8px"><div class="feld-anzeige"><b>Rolle</b><span>${esc(f.rolle || 'noch offen')}</span></div><div class="feld-anzeige"><b>Ziel</b><span>${esc(f.ziel || 'noch offen')}</span></div><div class="feld-anzeige"><b>Verfahren</b><span>${a.verfahren.map(v => `${esc(v.art)}${v.aktenzeichen ? ' · ' + esc(v.aktenzeichen) : ''}`).join('<br>') || 'noch keins'}</span></div></div>
      ${f.untertitel ? `<p class="untertitel" style="margin:0">${esc(f.untertitel)}</p>` : ''}</section>
      <div class="kacheln" style="margin-top:18px"><div class="kachel"><strong>${dokListe().length}</strong><span>Dokumente</span></div><div class="kachel"><strong>${a.aufgaben.filter(x => !x.erledigt).length}</strong><span>offene Aufgaben</span></div><div class="kachel"><strong>${a.fristen.filter(x => x.pruefstatus !== 'erledigt').length}</strong><span>Fristen und Termine</span></div><div class="kachel"><strong>${a.ereignisse.length}</strong><span>Ereignisse</span></div></div>
      <div class="raster"><section class="tafel"><div class="tafel-kopf"><h2>Nächste Fristen</h2><a href="${fallLink(f.id, 'fristen')}">Alle</a></div>${fristen.length ? fristen.map(x => fristZeile(x, false)).join('') : '<p class="untertitel" style="margin:0">Keine offenen Fristen.</p>'}</section>
      <section class="tafel"><div class="tafel-kopf"><h2>Offene Aufgaben</h2><a href="${fallLink(f.id, 'aufgaben')}">Alle</a></div>${aufgaben.length ? aufgaben.map(x => `<div class="zeile"><div class="zeile-text"><h3>${esc(x.titel)}</h3><p>${x.faellig ? 'fällig ' + esc(datum(x.faellig)) + ' · ' : ''}${esc(x.detail)}</p></div></div>`).join('') : '<p class="untertitel" style="margin:0">Keine offenen Aufgaben.</p>'}</section></div>
      <div class="raster" style="margin-top:18px"><section class="tafel"><h2>Aktenbereiche</h2><div class="bereiche">${gruppen}</div></section>
      <section class="tafel"><div class="tafel-kopf"><h2>Angeheftet</h2></div>${f.angeheftet.length ? f.angeheftet.map(id => dok(id) ? `<div class="zeile"><div class="zeile-text"><h3><a href="${fallLink(f.id, 'dokumente', id)}">${esc(dok(id).titel)}</a></h3><p>${esc(id)} · ${esc(dok(id).pfad)}</p></div></div>` : '').join('') : '<p class="untertitel" style="margin:0">Wichtige Dokumente über „Ordnen“ anheften.</p>'}
      <div class="tafel-kopf" style="margin-top:16px"><h2>Zuletzt im Journal</h2><a href="${fallLink(f.id, 'journal')}">Journal</a></div>${j ? `<div class="zeile"><div class="datumsbox"><b>${datum(j.datum).slice(0, 5)}</b>${datum(j.datum).slice(6)}</div><div class="zeile-text"><h3>${esc(j.titel)}</h3><p>${esc(j.text)}</p></div></div>` : '<p class="untertitel" style="margin:0">Noch kein Eintrag.</p>'}</section></div>
      <section class="tafel" style="margin-top:18px"><div class="tafel-kopf"><h2>Notizen</h2><button class="knopf klein" data-aktion="neu" data-art="notiz">Notiz</button></div>${a.notizen.length ? a.notizen.map(n => `<div class="zeile"><div class="zeile-text"><h3>${esc(n.titel)}</h3><p>${esc(n.text)}</p><p>${esc(datum(n.datum))}</p></div><div class="aktionen"><button class="knopf klein" data-aktion="bearbeiten" data-art="notiz" data-id="${esc(n.id)}">Bearbeiten</button></div></div>`).join('') : '<p class="untertitel" style="margin:0">Keine Notizen.</p>'}</section>`;
    return [f.titel, '', inhalt, `<button class="knopf still" data-aktion="neu-laden">Neu einlesen</button><button class="knopf" data-aktion="finder" data-fall="${esc(f.id)}">Ordner im Finder</button><button class="knopf primaer" data-aktion="hochladen" data-ziel="fall">Dokument hinzufügen</button>`];
  },
  async dokumente() {
    const l = gefilterteDoks(); const typen = [...new Set(dokListe().map(d => d.typ).filter(Boolean))].sort();
    const inhalt = `<div class="filter"><input id="dok-suche" type="search" value="${esc(S.filter.q)}" placeholder="Dokumente, Personen oder Inhalte suchen …" aria-label="Akte durchsuchen"><select id="f-gruppe" aria-label="Bereich">${opt(GRUPPEN, S.filter.gruppe, 'Alle Bereiche')}</select><select id="f-typ" aria-label="Dateityp">${opt(typen, S.filter.typ, 'Alle Typen')}</select><select id="f-stand" aria-label="Stand">${opt(DOK_STAND, S.filter.stand, 'Jeder Stand')}</select><span class="zaehler">${l.length} von ${dokListe().length}</span></div>
      <div class="dok-tabelle"><div class="dok-kopf"><span>Dokument</span><span>Datum</span><span>Stand</span></div>${l.map(dokZeile).join('') || '<div class="leer"><h2>Nichts gefunden</h2><p>Andere Suche oder Filter zurücksetzen. Neue Dateien mit „Dokument hinzufügen“ oder im Finder in 01 Eingang ablegen.</p></div>'}</div>`;
    return ['Dokumente', '', inhalt, `<button class="knopf still" data-aktion="neu-laden">Neu einlesen</button><button class="knopf" data-aktion="finder" data-fall="${esc(fallId())}" data-gruppe="01 Eingang">Eingang im Finder</button><button class="knopf primaer" data-aktion="hochladen" data-ziel="fall">Dokument hinzufügen</button>`];
  },
  async beteiligte() {
    const l = akte().beteiligte;
    const inhalt = l.length ? `<table class="tabelle"><thead><tr><th>Kennung</th><th>Name</th><th>Rolle</th><th>Aktenzeichen</th><th>Kontakt</th><th></th></tr></thead><tbody>${l.map(b => `<tr><td>${esc(b.id)}</td><td><b>${esc(b.name)}</b>${b.anschrift ? '<br><small>' + esc(b.anschrift) + '</small>' : ''}</td><td>${badge(b.rolle)}</td><td>${esc(b.aktenzeichen)}</td><td>${esc(b.kontakt)}</td><td><button class="knopf klein" data-aktion="bearbeiten" data-art="beteiligter" data-id="${esc(b.id)}">Bearbeiten</button></td></tr>`).join('')}</tbody></table>` : '<div class="leer"><h2>Noch keine Beteiligten</h2><p>Gegner, Gericht, Behörde, Anwalt, Zeugen. Dokumente und Verfahren verweisen auf diese Kennungen.</p></div>';
    return ['Beteiligte', 'Wer ist beteiligt, in welcher Rolle, unter welchem Aktenzeichen.', inhalt, '<button class="knopf primaer" data-aktion="neu" data-art="beteiligter">Beteiligter</button>'];
  },
  async verfahren() {
    const l = akte().verfahren;
    const inhalt = l.length ? `<div class="raster">${l.map(v => `<article class="karte"><span class="kennung">${esc(v.id)}</span><h2>${esc(v.art)}</h2><p><b>Stelle:</b> ${esc(personName(v.stelle) || 'offen')}<br><b>Aktenzeichen:</b> ${esc(v.aktenzeichen || 'noch keins')}<br><b>Stand:</b> ${esc(v.stand || 'offen')}<br><b>Ordner:</b> ${esc(v.ordner || '')}</p><div class="karte-fuss"><button class="knopf klein" data-aktion="bearbeiten" data-art="verfahren" data-id="${esc(v.id)}">Bearbeiten</button></div></article>`).join('')}</div>` : '<div class="leer"><h2>Noch kein Verfahren</h2><p>Ein Verfahren ist alles mit eigener Stelle und eigenem Aktenzeichen: Klage, Bußgeldbescheid, Widerspruch, Mahnverfahren, Strafanzeige.</p></div>';
    return ['Verfahren', 'Mehrere Verfahren in einem Konflikt werden getrennt geführt, mit getrennten Fristen.', inhalt, '<button class="knopf primaer" data-aktion="neu" data-art="verfahren">Verfahren</button>'];
  },
  async chronologie() {
    const l = [...akte().ereignisse].sort((a, b) => a.datum.localeCompare(b.datum));
    return ['Chronologie', 'Ereignisse nach belegtem Zeitpunkt. Zugang, Versand und Dokumentdatum sind verschiedene Dinge.', l.length ? zeitstrahl(l, 'ereignis') : '<div class="leer"><h2>Noch kein Ereignis</h2></div>', '<button class="knopf primaer" data-aktion="neu" data-art="ereignis">Ereignis</button>'];
  },
  async fristen() {
    const l = [...akte().fristen].sort((a, b) => a.datum.localeCompare(b.datum));
    const inhalt = l.length ? `<table class="tabelle"><thead><tr><th>Datum</th><th>Frist oder Termin</th><th>Art</th><th>Prüfstatus</th><th>Grundlage</th><th></th></tr></thead><tbody>${l.map(f => { const t = tageBis(f.datum); return `<tr><td style="white-space:nowrap"><b>${esc(datum(f.datum))}</b><br><small>${f.pruefstatus === 'erledigt' ? 'erledigt' : t < 0 ? 'vorbei' : t === 0 ? 'heute' : 'in ' + t + ' Tagen'}</small></td><td><b>${esc(f.titel)}</b><br><small>${esc(f.ausloeser)}</small></td><td>${badge(f.art)}</td><td>${badge(f.pruefstatus, statusTon(f.pruefstatus))}</td><td><small>${esc(f.rechtsgrundlage)}</small>${f.quelle ? `<br><a href="${fallLink(fallId(), 'dokumente', f.quelle)}">${esc(f.quelle)}</a>` : ''}</td><td><button class="knopf klein" data-aktion="bearbeiten" data-art="frist" data-id="${esc(f.id)}">Bearbeiten</button></td></tr>`; }).join('')}</tbody></table>` : '<div class="leer"><h2>Noch keine Frist</h2><p>Jede Frist mit Auslöser, Rechtsgrundlage, Rechnung und Quelle. Der Rechner hilft bei der Rechnung.</p></div>';
    return ['Fristen und Termine', '„Bestätigt“ nur mit Auslöser, Rechtsgrundlage, Rechnung und Quelle. Der Rechner entscheidet nicht, welche Frist gilt.', inhalt, '<button class="knopf" data-aktion="rechner">Fristenrechner</button><button class="knopf primaer" data-aktion="neu" data-art="frist">Frist oder Termin</button>'];
  },
  async aufgaben() {
    const l = akte().aufgaben;
    const inhalt = l.length ? `<section class="tafel">${l.map(x => `<div class="aufgabe ${x.erledigt ? 'erledigt' : ''}"><input type="checkbox" data-aufgabe="${esc(x.id)}" ${x.erledigt ? 'checked' : ''} aria-label="Erledigt: ${esc(x.titel)}"><div class="zeile-text"><h3>${esc(x.titel)}</h3><p>${esc(x.detail)}</p><p>${x.faellig ? 'fällig ' + esc(datum(x.faellig)) : ''}${x.quelle ? ` · <a href="${fallLink(fallId(), 'dokumente', x.quelle)}">${esc(x.quelle)}</a>` : ''}</p></div><div class="aktionen"><button class="knopf klein" data-aktion="bearbeiten" data-art="aufgabe" data-id="${esc(x.id)}">Bearbeiten</button></div></div>`).join('')}</section>` : '<div class="leer"><h2>Keine Aufgaben</h2></div>';
    return ['Aufgaben', '', inhalt, '<button class="knopf primaer" data-aktion="neu" data-art="aufgabe">Aufgabe</button>'];
  },
  async entwuerfe() {
    const l = akte().entwuerfe; const dateien = dokListe().filter(d => d.gruppe === '06 Entwürfe');
    const inhalt = `<section class="tafel"><h2>Entwürfe mit Fassung</h2>${l.length ? l.map(w => `<div class="zeile"><div class="zeile-text"><h3>${esc(w.titel)}</h3><p>Fassung ${w.fassung} · ${esc(w.datei)}${w.versandt_als ? ` · versandt als <a href="${fallLink(fallId(), 'dokumente', w.versandt_als)}">${esc(w.versandt_als)}</a>` : ''}</p></div>${badge(w.status, w.status === 'versandt' ? 'gruen' : w.status === 'geprüft' ? 'blau' : 'gelb')}<div class="aktionen"><button class="knopf klein" data-aktion="bearbeiten" data-art="entwurf" data-id="${esc(w.id)}">Bearbeiten</button></div></div>`).join('') : '<p class="untertitel" style="margin:0">Noch kein Entwurf erfasst. Ein Entwurf bleibt Entwurf, bis der Versand belegt ist.</p>'}</section>
      <section class="tafel"><h2>Dateien in 06 Entwürfe</h2>${dateien.length ? dateien.map(d => `<div class="zeile"><div class="zeile-text"><h3><a href="${fallLink(fallId(), 'dokumente', d.id)}">${esc(d.titel)}</a></h3><p>${esc(d.id)} · ${esc(d.pfad)}</p></div>${badge(d.stand, statusTon(d.stand))}</div>`).join('') : '<p class="untertitel" style="margin:0">Keine Dateien im Ordner 06 Entwürfe.</p>'}</section>`;
    return ['Entwürfe', 'Noch nicht versandte Texte. Dateiname endet auf _ENTWURF. Versand nur nach Freigabe, dann Beleg als Dokument.', inhalt, '<button class="knopf primaer" data-aktion="neu" data-art="entwurf">Entwurf erfassen</button>'];
  },
  async anlagen() {
    const nat = s => String(s).replace(/\d+/g, m => m.padStart(5, '0'));
    const anl = dokListe().filter(d => d.anlage).sort((a, b) => nat(a.anlage).localeCompare(nat(b.anlage)));
    const bew = dokListe().filter(d => d.gruppe === '05 Beweise');
    const inhalt = `<section class="tafel"><h2>Anlagenverzeichnis</h2><p class="untertitel" style="margin-bottom:10px">Zuordnung vorhandener Dateien zu Anlagenkennungen. Kein Nachweis, welcher Satz tatsächlich eingereicht wurde.</p>${anl.length ? `<table class="tabelle"><thead><tr><th>Anlage</th><th>Dokument</th><th>Datum</th><th>Stand</th></tr></thead><tbody>${anl.map(d => `<tr class="klick" data-dok-link="${esc(d.id)}"><td><b>${esc(d.anlage)}</b></td><td>${esc(d.titel)}<br><small>${esc(d.id)} · ${esc(d.pfad)}</small></td><td>${esc(datum(d.datum))}</td><td>${badge(d.stand, statusTon(d.stand))}</td></tr>`).join('')}</tbody></table>` : '<p class="untertitel" style="margin:0">Noch keine Anlagenkennungen vergeben. Über „Ordnen“ am Dokument.</p>'}</section>
      <section class="tafel"><h2>Beweise (05 Beweise)</h2>${bew.length ? `<div class="raster drei">${bew.map(d => `<article class="karte"><span class="kennung">${esc(d.id)}</span><h2 style="font-size:.95rem"><a href="${fallLink(fallId(), 'dokumente', d.id)}">${esc(d.titel)}</a></h2><p>${esc(d.pfad)}</p></article>`).join('')}</div>` : '<p class="untertitel" style="margin:0">Keine Dateien in 05 Beweise.</p>'}</section>`;
    return ['Beweise und Anlagen', '', inhalt, ''];
  },
  async journal() {
    const l = [...S.fall.journal].reverse();
    const inhalt = l.length ? `<section class="tafel">${l.map(j => `<div class="zeile"><div class="datumsbox"><b>${datum(j.datum).slice(0, 5)}</b>${datum(j.datum).slice(6)}</div><div class="zeile-text"><h3>${esc(j.titel)} ${badge(j.art)}</h3><p>${esc(j.text)}</p></div></div>`).join('')}</section>` : '<div class="leer"><h2>Noch kein Eintrag</h2></div>';
    return ['Journal', 'Verlauf des Falls, nur anhängen. Aufgaben und Fristen stehen nicht hier.', inhalt, '<button class="knopf primaer" data-aktion="journal">Eintrag</button>'];
  },
};

// ---------------------------------------------------------------- Vorschau
async function vorschau(zeigen) {
  const v = $('#vorschau'), b = $('#bereich');
  if (!zeigen || !dok(S.auswahl)) { v.hidden = true; b.classList.remove('hat-vorschau', 'breit'); S.breit = false; return; }
  const d = dok(S.auswahl); v.hidden = false; b.classList.add('hat-vorschau'); b.classList.toggle('breit', S.breit);
  const tab = S.tab, id = fallId();
  const kopf = `<div class="vorschau-kopf"><div class="tafel-kopf"><span class="kennung">${esc(d.id)}${d.anlage ? ' · ' + esc(d.anlage) : ''}</span><button class="symbol" data-aktion="vorschau-zu" aria-label="Vorschau schließen">×</button></div><h2>${esc(d.titel)}</h2>
    <div class="aktionen"><button class="knopf klein primaer" data-aktion="ordnen">Ordnen</button><button class="knopf klein" data-aktion="einsortieren">Einsortieren</button><button class="knopf klein" data-aktion="oeffnen">Öffnen</button><button class="knopf klein" data-aktion="finder" data-fall="${esc(id)}" data-dok="${esc(d.id)}">Im Finder zeigen</button><button class="knopf klein still" data-aktion="breit">${S.breit ? 'Geteilte Ansicht' : 'Groß lesen'}</button></div>
    <div class="tabs" style="margin:12px 0 0">${[['vorschau', 'Vorschau'], ['text', 'Text'], ['angaben', 'Angaben']].map(([k, n]) => `<button data-tab="${k}" class="${tab === k ? 'aktiv' : ''}">${n}</button>`).join('')}</div></div>`;
  let inhalt = '', klasse = 'vorschau-inhalt';
  if (d.fehlt) inhalt = '<div class="hinweis rot">Die Datei fehlt am registrierten Ort. Bestand neu einlesen oder im Finder nachsehen.</div>';
  else if (tab === 'vorschau') {
    klasse += ' dokument';
    if (['JPG', 'JPEG', 'PNG', 'GIF'].includes(d.typ)) inhalt = `<img src="/raw/${id}/${d.id}" alt="${esc(d.titel)}">`;
    else if (['PDF', 'HTML', 'TXT', 'MD', 'HTM'].includes(d.typ)) inhalt = `<iframe src="/raw/${id}/${d.id}" title="${esc(d.titel)}" sandbox="allow-scripts"></iframe>`;
    else { klasse = 'vorschau-inhalt'; inhalt = `<div class="hinweis">Für ${esc(d.typ)} gibt es keine eingebettete Anzeige. „Text“ zeigt den Inhalt, „Öffnen“ startet das passende Programm.</div>`; }
  } else if (tab === 'text') {
    klasse += ' dokument';
    v.innerHTML = kopf + `<div class="${klasse}"><pre>Text wird gelesen …</pre></div>`;
    try { const t = await api.get(`/api/fall/${id}/text/${d.id}`); inhalt = (t.hinweis ? `<div class="hinweis" style="margin:12px 16px">${esc(t.hinweis)}</div>` : '') + `<pre>${esc(t.text || '(kein Text)')}</pre>`; } catch (e) { inhalt = `<div class="hinweis rot">${esc(e.message)}</div>`; }
  } else {
    const felder = [['Pfad', d.pfad], ['Datum', datum(d.datum) + ' (Ordnungsdatum, kein Zugangsnachweis)'], ['Art', d.art], ['Stand', d.stand], ['Themen', d.themen.join(', ')], ['Anlage', d.anlage], ['Personen', d.personen.map(personName).join('; ')], ['Verweise', d.verweise.join(', ')], ['Notiz', d.notiz], ['Größe', groesse(d.groesse)]];
    inhalt = felder.map(([k, w]) => `<div class="feld-anzeige"><b>${k}</b><span>${esc(w || '–')}</span></div>`).join('') + (d.verweise.length ? `<div class="feld-anzeige"><b>Verknüpfte Dokumente</b>${d.verweise.map(x => dok(x) ? `<span><a href="${fallLink(id, 'dokumente', x)}">${esc(x)} · ${esc(dok(x).titel)}</a></span><br>` : '').join('')}</div>` : '');
  }
  v.innerHTML = kopf + `<div class="${klasse}">${inhalt}</div>`;
}

// ---------------------------------------------------------------- Dialoge und Speichern
let dialogSpeichern = null, dialogVeraendert = false;
function feld(name, label, wert = '', art = 'text', extra = {}) {
  const hinweis = extra.hinweis ? `<small>${esc(extra.hinweis)}</small>` : '';
  if (art === 'textarea') return `<label class="feld">${esc(label)}<textarea name="${name}" ${extra.rows ? `rows="${extra.rows}"` : ''}>${esc(wert)}</textarea>${hinweis}</label>`;
  if (art === 'select') return `<label class="feld">${esc(label)}<select name="${name}">${extra.optionen}</select>${hinweis}</label>`;
  return `<label class="feld">${esc(label)}<input name="${name}" type="${art}" value="${esc(wert)}" ${extra.attr || ''}>${hinweis}</label>`;
}
function dialog(titel, inhalt, speichern, knopf = 'Speichern') {
  $('#dialog-titel').textContent = titel; $('#dialog-inhalt').innerHTML = inhalt; $('#dialog-fehler').hidden = true;
  $('#dialog-speichern').textContent = knopf; $('#dialog-speichern').hidden = !speichern; $('#dialog-abbrechen').textContent = speichern ? 'Abbrechen' : 'Schließen';
  dialogSpeichern = speichern; dialogVeraendert = false; $('#dialog').showModal();
}
function dialogZu() { if (dialogVeraendert && !confirm('Ungespeicherte Angaben verwerfen?')) return; dialogVeraendert = false; $('#dialog').close(); }
async function akteSpeichern(aendern, meldung = 'Gespeichert.') {
  const kopie = JSON.parse(JSON.stringify(akte())); aendern(kopie);
  const r = await api.post('/api/fall/' + fallId(), {akte: kopie, revision: S.fall.revision});
  await ladeFall(fallId()); if (meldung) toast(meldung); await render();
}
const liste = s => s.split(/[;,]/).map(x => x.trim()).filter(Boolean);

const FORMULARE = {
  beteiligter: {liste: 'beteiligte', kennung: 'P', titel: 'Beteiligter', felder: b => `<div class="feld-reihe">${feld('name', 'Name oder Stelle', b.name)}${feld('rolle', 'Rolle', b.rolle, 'select', {optionen: opt(ROLLEN, b.rolle, 'Keine Angabe')})}</div>${feld('anschrift', 'Anschrift', b.anschrift)}<div class="feld-reihe">${feld('kontakt', 'Kontakt', b.kontakt)}${feld('aktenzeichen', 'Aktenzeichen dieser Stelle', b.aktenzeichen)}</div>`,
    lesen: f => ({name: f.get('name').trim(), rolle: f.get('rolle'), anschrift: f.get('anschrift').trim(), kontakt: f.get('kontakt').trim(), aktenzeichen: f.get('aktenzeichen').trim()}), leer: {name: '', rolle: '', anschrift: '', kontakt: '', aktenzeichen: ''}},
  verfahren: {liste: 'verfahren', kennung: 'V', titel: 'Verfahren', felder: v => `${feld('art', 'Art des Verfahrens', v.art, 'text', {hinweis: 'z. B. Klage Arbeitsgericht, Bußgeldverfahren, Widerspruch, Mahnverfahren'})}<div class="feld-reihe">${feld('stelle', 'Zuständige Stelle', v.stelle, 'select', {optionen: personOptionen(v.stelle)})}${feld('aktenzeichen', 'Aktenzeichen', v.aktenzeichen)}</div>${feld('stand', 'Verfahrensstand', v.stand)}${feld('ordner', 'Unterordner in 04 Verfahren', v.ordner, 'text', {hinweis: 'z. B. 04 Verfahren/01 Teilkündigung'})}`,
    lesen: f => ({art: f.get('art').trim(), stelle: f.get('stelle'), aktenzeichen: f.get('aktenzeichen').trim(), stand: f.get('stand').trim(), ordner: f.get('ordner').trim()}), leer: {art: '', stelle: '', aktenzeichen: '', stand: '', ordner: ''}},
  ereignis: {liste: 'ereignisse', kennung: 'E', titel: 'Ereignis', felder: e => `<div class="feld-reihe">${feld('datum', 'Datum', e.datum, 'date')}${feld('art', 'Art', e.art, 'select', {optionen: opt(EREIGNIS_ART, e.art || 'Vermerk')})}</div>${feld('titel', 'Kurztitel', e.titel)}${feld('quelle', 'Quelle', e.quelle, 'select', {optionen: dokOptionen(e.quelle)})}${feld('detail', 'Einzelheiten', e.detail, 'textarea', {hinweis: 'Was steht im Dokument, was ist eigene Angabe, was ist Behauptung der Gegenseite?'})}`,
    lesen: f => ({datum: f.get('datum'), art: f.get('art'), titel: f.get('titel').trim(), quelle: f.get('quelle'), detail: f.get('detail').trim()}), leer: {datum: heute(), titel: '', art: 'Vermerk', quelle: '', detail: ''}},
  frist: {liste: 'fristen', kennung: 'F', titel: 'Frist oder Termin', felder: x => `<div class="rechner"><h3>Fristenrechner (§§ 187, 188, 193 BGB, Feiertage nach Einstellung)</h3><div class="feld-reihe drei">${feld('r_start', 'Ereignistag (Zugang)', x.r_start || '', 'date')}${feld('r_menge', 'Dauer', x.r_menge || 2, 'number', {attr: 'min="1"'})}${feld('r_einheit', 'Einheit', x.r_einheit || 'wochen', 'select', {optionen: opt(['tage', 'wochen', 'monate', 'jahre'], x.r_einheit || 'wochen')})}</div><div class="feld-reihe">${feld('r_ereignis', 'Ereignistag zählt', 'ja', 'select', {optionen: opt([['ja', 'nicht mit (§ 187 Abs. 1, Regelfall)'], ['nein', 'mit (§ 187 Abs. 2)']], 'ja')})}${feld('r_werktag', 'Wochenende und Feiertag', 'ja', 'select', {optionen: opt([['ja', 'auf nächsten Werktag (§ 193)'], ['nein', 'nicht verschieben']], 'ja')})}</div><button type="button" class="knopf klein" data-aktion="berechnen">Berechnen und übernehmen</button><div class="ergebnis" id="rechner-ergebnis"></div></div>
    <div class="feld-reihe">${feld('datum', 'Fristende oder Termin', x.datum, 'date')}${feld('art', 'Art', x.art, 'select', {optionen: opt(FRIST_ART, x.art || 'gesetzlich')})}</div>${feld('titel', 'Kurztitel', x.titel)}${feld('ausloeser', 'Auslöser und Zugang', x.ausloeser, 'text', {hinweis: 'z. B. Zustellung am 05.09.2026, Umschlag D0004'})}${feld('rechtsgrundlage', 'Rechtsgrundlage', x.rechtsgrundlage, 'text', {hinweis: 'Norm mit Absatz und Gesetz, z. B. § 67 Abs. 1 OWiG'})}${feld('berechnung', 'Rechnung', x.berechnung, 'textarea')}<div class="feld-reihe">${feld('pruefstatus', 'Prüfstatus', x.pruefstatus, 'select', {optionen: opt(FRIST_STATUS, x.pruefstatus || 'offen'), hinweis: '„bestätigt“ nur mit Auslöser, Grundlage, Rechnung und Quelle.'})}${feld('quelle', 'Quelle', x.quelle, 'select', {optionen: dokOptionen(x.quelle)})}</div>`,
    lesen: f => ({datum: f.get('datum'), art: f.get('art'), titel: f.get('titel').trim(), ausloeser: f.get('ausloeser').trim(), rechtsgrundlage: f.get('rechtsgrundlage').trim(), berechnung: f.get('berechnung').trim(), pruefstatus: f.get('pruefstatus'), quelle: f.get('quelle')}), leer: {datum: '', titel: '', art: 'gesetzlich', ausloeser: '', rechtsgrundlage: '', berechnung: '', pruefstatus: 'offen', quelle: ''}},
  aufgabe: {liste: 'aufgaben', kennung: 'A', titel: 'Aufgabe', felder: a => `${feld('titel', 'Aufgabe', a.titel)}${feld('detail', 'Einzelheiten', a.detail, 'textarea')}<div class="feld-reihe drei">${feld('faellig', 'Fällig', a.faellig, 'date')}${feld('quelle', 'Quelle', a.quelle, 'select', {optionen: dokOptionen(a.quelle)})}${feld('erledigt', 'Erledigt', a.erledigt ? 'ja' : 'nein', 'select', {optionen: opt([['nein', 'Nein'], ['ja', 'Ja']], a.erledigt ? 'ja' : 'nein')})}</div>`,
    lesen: f => ({titel: f.get('titel').trim(), detail: f.get('detail').trim(), faellig: f.get('faellig'), quelle: f.get('quelle'), erledigt: f.get('erledigt') === 'ja'}), leer: {titel: '', detail: '', faellig: '', quelle: '', erledigt: false}},
  entwurf: {liste: 'entwuerfe', kennung: 'W', titel: 'Entwurf', felder: w => `${feld('titel', 'Titel', w.titel)}${feld('datei', 'Datei', w.datei, 'text', {hinweis: 'Pfad im Fallordner, z. B. 06 Entwürfe/Einspruch_ENTWURF.txt'})}<div class="feld-reihe drei">${feld('fassung', 'Fassung', w.fassung || 1, 'number', {attr: 'min="1"'})}${feld('status', 'Status', w.status, 'select', {optionen: opt(ENTWURF_STATUS, w.status || 'in Arbeit')})}${feld('versandt_als', 'Versandt als', w.versandt_als, 'select', {optionen: dokOptionen(w.versandt_als, 'Noch nicht versandt'), hinweis: 'Pflicht bei Status versandt'})}</div>`,
    lesen: f => ({titel: f.get('titel').trim(), datei: f.get('datei').trim(), fassung: parseInt(f.get('fassung'), 10) || 1, status: f.get('status'), versandt_als: f.get('versandt_als')}), leer: {titel: '', datei: '', fassung: 1, status: 'in Arbeit', versandt_als: ''}},
  notiz: {liste: 'notizen', kennung: 'N', titel: 'Notiz', felder: n => `${feld('titel', 'Titel', n.titel)}${feld('text', 'Text', n.text, 'textarea', {rows: 8})}`,
    lesen: f => ({titel: f.get('titel').trim(), text: f.get('text').trim(), datum: heute()}), leer: {titel: '', text: '', datum: ''}},
};
function eintragDialog(art, id) {
  const F = FORMULARE[art]; const vorhanden = id ? akte()[F.liste].find(x => x.id === id) : null; const werte = vorhanden || {id: '', ...F.leer};
  dialog((id ? 'Bearbeiten: ' : 'Neu: ') + F.titel + (id ? ' ' + id : ''), F.felder(werte) + (id ? `<p><button type="button" class="knopf klein" data-aktion="eintrag-entfernen" data-art="${art}" data-id="${esc(id)}">Eintrag entfernen</button> <small style="color:var(--muted)">Nur möglich, wenn nichts darauf verweist.</small></p>` : ''),
    async f => { const neu = F.lesen(f); await akteSpeichern(a => { const l = a[F.liste]; if (id) Object.assign(l.find(x => x.id === id), neu); else l.push({id: naechste(l, F.kennung), ...neu}); }); });
}
function ordnenDialog(d) {
  dialog('Ordnen: ' + d.id, `<div class="hinweis">Nur Ordnungsangaben. Datei, Dateiname und Inhalt bleiben unverändert.</div>${feld('titel', 'Anzeigetitel', d.titel)}<div class="feld-reihe drei">${feld('datum', 'Dokumentdatum', d.datum, 'date', {hinweis: 'kein Zugangsnachweis'})}${feld('art', 'Art', d.art, 'select', {optionen: opt(DOK_ART, d.art, 'Keine Angabe')})}${feld('stand', 'Stand', d.stand, 'select', {optionen: opt(DOK_STAND, d.stand)})}</div><div class="feld-reihe">${feld('themen', 'Themen', d.themen.join(', '), 'text', {hinweis: 'durch Komma getrennt'})}${feld('anlage', 'Anlagenkennung', d.anlage, 'text', {hinweis: 'z. B. K 8 oder B 1, so wie im Schriftsatz'})}</div>
    <label class="feld">Personen<div class="hinweis" style="margin:6px 0">${akte().beteiligte.length ? akte().beteiligte.map(b => `<label style="display:block;font-weight:400"><input type="checkbox" name="personen" value="${esc(b.id)}" ${d.personen.includes(b.id) ? 'checked' : ''}> ${esc(b.id)} · ${esc(b.name)}</label>`).join('') : 'Noch keine Beteiligten erfasst.'}</div></label>
    ${feld('verweise', 'Verweise auf Dokumente', d.verweise.join(', '), 'text', {hinweis: 'D-Kennungen, durch Komma getrennt'})}${feld('notiz', 'Ordnungsnotiz', d.notiz, 'textarea')}${feld('angeheftet', 'Auf der Übersicht anheften', akte().fall.angeheftet.includes(d.id) ? 'ja' : 'nein', 'select', {optionen: opt([['nein', 'Nein'], ['ja', 'Ja']], akte().fall.angeheftet.includes(d.id) ? 'ja' : 'nein')})}`,
    async f => { await akteSpeichern(a => { const x = a.dokumente[d.id]; Object.assign(x, {titel: f.get('titel').trim(), datum: f.get('datum'), art: f.get('art'), stand: f.get('stand'), themen: liste(f.get('themen')), anlage: f.get('anlage').trim(), personen: f.getAll('personen'), verweise: liste(f.get('verweise')).map(s => s.toUpperCase()), notiz: f.get('notiz').trim()});
      const p = a.fall.angeheftet.filter(i => i !== d.id); if (f.get('angeheftet') === 'ja') p.push(d.id); a.fall.angeheftet = p; }); });
}
function einsortierenDialog(d) {
  dialog('Einsortieren: ' + d.titel, `<p class="pfad">${esc(d.pfad)}</p><div class="feld-reihe">${feld('bereich', 'Aktenbereich', d.gruppe, 'select', {optionen: opt(GRUPPEN, d.gruppe)})}${feld('unterordner', 'Unterordner', d.pfad.split('/').slice(1, -1).join('/'), 'text', {hinweis: 'optional, z. B. An Vorstand oder Versandnachweise'})}</div><div class="hinweis">Kennung und Inhalt bleiben erhalten. Eine gleichnamige Datei am Ziel wird nie überschrieben.</div>`,
    async f => { await api.werkzeug('dokument_verschieben', {fall: fallId(), dokument: d.id, bereich: f.get('bereich'), unterordner: f.get('unterordner').trim()}); await ladeFall(fallId()); toast('Einsortiert.'); await render(); }, 'Verschieben');
}
function neuerFallDialog() {
  dialog('Neuen Fall anlegen', `${feld('titel', 'Kurze Bezeichnung', '', 'text', {attr: 'required maxlength="120"'})}<div class="feld-reihe">${feld('bereich', 'Bereich', 'Allgemein', 'select', {optionen: opt(BEREICHE, 'Allgemein')})}${feld('rolle', 'Deine Rolle, falls bekannt', '', 'text', {hinweis: 'z. B. Betroffener, Mieter, Arbeitnehmer, Käufer'})}</div>${feld('ziel', 'Was möchtest du erreichen?', '', 'textarea')}<div class="hinweis">Verfahrensart, zuständige Stelle und Zugangsdaten bleiben offen, bis die Unterlagen gelesen sind. Aus Dateinamen wird nichts abgeleitet.</div>`,
    async f => { const c = await api.post('/api/fall', {titel: f.get('titel').trim(), bereich: f.get('bereich'), rolle: f.get('rolle').trim(), ziel: f.get('ziel').trim()}); S.zentrale = null; toast(`Fall ${c.id} angelegt.`); location.hash = fallLink(c.id).slice(1); }, 'Fall anlegen');
}
function fallBearbeitenDialog() {
  const f0 = akte().fall;
  dialog('Fall bearbeiten: ' + f0.id, `${feld('titel', 'Bezeichnung', f0.titel)}${feld('untertitel', 'Untertitel', f0.untertitel)}<div class="feld-reihe">${feld('bereich', 'Bereich', f0.bereich, 'select', {optionen: opt(BEREICHE, f0.bereich)})}${feld('status', 'Status', f0.status, 'select', {optionen: opt(['offen', 'ruhend', 'abgeschlossen'], f0.status)})}</div><div class="feld-reihe">${feld('rolle', 'Deine Rolle', f0.rolle)}${feld('rechtsordnung', 'Rechtsordnung', f0.rechtsordnung || 'DE', 'text', {hinweis: 'DE; bei Auslandsbezug Land und Sprache'})}</div>${feld('themen', 'Themen', f0.themen.join(', '), 'text', {hinweis: 'durch Komma getrennt'})}${feld('ziel', 'Ziel', f0.ziel, 'textarea')}`,
    async f => { await akteSpeichern(a => Object.assign(a.fall, {titel: f.get('titel').trim(), untertitel: f.get('untertitel').trim(), bereich: f.get('bereich'), status: f.get('status'), rolle: f.get('rolle').trim(), rechtsordnung: f.get('rechtsordnung').trim(), themen: liste(f.get('themen')), ziel: f.get('ziel').trim()})); S.zentrale = null; });
}
function journalDialog() {
  dialog('Journal-Eintrag', `<div class="feld-reihe">${feld('art', 'Art', 'Arbeit', 'select', {optionen: opt(JOURNAL_ARTEN, 'Arbeit')})}${feld('titel', 'Kurztitel', '')}</div>${feld('text', 'Text', '', 'textarea', {rows: 7, hinweis: 'Bezug auf Kennungen wie D0012, F01, A03. Wird angehängt, nie umgeschrieben.'})}`,
    async f => { await api.werkzeug('journal_schreiben', {fall: fallId(), art: f.get('art'), titel: f.get('titel').trim(), text: f.get('text').trim()}); await ladeFall(fallId()); toast('Eingetragen.'); await render(); }, 'Anhängen');
}
function rechnerDialog() {
  dialog('Fristenrechner', FORMULARE.frist.felder({}).split('<div class="feld-reihe">')[0] + '<p class="untertitel">Zum Eintragen einer Frist „Frist oder Termin“ verwenden; dort steht derselbe Rechner.</p>', null);
}
function zuordnenDialog(name) {
  const f = S.zentrale.faelle.filter(c => !c.fehler);
  if (!f.length) return toast('Bitte zuerst einen Fall anlegen.', true);
  dialog('Datei einem Fall zuordnen', `<p class="pfad">${esc(name)}</p>${feld('fall', 'Ziel-Fall', '', 'select', {optionen: opt(f.map(c => [c.id, c.id + ' · ' + c.titel]))})}`,
    async fd => { await api.post('/api/eingang/zuordnen', {name, fall: fd.get('fall')}); S.zentrale = null; toast('Zugeordnet, liegt jetzt im Eingang des Falls.'); await render(); }, 'Zuordnen');
}
async function hochladen(ziel) {
  const dateien = [...$('#upload').files]; $('#upload').value = ''; let n = 0;
  try {
    for (const f of dateien) {
      if (f.size > 25 * 1024 * 1024) throw new Error(f.name + ': über 25 MB, bitte im Finder ablegen.');
      const inhalt = await new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1]); r.onerror = rej; r.readAsDataURL(f); });
      await api.post(ziel === 'fall' ? `/api/fall/${fallId()}/eingang` : '/api/eingang', {name: f.name, inhalt}); n++;
    }
    toast(n + ' Datei(en) abgelegt.');
  } catch (e) { toast(n + ' abgelegt. ' + e.message, true); }
  S.zentrale = null; if (S.fall) await ladeFall(fallId()); await render();
}

// ---------------------------------------------------------------- Ereignisse
document.addEventListener('click', async e => {
  const zeile = e.target.closest('[data-dok]'); if (zeile && !e.target.closest('a')) { S.auswahl = zeile.dataset.dok; S.tab = 'vorschau'; gehe({seite: 'dokumente', fall: fallId(), dok: S.auswahl}); return; }
  const tr = e.target.closest('[data-dok-link]'); if (tr) { gehe({seite: 'dokumente', fall: fallId(), dok: tr.dataset.dokLink}); return; }
  const tab = e.target.closest('[data-tab]'); if (tab) { S.tab = tab.dataset.tab; vorschau(true); return; }
  const b = e.target.closest('button[data-aktion]'); if (!b) return;
  const a = b.dataset.aktion;
  try {
    if (a === 'neuer-fall') neuerFallDialog();
    else if (a === 'beispiel-laden') { const r = await api.werkzeug('beispiel_laden', {}); S.zentrale = null; toast(`Beispielfall ${r.id} angelegt.`); location.hash = `#seite=uebersicht&fall=${r.id}`; }
    else if (a === 'neu-laden') { S.zentrale = null; S.quellen = null; if (S.fall) await ladeFall(fallId()); await render(); toast('Neu eingelesen.'); }
    else if (a === 'finder') await api.post('/api/oeffnen', {fall: b.dataset.fall, dokument: b.dataset.dok, bereich: b.dataset.gruppe || b.dataset.ort, zeigen: !!b.dataset.dok});
    else if (a === 'oeffnen') await api.post('/api/oeffnen', {fall: fallId(), dokument: S.auswahl});
    else if (a === 'hochladen') { $('#upload').onchange = () => hochladen(b.dataset.ziel); $('#upload').click(); }
    else if (a === 'zuordnen') zuordnenDialog(b.dataset.name);
    else if (a === 'kopieren') { await navigator.clipboard.writeText(b.dataset.text); toast('Kopiert.'); }
    else if (a === 'gruppe') { S.filter.gruppe = b.dataset.gruppe; S.treffer = null; S.filter.q = ''; gehe({seite: 'dokumente', fall: fallId()}); }
    else if (a === 'fall-bearbeiten') fallBearbeitenDialog();
    else if (a === 'neu') eintragDialog(b.dataset.art, '');
    else if (a === 'bearbeiten') eintragDialog(b.dataset.art, b.dataset.id);
    else if (a === 'eintrag-entfernen') { const F = FORMULARE[b.dataset.art]; if (!confirm('Eintrag ' + b.dataset.id + ' wirklich entfernen?')) return; await akteSpeichern(x => { x[F.liste] = x[F.liste].filter(y => y.id !== b.dataset.id); }, 'Entfernt.'); $('#dialog').close(); }
    else if (a === 'ordnen') ordnenDialog(dok(S.auswahl));
    else if (a === 'einsortieren') einsortierenDialog(dok(S.auswahl));
    else if (a === 'vorschau-zu') { S.auswahl = ''; gehe({seite: 'dokumente', fall: fallId()}); }
    else if (a === 'breit') { S.breit = !S.breit; vorschau(true); }
    else if (a === 'journal') journalDialog();
  } catch (err) { toast(err.message, true); }
});
document.addEventListener('keydown', e => { const z = e.target.closest && e.target.closest('[data-dok]'); if (z && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); z.click(); } if ((e.metaKey || e.ctrlKey) && e.key === 'k' && $('#dok-suche')) { e.preventDefault(); $('#dok-suche').focus(); } });
let suchTimer;
document.addEventListener('input', e => {
  if (e.target.closest('#formular')) dialogVeraendert = true;
  if (e.target.id === 'dok-suche') { S.filter.q = e.target.value; clearTimeout(suchTimer); suchTimer = setTimeout(async () => { try { S.treffer = S.filter.q.trim().length > 1 ? (await api.get(`/api/fall/${fallId()}/suche?q=${encodeURIComponent(S.filter.q.trim())}`)).treffer : null; } catch (err) { toast(err.message, true); } const f = $('#dok-suche'); const pos = f && f.selectionStart; await render(); const g = $('#dok-suche'); if (g) { g.focus(); g.setSelectionRange(pos, pos); } }, 300); }
  if (e.target.id === 'fall-suche' || e.target.id === 'fall-filter') { const q = $('#fall-suche').value.toLocaleLowerCase('de'), s = $('#fall-filter').value; $('#fall-liste').innerHTML = S.zentrale.faelle.filter(c => (c.id + ' ' + c.titel + ' ' + (c.bereich || '')).toLocaleLowerCase('de').includes(q) && (s === 'Alle' || c.status === s)).map(fallKarte).join('') || '<div class="leer">Kein passender Fall.</div>'; }
  if (e.target.id === 'quellen-suche') { const q = e.target.value.toLocaleLowerCase('de'); $('#quellen-liste').innerHTML = S._quellenKarten(S.quellen.quellen.filter(x => JSON.stringify(x).toLocaleLowerCase('de').includes(q))); }
});
document.addEventListener('change', async e => {
  try {
    if (['f-gruppe', 'f-typ', 'f-stand'].includes(e.target.id)) { S.filter[e.target.id.slice(2)] = e.target.value; await render(); }
    if (e.target.id === 'fall-filter') e.target.dispatchEvent(new Event('input', {bubbles: true}));
    if (e.target.dataset.fallstatus) { await api.werkzeug('fall_status_setzen', {fall: e.target.dataset.fallstatus, status: e.target.value}); S.zentrale = null; toast('Fallstatus gespeichert.'); await render(); }
    if (e.target.dataset.aufgabe) { const id = e.target.dataset.aufgabe, w = e.target.checked; await akteSpeichern(a => { a.aufgaben.find(x => x.id === id).erledigt = w; }, w ? 'Erledigt.' : 'Wieder offen.'); }
  } catch (err) { toast(err.message, true); await render(); }
});
document.addEventListener('submit', async e => {
  if (e.target.id === 'einstellungen') {
    e.preventDefault(); const f = new FormData(e.target);
    const daten = {sicherung: {ziel: f.get('ziel').trim(), zweites_ziel: f.get('zweites_ziel').trim()}, einstellungen: {feiertagsland: f.get('feiertagsland') || ''}};
    try { await api.post('/api/einstellungen', daten); S.zentrale = null; toast('Einstellungen gespeichert.'); await render(); } catch (err) { toast(err.message, true); }
  }
});
$('#formular').onsubmit = async e => { e.preventDefault(); if (!dialogSpeichern) return; const k = $('#dialog-speichern'); k.disabled = true; $('#dialog-fehler').hidden = true;
  try { await dialogSpeichern(new FormData(e.target)); dialogVeraendert = false; if ($('#dialog').open) $('#dialog').close(); } catch (err) { $('#dialog-fehler').textContent = err.message; $('#dialog-fehler').hidden = false; } finally { k.disabled = false; } };
$('#dialog-schliessen').onclick = dialogZu; $('#dialog-abbrechen').onclick = dialogZu; $('#dialog').addEventListener('cancel', e => { e.preventDefault(); dialogZu(); });
window.addEventListener('hashchange', render);
window.addEventListener('beforeunload', e => { if (dialogVeraendert) { e.preventDefault(); e.returnValue = ''; } });
render();
