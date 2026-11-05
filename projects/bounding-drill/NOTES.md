# European bounding drill (Nov 2026)

## Inputs (Dropbox folder, not committed)
- `raw/talking_head.mov`: 4K, 71.2 s.
- `raw/clip_720p.mp4`: the Instagram drill clip. **720×1280, below the 1080p rule.** It's the subject of the video and the only footage of the drill, so it's used anyway, including a slow-motion replay (`work/clip_slow.mp4`, motion-interpolated at 0.5×).

## Stock photos (Wikimedia Commons, all at least 2159 px on the short side; credit required)
- `letzigrund_sunset.jpg`: "Sunset on Letzigrund 2" by Joel Bez, CC BY 2.0.
- `sdf_2024.jpg`: "Stade de France, Olympics 2024" by Rmpbedford, CC BY-SA 4.0.
- `zurich_dl.jpg`, `zurich_400.jpg`, `zurich_800.jpg`: Weltklasse Zürich / Wanda Diamond League photos by Peter Arnold, CC BY-SA 4.0.
- `tj_a.jpg`: "Men triple jump French Athletics Championships 2013" by Marie-Lan Nguyen, CC BY 3.0.
- `spikes.jpg`: "Nike track spikes" by Santeri Viinamäki, CC BY-SA 4.0.

## Steps
1. Crop the face to 2000×1778 at (813, 250), scale to 1440×1280, then run `tighten.py` (71.2 s → 68.5 s).
2. Transcript: medium.en misheard several words, so they were checked against large-v3. Fixes: "mid-rep", "mid-run", "mid-bound", "mid-race", "track meet", "get you rolled".
3. New motion kinds:
   - `track`: top-down oval where two runners come off the curve and start bounding (`tc`, `tb`, `back`).
   - `jail`: bars slam down on a coach figure, then the sentence text.
4. Render with `python3 ../../editor/build.py plan.json`, then re-encode at `-crf 20 -preset slow` (plus a `-crf 24` phone copy).

## Notes
- "120 OR 150?" is the owner's estimate, shown with a question mark.
- The chat bubbles are generic illustrative reactions, not real messages.
