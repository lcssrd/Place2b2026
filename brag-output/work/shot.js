// Capture rapide d'une URL locale : node shot.js <url> <out.png>
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(process.argv[2]); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  await p.screenshot({ path: process.argv[3] }); await b.close();
})();
