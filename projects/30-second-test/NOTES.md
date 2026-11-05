# 30-second test (Nov 2026)

A storytelling edit: first time in spikes this season, a 30-second test run in 281 m last year vs 283 m today.

## Inputs
These came in a Dropbox folder and are not committed.
- `talking.mov`: 4K, 73.3 s.
- `test300.mov`: today's test, filmed on a phone. The owner runs in neon shorts, and the clear finish is at 24–31 s. **It is 1280×720, below the 1080p rule.** The owner explicitly asked for it, so it's used (`skip_res_check`). It's mostly in the split; one full-screen shot (35.3–39.4 s) is visibly softer.
- `train_jun01.mov`: 4K at 120 fps. Used for the bend-sprint slow motion and the crouch/recovery B-roll.
- `train_jun13.mov`: 1126×2160 at 120 fps. A wide pan past the GCU banners.

## Steps
1. **Crop the face:** crop 2430×2160 at (680, 0), scale to 1440×1280 at 30 fps, then run `tighten.py` (73.3 s → 68.8 s).
2. **Fix the transcript:** merge "21 .4," → "21.4," and "20 .8," → "20.8,"; caption "shit" as "SH*T".
3. **Cut the B-roll** (`broll/`, built with ffmpeg):
   - `curve_slo`: jun01 0–4.6 s at `setpts=4*PTS`, giving real 4× slow motion from 120 fps.
   - `curve_rt`: jun01 0–8 s.
   - `crouch`: jun01 48–67 s.
   - `hurdles`: jun01 16–25 s.
   - `gcu`: jun13.
   - `gcu_slo`: jun13 9–15 s at 3×.
4. **Neon look (owner request):**
   - Captions use `caption_colors` neon pink `#FF2BD6` and neon yellow `#E6FF00` instead of the red/yellow house colors.
   - `accent` is `#FF2BD6`.
   - New `neon` and `battery` motion graphics.
5. **Export:** the build output was 121 MB even at `-crf 20`, so it was re-encoded two-pass at 10.5 Mbps (91.8 MB). The audio is copied.

## Data notes
- **281 m and 283 m:** the owner's distances for the 30-second test, last year vs this year.
- **First-200 splits:** 21.4–21.5 is this year's *plan*; 20.8–20.9 is last year's all-out pace. These are what he said, not measured splits from today.
- **45:** his 400m. It's shown as "45", exactly as said.
- **Battery levels:** illustrative ("died" vs "gas left"); no percentages are shown.

## v2: today's yellow-shorts footage as the running highlight
- **Owner's note:** the running highlights must be today's test (yellow shorts), not the June training clips (orange shorts).
- **What changed:**
  - Every running shot now comes from `test300.mov`.
  - `t_slo.mp4` is test300 23.5–31.2 s at 2× slow motion (`minterpolate`, mci, 60 fps, then `setpts=2*PTS`).
  - The June clips stay only as behind-the-scenes B-roll: the crouch, the empty hurdles and the GCU pan.
- **Why most running shots are in the split:** the clip is 720p and the owner is small in the frame. So only the hook (0–2.85 s) and the 283 m reveal (35.3–39.4 s) are full screen. Split shots of the run are cropped in on him (crop 960×540 at (83, 126)).
- **"THAT'S ME" spotlights:** added on both full-screen shots so viewers can find him.
- **Export:** `exports/30_second_test_tiktok_v2.mp4`.
