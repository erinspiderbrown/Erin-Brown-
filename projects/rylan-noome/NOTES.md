# Rylan Noome's 35.3 300 m (Nov 2026)

## Inputs (not committed)
- `raw/talking_head.mov`: 4K (3840×2160 after rotation), 72 s, Dropbox folder link.
- Owner's media, all **below the 1080p rule** and flagged to the owner:
  - `clip_a.mp4`: the 300 m race. A 720×1280 phone video with the race in a 720×402 strip (the rest is black bars and a "POV" caption). It's cropped to the strip and shown **framed at native size** in `broll/race_card.mp4`, a 1080×960 bottom-half panel over a dimmed sharp photo. It's never stretched.
  - `clip_b.mp4`: Noome making a shake, 720×1280. Shown framed the same way in `broll/fitness_card.mp4`.
  - `photo_a.jpg` (984×1211, pointing): used in the split only.
  - `photo_b.jpg` (1206×1171, relay finish) passes the rule. Split only.
- `broll/`: Wikimedia Commons, all ≥1080p. Every full-screen shot is a high-res photo (2188 px or more on the short side).

## Steps
1. Crop the talking head to 2430×2160 at (605, 0) and scale to 1440×1280.
2. Declip the voice: about 2,600 flat tops, 3,068 peaks rebuilt. Mux it onto the face, then `tighten.py`: 72.0 s → 69.0 s.
3. Transcript fixes:
   - "Ryland Noom" → RYLAN NOOME (World Athletics spelling).
   - "Caleb" → CAELEB (Dressel's spelling).
   - "35 .3" → 35.3, and "y 'all" → Y'ALL.
4. `python3 ../../editor/build.py plan.json`, then export at CRF 20 (76 MB).

## Data (no invented numbers)
- Name card: age 20, 100 m PB 10.48 (14 Mar 2026). Source: World Athletics profile.
- 35.3 (300 m), the 33.3/34.3 comparison and the 51-second 400 m projection are **the owner's own numbers**. They're labelled "his take" and "my projection", not presented as official results. World Athletics doesn't list the 300 m.
- The poll has no percentages.

## Tool change
The SFX spacing rule now measures between the actual sounds of two moments (closest pair), not their start times. A counter whose pop landed late had ended up 1.7 s before the next whoosh.

## B-roll credits (Wikimedia Commons)
Paste this in the caption or a pinned comment:

> B-roll via Wikimedia Commons: Fernando Frazão/Agência Brasil (CC BY 3.0 BR); Daieuxetdailleurs (CC BY 4.0); cogdogblog (CC BY 2.0); Ansgar Koreng (CC BY-SA 4.0); It is a wonderful world (CC BY-SA 4.0); Mikolka221 (CC BY 3.0); FISUTV (CC BY 3.0).

| file | Commons source | author | license |
|---|---|---|---|
| phelps_dressel.jpg | Michael Phelps and Caeleb Dressel Rio 2016.jpg | Fernando Frazão/Agência Brasil | CC BY 3.0 BR |
| olympic_400_action.jpg, olympic_400_board.jpg | Athletics at the 2024 Summer Olympics – Men's 400 m semi-final 2- 05.jpg, 03.jpg | Daieuxetdailleurs | CC BY 4.0 |
| auckland_tower.jpg | Auckland Skyline Blocks (15499793692).jpg | cogdogblog | CC BY 2.0 |
| stopwatch.jpg | Stopwatch, 1810201155, ako.jpg | Ansgar Koreng | CC BY-SA 4.0 |
| butterfly_above.mp4, butterfly_under.mp4 | Butterfly stroke from above / from underwater.webm | It is a wonderful world | CC BY-SA 4.0 |
| slo_400m.mp4 | AZS - Odprto prvenstvo Slovenije Koper 2011 400m moski (HD 1080p).webm | Mikolka221 | CC BY 3.0 |
| hurdles.mp4, univ200.mp4 | 100 metres hurdles.webm; Athletics Men's 200 Final - 27th Summer Universiade 2013 | FISUTV | CC BY 3.0 |
