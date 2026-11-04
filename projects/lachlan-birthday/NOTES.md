# Lachlan Kennedy birthday (Nov 2026)

## Inputs (Dropbox folder, not committed)
- `raw/talking_head.mov`: 4K, 75.0 s.
- `raw/photo1.jpg` (1170×1531, school photo), `raw/photo2.jpg` (1640×2048, Commonwealth Games), `raw/photo3.webp` (1200×1200, Aus Champs).
- `raw/clip_608p.mp4`: Summer Series men's 100 m final. **1080×608, below the 1080p rule.** Used in the split (with sharpening), never full-screen, because it's the only race footage.
- `raw/photo_720p.jpg`: 1280×720 celebration photo. **Below the 1080p rule, so not used.**

## Steps
1. Crop the face to 2000×1778 at (820, 300), scale to 1440×1280, then run `tighten.py` (75.0 s → 66.7 s).
2. Transcript fixes: "top -end" → "top-end"; the sign-off "flower bring it" → "flower bringing".
3. Race crop `[1080,530,0,16]` removes the Summer Series logo and the bottom graphics bar.
4. Render with `python3 ../../editor/build.py plan.json`, then re-encode at `-crf 20 -preset slow` (the first render was 100.6 MB).

## Notes
- New motion kind `birthday`: number candles light up, confetti, "HAPPY BIRTHDAY" plus the name. Hand-built, no AI.
- "23" comes from the owner's script. No race times are shown on screen.
