# Kendall Ellis 4x400 scratch (Nov 2026)

## Inputs (Dropbox folder, not committed)
- `raw/talking_head.mov`: 4K, 67.5 s.
- `raw/screen1.mov`: 2018 NCAA women's 4x400, USC anchor leg. **1206×654 screen recording, below the 1080p rule.**
- `raw/screen2.mov`: 2024 U.S. Trials women's 400 m final (49.46). **1206×658, below the 1080p rule.**
- Both are the only race footage, so they're used in the split only (cropped `[1100,h,0,0]` to drop the broadcast clock box), never full-screen.
- `raw/shot1-4.png`: the X post and ESPN article screenshots (1206×2622). They're cropped and padded onto matching black or white canvases (`work/img/`) so the push-in never cuts off text.
- `raw/photo1-3.jpg`: Trials emotion collage, Trials running and Paris. All at least 1080 px on the short side.

## Steps
1. Crop the face to 2000×1778 at (863, 250), scale to 1440×1280, then run `tighten.py` (67.5 s → 63.6 s).
2. Render with `python3 ../../editor/build.py plan.json`, then re-encode at `-crf 20 -preset slow`.

## Facts on screen (checked)
- 50.05: Ellis's anchor split, 2018 NCAA. USC won by 0.07 s (NCAA.com, SI, NBC).
- 49.46: her 2024 U.S. Trials 400 m win, read off the broadcast clock in `screen2.mov`.
- "4 MINUTES before call time": her own X post and ESPN's report.
- "2024 U.S. 400M CHAMPION": ESPN calls her "the reigning U.S. 400-meter champion".
- No numbers are shown for "you're faster than them"; that is the owner's opinion.
