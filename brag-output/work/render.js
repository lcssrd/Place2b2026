// Rendu image par image (fonction pure du temps) -> ffmpeg. Image 0 = affiche.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const FPS = 30, DUR = 22.0, POSTER_T = 10.75;
const total = Math.round(DUR * FPS);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.goto('http://127.0.0.1:8765/comp.html');
  await p.evaluate(() => window.ready);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(FPS), 'video-only.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < total; i++) {
    const t = i === 0 ? POSTER_T : i / FPS;
    await p.evaluate(t => window.render(t), t);
    const buf = await p.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log(`frame ${i}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await p.evaluate(t => window.render(t), POSTER_T);
  await p.screenshot({ path: '../brag.jpg', type: 'jpeg', quality: 92 });
  await b.close();
  console.log('done', ((Date.now() - t0) / 1000).toFixed(0) + 's');
})();
