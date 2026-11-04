# Charlotte Ehioghae (Nov 2026)

A reference project showing the full house style.

## Inputs (not committed)
- `raw/talking_head.mov`: 4K, delivered as a Dropbox link.
- `raw/race.mp4`: the race footage. Instagram download, **720p, below the 1080p rule**. It was used with sharpening because it was the only race footage.
- `raw/photo_finish.jpg` and `raw/photo_headtouch.jpg`: photos. A third photo at 620×413 was excluded.

## Steps
1. Crop the talking head to 2000×1778 at (882, 382), scale to 1440×1280, then run `tighten.py` (74.1 s → 68.2 s).
2. Fix the transcript by hand:
   - Name: Ehioghae.
   - Numbers: "22 .8" → 22.8, "11 7" → 11.7, "hundred" → 100.
3. Render with `python3 ../../editor/build.py plan.json`.

## Notes
- "23 mid / 23 high" are shown as 23.5 / 23.8. That's an interpretation, labelled on screen as "Usual · 23 mid".
- Race footage crop `[720,1100,0,0]` removes a source tag in the bottom corners.
