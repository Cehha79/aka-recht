'use strict';
/* AKA Recht, Oberfläche. Reines JavaScript ohne Bibliotheken.
   Aufbau: Hilfen, Verbindung zum Dienst, Zustand und Routen, Seitenleiste,
   Seiten der Zentrale, Seiten der Fallakte, Vorschau, Dialoge, Ereignisse. */

// ---------------------------------------------------------------- Hilfen
const $ = (s, r = document) => r.querySelector(s);
// Sprache der Oberfläche (Stufe 11): alle Beschriftungen kommen aus sprachen/<kürzel>.json, der Dienst liefert die eingestellte
// Sprache unter /sprachen/aktuell.json. t() holt einen Text und füllt Platzhalter {name}; fehlt eine Kennung, erscheint sie selbst,
// damit ein Fehler auffällt statt zu verschwinden. wert() zeigt feste Werte aus akte.json (Stand, Art, Status …) übersetzt an,
// wenn die Sprachdatei eine Kennung wert.<Wert> hat; in der Akte bleiben die Werte deutsch (Datenformat).
let TEXTE = {}, RUECKFALL = {}, SPRACHE = 'de';   // RUECKFALL: die deutschen Texte, wenn eine andere Sprache eine Kennung noch nicht hat
const t = (k, v) => { let s = TEXTE[k] ?? RUECKFALL[k]; if (s === undefined) { console.warn('Text fehlt in der Sprachdatei: ' + k); s = k; } return v ? s.replace(/\{(\w+)\}/g, (m, n) => n in v ? String(v[n]) : m) : s; };
const wert = w => (w && (TEXTE['wert.' + w] ?? RUECKFALL['wert.' + w])) || w;
// Name des Dateimanagers für Beschriftungen; der Browser läuft auf demselben Rechner wie der Dienst (nur 127.0.0.1).
const dm = () => /Mac/i.test(navigator.userAgent) ? 'Finder' : /Windows/i.test(navigator.userAgent) ? 'Explorer' : t('allg.dateimanager');
async function ladeTexte() {
  const r = await fetch('/sprachen/aktuell.json'); if (!r.ok) throw new Error('Sprachdatei nicht geladen (' + r.status + ').');
  TEXTE = await r.json(); SPRACHE = r.headers.get('X-AKA-Sprache') || 'de'; S.anleitung = null;
  RUECKFALL = SPRACHE === 'de' ? {} : await (await fetch('/sprachen/de.json')).json();
  document.documentElement.lang = SPRACHE; document.title = t('app.titel');
  document.querySelectorAll('[data-t]').forEach(el => { el.textContent = t(el.dataset.t, {dm: dm()}); });
}
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const datum = iso => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ''); return m ? `${m[3]}.${m[2]}.${m[1]}` : (iso || ''); };
const heute = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
const tageBis = iso => Math.round((new Date(iso + 'T12:00:00') - new Date(heute() + 'T12:00:00')) / 86400000);
const tageText = n => n < 0 ? t('allg.tage_vorbei', {n: -n}) : n === 0 ? t('allg.heute') : t('allg.in_tagen', {n});
const groesse = n => n >= 1048576 ? (n / 1048576).toLocaleString('de-DE', {maximumFractionDigits: 1}) + ' ' + t('allg.mb') : Math.max(1, Math.round(n / 1024)) + ' ' + t('allg.kb');
const badge = (text, ton = '') => text ? `<span class="badge ${ton}">${esc(wert(text))}</span>` : '';
const opt = (liste, wert_, leer) => (leer !== undefined ? `<option value="">${esc(leer)}</option>` : '') + liste.map(x => { const [v, n] = Array.isArray(x) ? x : [x, wert(x)]; return `<option value="${esc(v)}"${v === wert_ ? ' selected' : ''}>${esc(n)}</option>`; }).join('');
// Nächste Kennung über den Zähler der Akte: entfernte Kennungen kommen nie wieder (Prüfbericht F11). Gleiche Regel wie akte_schema.naechste_kennung.
const naechste = (akte, liste, buchstabe, breite = 2) => { const z = akte.zaehler = akte.zaehler || {}; const n = Math.max(z[buchstabe] || 0, ...akte[liste].map(x => parseInt(String(x.id).slice(1), 10) || 0)) + 1; z[buchstabe] = n; return buchstabe + String(n).padStart(breite, '0'); };
const statusTon = s => ({'bestätigt': 'gruen', 'offen': 'gelb', 'abgelaufen': 'rot', 'erledigt': '', 'Original': 'blau', 'Entwurf': 'gelb', 'Versandt': 'gruen', 'Zugegangen': 'blau', 'Historisch': '', 'Vermerk': '', 'offen ': ''}[s] || '');
let toastTimer;
function toast(text, fehler = false) { const t = $('#toast'); clearTimeout(toastTimer); t.textContent = text; t.className = fehler ? 'fehler' : ''; t.hidden = false; toastTimer = setTimeout(() => t.hidden = true, fehler ? 9000 : 5000); }

