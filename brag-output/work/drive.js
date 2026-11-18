// Pilote la vraie application avec les données fictives, et sauvegarde l'état.
const { chromium } = require('playwright');
const fs = require('fs');
const APP = 'file:///home/user/Place2b2026/Place2b2026.html';
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error') console.log('console:', m.text().slice(0, 200)); });
  await page.goto(APP);
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'shots/00-empty.png' });
  await page.setInputFiles('#fileStages', 'data/lieux-de-stage.csv');
  await page.waitForTimeout(1500);
  await page.setInputFiles('#fileStudents', 'data/etudiants.csv');
  // attend la fin du pipeline (géocodage + trajets)
  const t0 = Date.now();
  for (;;) {
    await page.waitForTimeout(2000);
    const st = await page.evaluate(() => ({ prog: !document.querySelector('#progress').classList.contains('hidden'), lbl: document.querySelector('#progLbl').textContent, num: document.querySelector('#progNum').textContent, busy }));
    console.log(((Date.now() - t0) / 1000).toFixed(0) + 's', JSON.stringify(st));
    if (!st.prog && !st.busy) break;
    if (Date.now() - t0 > 240000) break;
  }
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'shots/01-loaded.png' });
  fs.writeFileSync('data/state-loaded.json', await page.evaluate(() => JSON.stringify(S)));
  await browser.close();
})();
