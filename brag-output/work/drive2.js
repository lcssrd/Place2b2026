// Suite du parcours réel : placement automatique, vues Parcours et Tableau de bord.
const { chromium } = require('playwright');
const fs = require('fs');
const APP = 'file:///home/user/Place2b2026/Place2b2026.html';
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(APP);
  await page.waitForTimeout(800);
  // recharge l'état obtenu par drive.js (même format qu'une sauvegarde .json de l'application)
  const state = fs.readFileSync('data/state-loaded.json', 'utf8');
  await page.evaluate(txt => loadText(txt), state);
  await page.waitForTimeout(2500);
  const est = await page.evaluate(() => Object.values(S.times).flatMap(o => Object.values(o)).filter(v => v && v.est).length);
  console.log('estimated times:', est);
  await page.screenshot({ path: 'shots/02-reloaded.png' });
  await page.click('#btnAuto');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'shots/03-auto-dialog.png' });
  await page.click('#aRun');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'shots/04-result.png' });
  await page.evaluate(() => document.getElementById('dlgResult').close());
  await page.check('input[data-layer="links"]');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: 'shots/05-placed-links.png' });
  fs.writeFileSync('data/state-placed.json', await page.evaluate(() => JSON.stringify(S)));
  await page.click('#viewParcours');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: 'shots/06-parcours.png' });
  await page.click('#viewDash');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: 'shots/07-dash.png' });
  await browser.close();
})();
