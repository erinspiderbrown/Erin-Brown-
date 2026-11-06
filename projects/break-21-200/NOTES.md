# "How to break 21 in the 200" (Nov 2026)

**Title (YouTube Shorts / TikTok):** How to Break 21 Seconds in the 200 (The Race Model Nobody Teaches)
Alternates:
- Stuck at 21.3 in the 200? You're Running It Wrong
- The 200 Is Just a Short 400… Run It Like One to Break 21
- Stop Going Out Hard in the 200. Do This to Break 21

Thumbnails: `exports/thumbnails/break21_200_thumb.jpg` (3:4) and `break21_200_thumb_916.jpg` (9:16), with no text and no talking-head face (per the owner's request).
- Top: the owner clear of the field down the home straight at the WAC Championships final (broadcast frame, neural 2x upscale, scoreboard cropped out).
- Bottom: the owner in the white GCU top at the WAC indoor meet (native 1080×1920 frame).
- Built by `editor/thumb.py` from `thumb_spec.json`.

## Footage
The owner's talking head is 4K; his six race and training clips came in at mixed quality:

| clip | what | source res | use |
|---|---|---|---|
| 1 | training, block starts | 960×540 | neural 2x → 1920×1080, split only |
| 2 | GCU race (screen-recorded repost) | ~1080×552 picture inside a 1080×1920 frame | cropped to the picture, neural 2x → 2160×1104, split only |
| 3 | WAC indoor, white GCU top | 1080×1920 | full-screen |
| 4 | Arizona night race | 1280×720 | neural 2x → 2560×1440, split only |
| 5 | NCAA track (UAMS Health board) | 1080×1920 (rotated) | full-screen |
| 6 | WAC Championships final | 1280×720 | neural 2x → 2560×1440, split only |

- **Upscaling:** `editor/upscale.py` runs a light denoise, FSRCNN x2 neural super-resolution, then fine sharpening. It is visibly cleaner than a plain resize, but it can't add detail the camera didn't capture: the out-of-focus foreground in clip 2 stays soft. Per the house rules, the sub-1080p clips go in the bottom half only. Full-screen uses the native vertical 1080p clips (3, 5).
- **Clip 6 scoreboard:** the broadcast graphic reads "WAC CHAMPIONSHIPS · FINAL · MEN'S 200 HURDLES". The clip carries no on-screen label or time in the edit, so nothing claims which race it is.

## Facts on screen
- **Race model (`race200` graphic):** the owner's phases: drive the first ~45 m ("35–40 ish… some push it to 50… I get out for about 45"), chill, re-accelerate in the relay exchange zone off the curve, then come home with front-side mechanics.
- **80–110 m for the exchange zone (my interpretation):** the owner says "a 30 meter zone coming off the curve". In a 200, the third-to-fourth 4×100 takeover zone runs 80–110 m from the 200 start: World Athletics' 30 m takeover zone starts 20 m before the 100 m line. So the graphic labels the phases 0–45 DRIVE, 45–80 CHILL, 80–110 RE-ACCELERATE, 110–200 HOME. The 45 and 30 are his numbers; 80 and 110 follow from the rule.
- **Captions:** "21 1, 21 2…" are written as 21.1, 21.2…, and "21 for range" as 21.4 (what he means). "20 point" is written as "20-POINT" (a 20.xx time).
- No other stats are added. The `bubbles` are generic illustrative requests, not real comments.

## Structure (Yohan Blake method)
1. **Hook:** full-screen on the NCAA track; "SUB 21 IN THE 200?"; "THE SAUCE" stamp; request bubbles.
2. **Problem:** stuck at 21.1–21.4, stamped "DOING IT WRONG".
3. **Context:** strategy → race model → execution (`flow`), then a board of the 400's phases: accelerate, chill, re-accelerate, come home.
4. **Turn:** "ask me how I know… I ran a 400", full-screen (hit), then "SAME PHASES. FASTER."
5. **The mistake:** "BIGGEST MISTAKE", "GET OUT HARD → HOLD ON", "NO STRATEGY", "NO PHASES".
6. **How to run sub 21:** full-screen (hit), training footage for "MUSCLE MEMORY", then the race model built over three passes (drive/chill → exchange zone → home), with "SPEED THE ARMS UP", "LEG FREQUENCY ↑", "20-POINT. EVERY TIME" and "NO SWIMMING".
7. **Callback:** full-screen "HOPE & PRAY?" and "GOOD LUCK", then a poll: "WHAT'S YOUR 200 PR? SUB 21 / 21-POINT".
