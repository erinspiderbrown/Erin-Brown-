// node render.js out_dir  -> felix_tarmoh_viral_thumb_916.jpg (1080x1920) + felix_tarmoh_viral_thumb.jpg (1080x1440); rendered at 2x then downscaled
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
const out = process.argv[2];
const layouts = {
  '_916': { W: 1080, H: 1920, t1: 250, s1: 175, t2: 405, s2: 340, t3: 755, fx: 150, fy: 900, fw: 1150, px: 26, py: 1290, pw: 360 },
  '':     { W: 1080, H: 1440, t1: 40,  s1: 160, t2: 180, s2: 300, t3: 478, fx: 230, fy: 668, fw: 1000, px: 20, py: 900,  pw: 330 },
};
(async () => {
  const b = await chromium.launch();
  for (const [k, L] of Object.entries(layouts)) {
    const p = await b.newPage({ viewport: { width: L.W, height: L.H }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(__dirname, 'thumb.html') + '#' + encodeURIComponent(JSON.stringify(L)));
    await p.waitForTimeout(400);
    const png = path.join(out, `big${k}.png`); await p.screenshot({ path: png });
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', png, '-vf', `scale=${L.W}:${L.H}:flags=lanczos`, '-q:v', '1', path.join(out, `felix_tarmoh_viral_thumb${k}.jpg`)]);
  }
  await b.close();
})();
