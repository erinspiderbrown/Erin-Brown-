// node render.js out_dir name -> <name>_viral_thumb_916.jpg (1080x1920) + <name>_viral_thumb.jpg (1080x1440); 2x render then downscale
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
const [out, name] = process.argv.slice(2);
const mask = 'linear-gradient(to bottom, #000 62%, transparent 92%)';
const lines = (t1, t2, t3, s1, s2, s3) => [{ text: '15 YEARS OLD', cls: 'g', top: t1, size: s1 }, { text: '10.28', cls: 'w', top: t2, size: s2 },
                                         { text: "AFRICA'S NEXT STAR?", cls: 'g', top: t3, size: s3 }];
const layouts = {
  '_916': { W: 1080, H: 1920, lines: lines(255, 395, 712, 150, 330, 100),
            subject: { src: 'subject.png', left: -80, top: 815, width: 1240, mask }, polaroid: { src: 'polaroid_photo.png', left: 26, top: 1330, width: 340, rot: -8 } },
  '':     { W: 1080, H: 1440, lines: lines(36, 172, 470, 140, 310, 92), 
            subject: { src: 'subject.png', left: -30, top: 560, width: 1140, mask }, polaroid: { src: 'polaroid_photo.png', left: 16, top: 990, width: 290, rot: -8 } },
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
