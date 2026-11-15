// node render.js out_dir name -> <name>_viral_thumb_916.jpg (1080x1920) + <name>_viral_thumb.jpg (1080x1440); 2x render then downscale
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
const [out, name] = process.argv.slice(2);
const mask = 'radial-gradient(ellipse 62% 58% at 50% 46%, #000 58%, transparent 100%)';
const lines = (t1, t2, t3, s1, s2, s3) => [{ text: 'OLYMPIC CHAMP', cls: 'g', top: t1, size: s1 }, { text: 'HACKED?', cls: 'w', top: t2, size: s2 },
                                         { text: "BY TEAMMATE'S BROTHER", cls: 'g', top: t3, size: s3 }];
const layouts = {
  '_916': { W: 1080, H: 1920, lines: lines(270, 420, 720, 140, 282, 88),
            subject: { src: 'subject.png', left: -100, top: 900, width: 1280, mask }, polaroid: { src: 'polaroid_photo.png', left: 30, top: 1395, width: 330, rot: -8 } },
  '':     { W: 1080, H: 1440, lines: lines(40, 180, 490, 140, 290, 86),
            subject: { src: 'subject.png', left: -60, top: 600, width: 1200, mask }, polaroid: { src: 'polaroid_photo.png', left: 18, top: 1010, width: 290, rot: -8 } },
};
(async () => {
  const b = await chromium.launch();
  for (const [k, L] of Object.entries(layouts)) {
    const p = await b.newPage({ viewport: { width: L.W, height: L.H }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(__dirname, 'thumb.html') + '#' + encodeURIComponent(JSON.stringify(L)));
    await p.waitForTimeout(400);
    const png = path.join(out, `big${k}.png`); await p.screenshot({ path: png });
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', png, '-vf', `scale=${L.W}:${L.H}:flags=lanczos`, '-q:v', '1', path.join(out, `${name}_viral_thumb${k}.jpg`)]);
  }
  await b.close();
})();
