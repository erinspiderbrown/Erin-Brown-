// Render one animated data graphic to a transparent .mov (PNG codec, alpha) + events JSON for SFX.
// usage: node render.js spec.json out.mov
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');

(async () => {
  const [specPath, out] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const FPS = 30, frames = Math.round(spec.dur * FPS);
  const tmp = fs.mkdtempSync(path.join(path.dirname(out), 'frames-'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1200 } });
  await page.goto('file://' + path.join(__dirname, 'gfx.html'));
  const info = await page.evaluate(s => window.setup(s), spec);
  await page.setViewportSize({ width: info.w, height: info.h });
  for (let i = 0; i < frames; i++) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    await page.screenshot({ path: path.join(tmp, String(i).padStart(4, '0') + '.png'), omitBackground: true });
  }
  await browser.close();
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(tmp, '%04d.png'),
                          '-c:v', 'png', '-pix_fmt', 'rgba', out]);
  fs.rmSync(tmp, { recursive: true, force: true });
  fs.writeFileSync(out.replace(/\.mov$/, '.json'), JSON.stringify(info));
  console.log(JSON.stringify(info));
})().catch(e => { console.error(e); process.exit(1); });
