# California is not a top-5 sprint state (Nov 2026)

## Inputs (not committed)
- `raw/talking_head.mov`: 4K (3840×2160 after rotation), Dropbox folder link.
- `raw/photo_ca.jpg`: the owner's California high school photo. **1200×810, below the 1080p rule.** It's used in the split for one beat (12.3–15.0 s), at the owner's request; it's never used full-screen. `skip_res_check` is on only because of this photo.
- `broll/`: found B-roll from Wikimedia Commons (below). Videos are re-encoded to 1080p H.264 and photos to 2400 px on the long side. Everything is ≥1080 on the short side.

## Steps
1. Crop the talking head to 2430×2160 at (619, 0) and scale to 1440×1280. This frame is wider than Charlotte's because he leans in. Then `tighten.py`: 79.5 s → 76.4 s.
2. Transcript fixes:
   - "y 'all" → "Y'ALL".
   - "have to is" → "have too is".
   - Swears are softened in the captions only ("SH*T", "A**"). The audio is untouched. `build.py` `clean()` now keeps `*`.
   - ~56.8 s: Whisper hears "that sh*t just **all**" twice. It may be "off", so it's left as heard. **Check this.**
3. `python3 ../../editor/build.py plan.json`
4. Export. CRF 20 came out at 104 MB, so it's a two-pass encode at 9 Mbps instead: 88 MB, 76.4 s, −14.4 LUFS.

The `work`, `raw` and `broll` folders were scratch symlinks in the editing session. Re-download the sources to rebuild.

## Data (no invented numbers)
- California population: shown as **39.4 M** (US Census Bureau Vintage 2025 estimate, July 1 2025: 39,355,309). He says "damn near 40 million", which matches.
- Population bars, same source (millions): CA 39.4, TX 31.7, FL 23.5. GA 11.3 and NC 11.2 were cut so the card fits.
- "2-5 good sprinters a year", "3-4 athletes" and "2 of 40,000,000" are his own words, shown as keywords, not as stats.

## New graphic: `usmap`
`motion.html` kind `usmap`: the US map (Census boundaries via us-atlas, pre-projected) with states lighting up in time with the voice.
- Spec: `groups: [{names, label, at, dx, dy}]`, optional `cross: {names, label, at}` (red fill and X), and `title`.
- The map paths are in `datagfx/us_states.js`, made by `editor/make_usmap.py`.

## B-roll credits (Wikimedia Commons)
CC BY / BY-SA need attribution. Paste this in the caption or a pinned comment:

> B-roll via Wikimedia Commons: FISUTV (CC BY 3.0); the Dronalist (CC BY 3.0); REVisuals LA (CC BY 3.0); Third Coast Drone (CC BY 3.0); The Nomad With The Drone (CC BY 3.0); Neil Narain (CC BY 3.0); ProtoplasmaKid (CC BY-SA 4.0); 2017 Canada Summer Games (CC BY 2.0); Michael Barera (CC BY-SA 4.0); Habst (CC BY-SA 4.0); Daieuxetdailleurs (CC BY 4.0).

| file | Commons source | author | license |
|---|---|---|---|
| univ200.mp4 | Athletics Men's 200 Final - 27th Summer Universiade 2013 - Kazan (RUS).webm | FISUTV | CC BY 3.0 |
| hurdles.mp4 | 100 metres hurdles.webm | FISUTV | CC BY 3.0 |
| hollywood.mp4 | Aerial views of Hollywood Sign, Hollywoodland, Griffith Observatory… .webm | the Dronalist | CC BY 3.0 |
| la_sunrise.mp4 | Aerial views of Downtown Los Angeles California USA at sunrise.webm | the Dronalist | CC BY 3.0 |
| venice.mp4 | Venice Beach 4K Drone in Los Angeles CA.webm | REVisuals LA | CC BY 3.0 |
| goldengate.mp4 | Ship crossing the Golden Gate.webm | ProtoplasmaKid | CC BY-SA 4.0 |
| houston.mp4 | Houston Be Someone Bridge Drone Aerial Video.webm | Third Coast Drone | CC BY 3.0 |
| miami.mp4 | Miami DJI Mini 4 Pro Cinematic 4K (60FPS).webm | The Nomad With The Drone | CC BY 3.0 |
| charlotte_nc.mp4 | Aerial Video of Charlotte, NC (4K Drone Footage).webm | Neil Narain | CC BY 3.0 |
| hs_400m.jpg | Jaedon In a 400m Race.jpg | SprintsA11 | CC0 |
| hs_sprinter.jpg | Oregon City Track & field - IMG 8800 (52865760653).jpg | Oregon City High School | Public domain |
| relay_handoff.jpg | 2017-08-04-Matt Duboff-4x100 (35543395104).jpg | 2017 Canada Summer Games | CC BY 2.0 |
| texas_meet.jpg | 2017 Lone Star Conference Outdoor Track and Field Championships 01 … .jpg | Michael Barera | CC BY-SA 4.0 |
| penn_relays.jpg, penn_relays2(_full).jpg | 2024 Penn Relays 35.jpg, 29.jpg | Habst | CC BY-SA 4.0 |
| olympic_4x100.jpg | Athletics at the 2024 Summer Olympics – Men's 4 × 100 metres relay final - 01.jpg | Daieuxetdailleurs | CC BY 4.0 |

## v2 (owner feedback)
- **Full-screen quality:** every full-screen shot is now 4K or full-res. The 1080p race clips are only used in the split.
  - Opening: the full 8256×5504 photo of the high school runner.
  - Hollywood and LA drone shots: native 4K intermediates (`*_4k.mp4`).
  - Mid-video: the Penn Relays photo (3024×4032, natively vertical).
- **Sound:**
  - Removed the two 4 s risers (the loud, drawn-out noise).
  - New spacing rule: at least 3 s between sound moments.
  - No sound is used twice in a row. 14 sound moments in total.
