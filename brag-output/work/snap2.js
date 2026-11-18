// Instantanés de la vraie app pour la v2 : vue d'ensemble, sélection d'un étudiant, aperçus de trajet.
const { chromium } = require('playwright');
const fs = require('fs'); const crypto = require('crypto');
const APP = 'file:///home/user/Place2b2026/Place2b2026.html';
const STUDENT = 'BONNET Manon';
const tileMap = {};
const serializeFn = () => {
  document.querySelectorAll('input').forEach(i => { if (i.type === 'checkbox') { if (i.checked) i.setAttribute('checked', ''); else i.removeAttribute('checked'); } else i.setAttribute('value', i.value); });
  document.querySelectorAll('select').forEach(s => [...s.options].forEach(o => { if (o.selected) o.setAttribute('selected', ''); else o.removeAttribute('selected'); }));
  const doc = document.documentElement.cloneNode(true);
  doc.querySelectorAll('script, link[href*="fonts.g"]').forEach(s => s.remove());
  doc.querySelector('#toasts').innerHTML = '';
  return '<!doctype html>\n' + doc.outerHTML;
};
async function serialize(page, file) {
  let html = await page.evaluate(serializeFn);
  html = html.replace(/src="([^"]+)"/g, (m, u) => { const k = u.replace(/&amp;/g, '&'); return tileMap[k] ? `src="/tiles/${tileMap[k]}"` : m; });
  html = html.replace('</head>', '<link rel="stylesheet" href="/fonts/fonts.css"><style id="video">*,*::before,*::after{transition:none!important;animation:none!important;caret-color:transparent}</style></head>');
  fs.writeFileSync(file, html);
  console.log(file, (html.length / 1024).toFixed(0) + 'KB', 'remote src left:', (html.match(/src="https?:[^"]+"/g) || []).length);
}
async function setView(page, v) {
  await page.evaluate(v => { map.setView(v.c, v.z + 1, { animate: false }); map.setView(v.c, v.z, { animate: false }); }, v);
  await page.waitForTimeout(2500);
  await page.waitForFunction(() => [...document.querySelectorAll('img.leaflet-tile')].every(i => i.complete));
  await page.waitForTimeout(600);
}
const annotate = page => page.evaluate(() => {
  const same = (a, b) => Math.abs(a.lat - b.lat) < 1e-9 && Math.abs(a.lng - b.lng) < 1e-9;
  const P = ll => { const p = map.latLngToLayerPoint(ll); return [p.x, p.y]; };
  const out = { dots: [], pins: [] };
  for (const k of ['a1', 'a2', 'focus']) LG[k].eachLayer(ly => { if (!ly.getLatLng) return; const g = ly.getLatLng(); const st = S.students.find(s => (s.g1 && same(s.g1, g)) || (s.g2 && same(s.g2, g))); if (st && ly._path) { ly._path.dataset.sid = st.id; out.dots.push({ sid: st.id, p: P(g) }); } });
  LG.stages.eachLayer(m => { const g = m.getLatLng(); const lk = Object.keys(S.locations).find(k => same(S.locations[k], g)); m._icon.dataset.loc = lk; out.pins.push({ loc: lk, n: (D.byLoc.get(lk) || []).length, p: P(g), name: S.locations[lk].etab }); });
  return out;
});
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('response', async r => { const u = r.url(); if (/wmts|arcgisonline/.test(u) && r.status() === 200 && !tileMap[u]) { try { const b = await r.body(); const f = crypto.createHash('md5').update(u).digest('hex') + '.png'; fs.writeFileSync('tiles/' + f, b); tileMap[u] = f; } catch (e) {} } });
  await page.goto(APP); await page.waitForTimeout(800);
  await page.evaluate(txt => loadText(txt), fs.readFileSync('data/state-loaded.json', 'utf8')); await page.waitForTimeout(1500);
  await page.evaluate(() => { map.flyTo = function () { return this; }; map.flyToBounds = function () { return this; }; });
  const man = JSON.parse(fs.readFileSync('data/manifest.json', 'utf8'));
  const V0 = man.view;
  const sid = await page.evaluate(n => S.students.find(s => s.nom === n).id, STUDENT);
  // vue d'ensemble
  await setView(page, V0);
  const ov = await annotate(page);
  ov.rowRect = await page.evaluate(id => document.querySelector(`#list .row[data-id="${id}"]`).getBoundingClientRect().toJSON(), sid);
  await serialize(page, 'snaps2/ov.html');
  // étudiant sélectionné, même cadrage
  await page.evaluate(id => select('student', id), sid); await page.waitForTimeout(600);
  await setView(page, V0);
  const pt = await page.evaluate(id => { const st = D.student.get(id); return [st.g1.lat, st.g1.lng]; }, sid);
  await serialize(page, 'snaps2/sel0.html');
  // zoom 11 centré pour cadrer Pavilly, Rouen, Yvetot
  const V1 = { c: [pt[0] - 0.005, pt[1] + 0.035], z: 11 };
  await setView(page, V1);
  await serialize(page, 'snaps2/sel1.html');
  const geo = await page.evaluate(v => { const c0 = map.project(L.latLng(v.c), v.z - 1); return { size: map.getSize() }; }, V1);
  // aperçus de trajet au survol
  const opts = await page.evaluate(() => [...document.querySelectorAll('#optList .opt')].map((o, i) => ({ i, l: o.dataset.pvL, txt: o.innerText.replace(/\s+/g, ' ').slice(0, 90) })));
  console.log(opts.slice(0, 6));
  const scrollTop = await page.evaluate(() => { const b = document.querySelector('#detailBody'); const t = document.querySelector('#optList').offsetTop; b.scrollTop = 1e6; return b.scrollTop; });
  console.log('scrollTop', scrollTop);
  const pv = {};
  for (const [name, idx] of [['pv2', 2], ['pv3', 6]]) {
    await page.evaluate(() => { const b = document.querySelector('#detailBody'); b.scrollTop = 1e6; });
    const sel = `#optList .opt:nth-child(${idx + 1}) .opt-main`;
    await page.hover(sel); await page.waitForTimeout(700);
    pv[name] = await page.evaluate(i => { const o = document.querySelectorAll('#optList .opt')[i]; const r = o.getBoundingClientRect().toJSON(); return { idx: i, rect: r, scroll: document.querySelector('#detailBody').scrollTop, label: document.querySelector('.pv-label')?.innerText }; }, idx);
    await serialize(page, `snaps2/${name}.html`);
    await page.screenshot({ path: `shots/live-${name}.png` });
    await page.mouse.move(1900, 1070); await page.waitForTimeout(300);
  }
  const selRect = await page.evaluate(() => ({ detail: document.querySelector('#detail').getBoundingClientRect().toJSON() }));
  fs.writeFileSync('data/manifest2.json', JSON.stringify({ V0, V1, sid, pt, ov, pv, opts, selRect }, null, 1));
  console.log(JSON.stringify(pv));
  fs.writeFileSync('data/tiles.json', JSON.stringify(tileMap, null, 1));
  await browser.close();
})();
