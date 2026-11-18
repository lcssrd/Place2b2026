// Instantanés DOM de la vraie application (sans scripts), pour la composition vidéo.
const { chromium } = require('playwright');
const fs = require('fs');
const crypto = require('crypto');
const APP = 'file:///home/user/Place2b2026/Place2b2026.html';
const tileMap = {};

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('response', async r => {
    const u = r.url();
    if (/wmts|arcgisonline/.test(u) && r.status() === 200 && !tileMap[u]) {
      try { const b = await r.body(); const f = crypto.createHash('md5').update(u).digest('hex') + '.png'; fs.writeFileSync('tiles/' + f, b); tileMap[u] = f; } catch (e) {}
    }
  });
  await page.goto(APP);
  await page.waitForTimeout(800);
  await page.evaluate(txt => loadText(txt), fs.readFileSync('data/state-loaded.json', 'utf8'));
  await page.waitForTimeout(1500);
  await page.check('input[data-layer="links"]');
  return page;
}
async function setView(page, v) {
  await page.evaluate(v => { map.setView(v.c, v.z + 1, { animate: false }); map.setView(v.c, v.z, { animate: false }); }, v);
  await page.waitForTimeout(2500);
  await page.waitForFunction(() => [...document.querySelectorAll('img.leaflet-tile')].every(i => i.complete));
  await page.waitForTimeout(800);
}
async function annotate(page) {
  return page.evaluate(() => {
    const same = (a, b) => Math.abs(a.lat - b.lat) < 1e-9 && Math.abs(a.lng - b.lng) < 1e-9;
    const P = ll => { const p = map.latLngToLayerPoint(ll); return [p.x, p.y]; };
    const out = { links: [], dots: [], pins: [] };
    for (const [sid, pid] of D.placeOf) {
      const st = D.student.get(sid), p = D.place.get(pid), l = S.locations[p.loc], b = best(st, p.loc);
      LG.links.eachLayer(ly => { const [a, e] = ly.getLatLngs(); if (same(a, b.g) && same(e, l) && !ly._path.dataset.sid) { ly._path.dataset.sid = sid; ly._path.dataset.loc = p.loc; } });
      out.links.push({ sid, nom: st.nom, loc: p.loc, min: b.min, a: P(b.g), b: P(l) });
    }
    for (const k of ['a1', 'a2']) LG[k].eachLayer(ly => { const g = ly.getLatLng(); const st = S.students.find(s => s['g' + k[1]] && same(s['g' + k[1]], g)); if (st) { ly._path.dataset.sid = st.id; ly._path.dataset.k = k; out.dots.push({ sid: st.id, k, p: P(g) }); } });
    LG.stages.eachLayer(m => { const g = m.getLatLng(); const lk = Object.keys(S.locations).find(k => same(S.locations[k], g)); m._icon.dataset.loc = lk; out.pins.push({ loc: lk, n: (D.byLoc.get(lk) || []).length, p: P(g), name: S.locations[lk].etab }); });
    out.view = { c: [map.getCenter().lat, map.getCenter().lng], z: map.getZoom() };
    out.mapRect = document.querySelector('#map').getBoundingClientRect().toJSON();
    out.stats = document.querySelector('#stats').innerHTML;
    out.rows = Object.fromEntries([...document.querySelectorAll('#list .row')].map(r => [r.dataset.id, r.innerHTML]));
    out.pinHtml = Object.fromEntries([...document.querySelectorAll('.leaflet-marker-icon[data-loc]')].map(m => [m.dataset.loc, m.innerHTML]));
    return out;
  });
}
async function serialize(page, file) {
  let html = await page.evaluate(() => {
    document.querySelectorAll('input').forEach(i => { if (i.type === 'checkbox') { if (i.checked) i.setAttribute('checked', ''); else i.removeAttribute('checked'); } else i.setAttribute('value', i.value); });
    document.querySelectorAll('select').forEach(s => [...s.options].forEach(o => { if (o.selected) o.setAttribute('selected', ''); else o.removeAttribute('selected'); }));
    const doc = document.documentElement.cloneNode(true);
    doc.querySelectorAll('script, link[href*="fonts.g"]').forEach(s => s.remove());
    doc.querySelector('#toasts').innerHTML = '';
    doc.querySelectorAll('.leaflet-tooltip, .leaflet-popup').forEach(e => e.remove());
    return '<!doctype html>\n' + doc.outerHTML;
  });
  html = html.replace(/src="([^"]+)"/g, (m, u) => { const k = u.replace(/&amp;/g, '&'); return tileMap[k] ? `src="/tiles/${tileMap[k]}"` : m; });
  html = html.replace('</head>', '<link rel="stylesheet" href="/fonts/fonts.css"><style id="video">*,*::before,*::after{transition:none!important;animation:none!important;caret-color:transparent}</style></head>');
  fs.writeFileSync(file, html);
  const left = (html.match(/src="https?:[^"]+"/g) || []).length;
  console.log(file, (html.length / 1024).toFixed(0) + 'KB', 'remote src left:', left);
}

(async () => {
  const browser = await chromium.launch();
  // 1. après placement automatique
  const pa = await newPage(browser);
  await pa.click('#btnAuto'); await pa.waitForTimeout(600);
  await pa.click('#aRun'); await pa.waitForTimeout(1200);
  await pa.evaluate(() => document.getElementById('dlgResult').close());
  await pa.evaluate(() => fitAll()); await pa.waitForTimeout(1500);
  const v = await pa.evaluate(() => ({ c: [map.getCenter().lat, map.getCenter().lng], z: map.getZoom() }));
  await setView(pa, v);
  const after = await annotate(pa);
  await serialize(pa, 'snaps/after.html');
  // 2. vue Parcours (même état)
  await pa.click('#viewParcours'); await pa.waitForTimeout(1200);
  await serialize(pa, 'snaps/parcours.html');
  // 3. avant placement, même cadrage
  const pb = await newPage(browser);
  await setView(pb, v);
  const before = await annotate(pb);
  await serialize(pb, 'snaps/before.html');
  fs.writeFileSync('data/manifest.json', JSON.stringify({ view: v, after, before }, null, 1));
  console.log('links', after.links.length, 'dots', after.dots.length, 'pins', after.pins.length, 'tiles', Object.keys(tileMap).length);
  console.log('same pins pos:', after.pins.every((p, i) => before.pins[i] && before.pins[i].loc === p.loc && Math.abs(before.pins[i].p[0] - p.p[0]) < .5));
  await browser.close();
})();
