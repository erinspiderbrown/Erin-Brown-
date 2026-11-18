// node render.js out_dir name : renders designs A and B in 9:16 (1080x1920) and 3:4 (1080x1440); 2x then downscaled
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
const [out, name, only] = process.argv.slice(2);
const D = require('./layouts.json');
(async () => {
  const b = await chromium.launch();
  for (const [k, L] of Object.entries(D)) {
    if (only && !k.startsWith(only)) continue;
    const p = await b.newPage({ viewport: { width: L.W, height: L.H }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(__dirname, 'thumb.html') + '#' + encodeURIComponent(JSON.stringify(L)));
    await p.waitForTimeout(500);
    const png = path.join(out, `big_${k}.png`); await p.screenshot({ path: png });
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', png, '-vf', `scale=${L.W}:${L.H}:flags=lanczos`, '-q:v', '1', path.join(out, `${name}_${k}.jpg`)]);
    require('fs').unlinkSync(png);
  }
  await b.close();
})();
