const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file:///home/user/Place2b2026/Place2b2026.html'); await p.waitForTimeout(800);
  await p.evaluate(txt => loadText(txt), fs.readFileSync('data/state-loaded.json', 'utf8')); await p.waitForTimeout(1500);
  const out = await p.evaluate(() => S.students.map(st => ({ nom: st.nom, car: st.car, city: st.g1 && st.g1.city, lim: limitFor(st),
    opts: S.stages.map(x => ({ x, b: best(st, x.loc) })).filter(o => o.b).sort((a, c) => a.b.min - c.b.min)
      .filter((o, i, A) => A.findIndex(z => z.x.loc === o.x.loc) === i).slice(0, 6).map(o => `${o.b.min}m/${o.b.km}km ${S.locations[o.x.loc].ville}`) })));
  for (const s of out) console.log(s.nom.padEnd(18), s.car ? 'car ' : 'nocar', (s.city || '').padEnd(22), s.opts.join(' | '));
  await b.close();
})();
