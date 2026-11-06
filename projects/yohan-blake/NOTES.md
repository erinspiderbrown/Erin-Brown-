# Yohan Blake: "born in the wrong era" is a lie (Nov 2026)

**Title (YouTube Shorts / TikTok):** Yohan Blake Wasn't Born in the Wrong Era — The Results Prove It

The owner sent only a talking head (4K, displays 3840×2160) and asked for the clips to be pulled from the internet.

## B-roll
- **Race footage (YouTube):** couldn't be downloaded. YouTube serves this environment a bot check, and getting around it isn't allowed. The official uploads exist (World Athletics, Olympics, Diamond League channels) and are listed in `footage_wanted.md`. They're 1080p landscape, so they'd go in the bottom half only.
- **What's used:** freely licensed Wikimedia Commons photos, all 1300–3200 px on the short/long side, with credits in `CREDITS.md`.
  - Full-screen shots use vertical or ≥3800 px photos only: Blake in Lausanne 2012 (×2), Blake in Brussels 2012, and the London 2012 200 m heat.
  - EXIF orientation is baked in (two photos were rotated), and photos are capped at 3200 px for render speed.

## Steps
1. Crop `crop=2430:2160:670:0`, scale to 1440×1280, `tighten.py` (120.2 s → 107.8 s).
2. Transcript fix: "Johan" → Yohan.
3. `python3 ../../editor/build.py plan.json` (paths relative to the scratch workdir: `w2/`, `raw2/ph/`).

## Facts shown on screen (checked, not from the voiceover)
- 19.26 (200 m, Brussels 2011) and 9.69 (100 m, Lausanne 2012) as the #2 all-time marks. The 9.69 is tied #2 with Tyson Gay, marked "(=)".
- Final results:
  - London 2017: Gatlin 9.92, Coleman 9.94, Bolt 9.95, Blake 9.99 (4th).
  - Rio 2016: Bolt 9.81, Gatlin 9.89, De Grasse 9.91, Blake 9.93 (4th).
  - Doha 2019: Coleman 9.76, Gatlin 9.89, De Grasse 9.90, Simbine 9.93, Blake 9.97 (5th).
- Gatlin's four silvers behind Bolt: 2013 Worlds 100, 2015 Worlds 100 and 200, 2016 Olympics 100.
- The opening chat bubbles are illustrative reactions, not real quotes.

## Owner's wording worth knowing
- "Finished behind Bolt one year": Blake also finished behind Bolt in Rio 2016 and London 2017, but as 4th, not 2nd. The graphic says "Runner-up to Bolt · 2012", which is accurate.
- "Over about eight years" (Gatlin): the four silvers span 2013–2016. Not put on screen.
