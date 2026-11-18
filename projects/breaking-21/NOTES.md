# Breaking 21 in the 200 (Nov 2026)

**Title (YouTube Shorts / TikTok):** Why Breaking 21 Seconds in the 200 Changes Everything ⏱️
**Alternates:**
- Sub-21 Is the Hardest Milestone in Sprinting — Here's Why
- I Broke 21 in the 200… and Never Went Back

**Thumbnail** (3:4, 1080×1440): `exports/thumbnails/breaking_21_thumb.jpg`, made from the NCAA photo with "SUB 21" by `thumbnail.py`.

## v2: house style (Yohan Blake / Tebogo)
- **Owner's note:** he rejected the neon theme. v2 uses the default house style.
  - No neon graphics and no "epic" transition/sound overrides.
  - Graphics: a name tag, keywords and stamps on almost every beat, boards, the scoreboard, a counter, a stopwatch, and a closing poll.
  - Sound: auto transitions with only 3 quiet whooshes.
- **Full screen:** 3 shots — the hook photo, the "SUB 21" turn (hit), and the "hardest milestone" callback (hit). The only full-screen-sharp sources are the two NCAA photos; the race streams are upscaled and stay in the split.
- **Export:** `exports/breaking_21_tiktok_v2.mp4` (crf 20, 76.7 MB).

## Inputs
These came from a Dropbox folder and are not committed.
- `talking.mov`: 4K, 74 s.
- `race_may24.mov`: 3710×1886, a phone recording of the outdoor meet (Heat 1).
  - It's color-corrected and sharpened into `broll/may_cc.mp4` (raw 12–32 s; `eq` contrast 1.12, saturation 1.18, gamma 0.94, plus `unsharp`).
- `race_dec24.mov`: **444×782**, a Runnerspace indoor stream ("Top Finisher 20.79").
- `race_apr25.mp4`: **628×360**, the FloTrack Albuquerque stream (Don Kirby Elite Invitational, "E. Brown 20.68").
- `photo1.jpg` and `photo2.jpg`: 1728×2160, NCAA meet, bib 420.

## Steps
1. **Crop the face:** crop 2000×1778 at (860, 330), scale to 1440×1280.
2. **Cut a slip:** remove "under 26 or" (24.10–25.48 s), so the line reads "running under 21 seconds".
3. **Tighten:** 72.8 s → 68.0 s.
4. **Fix the transcript:** merge "46, seven" → 46.7, "10, eight" → 10.8 and "10, seven" → 10.7.
5. **AI-upscale the two low-res streams** (`editor/upscale.py`, 4× then to 1920 wide, 30 fps):
   - `dec_fin` (21–26 s) and `dec_close` (29.5–37 s).
   - `apr_fin` (19–23.5 s) and `apr_close` (32–45.5 s).
   - These are only ever used in the split, never full screen.
6. **Crop out chopped stream overlays:**
   - `dec_close` uses crop `[1920,760,0,0]`, which drops the Runnerspace lower third. 20.79 is shown in our own counter instead.
   - `apr_close` at 39.7 s uses crop `[1440,1100,480,0]`, which drops the FloTrack box. At 51.7 s the FloTrack results box is kept in full (focus 0).
7. **Full-screen shots:** only the NCAA photos (the hook, and the "SUB 21" hit).
8. **Transitions and sound:** `transition_style: "epic"` and `transition_sfx: true`.
9. **Export:** two-pass at 10.5 Mbps.

## Data notes (all real)
- **20.69 and 21.12** (Heat 1, May 2024 outdoor): confirmed by the owner, because the real scoreboard is too blurry to read. They're shown on our `scoreboard` graphic. The scoreboard displays "Cameron Frank"; the owner gave the full name, Cameron Franklin.
- **20.79:** from the Runnerspace graphic.
- **20.68:** from the FloTrack results box.
- **The owner's own claims:** sub 21, sub 11, sub 46; 46.7 → 47s–48s; 10.8/10.7 → 11s; slowest since breaking 21 is 21 flat; first broke 21 "three, four years ago". These are as he said them.