// ---------------------------------------------------------------- Verbindung zum Dienst
const api = {
  csrf: '',
  async get(url) { return antwort(await fetch(url)); },
  async post(url, daten) { return antwort(await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-AKA-CSRF': api.csrf}, body: JSON.stringify(daten)})); },
  async werkzeug(name, parameter, bestaetigt = true) { const r = await api.post('/api/werkzeug', {name, parameter, bestaetigt}); S.zentrale = null; return r; },   // F14: nach jedem Werkzeugaufruf die Zentrale neu einlesen
};
async function antwort(r) {
  let d; try { d = await r.json(); } catch { throw new Error(t('app.keine_verbindung')); }
  if (!r.ok) throw new Error(d.fehler || t('app.anfrage_fehlgeschlagen'));
  return d;
}

// ---------------------------------------------------------------- Zustand und Routen
const S = {zentrale: null, fall: null, route: {}, auswahl: '', tab: 'vorschau', breit: false, filter: {q: '', gruppe: '', typ: '', stand: ''}, treffer: null, quellen: null, anleitung: null};
// Seiten der Seitenleiste; die Namen stehen in der Sprachdatei unter nav.<Kennung>
const ZENTRALE_SEITEN = ['home', 'faelle', 'eingang', 'fristen', 'quellen', 'bestand', 'einstellungen', 'anleitung'];
const FALL_SEITEN = ['uebersicht', 'dokumente', 'beteiligte', 'verfahren', 'chronologie', 'fristen', 'aufgaben', 'entwuerfe', 'anlagen', 'journal'];
const GRUPPEN = ['01 Eingang', '02 Grundlagen', '03 Schriftverkehr', '04 Verfahren', '05 Beweise', '06 Entwürfe', '07 Recherche', '08 Archiv'];
const BEREICHE = ['Allgemein', 'Arbeit', 'Verkehr und Bußgeld', 'Steuern und Abgaben', 'Behörden und Bescheide', 'Sozialleistungen und Rente', 'Gesundheit und Pflege', 'Wohnen und Miete', 'Bauen und Nachbarn', 'Verträge und Verbraucher', 'Forderungen und Inkasso', 'Versicherungen', 'Familie und Unterhalt', 'Erbe und Vorsorge', 'Strafsachen und Anzeigen', 'Schule, Ausbildung und Studium', 'Aufenthalt und Staatsangehörigkeit', 'Geschäft, Datenschutz und Internet', 'Vereine und Ehrenamt'];
const DOK_STAND = ['Original', 'Entwurf', 'Versandt', 'Zugegangen', 'Historisch', 'Vermerk'];
const DOK_TEXTSTAND = ['direkt ausgelesen', 'OCR-erkannt', 'visuell geprüft', 'teilweise lesbar', 'nicht lesbar'];   // F34: was tatsächlich gelesen wurde
const DOK_ART = ['Schreiben', 'E-Mail', 'Foto', 'Vertrag', 'Bescheid', 'Urteil', 'Entwurf', 'Beleg', 'Übersicht', 'Gesetz', 'Sonstiges'];
const ROLLEN = ['Ich', 'Gegner', 'Gericht', 'Behörde', 'Anwalt', 'Zeuge', 'Stelle', 'Versicherung', 'Sonstige'];
const EREIGNIS_ART = ['Zugang', 'Versand', 'Termin', 'Gespräch', 'Vorfall', 'Entscheidung', 'Vermerk', 'Arbeitsstand'];
const FRIST_ART = ['gesetzlich', 'selbst gesetzt', 'von Gegenseite gesetzt', 'vorsorglich', 'Termin'];
const FRIST_STATUS = ['offen', 'bestätigt', 'abgelaufen', 'erledigt'];
const ZEITPUNKT = ['genau', 'ungefähr', 'zeitraum', 'unbekannt'];   // F13; Anzeigenamen in der Sprachdatei unter wert.zeitpunkt.<Wert>
// F13: Anzeige des Zeitpunkts eines Ereignisses; datum ist bei allem außer „genau“ nur das Sortierdatum
const zeitAnzeige = e => { const z = e.zeitpunkt || 'genau'; const zt = e.zeitpunkt_text ? `<br><small>${esc(e.zeitpunkt_text)}</small>` : '';
  if (z === 'ungefähr') return `${esc(t('allg.ca', {datum: datum(e.datum)}))}${zt}`;
  if (z === 'zeitraum') return `${esc(t('allg.bis', {von: datum(e.datum), bis: datum(e.datum_bis || e.datum)}))}${zt}`;
  if (z === 'unbekannt') return `<span class="u-rot">${esc(t('allg.unbekannt'))}</span><br><small>${esc(t('allg.einsortiert_bei', {datum: datum(e.datum)}))}</small>${zt}`;
  return esc(datum(e.datum)); };
const ereignisSicher = id => { const e = S.fall && akte().ereignisse.find(x => x.id === id); return e ? (e.zeitpunkt || 'genau') === 'genau' : null; };
// F12: drei Eigenschaften einer Frist, gleiche Regel wie akte_schema.frist_eigenschaften (gerechnet, belegt, geprüft, offene Marker)
const fristEigenschaften = f => {
  const d = f.datum || ''; const de = d ? d.slice(8, 10) + '.' + d.slice(5, 7) + '.' + d.slice(0, 4) : ''; const termin = f.art === 'Termin'; const r = f.berechnung || '';
  const marker = ['titel', 'ausloeser', 'rechtsgrundlage', 'berechnung'].flatMap(k => String(f[k] || '').match(/\[(PRÜFEN|QUELLE|BELEG)\b[^\]]*\]?/g) || []);
  return {gerechnet: termin ? null : !!(d && (r.includes(d) || (de && r.includes(de)))), belegt: /^D\d{4,}$/.test(f.quelle || '') && (termin || !!(f.ausloeser || '').trim()),
    geprueft: f.pruefstatus === 'bestätigt' && !!(f.geprueft_am || '').trim(), ausloeser_sicher: f.ausloeser_ereignis ? ereignisSicher(f.ausloeser_ereignis) : null, offene_marker: marker};
};
const eigenschaftenBadges = f => { const e = f.eigenschaften || fristEigenschaften(f); return [
  e.gerechnet === null ? '' : badge(t(e.gerechnet ? 'allg.gerechnet' : 'allg.nicht_gerechnet'), e.gerechnet ? 'gruen' : 'gelb'),
  badge(t(e.belegt ? 'allg.belegt' : 'allg.nicht_belegt'), e.belegt ? 'gruen' : 'gelb'),
  f.pruefstatus === 'bestätigt' ? badge(e.geprueft ? t('allg.geprueft_am', {datum: datum(f.geprueft_am)}) + (f.geprueft_von ? ' · ' + f.geprueft_von : '') : t('allg.ohne_pruefdatum'), e.geprueft ? 'gruen' : 'gelb') : '',
  e.ausloeser_sicher === false ? badge(t('allg.ausloeser_unsicher'), 'rot') : '',
  e.offene_marker.length ? badge(t('allg.offener_marker'), 'rot') : ''].filter(Boolean).join(' '); };
const ENTWURF_STATUS = ['in Arbeit', 'geprüft', 'versandt', 'verworfen'];
const JOURNAL_ARTEN = ['Eingang', 'Versand', 'Entscheidung', 'Gespräch', 'Termin', 'Arbeit', 'Vermerk'];

function routeLesen() { const p = new URLSearchParams(location.hash.slice(1)); return {seite: p.get('seite') || '', fall: p.get('fall') || '', dok: p.get('dok') || ''}; }
function gehe(teile) { const p = new URLSearchParams(); for (const [k, v] of Object.entries(teile)) if (v) p.set(k, v); location.hash = p.toString(); }
const fallLink = (id, seite = 'uebersicht', dok = '') => '#' + new URLSearchParams(Object.assign({seite, fall: id}, dok ? {dok} : {})).toString();

async function ladeZentrale() { S.zentrale = await api.get('/api/zentrale'); api.csrf = S.zentrale.csrf; }
async function ladeFall(id) {
  S.fall = await api.get('/api/fall/' + id);
  // Lesen schreibt nichts mehr (Prüfbericht F03). Neue oder verschobene Dateien registriert die
  // Oberfläche ausdrücklich über das schreibende Werkzeug und liest den Fall danach neu.
  const a = S.fall.abweichungen || {};
  if (api.csrf && ((a.nicht_erfasst || []).length || (a.verschoben || []).length || (S.fall.ergaenzt || []).length)) {
    try { await api.werkzeug('bestand_abgleichen', {fall: id}); S.fall = await api.get('/api/fall/' + id); }
    catch (e) { toast(t('meld.bestand_nicht_abgeglichen', {fehler: e.message}), true); }
  }
}
const akte = () => S.fall.akte;
const fallId = () => akte().fall.id;
const dokListe = () => S.fall.dokumente;
const dok = id => dokListe().find(d => d.id === id);
const dokOptionen = (wert_, leer = t('allg.kein_dokument')) => opt(dokListe().map(d => [d.id, `${d.id} · ${d.titel}`]), wert_, leer);
const personOptionen = (wert_, leer = t('allg.keine_angabe')) => opt(akte().beteiligte.map(b => [b.id, `${b.id} · ${b.name}`]), wert_, leer);
const personName = id => (akte().beteiligte.find(b => b.id === id) || {}).name || id;

async function render() {
  S.route = routeLesen();
  try {
    if (!S.zentrale) await ladeZentrale();
    if (S.route.fall && (!S.fall || fallId() !== S.route.fall)) { await ladeFall(S.route.fall); S.auswahl = ''; S.treffer = null; }
    if (!S.route.fall) S.fall = null;
  } catch (e) { $('#content').innerHTML = `<div class="leer"><h2>${esc(t('app.oeffnen'))}</h2><p>${esc(e.message)}</p></div>`; return; }
  if (S.route.dok) S.auswahl = S.route.dok;
  seitenleiste();
  const seite = S.route.seite || (S.fall ? 'uebersicht' : 'home');
  const seiten = S.fall ? FALL : ZENTRALE;
  const fn = seiten[seite] || (S.fall ? FALL.uebersicht : ZENTRALE.home);
  $('#brotkrumen').textContent = S.fall ? `${fallId()} · ${wert(akte().fall.bereich)}`.toUpperCase() : t('app.brotkrumen');
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
  $('#marke-unter').textContent = S.fall ? akte().fall.titel : t('app.untertitel');
  const zahlen = {};
  if (S.fall) {
    const a = akte(); Object.assign(zahlen, {dokumente: dokListe().length, beteiligte: a.beteiligte.length, verfahren: a.verfahren.length, chronologie: a.ereignisse.length,
      fristen: a.fristen.filter(f => f.pruefstatus !== 'erledigt').length, aufgaben: a.aufgaben.filter(x => !x.erledigt).length, entwuerfe: a.entwuerfe.length, journal: S.fall.journal.length});
  } else if (S.zentrale) { zahlen.faelle = S.zentrale.faelle.length; zahlen.eingang = S.zentrale.eingang.length; }
  const liste = S.fall ? FALL_SEITEN : ZENTRALE_SEITEN;
  $('#navigation').innerHTML = `<div class="abschnitt">${esc(t(S.fall ? 'nav.fallakte' : 'nav.ueberblick'))}</div>` + liste.map((id, i) =>
    `<a href="${S.fall ? fallLink(fallId(), id) : '#seite=' + id}" class="${aktiv === id ? 'aktiv' : ''}"${aktiv === id ? ' aria-current="page"' : ''}><span class="nr">${String(i + 1).padStart(2, '0')}</span>${esc(t('nav.' + id))}${zahlen[id] !== undefined ? `<span class="zahl">${zahlen[id]}</span>` : ''}</a>`).join('');
}

// ---------------------------------------------------------------- Seiten der Zentrale
function fallKarte(c) {
  if (c.fehler) return `<article class="karte"><span class="kennung">${esc(c.id)}</span><h2>${esc(c.titel)}</h2><p class="hinweis rot">${esc(c.fehler)}</p></article>`;
  return `<article class="karte"><div class="tafel-kopf"><span class="kennung">${esc(c.id)}</span>${badge(c.bereich)}</div><h2>${esc(c.titel)}</h2><p>${esc(c.rolle || t('karte.rolle_offen'))}</p>
    <p>${esc(t('karte.zahlen', {dokumente: c.dokumente, aufgaben: c.offene_aufgaben, fristen: c.fristen_offen}))}</p>
    <div class="karte-fuss"><a class="knopf primaer" href="${fallLink(c.id)}">${esc(t('karte.akte_oeffnen'))}</a><select data-fallstatus="${esc(c.id)}" aria-label="${esc(t('karte.status_fuer', {titel: c.titel}))}">${opt(['offen', 'ruhend', 'abgeschlossen'], c.status)}</select></div></article>`;
}
function fristenAllerFaelle() {
  return S.zentrale.faelle.flatMap(c => (c.fristen || []).map(f => ({...f, fallId: c.id, fallTitel: c.titel}))).sort((a, b) => a.datum.localeCompare(b.datum));
}
function fristZeile(f, mitFall = true) {
  const n = tageBis(f.datum); const ton = f.pruefstatus === 'erledigt' ? '' : n < 0 ? 'dringend' : n <= 7 ? 'dringend' : n <= 21 ? 'bald' : '';
  const link = mitFall ? fallLink(f.fallId, 'fristen') : fallLink(fallId(), 'fristen');
  return `<div class="zeile"><div class="datumsbox ${ton}"><b>${datum(f.datum).slice(0, 5)}</b>${datum(f.datum).slice(6)}</div><div class="zeile-text"><h3>${esc(f.titel)}</h3>
    <p>${mitFall ? esc(f.fallId + ' · ' + f.fallTitel) + ' · ' : ''}${esc(wert(f.art))} · ${esc(tageText(n))}</p>
    <div class="themen">${badge(t('allg.pruefstatus', {status: wert(f.pruefstatus)}), statusTon(f.pruefstatus))}${(() => { const e = f.eigenschaften || fristEigenschaften(f); return (f.pruefstatus === 'bestätigt' && !e.geprueft ? ' ' + badge(t('allg.ohne_pruefdatum'), 'gelb') : '') + (e.offene_marker.length ? ' ' + badge(t('allg.offener_marker'), 'rot') : ''); })()}</div></div><div class="aktionen"><a class="knopf klein" href="${link}">${esc(t('karte.zur_akte'))}</a></div></div>`;
}
const ZENTRALE = {
  async home() {
    const z = S.zentrale, gueltig = z.faelle.filter(c => !c.fehler), offen = gueltig.filter(c => c.status !== 'abgeschlossen');
    const fristen = fristenAllerFaelle().filter(f => f.pruefstatus !== 'erledigt' && f.datum >= heute()).slice(0, 6);
    const inhalt = `<div class="kacheln"><div class="kachel"><strong>${offen.length}</strong><span>${esc(t('home.offene_faelle'))}</span></div><div class="kachel"><strong>${gueltig.reduce((n, c) => n + c.dokumente, 0)}</strong><span>${esc(t('home.dokumente'))}</span></div>
      <div class="kachel"><strong>${gueltig.reduce((n, c) => n + c.offene_aufgaben, 0)}</strong><span>${esc(t('home.aufgaben'))}</span></div><div class="kachel"><strong>${z.eingang.length}</strong><span>${esc(t('home.eingang'))}</span></div></div>
      <div class="tafel-kopf"><h2>${esc(t('home.deine_faelle'))}</h2><span><button class="knopf still" data-aktion="beispiel-laden" title="${esc(t('home.beispiel_hinweis'))}">${esc(t('home.beispiel_laden'))}</button> <a href="#seite=faelle">${esc(t('home.alle_faelle'))}</a></span></div><div class="raster">${offen.length ? offen.slice(0, 4).map(fallKarte).join('') : `<div class="leer"><h2>${esc(t('home.kein_fall'))}</h2><p>${esc(t('home.kein_fall_text'))}</p><p class="u-mt14"><button class="knopf primaer" data-aktion="neuer-fall">${esc(t('home.neuer_fall'))}</button></p></div>`}</div>
      <div class="raster u-mt18"><section class="tafel"><h2>${esc(t('home.naechste_fristen'))}</h2><p class="untertitel u-mb8">${esc(t('home.naechste_fristen_text'))}</p>${fristen.length ? fristen.map(f => fristZeile(f)).join('') : `<p class="untertitel">${esc(t('home.keine_fristen'))}</p>`}</section>
      <section class="tafel"><h2>${esc(t('home.so_weiter'))}</h2><p class="untertitel u-mb8">${esc(t('home.so_weiter_text'))}</p><div class="karte-fuss"><a class="knopf" href="#seite=eingang">${esc(t('home.posteingang'))}</a><a class="knopf" href="#seite=quellen">${esc(t('home.rechtsquellen'))}</a><a class="knopf" href="#seite=bestand">${esc(t('home.sicherung'))}</a></div>
      ${z.sicherung.vorhanden ? `<div class="hinweis">${esc(t('home.letzte_sicherung', {datum: datum(z.sicherung.zeit), zusatz: z.sicherung.unveraendert ? '' : t('home.sicherung_veraendert')}))}</div>` : `<div class="hinweis gelb">${esc(t('home.keine_sicherung'))}</div>`}</section></div>`;
    return [t('home.titel'), '', inhalt, `<button class="knopf still" data-aktion="neu-laden">${esc(t('allg.neu_einlesen'))}</button><button class="knopf primaer" data-aktion="neuer-fall">${esc(t('home.neuer_fall'))}</button>`];
  },
  async faelle() {
    const inhalt = `<div class="filter"><input id="fall-suche" type="search" placeholder="${esc(t('faelle.suchen'))}" aria-label="${esc(t('faelle.suchen_label'))}"><select id="fall-filter" aria-label="${esc(t('faelle.filter_label'))}">${opt([['Alle', t('allg.alle')], 'offen', 'ruhend', 'abgeschlossen'], 'Alle')}</select></div>
      <div class="raster" id="fall-liste">${S.zentrale.faelle.map(fallKarte).join('') || `<div class="leer"><h2>${esc(t('faelle.kein_fall'))}</h2></div>`}</div>
      <section class="tafel u-mt18"><h2>${esc(t('faelle.vertraege'))}</h2><p class="untertitel u-mb8">${esc(t('faelle.vertraege_text'))}</p><button class="knopf klein" data-aktion="finder" data-ort="vertraege">${esc(t('faelle.ablage', {dm: dm()}))}</button></section>`;
    return [t('faelle.titel'), t('faelle.untertitel'), inhalt, `<button class="knopf primaer" data-aktion="neuer-fall">${esc(t('home.neuer_fall'))}</button>`];
  },
  async eingang() {
    const e = S.zentrale.eingang;
    const inhalt = `<section class="tafel">${e.length ? e.map(f => `<div class="zeile"><div class="zeile-text"><h3>${esc(f.name)}</h3><p>${groesse(f.groesse)}</p></div><div class="aktionen"><button class="knopf klein" data-aktion="zuordnen" data-name="${esc(f.name)}">${esc(t('eingang.zuordnen'))}</button></div></div>`).join('') : `<div class="leer"><h2>${esc(t('eingang.frei'))}</h2><p>${esc(t('eingang.frei_text'))}</p></div>`}</section>`;
    return [t('eingang.titel'), t('eingang.untertitel'), inhalt, `<button class="knopf" data-aktion="finder" data-ort="eingang">${esc(t('eingang.im_dm', {dm: dm()}))}</button><button class="knopf primaer" data-aktion="hochladen" data-ziel="eingang">${esc(t('eingang.hinzufuegen'))}</button>`];
  },
  async fristen() {
    const alle = fristenAllerFaelle();
    const inhalt = alle.length ? `<section class="tafel">${alle.map(f => fristZeile(f)).join('')}</section>` : `<div class="leer"><h2>${esc(t('fristen.keine'))}</h2><p>${esc(t('fristen.keine_text'))}</p></div>`;
    return [t('fristen.titel'), t('fristen.untertitel'), inhalt, ''];
  },
  async quellen() {
    if (!S.quellen) S.quellen = await api.get('/api/quellen');
    const karten = l => l.map(q => `<article class="karte">${badge(q.category || q.kategorie)}<h2><a href="${/^https:\/\//.test(q.url) ? esc(q.url) : '#'}" target="_blank" rel="noopener noreferrer">${esc(q.title || q.titel)} ↗</a></h2><p>${esc(q.use || q.verwendung)}</p><div class="hinweis">${esc(q.limit || q.grenze || '')}</div><span class="pfad">${esc(q.url)}</span><div class="karte-fuss"><button class="knopf klein" data-aktion="kopieren" data-text="${esc(q.url)}">${esc(t('quellen.kopieren'))}</button><small class="u-muted-klein">${esc(t('quellen.geprueft', {datum: datum(q.catalog_checked || q.geprueft)}))}</small></div></article>`).join('') || `<div class="leer">${esc(t('quellen.kein_treffer'))}</div>`;
    const inhalt = `<div class="filter"><input id="quellen-suche" type="search" placeholder="${esc(t('quellen.suchen'))}" aria-label="${esc(t('quellen.suchen_label'))}"></div><div class="raster" id="quellen-liste">${karten(S.quellen.quellen)}</div>`;
    S._quellenKarten = karten;
    return [t('quellen.titel'), t('quellen.untertitel'), inhalt, `<button class="knopf" data-aktion="finder" data-ort="quellen">${esc(t('quellen.katalog_dm', {dm: dm()}))}</button>`];
  },
  async bestand() {
    const s = S.zentrale.sicherung;
    const inhalt = `<section class="tafel"><div class="tafel-kopf"><h2>${esc(t('bestand.pruefen'))}</h2>${badge(t('bestand.manuell'))}</div><p class="untertitel u-mb10">${esc(t('bestand.pruefen_text'))}</p><button class="knopf primaer" data-aktion="bestand-pruefen">${esc(t('bestand.pruefung_starten'))}</button><div id="bestand-ergebnis"></div></section>
      <section class="tafel"><h2>${esc(t('bestand.sicherung'))}</h2><p class="untertitel">${esc(t('bestand.ziel', {ziel: s.ziel || '–'}))}${s.ziel_hinweis ? ' (' + esc(s.ziel_hinweis) + ')' : ''}<br>${esc(t('bestand.zweites_ziel', {ziel: s.zweites_ziel_eingestellt || t('bestand.keins')}))}${s.zweites_ziel_hinweis_cloud ? ' (' + esc(s.zweites_ziel_hinweis_cloud) + ')' : ''}<br>${esc(t('bestand.ebenen'))}</p>
      ${s.vorhanden ? `<p class="pfad">${esc(s.pfad)}</p><p class="untertitel">${esc(t('bestand.erstellt', {datum: datum(s.zeit), dateien: s.dateien, groesse: groesse(s.groesse)}))} · ${badge(t(s.unveraendert ? 'bestand.unveraendert' : 'bestand.veraendert'), s.unveraendert ? 'gruen' : 'rot')}${s.zweites_ziel ? `<br>${esc(t('bestand.kopie', {pfad: s.zweites_ziel}))} ${badge(t(s.zweites_ziel_unveraendert ? 'bestand.kopie_unveraendert' : 'bestand.kopie_veraendert'), s.zweites_ziel_unveraendert ? 'gruen' : 'rot')}` : ''}${s.zweites_ziel_hinweis ? `<br>${esc(s.zweites_ziel_hinweis)}` : ''}</p>` : `<div class="hinweis gelb">${esc(t('bestand.keine_sicherung'))}</div>`}
      <div class="karte-fuss"><button class="knopf primaer" data-aktion="sicherung">${esc(t('bestand.sicherung_erstellen'))}</button>${s.vorhanden ? `<button class="knopf" data-aktion="sicherung-probe">${esc(t('bestand.probe'))}</button>` : ''}</div><p class="untertitel">${esc(t('bestand.sicherung_text'))}</p><div id="probe-ergebnis"></div></section>`;
    return [t('bestand.titel'), '', inhalt, ''];
  },
  async einstellungen() {
    const e = await api.get('/api/einstellungen'); const ab = e.einstellungen.absender || {};
    const inhalt = `<form id="einstellungen" class="tafel"><h2>${esc(t('einst.sicherung'))}</h2>
      ${feld('ziel', t('einst.ziel'), e.sicherung.ziel, 'text', {hinweis: t('einst.ziel_hinweis')})}
      ${feld('zweites_ziel', t('einst.zweites_ziel'), e.sicherung.zweites_ziel || '', 'text', {hinweis: t('einst.zweites_ziel_hinweis')})}
      <h2>${esc(t('einst.absender'))}</h2>
      <p class="untertitel">${esc(t('einst.absender_text'))}</p>
      <div class="feld-reihe">${feld('ab_name', t('einst.name'), ab.name || '')}${feld('ab_strasse', t('einst.strasse'), ab.strasse || '')}</div>
      <div class="feld-reihe drei">${feld('ab_plz_ort', t('einst.plz_ort'), ab.plz_ort || '')}${feld('ab_telefon', t('einst.telefon'), ab.telefon || '')}${feld('ab_email', t('einst.email'), ab.email || '')}</div>
      <h2>${esc(t('einst.fristen'))}</h2>
      ${feld('feiertagsland', t('einst.bundesland'), e.einstellungen.feiertagsland, 'select', {optionen: opt(Object.entries(e.laender || {}), e.einstellungen.feiertagsland), hinweis: t('einst.bundesland_hinweis')})}
      <h2>${esc(t('einst.sprache'))}</h2>
      ${feld('sprache', t('einst.sprache'), e.sprache, 'select', {optionen: opt((e.sprachen || ['de']).map(k => [k, TEXTE['sprache.' + k] || k]), e.sprache), hinweis: t('einst.sprache_hinweis')})}
      <button class="knopf primaer" type="submit">${esc(t('einst.speichern'))}</button></form>`;
    return [t('einst.titel'), '', inhalt, ''];
  },
  async anleitung() {
    // Die Anleitung ist ein HTML-Fragment je Sprache (sprachen/anleitung.<kürzel>.html); {dm} wird durch den Dateimanager ersetzt
    if (!S.anleitung) { const r = await fetch('/sprachen/anleitung.aktuell.html'); S.anleitung = r.ok ? await r.text() : `<p>${esc(t('anleitung.fehlt'))}</p>`; }
    return [t('anleitung.titel'), '', `<article class="tafel anleitung">${S.anleitung.replace(/\{dm\}/g, esc(dm()))}</article>`, `<button class="knopf" data-aktion="finder" data-ort="doku">${esc(t('anleitung.doku_dm', {dm: dm()}))}</button>`];
  },
};

// ---------------------------------------------------------------- Seiten der Fallakte
function dokZeile(d) {
  return `<div class="dok-zeile ${S.auswahl === d.id ? 'gewaehlt' : ''}" data-dok="${esc(d.id)}" tabindex="0" role="button"><div class="dok-zelle"><div class="dateisymbol ${esc(d.typ)}">${esc(d.typ || '?')}</div><div class="u-minw0"><div class="dok-titel">${esc(d.titel)}</div><div class="dok-unter">${esc(d.id)}${d.anlage ? ' · ' + esc(d.anlage) : ''} · ${esc(d.pfad)}${d.fehlt ? ` · <b class="u-rot">${esc(t('fall.datei_fehlt'))}</b>` : ''}</div>${d.themen.length ? `<div class="themen">${d.themen.map(th => `<span class="thema">${esc(th)}</span>`).join('')}</div>` : ''}</div></div>
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
  return `<div class="zeitstrahl">${eintraege.map(e => `<div class="zs-zeile"><div class="zs-datum">${zeitAnzeige(e)}</div><div class="zs-karte"><div class="zs-inhalt"><div class="tafel-kopf"><span>${badge(e.art)}${e.pruefstatus ? ' ' + badge(t('allg.pruefstatus', {status: wert(e.pruefstatus)}), statusTon(e.pruefstatus)) : ''}</span><button class="knopf klein" data-aktion="bearbeiten" data-art="${art}" data-id="${esc(e.id)}">${esc(t('allg.bearbeiten'))}</button></div><h3>${esc(e.titel)}</h3><p>${esc(e.detail || e.berechnung || '')}</p>${e.quelle ? `<p class="u-mt6"><a href="${fallLink(fallId(), 'dokumente', e.quelle)}">${esc(t('dok.quelle', {id: e.quelle}))}${dok(e.quelle) ? ' · ' + esc(dok(e.quelle).titel) : ''}</a></p>` : ''}</div></div></div>`).join('')}</div>`;
}
const FALL = {
  async uebersicht() {
    const a = akte(), f = a.fall;
    const fristen = a.fristen.filter(x => x.pruefstatus !== 'erledigt').sort((x, y) => x.datum.localeCompare(y.datum)).slice(0, 5).map(x => ({...x, fallId: f.id, fallTitel: f.titel}));
    const aufgaben = a.aufgaben.filter(x => !x.erledigt).slice(0, 5);
    const gruppen = GRUPPEN.map((g, i) => `<button class="bereich-link" data-aktion="gruppe" data-gruppe="${esc(g)}"><b>${g.slice(0, 2)}</b>${esc(g.slice(3))}<span>${dokListe().filter(d => d.gruppe === g).length}</span></button>`).join('');
    const j = S.fall.journal.slice(-1)[0];
    const bearb = (art, id) => `<button class="knopf klein" data-aktion="bearbeiten" data-art="${art}" data-id="${esc(id)}">${esc(t('allg.bearbeiten'))}</button>`;
    const inhalt = `<section class="tafel"><div class="tafel-kopf"><div><span class="kennung">${esc(f.id)}</span> ${badge(f.bereich)} ${badge(f.status, f.status === 'offen' ? 'gruen' : '')}</div><button class="knopf klein" data-aktion="fall-bearbeiten">${esc(t('fall.bearbeiten'))}</button></div>
      <div class="raster drei u-mt8"><div class="feld-anzeige"><b>${esc(t('fall.rolle'))}</b><span>${esc(f.rolle || t('fall.noch_offen'))}</span></div><div class="feld-anzeige"><b>${esc(t('fall.ziel'))}</b><span>${esc(f.ziel || t('fall.noch_offen'))}</span></div><div class="feld-anzeige"><b>${esc(t('fall.verfahren'))}</b><span>${a.verfahren.map(v => `${esc(v.art)}${v.aktenzeichen ? ' · ' + esc(v.aktenzeichen) : ''}`).join('<br>') || esc(t('fall.noch_keins'))}</span></div></div>
      ${f.untertitel ? `<p class="untertitel u-m0">${esc(f.untertitel)}</p>` : ''}</section>
      <div class="kacheln u-mt18"><div class="kachel"><strong>${dokListe().length}</strong><span>${esc(t('fall.k_dokumente'))}</span></div><div class="kachel"><strong>${a.aufgaben.filter(x => !x.erledigt).length}</strong><span>${esc(t('fall.k_aufgaben'))}</span></div><div class="kachel"><strong>${a.fristen.filter(x => x.pruefstatus !== 'erledigt').length}</strong><span>${esc(t('fall.k_fristen'))}</span></div><div class="kachel"><strong>${a.ereignisse.length}</strong><span>${esc(t('fall.k_ereignisse'))}</span></div></div>
      <div class="raster"><section class="tafel"><div class="tafel-kopf"><h2>${esc(t('fall.naechste_fristen'))}</h2><a href="${fallLink(f.id, 'fristen')}">${esc(t('fall.alle'))}</a></div>${fristen.length ? fristen.map(x => fristZeile(x, false)).join('') : `<p class="untertitel u-m0">${esc(t('fall.keine_fristen'))}</p>`}</section>
      <section class="tafel"><div class="tafel-kopf"><h2>${esc(t('fall.offene_aufgaben'))}</h2><a href="${fallLink(f.id, 'aufgaben')}">${esc(t('fall.alle'))}</a></div>${aufgaben.length ? aufgaben.map(x => `<div class="zeile"><div class="zeile-text"><h3>${esc(x.titel)}</h3><p>${x.faellig ? esc(t('fall.faellig', {datum: datum(x.faellig)})) + ' · ' : ''}${esc(x.detail)}</p></div></div>`).join('') : `<p class="untertitel u-m0">${esc(t('fall.keine_aufgaben'))}</p>`}</section></div>
      <div class="raster u-mt18"><section class="tafel"><h2>${esc(t('fall.bereiche'))}</h2><div class="bereiche">${gruppen}</div></section>
      <section class="tafel"><div class="tafel-kopf"><h2>${esc(t('fall.angeheftet'))}</h2></div>${f.angeheftet.length ? f.angeheftet.map(id => dok(id) ? `<div class="zeile"><div class="zeile-text"><h3><a href="${fallLink(f.id, 'dokumente', id)}">${esc(dok(id).titel)}</a></h3><p>${esc(id)} · ${esc(dok(id).pfad)}</p></div></div>` : '').join('') : `<p class="untertitel u-m0">${esc(t('fall.angeheftet_leer'))}</p>`}
      <div class="tafel-kopf u-mt16"><h2>${esc(t('fall.zuletzt_journal'))}</h2><a href="${fallLink(f.id, 'journal')}">${esc(t('fall.journal'))}</a></div>${j ? `<div class="zeile"><div class="datumsbox"><b>${datum(j.datum).slice(0, 5)}</b>${datum(j.datum).slice(6)}</div><div class="zeile-text"><h3>${esc(j.titel)}</h3><p>${esc(j.text)}</p></div></div>` : `<p class="untertitel u-m0">${esc(t('fall.kein_eintrag'))}</p>`}</section></div>
      <section class="tafel u-mt18"><div class="tafel-kopf"><h2>${esc(t('fall.notizen'))}</h2><button class="knopf klein" data-aktion="neu" data-art="notiz">${esc(t('fall.notiz'))}</button></div>${a.notizen.length ? a.notizen.map(n => `<div class="zeile"><div class="zeile-text"><h3>${esc(n.titel)}</h3><p>${esc(n.text)}</p><p>${esc(datum(n.datum))}</p></div><div class="aktionen">${bearb('notiz', n.id)}</div></div>`).join('') : `<p class="untertitel u-m0">${esc(t('fall.keine_notizen'))}</p>`}</section>`;
    return [f.titel, '', inhalt, `<button class="knopf still" data-aktion="neu-laden">${esc(t('allg.neu_einlesen'))}</button><button class="knopf" data-aktion="finder" data-fall="${esc(f.id)}">${esc(t('fall.ordner_dm', {dm: dm()}))}</button><button class="knopf primaer" data-aktion="hochladen" data-ziel="fall">${esc(t('fall.dok_hinzufuegen'))}</button>`];
  },
  async dokumente() {
    const l = gefilterteDoks(); const typen = [...new Set(dokListe().map(d => d.typ).filter(Boolean))].sort();
    const inhalt = `<div class="filter"><input id="dok-suche" type="search" value="${esc(S.filter.q)}" placeholder="${esc(t('dok.suchen'))}" aria-label="${esc(t('dok.suchen_label'))}"><select id="f-gruppe" aria-label="${esc(t('dok.bereich'))}">${opt(GRUPPEN, S.filter.gruppe, t('dok.alle_bereiche'))}</select><select id="f-typ" aria-label="${esc(t('dok.dateityp'))}">${opt(typen, S.filter.typ, t('dok.alle_typen'))}</select><select id="f-stand" aria-label="${esc(t('dok.stand'))}">${opt(DOK_STAND, S.filter.stand, t('dok.jeder_stand'))}</select><span class="zaehler">${esc(t('dok.von', {n: l.length, gesamt: dokListe().length}))}</span></div>
      <div class="dok-tabelle"><div class="dok-kopf"><span>${esc(t('dok.sp_dokument'))}</span><span>${esc(t('dok.sp_datum'))}</span><span>${esc(t('dok.sp_stand'))}</span></div>${l.map(dokZeile).join('') || `<div class="leer"><h2>${esc(t('dok.nichts'))}</h2><p>${esc(t('dok.nichts_text', {dm: dm()}))}</p></div>`}</div>`;
    return [t('dok.titel'), '', inhalt, `<button class="knopf still" data-aktion="neu-laden">${esc(t('allg.neu_einlesen'))}</button><button class="knopf" data-aktion="finder" data-fall="${esc(fallId())}" data-gruppe="01 Eingang">${esc(t('dok.eingang_dm', {dm: dm()}))}</button><button class="knopf primaer" data-aktion="hochladen" data-ziel="fall">${esc(t('fall.dok_hinzufuegen'))}</button>`];
  },
  async beteiligte() {
    const l = akte().beteiligte; const bearb = t('allg.bearbeiten');
    const inhalt = l.length ? `<table class="tabelle"><thead><tr><th>${esc(t('bet.kennung'))}</th><th>${esc(t('bet.name'))}</th><th>${esc(t('bet.rolle'))}</th><th>${esc(t('bet.aktenzeichen'))}</th><th>${esc(t('bet.kontakt'))}</th><th></th></tr></thead><tbody>${l.map(b => `<tr><td>${esc(b.id)}</td><td><b>${esc(b.name)}</b>${b.anschrift ? '<br><small>' + esc(b.anschrift) + '</small>' : ''}</td><td>${badge(b.rolle)}</td><td>${esc(b.aktenzeichen)}</td><td>${esc(b.kontakt)}</td><td><button class="knopf klein" data-aktion="bearbeiten" data-art="beteiligter" data-id="${esc(b.id)}">${esc(bearb)}</button></td></tr>`).join('')}</tbody></table>` : `<div class="leer"><h2>${esc(t('bet.keine'))}</h2><p>${esc(t('bet.keine_text'))}</p></div>`;
    return [t('bet.titel'), t('bet.untertitel'), inhalt, `<button class="knopf primaer" data-aktion="neu" data-art="beteiligter">${esc(t('bet.neu'))}</button>`];
  },
  async verfahren() {
    const l = akte().verfahren;
    const inhalt = l.length ? `<div class="raster">${l.map(v => `<article class="karte"><span class="kennung">${esc(v.id)}</span><h2>${esc(v.art)}</h2><p><b>${esc(t('verf.stelle'))}:</b> ${esc(personName(v.stelle) || t('verf.offen'))}<br><b>${esc(t('verf.aktenzeichen'))}:</b> ${esc(v.aktenzeichen || t('fall.noch_keins'))}<br><b>${esc(t('verf.stand'))}:</b> ${esc(v.stand || t('verf.offen'))}<br><b>${esc(t('verf.ordner'))}:</b> ${esc(v.ordner || '')}</p><div class="karte-fuss"><button class="knopf klein" data-aktion="bearbeiten" data-art="verfahren" data-id="${esc(v.id)}">${esc(t('allg.bearbeiten'))}</button></div></article>`).join('')}</div>` : `<div class="leer"><h2>${esc(t('verf.keins'))}</h2><p>${esc(t('verf.keins_text'))}</p></div>`;
    return [t('verf.titel'), t('verf.untertitel'), inhalt, `<button class="knopf primaer" data-aktion="neu" data-art="verfahren">${esc(t('verf.neu'))}</button>`];
  },
  async chronologie() {
    const l = [...akte().ereignisse].sort((a, b) => a.datum.localeCompare(b.datum));
    return [t('chron.titel'), t('chron.untertitel'), l.length ? zeitstrahl(l, 'ereignis') : `<div class="leer"><h2>${esc(t('chron.keins'))}</h2></div>`, `<button class="knopf primaer" data-aktion="neu" data-art="ereignis">${esc(t('chron.neu'))}</button>`];
  },
  async fristen() {
    const l = [...akte().fristen].sort((a, b) => a.datum.localeCompare(b.datum));
    const inhalt = l.length ? `<table class="tabelle"><thead><tr><th>${esc(t('fristen_fall.sp_datum'))}</th><th>${esc(t('fristen_fall.sp_titel'))}</th><th>${esc(t('fristen_fall.sp_art'))}</th><th>${esc(t('fristen_fall.sp_status'))}</th><th>${esc(t('fristen_fall.sp_grundlage'))}</th><th></th></tr></thead><tbody>${l.map(f => { const n = tageBis(f.datum); return `<tr><td class="u-nowrap"><b>${esc(datum(f.datum))}</b><br><small>${esc(f.pruefstatus === 'erledigt' ? t('allg.erledigt') : n < 0 ? t('allg.vorbei') : tageText(n))}</small></td><td><b>${esc(f.titel)}</b><br><small>${esc(f.ausloeser)}${f.verfahren ? ' · ' + esc(f.verfahren) : ''}${f.ausloeser_ereignis ? ' · ' + esc(t('fristen_fall.ausloeser', {id: f.ausloeser_ereignis})) : ''}</small></td><td>${badge(f.art)}</td><td>${badge(f.pruefstatus, statusTon(f.pruefstatus))}<br><small>${eigenschaftenBadges(f)}</small></td><td><small>${esc(f.rechtsgrundlage)}</small>${f.quelle ? `<br><a href="${fallLink(fallId(), 'dokumente', f.quelle)}">${esc(f.quelle)}</a>` : ''}</td><td><button class="knopf klein" data-aktion="bearbeiten" data-art="frist" data-id="${esc(f.id)}">${esc(t('allg.bearbeiten'))}</button></td></tr>`; }).join('')}</tbody></table>` : `<div class="leer"><h2>${esc(t('fristen_fall.keine'))}</h2><p>${esc(t('fristen_fall.keine_text'))}</p></div>`;
    return [t('fristen_fall.titel'), t('fristen_fall.untertitel'), inhalt, `<button class="knopf" data-aktion="rechner">${esc(t('fristen_fall.rechner'))}</button><button class="knopf primaer" data-aktion="neu" data-art="frist">${esc(t('fristen_fall.neu'))}</button>`];
  },
  async aufgaben() {
    const l = akte().aufgaben;
    const inhalt = l.length ? `<section class="tafel">${l.map(x => `<div class="aufgabe ${x.erledigt ? 'erledigt' : ''}"><input type="checkbox" data-aufgabe="${esc(x.id)}" ${x.erledigt ? 'checked' : ''} aria-label="${esc(t('aufg.erledigt_label', {titel: x.titel}))}"><div class="zeile-text"><h3>${esc(x.titel)}</h3><p>${esc(x.detail)}</p><p>${x.faellig ? esc(t('fall.faellig', {datum: datum(x.faellig)})) : ''}${x.quelle ? ` · <a href="${fallLink(fallId(), 'dokumente', x.quelle)}">${esc(x.quelle)}</a>` : ''}</p></div><div class="aktionen"><button class="knopf klein" data-aktion="bearbeiten" data-art="aufgabe" data-id="${esc(x.id)}">${esc(t('allg.bearbeiten'))}</button></div></div>`).join('')}</section>` : `<div class="leer"><h2>${esc(t('aufg.keine'))}</h2></div>`;
    return [t('aufg.titel'), '', inhalt, `<button class="knopf primaer" data-aktion="neu" data-art="aufgabe">${esc(t('aufg.neu'))}</button>`];
  },
  async entwuerfe() {
    const l = akte().entwuerfe; const dateien = dokListe().filter(d => d.gruppe === '06 Entwürfe');
    const eingefroren = w => (w.fassungen || []).filter(x => x.kopie_dokument).map(x => `${esc(t('entw.fassung_status', {n: x.fassung, status: wert(x.status), datum: datum(x.zeit)}))} <a href="${fallLink(fallId(), 'dokumente', x.kopie_dokument)}">${esc(x.kopie_dokument)}</a>`).join(' · ');
    const inhalt = `<section class="tafel"><h2>${esc(t('entw.mit_fassung'))}</h2>${l.length ? l.map(w => `<div class="zeile"><div class="zeile-text"><h3>${esc(w.titel)}</h3><p>${esc(t('entw.fassung', {n: w.fassung}))} · ${esc(w.datei)}${w.versandt_als ? ` · ${esc(t('entw.versandt_als'))} <a href="${fallLink(fallId(), 'dokumente', w.versandt_als)}">${esc(w.versandt_als)}</a>` : ''}</p>${eingefroren(w) ? `<p>${t('entw.eingefroren', {liste: eingefroren(w)})}</p>` : ''}</div>${badge(w.status, w.status === 'versandt' ? 'gruen' : w.status === 'geprüft' ? 'blau' : 'gelb')}<div class="aktionen"><button class="knopf klein" data-aktion="bearbeiten" data-art="entwurf" data-id="${esc(w.id)}">${esc(t('allg.bearbeiten'))}</button></div></div>`).join('') : `<p class="untertitel u-m0">${esc(t('entw.keiner'))}</p>`}</section>
      <section class="tafel"><h2>${esc(t('entw.dateien'))}</h2>${dateien.length ? dateien.map(d => `<div class="zeile"><div class="zeile-text"><h3><a href="${fallLink(fallId(), 'dokumente', d.id)}">${esc(d.titel)}</a></h3><p>${esc(d.id)} · ${esc(d.pfad)}</p></div>${badge(d.stand, statusTon(d.stand))}</div>`).join('') : `<p class="untertitel u-m0">${esc(t('entw.keine_dateien'))}</p>`}</section>`;
    return [t('entw.titel'), t('entw.untertitel'), inhalt, `<button class="knopf" data-aktion="vorlage">${esc(t('entw.aus_vorlage'))}</button><button class="knopf primaer" data-aktion="neu" data-art="entwurf">${esc(t('entw.erfassen'))}</button>`];
  },
  async anlagen() {
    const nat = s => String(s).replace(/\d+/g, m => m.padStart(5, '0'));
    const anl = dokListe().filter(d => d.anlage).sort((a, b) => nat(a.anlage).localeCompare(nat(b.anlage)));
    const bew = dokListe().filter(d => d.gruppe === '05 Beweise');
    const inhalt = `<section class="tafel"><h2>${esc(t('anl.verzeichnis'))}</h2><p class="untertitel u-mb10">${esc(t('anl.verzeichnis_text'))}</p>${anl.length ? `<table class="tabelle"><thead><tr><th>${esc(t('anl.sp_anlage'))}</th><th>${esc(t('anl.sp_dokument'))}</th><th>${esc(t('anl.sp_datum'))}</th><th>${esc(t('anl.sp_stand'))}</th></tr></thead><tbody>${anl.map(d => `<tr class="klick" data-dok-link="${esc(d.id)}"><td><b>${esc(d.anlage)}</b></td><td>${esc(d.titel)}<br><small>${esc(d.id)} · ${esc(d.pfad)}</small></td><td>${esc(datum(d.datum))}</td><td>${badge(d.stand, statusTon(d.stand))}</td></tr>`).join('')}</tbody></table>` : `<p class="untertitel u-m0">${esc(t('anl.keine'))}</p>`}</section>
      <section class="tafel"><h2>${esc(t('anl.beweise'))}</h2>${bew.length ? `<div class="raster drei">${bew.map(d => `<article class="karte"><span class="kennung">${esc(d.id)}</span><h2 class="u-fs95"><a href="${fallLink(fallId(), 'dokumente', d.id)}">${esc(d.titel)}</a></h2><p>${esc(d.pfad)}</p></article>`).join('')}</div>` : `<p class="untertitel u-m0">${esc(t('anl.keine_beweise'))}</p>`}</section>`;
    return [t('anl.titel'), '', inhalt, ''];
  },
  async journal() {
    const l = [...S.fall.journal].reverse();
    const inhalt = l.length ? `<section class="tafel">${l.map(j => `<div class="zeile"><div class="datumsbox"><b>${datum(j.datum).slice(0, 5)}</b>${datum(j.datum).slice(6)}</div><div class="zeile-text"><h3>${esc(j.titel)} ${badge(j.art)}</h3><p>${esc(j.text)}</p></div></div>`).join('')}</section>` : `<div class="leer"><h2>${esc(t('journal.keiner'))}</h2></div>`;
    return [t('journal.titel'), t('journal.untertitel'), inhalt, `<button class="knopf primaer" data-aktion="journal">${esc(t('journal.neu'))}</button>`];
  },
};

// ---------------------------------------------------------------- Vorschau
async function vorschau(zeigen) {
  const v = $('#vorschau'), b = $('#bereich');
  if (!zeigen || !dok(S.auswahl)) { v.hidden = true; b.classList.remove('hat-vorschau', 'breit'); S.breit = false; return; }
  const d = dok(S.auswahl); v.hidden = false; b.classList.add('hat-vorschau'); b.classList.toggle('breit', S.breit);
  const tab = S.tab, id = fallId();
  const kopf = `<div class="vorschau-kopf"><div class="tafel-kopf"><span class="kennung">${esc(d.id)}${d.anlage ? ' · ' + esc(d.anlage) : ''}</span><button class="symbol" data-aktion="vorschau-zu" aria-label="${esc(t('vorschau.schliessen'))}">×</button></div><h2>${esc(d.titel)}</h2>
    <div class="aktionen"><button class="knopf klein primaer" data-aktion="ordnen">${esc(t('vorschau.ordnen'))}</button><button class="knopf klein" data-aktion="einsortieren">${esc(t('vorschau.einsortieren'))}</button><button class="knopf klein" data-aktion="oeffnen">${esc(t('vorschau.oeffnen'))}</button><button class="knopf klein" data-aktion="finder" data-fall="${esc(id)}" data-dok="${esc(d.id)}">${esc(t('vorschau.im_dm', {dm: dm()}))}</button><button class="knopf klein still" data-aktion="breit">${esc(t(S.breit ? 'vorschau.geteilt' : 'vorschau.gross'))}</button></div>
    <div class="tabs u-mt12">${['vorschau', 'text', 'angaben'].map(k => `<button data-tab="${k}" class="${tab === k ? 'aktiv' : ''}">${esc(t('vorschau.tab_' + k))}</button>`).join('')}</div></div>`;
  let inhalt = '', klasse = 'vorschau-inhalt';
  if (d.fehlt) inhalt = `<div class="hinweis rot">${esc(t('vorschau.fehlt', {dm: dm()}))}</div>`;
  else if (tab === 'vorschau') {
    klasse += ' dokument';
    if (['JPG', 'JPEG', 'PNG', 'GIF'].includes(d.typ)) inhalt = `<img src="/raw/${id}/${d.id}" alt="${esc(d.titel)}">`;
    else if (['PDF', 'HTML', 'TXT', 'MD', 'HTM'].includes(d.typ)) inhalt = `<iframe src="/raw/${id}/${d.id}" title="${esc(d.titel)}" sandbox="allow-scripts"></iframe>`;
    else { klasse = 'vorschau-inhalt'; inhalt = `<div class="hinweis">${esc(t('vorschau.keine_anzeige', {typ: d.typ}))}</div>`; }
  } else if (tab === 'text') {
    klasse += ' dokument';
    v.innerHTML = kopf + `<div class="${klasse}"><pre>${esc(t('vorschau.text_laedt'))}</pre></div>`;
    try { const tx = await api.get(`/api/fall/${id}/text/${d.id}`); inhalt = `<div class="hinweis u-m12-16"><b>${esc(t('vorschau.textquelle'))}</b> ${esc(tx.textquelle_text || '')}${tx.seiten ? ` · ${esc(t('vorschau.seiten', {n: tx.seiten}))}` : ''}${tx.textstand ? ` · <b>${esc(t('vorschau.textstand'))}</b> ${esc(wert(tx.textstand))}` : ''}${tx.hinweis ? `<br>${esc(tx.hinweis)}` : ''}</div>` + (['bild', 'kein-text'].includes(tx.textquelle) ? `<div class="hinweis u-m12-16"><button class="knopf klein primaer" data-aktion="texterkennung">${esc(t('vorschau.ocr_knopf'))}</button> ${esc(t('vorschau.ocr_text'))}</div>` : tx.texterkennung ? `<div class="hinweis u-m12-16">${esc(t('vorschau.aus_ocr'))} <a href="${fallLink(id, 'dokumente', tx.texterkennung)}">${esc(tx.texterkennung)}</a>. ${esc(t('vorschau.aus_ocr_pruefen'))}</div>` : '') + `<pre>${esc(tx.text || t('vorschau.kein_text'))}</pre>`; } catch (e) { inhalt = `<div class="hinweis rot">${esc(e.message)}</div>`; }
  } else {
    const felder = [['pfad', d.pfad], ['datum', datum(d.datum) + ' ' + t('vorschau.f_datum_zusatz')], ['art', wert(d.art)], ['stand', wert(d.stand)], ['themen', d.themen.join(', ')], ['anlage', d.anlage], ['personen', d.personen.map(personName).join('; ')], ['verweise', d.verweise.join(', ')], ['notiz', d.notiz], ['groesse', groesse(d.groesse)]];
    inhalt = felder.map(([k, w]) => `<div class="feld-anzeige"><b>${esc(t('vorschau.f_' + k))}</b><span>${esc(w || '–')}</span></div>`).join('') + (d.verweise.length ? `<div class="feld-anzeige"><b>${esc(t('vorschau.verknuepft'))}</b>${d.verweise.map(x => dok(x) ? `<span><a href="${fallLink(id, 'dokumente', x)}">${esc(x)} · ${esc(dok(x).titel)}</a></span><br>` : '').join('')}</div>` : '');
  }
  v.innerHTML = kopf + `<div class="${klasse}">${inhalt}</div>`;
}

// ---------------------------------------------------------------- Dialoge und Speichern
let dialogSpeichern = null, dialogVeraendert = false;
// Personen im Ordnen-Dialog: Angekreuzte oben; ab sieben Beteiligten ein Suchfeld (Kennung, Name, Rolle), das nur filtert und nichts speichert.
function personenAuswahl(beteiligte, gewaehlt) {
  if (!beteiligte.length) return `<div class="hinweis u-m6-0">${esc(t('personen.keine'))}</div>`;
  const an = b => gewaehlt.includes(b.id);
  const zeilen = [...beteiligte.filter(an), ...beteiligte.filter(b => !an(b))].map(b => `<label class="u-block-normal" data-suchtext="${esc((b.id + ' ' + b.name + ' ' + (b.rolle || '')).toLocaleLowerCase('de'))}"><input type="checkbox" name="personen" value="${esc(b.id)}" ${an(b) ? 'checked' : ''}> ${esc(b.id)} · ${esc(b.name)}${b.rolle ? ` <span class="u-muted">${esc(wert(b.rolle))}</span>` : ''}</label>`).join('');
  const suche = beteiligte.length > 6 ? `<input type="search" id="personen-suche" placeholder="${esc(t('personen.suchen'))}" autocomplete="off" aria-label="${esc(t('personen.suchen_label'))}">` : '';
  return `${suche}<div class="hinweis u-m6-0 personen-liste">${zeilen}<p class="personen-leer u-muted" hidden>${esc(t('personen.leer'))}</p></div>`;
}
function feld(name, label, wert = '', art = 'text', extra = {}) {
  const hinweis = extra.hinweis ? `<small>${esc(extra.hinweis)}</small>` : '';
  if (art === 'textarea') return `<label class="feld">${esc(label)}<textarea name="${name}" ${extra.rows ? `rows="${extra.rows}"` : ''}>${esc(wert)}</textarea>${hinweis}</label>`;
  if (art === 'select') return `<label class="feld">${esc(label)}<select name="${name}">${extra.optionen}</select>${hinweis}</label>`;
  return `<label class="feld">${esc(label)}<input name="${name}" type="${art}" value="${esc(wert)}" ${extra.attr || ''}>${hinweis}</label>`;
}
function dialog(titel, inhalt, speichern, knopf = t('allg.speichern')) {
  $('#dialog-titel').textContent = titel; $('#dialog-inhalt').innerHTML = inhalt; $('#dialog-fehler').hidden = true;
  $('#dialog-speichern').textContent = knopf; $('#dialog-speichern').hidden = !speichern; $('#dialog-abbrechen').textContent = t(speichern ? 'allg.abbrechen' : 'allg.schliessen');
  dialogSpeichern = speichern; dialogVeraendert = false; $('#dialog').showModal();
}
function dialogZu() { if (dialogVeraendert && !confirm(t('dialog.verwerfen'))) return; dialogVeraendert = false; $('#dialog').close(); }
async function akteSpeichern(aendern, meldung = t('allg.gespeichert')) {
  const kopie = JSON.parse(JSON.stringify(akte())); aendern(kopie);
  const r = await api.post('/api/fall/' + fallId(), {akte: kopie, revision: S.fall.revision});
  S.zentrale = null;   // F14: Fristen und Aufgaben der Zentrale sonst veraltet
  await ladeFall(fallId()); if (meldung) toast(meldung); await render();
}
const liste = s => s.split(/[;,]/).map(x => x.trim()).filter(Boolean);

const FORMULARE = {
  beteiligter: {liste: 'beteiligte', kennung: 'P', titel: 'form.beteiligter', felder: b => `<div class="feld-reihe">${feld('name', t('form.name_stelle'), b.name)}${feld('rolle', t('form.rolle'), b.rolle, 'select', {optionen: opt(ROLLEN, b.rolle, t('allg.keine_angabe'))})}</div>${feld('anschrift', t('form.anschrift'), b.anschrift)}<div class="feld-reihe">${feld('kontakt', t('form.kontakt'), b.kontakt)}${feld('aktenzeichen', t('form.aktenzeichen_stelle'), b.aktenzeichen)}</div>`,
    lesen: f => ({name: f.get('name').trim(), rolle: f.get('rolle'), anschrift: f.get('anschrift').trim(), kontakt: f.get('kontakt').trim(), aktenzeichen: f.get('aktenzeichen').trim()}), leer: {name: '', rolle: '', anschrift: '', kontakt: '', aktenzeichen: ''}},
  verfahren: {liste: 'verfahren', kennung: 'V', titel: 'form.verfahren', felder: v => `${feld('art', t('form.verfahren_art'), v.art, 'text', {hinweis: t('form.verfahren_art_hinweis')})}<div class="feld-reihe">${feld('stelle', t('form.stelle'), v.stelle, 'select', {optionen: personOptionen(v.stelle)})}${feld('aktenzeichen', t('form.aktenzeichen'), v.aktenzeichen)}</div>${feld('stand', t('form.verfahrensstand'), v.stand)}${feld('ordner', t('form.unterordner_04'), v.ordner, 'text', {hinweis: t('form.unterordner_04_hinweis')})}`,
    lesen: f => ({art: f.get('art').trim(), stelle: f.get('stelle'), aktenzeichen: f.get('aktenzeichen').trim(), stand: f.get('stand').trim(), ordner: f.get('ordner').trim()}), leer: {art: '', stelle: '', aktenzeichen: '', stand: '', ordner: ''}},
  ereignis: {liste: 'ereignisse', kennung: 'E', titel: 'form.ereignis', felder: e => `<div class="feld-reihe">${feld('datum', t('form.datum'), e.datum, 'date')}${feld('art', t('form.art'), e.art, 'select', {optionen: opt(EREIGNIS_ART, e.art || 'Vermerk')})}</div>${feld('titel', t('form.kurztitel'), e.titel)}<div class="feld-reihe drei">${feld('zeitpunkt', t('form.zeitpunkt'), e.zeitpunkt || 'genau', 'select', {optionen: opt(ZEITPUNKT.map(k => [k, wert('zeitpunkt.' + k)]), e.zeitpunkt || 'genau'), hinweis: t('form.zeitpunkt_hinweis')})}${feld('datum_bis', t('form.bis'), e.datum_bis, 'date')}${feld('zeitpunkt_text', t('form.bekannt'), e.zeitpunkt_text, 'text', {hinweis: t('form.bekannt_hinweis')})}</div>${feld('quelle', t('form.quelle'), e.quelle, 'select', {optionen: dokOptionen(e.quelle)})}${feld('detail', t('form.einzelheiten'), e.detail, 'textarea', {hinweis: t('form.einzelheiten_hinweis')})}`,
    lesen: f => { const z = f.get('zeitpunkt') || 'genau'; return {datum: f.get('datum'), art: f.get('art'), titel: f.get('titel').trim(), quelle: f.get('quelle'), detail: f.get('detail').trim(), ...(z !== 'genau' ? {zeitpunkt: z, datum_bis: f.get('datum_bis') || '', zeitpunkt_text: f.get('zeitpunkt_text').trim()} : {zeitpunkt: 'genau', datum_bis: '', zeitpunkt_text: ''})}; }, leer: {datum: heute(), titel: '', art: 'Vermerk', quelle: '', detail: '', zeitpunkt: 'genau', datum_bis: '', zeitpunkt_text: ''}},
  frist: {liste: 'fristen', kennung: 'F', titel: 'form.frist', felder: x => rechnerHtml(x, true) + `
    <div class="feld-reihe">${feld('datum', t('form.fristende'), x.datum, 'date')}${feld('art', t('form.art'), x.art, 'select', {optionen: opt(FRIST_ART, x.art || 'gesetzlich')})}</div>${feld('titel', t('form.kurztitel'), x.titel)}<div class="feld-reihe">${feld('verfahren', t('form.verfahren'), x.verfahren, 'select', {optionen: opt(akte().verfahren.map(v => [v.id, v.id + ' · ' + v.art]), x.verfahren, t('allg.keine_angabe'))})}${feld('ausloeser_ereignis', t('form.ausloeser_ereignis'), x.ausloeser_ereignis, 'select', {optionen: opt([...akte().ereignisse].sort((a, b) => a.datum.localeCompare(b.datum)).map(e => [e.id, e.id + ' · ' + datum(e.datum) + ((e.zeitpunkt || 'genau') !== 'genau' ? ' (' + wert('zeitpunkt.' + e.zeitpunkt) + ')' : '') + ' · ' + e.titel]), x.ausloeser_ereignis, t('allg.keine_angabe')), hinweis: t('form.ausloeser_ereignis_hinweis')})}</div>${feld('ausloeser', t('form.ausloeser'), x.ausloeser, 'text', {hinweis: t('form.ausloeser_hinweis')})}${feld('rechtsgrundlage', t('form.rechtsgrundlage'), x.rechtsgrundlage, 'text', {hinweis: t('form.rechtsgrundlage_hinweis')})}${feld('berechnung', t('form.rechnung'), x.berechnung, 'textarea')}<div class="feld-reihe">${feld('pruefstatus', t('form.pruefstatus'), x.pruefstatus, 'select', {optionen: opt(FRIST_STATUS, x.pruefstatus || 'offen'), hinweis: t('form.pruefstatus_hinweis')})}${feld('quelle', t('form.quelle'), x.quelle, 'select', {optionen: dokOptionen(x.quelle)})}</div>${feld('geprueft_von', t('form.geprueft_von'), x.geprueft_von, 'text', {hinweis: t('form.geprueft_von_hinweis')})}<input type="hidden" name="geprueft_am" value="${esc(x.geprueft_am || '')}">`,
    lesen: f => ({datum: f.get('datum'), art: f.get('art'), titel: f.get('titel').trim(), ausloeser: f.get('ausloeser').trim(), rechtsgrundlage: f.get('rechtsgrundlage').trim(), berechnung: f.get('berechnung').trim(), pruefstatus: f.get('pruefstatus'), quelle: f.get('quelle'), geprueft_von: f.get('geprueft_von').trim(), geprueft_am: f.get('pruefstatus') === 'bestätigt' ? (f.get('geprueft_am') || heute()) : '', verfahren: f.get('verfahren') || '', ausloeser_ereignis: f.get('ausloeser_ereignis') || ''}), leer: {datum: '', titel: '', art: 'gesetzlich', ausloeser: '', rechtsgrundlage: '', berechnung: '', pruefstatus: 'offen', quelle: '', geprueft_von: '', geprueft_am: '', verfahren: '', ausloeser_ereignis: ''}},
  aufgabe: {liste: 'aufgaben', kennung: 'A', titel: 'form.aufgabe', felder: a => `${feld('titel', t('form.aufgabe'), a.titel)}${feld('detail', t('form.einzelheiten'), a.detail, 'textarea')}<div class="feld-reihe drei">${feld('faellig', t('form.faellig'), a.faellig, 'date')}${feld('quelle', t('form.quelle'), a.quelle, 'select', {optionen: dokOptionen(a.quelle)})}${feld('erledigt', t('form.erledigt'), a.erledigt ? 'ja' : 'nein', 'select', {optionen: opt([['nein', t('form.nein')], ['ja', t('form.ja')]], a.erledigt ? 'ja' : 'nein')})}</div>`,
    lesen: f => ({titel: f.get('titel').trim(), detail: f.get('detail').trim(), faellig: f.get('faellig'), quelle: f.get('quelle'), erledigt: f.get('erledigt') === 'ja'}), leer: {titel: '', detail: '', faellig: '', quelle: '', erledigt: false}},
  entwurf: {liste: 'entwuerfe', kennung: 'W', titel: 'form.entwurf', felder: w => `${feld('titel', t('form.titel'), w.titel)}${feld('datei', t('form.datei'), w.datei, 'text', {hinweis: t('form.datei_hinweis')})}<div class="feld-reihe drei">${feld('fassung', t('form.fassung'), w.fassung || 1, 'number', {attr: 'min="1"'})}${feld('status', t('form.status'), w.status, 'select', {optionen: opt(ENTWURF_STATUS, w.status || 'in Arbeit')})}${feld('versandt_als', t('form.versandt_als'), w.versandt_als, 'select', {optionen: dokOptionen(w.versandt_als, t('form.noch_nicht_versandt')), hinweis: t('form.versandt_als_hinweis')})}</div>`,
    lesen: f => ({titel: f.get('titel').trim(), datei: f.get('datei').trim(), fassung: parseInt(f.get('fassung'), 10) || 1, status: f.get('status'), versandt_als: f.get('versandt_als')}), leer: {titel: '', datei: '', fassung: 1, status: 'in Arbeit', versandt_als: ''}},
  notiz: {liste: 'notizen', kennung: 'N', titel: 'form.notiz', felder: n => `${feld('titel', t('form.titel'), n.titel)}${feld('text', t('form.text'), n.text, 'textarea', {rows: 8})}`,
    lesen: f => ({titel: f.get('titel').trim(), text: f.get('text').trim(), datum: heute()}), leer: {titel: '', text: '', datum: ''}},
};
function eintragDialog(art, id) {
  const F = FORMULARE[art]; const vorhanden = id ? akte()[F.liste].find(x => x.id === id) : null; const werte = vorhanden || {id: '', ...F.leer};
  dialog(id ? t('dialog.bearbeiten', {was: t(F.titel), id}) : t('dialog.neu', {was: t(F.titel)}), F.felder(werte) + (id ? `<p><button type="button" class="knopf klein" data-aktion="eintrag-entfernen" data-art="${art}" data-id="${esc(id)}">${esc(t('dialog.entfernen'))}</button> <small class="u-muted">${esc(t('dialog.entfernen_hinweis'))}</small></p>` : ''),
    async f => {
      const neu = F.lesen(f);
      // N03: „geprüft“ und „versandt“ frieren eine Fassung ein. Das kann nur entwurf_erfassen,
      // also geht dieser Statuswechsel über das Werkzeug statt über das Speichern der ganzen Akte.
      if (art === 'entwurf' && (neu.status === 'geprüft' || neu.status === 'versandt')) {
        const r = await api.werkzeug('entwurf_erfassen', {fall: fallId(), titel: neu.titel, datei: neu.datei, status: neu.status, versandt_als: neu.versandt_als || ''});
        await ladeFall(fallId());
        toast((r.hinweise && r.hinweise.length ? r.hinweise.join(' ') + ' ' : '') + t('entw.eingefroren_meldung', {status: neu.status, n: r.entwurf.fassung}));
        await render(); return;
      }
      await akteSpeichern(a => { const l = a[F.liste]; if (id) Object.assign(l.find(x => x.id === id), neu); else l.push({id: naechste(a, F.liste, F.kennung), ...neu}); });
    });
}
const jaNein = w => opt([['nein', t('form.nein')], ['ja', t('form.ja')]], w ? 'ja' : 'nein');
function ordnenDialog(d) {
  dialog(t('ordnen.titel', {id: d.id}), `<div class="hinweis">${esc(t('ordnen.hinweis'))}</div>${feld('titel', t('ordnen.anzeigetitel'), d.titel)}<div class="feld-reihe drei">${feld('datum', t('ordnen.dokumentdatum'), d.datum, 'date', {hinweis: t('ordnen.kein_zugang')})}${feld('art', t('form.art'), d.art, 'select', {optionen: opt(DOK_ART, d.art, t('allg.keine_angabe'))})}${feld('stand', t('ordnen.stand'), d.stand, 'select', {optionen: opt(DOK_STAND, d.stand)})}</div><div class="feld-reihe">${feld('textstand', t('ordnen.textstand'), d.textstand, 'select', {optionen: opt(DOK_TEXTSTAND, d.textstand, t('allg.keine_angabe')), hinweis: t('ordnen.textstand_hinweis')})}</div><div class="feld-reihe">${feld('themen', t('ordnen.themen'), d.themen.join(', '), 'text', {hinweis: t('ordnen.komma')})}${feld('anlage', t('ordnen.anlage'), d.anlage, 'text', {hinweis: t('ordnen.anlage_hinweis')})}</div>
    <div class="feld">${esc(t('ordnen.personen'))}${personenAuswahl(akte().beteiligte, d.personen)}</div>
    ${feld('verweise', t('ordnen.verweise'), d.verweise.join(', '), 'text', {hinweis: t('ordnen.verweise_hinweis')})}${feld('notiz', t('ordnen.notiz'), d.notiz, 'textarea')}${feld('angeheftet', t('ordnen.anheften'), akte().fall.angeheftet.includes(d.id) ? 'ja' : 'nein', 'select', {optionen: jaNein(akte().fall.angeheftet.includes(d.id))})}`,
    async f => { await akteSpeichern(a => { const x = a.dokumente[d.id]; Object.assign(x, {titel: f.get('titel').trim(), datum: f.get('datum'), art: f.get('art'), stand: f.get('stand'), themen: liste(f.get('themen')), anlage: f.get('anlage').trim(), personen: f.getAll('personen'), verweise: liste(f.get('verweise')).map(s => s.toUpperCase()), notiz: f.get('notiz').trim(), textstand: f.get('textstand') || ''});
      const p = a.fall.angeheftet.filter(i => i !== d.id); if (f.get('angeheftet') === 'ja') p.push(d.id); a.fall.angeheftet = p; }); });
}
async function vorlageDialog() {
  // Entwurf aus Vorlage: das Werkzeug vorlage_fuellen kopiert die Vorlage nach 06 Entwürfe und setzt Absender, Unterschrift, Datum ein
  const vorlagen = await api.werkzeug('vorlagen_auflisten', {});
  dialog(t('vorlage.titel'), `${feld('vorlage', t('vorlage.vorlage'), '', 'select', {optionen: opt(vorlagen.map(v => [v.name, v.name]), vorlagen[0] ? vorlagen[0].name : '')})}${feld('ziel', t('vorlage.dateiname'), '', 'text', {hinweis: t('vorlage.dateiname_hinweis')})}<div class="hinweis">${esc(t('vorlage.hinweis'))}</div>`,
    async f => { const r = await api.werkzeug('vorlage_fuellen', {fall: fallId(), vorlage: f.get('vorlage'), ziel: f.get('ziel').trim()}); await ladeFall(fallId()); toast(t('vorlage.angelegt', {datei: r.datei, absender: r.absender ? t('vorlage.absender', {quelle: r.absender_quelle}) : t('vorlage.kein_absender'), n: r.offene_platzhalter})); await render(); }, t('dialog.anlegen'));
}
function einsortierenDialog(d) {
  dialog(t('einsortieren.titel', {titel: d.titel}), `<p class="pfad">${esc(d.pfad)}</p><div class="feld-reihe">${feld('bereich', t('einsortieren.bereich'), d.gruppe, 'select', {optionen: opt(GRUPPEN.map(g => [g, g]), d.gruppe)})}${feld('unterordner', t('einsortieren.unterordner'), d.pfad.split('/').slice(1, -1).join('/'), 'text', {hinweis: t('einsortieren.unterordner_hinweis')})}</div><div class="hinweis">${esc(t('einsortieren.hinweis'))}</div>`,
    async f => { await api.werkzeug('dokument_verschieben', {fall: fallId(), dokument: d.id, bereich: f.get('bereich'), unterordner: f.get('unterordner').trim()}); await ladeFall(fallId()); toast(t('einsortieren.fertig')); await render(); }, t('dialog.verschieben'));
}
function neuerFallDialog() {
  dialog(t('neuerfall.titel'), `${feld('titel', t('neuerfall.bezeichnung'), '', 'text', {attr: 'required maxlength="120"'})}<div class="feld-reihe">${feld('bereich', t('neuerfall.bereich'), 'Allgemein', 'select', {optionen: opt(BEREICHE, 'Allgemein')})}${feld('rolle', t('neuerfall.rolle'), '', 'text', {hinweis: t('neuerfall.rolle_hinweis')})}</div>${feld('ziel', t('neuerfall.ziel'), '', 'textarea')}<div class="hinweis">${esc(t('neuerfall.hinweis'))}</div>`,
    async f => { const c = await api.post('/api/fall', {titel: f.get('titel').trim(), bereich: f.get('bereich'), rolle: f.get('rolle').trim(), ziel: f.get('ziel').trim()}); S.zentrale = null; toast(t('neuerfall.angelegt', {id: c.id})); location.hash = fallLink(c.id).slice(1); }, t('dialog.fall_anlegen'));
}
function fallBearbeitenDialog() {
  const f0 = akte().fall;
  dialog(t('fallbearb.titel', {id: f0.id}), `${feld('titel', t('fallbearb.bezeichnung'), f0.titel)}${feld('untertitel', t('fallbearb.untertitel'), f0.untertitel)}<div class="feld-reihe">${feld('bereich', t('neuerfall.bereich'), f0.bereich, 'select', {optionen: opt(BEREICHE, f0.bereich)})}${feld('status', t('fallbearb.status'), f0.status, 'select', {optionen: opt(['offen', 'ruhend', 'abgeschlossen'], f0.status)})}</div><div class="feld-reihe">${feld('rolle', t('fallbearb.rolle'), f0.rolle)}${feld('rechtsordnung', t('fallbearb.rechtsordnung'), f0.rechtsordnung || 'DE', 'text', {hinweis: t('fallbearb.rechtsordnung_hinweis')})}</div>${feld('themen', t('ordnen.themen'), f0.themen.join(', '), 'text', {hinweis: t('ordnen.komma')})}${feld('ziel', t('fallbearb.ziel'), f0.ziel, 'textarea')}`,
    async f => { await akteSpeichern(a => Object.assign(a.fall, {titel: f.get('titel').trim(), untertitel: f.get('untertitel').trim(), bereich: f.get('bereich'), status: f.get('status'), rolle: f.get('rolle').trim(), rechtsordnung: f.get('rechtsordnung').trim(), themen: liste(f.get('themen')), ziel: f.get('ziel').trim()})); S.zentrale = null; });
}
function journalDialog() {
  dialog(t('journal_dialog.titel'), `<div class="feld-reihe">${feld('art', t('form.art'), 'Arbeit', 'select', {optionen: opt(JOURNAL_ARTEN, 'Arbeit')})}${feld('titel', t('form.kurztitel'), '')}</div>${feld('text', t('form.text'), '', 'textarea', {rows: 7, hinweis: t('journal_dialog.text_hinweis')})}`,
    async f => { await api.werkzeug('journal_schreiben', {fall: fallId(), art: f.get('art'), titel: f.get('titel').trim(), text: f.get('text').trim()}); await ladeFall(fallId()); toast(t('journal_dialog.eingetragen')); await render(); }, t('dialog.anhaengen'));
}
// Fristenrechner: ein Block für den Frist-Dialog (mit Übernahme in die Felder) und für den eigenen Dialog (nur rechnen).
function rechnerHtml(x = {}, uebernehmen = true) {
  return `<div class="rechner"><h3>${esc(t('rechner.titel'))}</h3><div class="feld-reihe drei">${feld('r_start', t('rechner.ereignistag'), x.r_start || '', 'date')}${feld('r_menge', t('rechner.dauer'), x.r_menge || 2, 'number', {attr: 'min="1"'})}${feld('r_einheit', t('rechner.einheit'), x.r_einheit || 'wochen', 'select', {optionen: opt(['tage', 'wochen', 'monate', 'jahre'].map(k => [k, t('rechner.' + k)]), x.r_einheit || 'wochen')})}</div><div class="feld-reihe">${feld('r_ereignis', t('rechner.zaehlt'), 'ja', 'select', {optionen: opt([['ja', t('rechner.nicht_mit')], ['nein', t('rechner.mit')]], 'ja')})}${feld('r_werktag', t('rechner.wochenende'), 'ja', 'select', {optionen: opt([['ja', t('rechner.verschieben')], ['nein', t('rechner.nicht_verschieben')]], 'ja')})}</div><button type="button" class="knopf klein" data-aktion="berechnen" data-uebernehmen="${uebernehmen ? 'ja' : 'nein'}">${esc(t(uebernehmen ? 'rechner.berechnen_uebernehmen' : 'rechner.berechnen'))}</button><div class="ergebnis" id="rechner-ergebnis" aria-live="polite"></div></div>`;
}
function rechnerDialog() {
  dialog(t('rechner.dialog_titel'), rechnerHtml({}, false) + `<p class="untertitel">${esc(t('rechner.nur_rechnen'))}</p>`, null);
}
async function fristBerechnen(b) {
  const f = $('#formular'), d = new FormData(f), erg = $('#rechner-ergebnis');
  const start = d.get('r_start'), menge = parseInt(d.get('r_menge'), 10);
  if (!start) { erg.textContent = t('rechner.kein_start'); return; }
  if (!(menge >= 1)) { erg.textContent = t('rechner.dauer_min'); return; }
  b.disabled = true; erg.textContent = t('rechner.rechnet');
  try {
    const r = await api.post('/api/fristen/berechnen', {start, menge, einheit: d.get('r_einheit'), ereignisfrist: d.get('r_ereignis') === 'ja', werktagsregel: d.get('r_werktag') === 'ja'});
    erg.textContent = r.rechnung.join('\n') + '\n' + t('rechner.feiertage', {land: r.feiertagsland_name}) + (r.regional ? ' ' + r.regional : '') + '\n' + r.hinweis;
    if (b.dataset.uebernehmen === 'ja') {
      const setze = (name, w, nurWennLeer = false) => { const el = f.elements[name]; if (el && (!nurWennLeer || !el.value.trim())) el.value = w; };
      setze('datum', r.ende); setze('berechnung', r.rechnung.join('\n')); setze('rechtsgrundlage', r.grundlagen.join(', '), true);
      setze('ausloeser', t('rechner.ausloeser_vorlage', {datum: datum(r.start)}), true);
      dialogVeraendert = true; toast(t('rechner.uebernommen', {ende: r.ende_text}));
    }
  } catch (e) { erg.textContent = t('rechner.fehler', {fehler: e.message}); }
  finally { b.disabled = false; }
}
async function bestandPruefen(b) {
  const ziel = $('#bestand-ergebnis'); b.disabled = true; ziel.innerHTML = `<div class="hinweis">${esc(t('bestand.laeuft'))}</div>`;
  try {
    const r = await api.get('/api/bestand');
    const block = (titel, l, text) => l.length ? `<div class="feld-anzeige"><b>${esc(titel)} (${l.length})</b><span>${l.map(x => esc(text(x))).join('<br>')}</span></div>` : '';
    ziel.innerHTML = r.faelle.map(c => `<div class="ergebnisblock ${c.veraendert.length || c.fehlend.length ? 'schlecht' : 'gut'}">${esc(t('bestand.ergebnis', {fall: c.fall, geprueft: c.geprueft, veraendert: c.veraendert.length, fehlend: c.fehlend.length, ohne: c.nicht_erfasst.length, verschoben: c.verschoben_erkannt.length}))}</div>${block(t('bestand.block_veraendert'), c.veraendert, x => x.id + ' · ' + x.pfad)}${block(t('bestand.block_fehlend'), c.fehlend, x => x.id + ' · ' + x.pfad)}${block(t('bestand.block_ohne'), c.nicht_erfasst, x => x)}${block(t('bestand.block_verschoben'), c.verschoben_erkannt, x => x.id + ' · ' + x.von + ' → ' + x.nach)}`).join('') || `<div class="hinweis">${esc(t('bestand.kein_fall'))}</div>`;
    ziel.innerHTML += `<p class="untertitel">${esc(t('bestand.geprueft_um', {zeit: new Date().toLocaleString('de-DE')}))}</p>`;
  } catch (e) { ziel.innerHTML = `<div class="hinweis rot">${esc(e.message)}</div>`; }
  finally { b.disabled = false; }
}
async function sicherungProbe(b) {
  const ziel = $('#probe-ergebnis'); b.disabled = true; ziel.innerHTML = `<div class="hinweis">${esc(t('bestand.probe_laeuft'))}</div>`;
  try {
    const r = await api.post('/api/sicherung/probe', {});
    const faelle = r.faelle.map(c => esc(t('bestand.probe_fall', {fall: c.fall, geprueft: c.geprueft, veraendert: c.veraendert.length, fehlend: c.fehlend.length, schema: c.schema_fehler.length}))).join('<br>');
    ziel.innerHTML = `<div class="ergebnisblock ${r.bestanden ? 'gut' : 'schlecht'}">${esc(t(r.bestanden ? 'bestand.probe_bestanden' : 'bestand.probe_nicht_bestanden'))}<br>${esc(t('bestand.probe_dateien', {n: r.dateien, zusatz: r.pruefsummendatei === false ? t('bestand.probe_pruefsummen') : ''}))}<br>${faelle}${r.fehler.length ? '<br>' + r.fehler.map(esc).join('<br>') : ''}${(r.hinweise || []).length ? '<br>' + r.hinweise.map(esc).join('<br>') : ''}</div><p class="untertitel">${esc(r.hinweis)}</p>`;
  } catch (e) { ziel.innerHTML = `<div class="hinweis rot">${esc(e.message)}</div>`; }
  finally { b.disabled = false; }
}
async function sicherungErstellen(b) {
  const alt = b.textContent; b.disabled = true; b.textContent = t('bestand.sicherung_laeuft');
  const meldung = document.createElement('div'); meldung.className = 'hinweis'; meldung.textContent = t('bestand.sicherung_hinweis'); b.after(meldung);
  try {
    const r = await api.post('/api/sicherung', {});
    S.zentrale = null; await render();
    toast(t('bestand.sicherung_fertig', {dateien: r.dateien, groesse: groesse(r.groesse), zusatz: r.zweites_ziel ? t('bestand.sicherung_kopie') : '.'}));
  } catch (e) { meldung.className = 'hinweis rot'; meldung.textContent = t('bestand.sicherung_fehler', {fehler: e.message}); b.disabled = false; b.textContent = alt; }
}
function zuordnenDialog(name) {
  const f = S.zentrale.faelle.filter(c => !c.fehler);
  if (!f.length) return toast(t('zuordnen.erst_fall'), true);
  dialog(t('zuordnen.titel'), `<p class="pfad">${esc(name)}</p>${feld('fall', t('zuordnen.zielfall'), '', 'select', {optionen: opt(f.map(c => [c.id, c.id + ' · ' + c.titel]))})}`,
    async fd => { await api.post('/api/eingang/zuordnen', {name, fall: fd.get('fall')}); S.zentrale = null; toast(t('zuordnen.fertig')); await render(); }, t('dialog.zuordnen'));
}
async function hochladen(ziel) {
  const dateien = [...$('#upload').files]; $('#upload').value = ''; let n = 0;
  try {
    for (const f of dateien) {
      if (f.size > 25 * 1024 * 1024) throw new Error(t('upload.zu_gross', {name: f.name, dm: dm()}));
      const inhalt = await new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1]); r.onerror = rej; r.readAsDataURL(f); });
      await api.post(ziel === 'fall' ? `/api/fall/${fallId()}/eingang` : '/api/eingang', {name: f.name, inhalt}); n++;
    }
    toast(t('upload.abgelegt', {n}));
  } catch (e) { toast(t('upload.teilweise', {n, fehler: e.message}), true); }
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
    else if (a === 'beispiel-laden') { const r = await api.werkzeug('beispiel_laden', {}); S.zentrale = null; toast(t('meld.beispiel', {id: r.id})); location.hash = `#seite=uebersicht&fall=${r.id}`; }
    else if (a === 'neu-laden') { S.zentrale = null; S.quellen = null; if (S.fall) await ladeFall(fallId()); await render(); toast(t('allg.neu_eingelesen')); }
    else if (a === 'finder') await api.post('/api/oeffnen', {fall: b.dataset.fall, dokument: b.dataset.dok, bereich: b.dataset.gruppe || b.dataset.ort, zeigen: !!b.dataset.dok});
    else if (a === 'texterkennung') { b.disabled = true; toast(t('meld.ocr_laeuft')); const r = await api.werkzeug('texterkennung', {fall: fallId(), dokument: S.auswahl}); await ladeFall(fallId()); toast(t('meld.ocr_fertig', {id: r.texterkennung, seiten: r.seiten, zeichen: r.zeichen})); await render(); }
    else if (a === 'oeffnen') { const r = await api.post('/api/oeffnen', {fall: fallId(), dokument: S.auswahl}); if (r.hinweis) toast(r.hinweis); }
    else if (a === 'hochladen') { $('#upload').onchange = () => hochladen(b.dataset.ziel); $('#upload').click(); }
    else if (a === 'zuordnen') zuordnenDialog(b.dataset.name);
    else if (a === 'kopieren') { await navigator.clipboard.writeText(b.dataset.text); toast(t('allg.kopiert')); }
    else if (a === 'gruppe') { S.filter.gruppe = b.dataset.gruppe; S.treffer = null; S.filter.q = ''; gehe({seite: 'dokumente', fall: fallId()}); }
    else if (a === 'fall-bearbeiten') fallBearbeitenDialog();
    else if (a === 'neu') eintragDialog(b.dataset.art, '');
    else if (a === 'bearbeiten') eintragDialog(b.dataset.art, b.dataset.id);
    else if (a === 'eintrag-entfernen') { const F = FORMULARE[b.dataset.art]; if (!confirm(t('dialog.entfernen_frage', {id: b.dataset.id}))) return; await akteSpeichern(x => { x[F.liste] = x[F.liste].filter(y => y.id !== b.dataset.id); }, t('dialog.entfernt')); $('#dialog').close(); }
    else if (a === 'ordnen') ordnenDialog(dok(S.auswahl));
    else if (a === 'einsortieren') einsortierenDialog(dok(S.auswahl));
    else if (a === 'vorlage') await vorlageDialog();
    else if (a === 'vorschau-zu') { S.auswahl = ''; gehe({seite: 'dokumente', fall: fallId()}); }
    else if (a === 'breit') { S.breit = !S.breit; vorschau(true); }
    else if (a === 'journal') journalDialog();
    else if (a === 'rechner') rechnerDialog();
    else if (a === 'berechnen') await fristBerechnen(b);
    else if (a === 'bestand-pruefen') await bestandPruefen(b);
    else if (a === 'sicherung') await sicherungErstellen(b);
    else if (a === 'sicherung-probe') await sicherungProbe(b);
    else toast(t('allg.unbekannte_aktion', {aktion: a}), true);   // still nichts tun war F01 aus dem Prüfbericht
  } catch (err) { toast(err.message, true); }
});
document.addEventListener('keydown', e => { if (e.target.id === 'personen-suche' && e.key === 'Enter') { e.preventDefault(); return; } const z = e.target.closest && e.target.closest('[data-dok]'); if (z && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); z.click(); } if ((e.metaKey || e.ctrlKey) && e.key === 'k' && $('#dok-suche')) { e.preventDefault(); $('#dok-suche').focus(); } });
let suchTimer;
document.addEventListener('input', e => {
  if (e.target.closest('#formular') && e.target.id !== 'personen-suche') dialogVeraendert = true;
  if (e.target.id === 'personen-suche') { const q = e.target.value.trim().toLocaleLowerCase('de'); let sichtbar = 0; document.querySelectorAll('.personen-liste label').forEach(l => { l.hidden = !!q && !l.dataset.suchtext.includes(q); if (!l.hidden) sichtbar++; }); $('.personen-leer').hidden = sichtbar > 0; }
  if (e.target.id === 'dok-suche') { S.filter.q = e.target.value; clearTimeout(suchTimer); suchTimer = setTimeout(async () => { try { S.treffer = S.filter.q.trim().length > 1 ? (await api.get(`/api/fall/${fallId()}/suche?q=${encodeURIComponent(S.filter.q.trim())}`)).treffer : null; } catch (err) { toast(err.message, true); } const f = $('#dok-suche'); const pos = f && f.selectionStart; await render(); const g = $('#dok-suche'); if (g) { g.focus(); g.setSelectionRange(pos, pos); } }, 300); }
  if (e.target.id === 'fall-suche' || e.target.id === 'fall-filter') { const q = $('#fall-suche').value.toLocaleLowerCase('de'), s = $('#fall-filter').value; $('#fall-liste').innerHTML = S.zentrale.faelle.filter(c => (c.id + ' ' + c.titel + ' ' + (c.bereich || '')).toLocaleLowerCase('de').includes(q) && (s === 'Alle' || c.status === s)).map(fallKarte).join('') || `<div class="leer">${esc(t('faelle.kein_treffer'))}</div>`; }
  if (e.target.id === 'quellen-suche') { const q = e.target.value.toLocaleLowerCase('de'); $('#quellen-liste').innerHTML = S._quellenKarten(S.quellen.quellen.filter(x => JSON.stringify(x).toLocaleLowerCase('de').includes(q))); }
});
document.addEventListener('change', async e => {
  try {
    if (['f-gruppe', 'f-typ', 'f-stand'].includes(e.target.id)) { S.filter[e.target.id.slice(2)] = e.target.value; await render(); }
    if (e.target.id === 'fall-filter') e.target.dispatchEvent(new Event('input', {bubbles: true}));
    if (e.target.dataset.fallstatus) { await api.werkzeug('fall_status_setzen', {fall: e.target.dataset.fallstatus, status: e.target.value}); S.zentrale = null; toast(t('faelle.status_gespeichert')); await render(); }
    if (e.target.dataset.aufgabe) { const id = e.target.dataset.aufgabe, w = e.target.checked; await akteSpeichern(a => { a.aufgaben.find(x => x.id === id).erledigt = w; }, t(w ? 'meld.erledigt' : 'meld.wieder_offen')); }
  } catch (err) { toast(err.message, true); await render(); }
});
document.addEventListener('submit', async e => {
  if (e.target.id === 'einstellungen') {
    e.preventDefault(); const f = new FormData(e.target);
    const daten = {sicherung: {ziel: f.get('ziel').trim(), zweites_ziel: f.get('zweites_ziel').trim()}, einstellungen: {feiertagsland: f.get('feiertagsland') || '', sprache: f.get('sprache') || '',
      absender: {name: f.get('ab_name').trim(), strasse: f.get('ab_strasse').trim(), plz_ort: f.get('ab_plz_ort').trim(), telefon: f.get('ab_telefon').trim(), email: f.get('ab_email').trim()}}};
    try { await api.post('/api/einstellungen', daten); S.zentrale = null; if ((f.get('sprache') || SPRACHE) !== SPRACHE) await ladeTexte(); toast(t('einst.gespeichert')); await render(); } catch (err) { toast(err.message, true); }
  }
});
$('#formular').onsubmit = async e => { e.preventDefault(); if (!dialogSpeichern) return; const k = $('#dialog-speichern'); k.disabled = true; $('#dialog-fehler').hidden = true;
  try { await dialogSpeichern(new FormData(e.target)); dialogVeraendert = false; if ($('#dialog').open) $('#dialog').close(); } catch (err) { $('#dialog-fehler').textContent = err.message; $('#dialog-fehler').hidden = false; } finally { k.disabled = false; } };
$('#dialog-schliessen').onclick = dialogZu; $('#dialog-abbrechen').onclick = dialogZu; $('#dialog').addEventListener('cancel', e => { e.preventDefault(); dialogZu(); });
window.addEventListener('hashchange', render);
// F14: nach einem Tageswechsel bei lange geöffneter Anwendung stimmen „in n Tagen“ und die Fristenlisten nicht mehr; beim Zurückkommen neu einlesen
let renderTag = heute();
window.addEventListener('focus', async () => { if (heute() !== renderTag) { renderTag = heute(); S.zentrale = null; if (S.fall) await ladeFall(fallId()); await render(); } });
window.addEventListener('beforeunload', e => { if (dialogVeraendert) { e.preventDefault(); e.returnValue = ''; } });
// Erst die Texte der eingestellten Sprache laden, dann rendern; schlägt das Laden fehl, zeigt render() den Verbindungsfehler mit den Kennungen
ladeTexte().catch(e => console.warn(e.message)).then(render);
