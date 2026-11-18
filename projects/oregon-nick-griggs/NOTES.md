# Oregon / Nick Griggs: "Is it a double standard?" (Nov 18, 2026)

## Title
**Recommended:** Oregon Signed a Former Pro… Double Standard? 👀
- Alt: Jerry Schumacher Recruited an Ex-Puma Pro to College Track
- Alt: Coaches Hated This… Until Oregon Did It

Caption:
Oregon Signed a Former Pro… Double Standard? 👀 #trackandfield #oregonducks #NCAA #NIL #NickGriggs
Photos: Wikimedia Commons (Habst, Cacophony)

## Style
v2 cinematic (CLAUDE.md, "Default editing method"):
- No stickers, name tags or poll. Big moments are cinefx cards (`fx.json`).
- Cine captions with gold emphasis; B-roll graded; mostly hard cuts.
- Two quiet hits, at 31.5 s and 79.8 s.

## Inputs (Dropbox, not committed)
- `raw/talking_head.mov`: 4K, 79.2 s.
- `raw/coach_720p.mp4`: Jerry Schumacher interview. **720×1280, below the 1080p rule.**
  - Its burned-in caption ("OREGON HEAD COACH JERRY SCHUMACHER ON SIGNING IRISH ATHLETE NICK GRIGGS, DISCUSSING DIFFERENCE BETWEEN PRO RUNNER VS NIL") is cropped off (crop 720×640 at y=60).
  - Scaled to 1440×1280 (lanczos + unsharp) for the top speaker slot.
  - Not AI-upscaled: Real-ESRGAN on CPU would take about 1.7 h for 26 s.
  - The caption words are recreated at the bottom as `card.html` → `work/img/card2.png` while he speaks (owner's request).
- `raw/photo1.jpg`: Oregon "Signed" graphic, 1206×1506.
- `raw/photo_740.jpg`: 740×740, **below 1080p, not used.**

## Guest soundbite
- Coach clip 0–28 s, with his long pauses (13.9–15.0 and 19.0–20.1) cut out → 25.8 s.
- Inserted right after the owner's "as long as it's a part of the NCAA rules, it's all good" (37.75–63.55 in the A-roll).
- Loudness matched (+0.1 dB). His captions are merged into `words_final.json`.
- Not used: the part about Nick's brother's death.

## Transcript fixes
- "rabbit" → "rabid".
- "y'all".
- f*ck censored in captions only.

## Facts on screen (checked)
- Nick Griggs: former Puma pro, signed with Oregon with 3 years of NCAA eligibility, age 21. Sources: LetsRun, The Stride Report, Run Republic, Irish Times. The coach also says "three years left" in the full clip.
- "FOREIGN + PRO" reflects the owner's point; Griggs is from Newmills, Northern Ireland and runs for Ireland.

## B-roll (CC BY-SA, credit needed)
- `hay*.jpg`: "Day 1 at the 2024 United States Olympic Trials (track and field)" by Habst, CC BY-SA 4.0 (1920 px thumbnails).
- `haypano.jpg`: "HaywardFieldPano" by Cacophony, CC BY-SA 3.0. It shows the old, pre-renovation Hayward.

## Exports
- `exports/oregon_nick_griggs_hq.mp4`: Git LFS, 155 MB, SSIM 0.982 vs master.
- `exports/oregon_nick_griggs_phone.mp4`: 57 MB.

## Posted (Nov 18, 2026)
- Cover: the owner's own thumbnail (`exports/thumbnails/reference/oregon_nick_griggs_owner_thumb.png`), added as the first 0.1 s via `editor/social_cover.sh`.
- YouTube Short (The Erin Brown, public): https://www.youtube.com/watch?v=qtDpzvrssaY
- Instagram trial reel (@e.diamondz, MANUAL): https://www.instagram.com/reel/Df5cHVlivWG/
- TikTok (Erin Spider Brown, public): delivered; vidIQ returned no post URL.
- Facebook: the Page reconnect failed (Facebook didn't share the Page with vidIQ). The owner is posting it manually.
