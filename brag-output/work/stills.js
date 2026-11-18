// Images fixes de contrôle : node stills.js 0.5 3.2 ...
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.goto('http://127.0.0.1:8765/comp.html');
  await p.evaluate(() => window.ready);
  for (const a of process.argv.slice(2)) {
    const t = +a;
    await p.evaluate(t => window.render(t), t);
    await p.screenshot({ path: `shots/t${t.toFixed(2)}.png` });
  }
  await b.close();
})();
