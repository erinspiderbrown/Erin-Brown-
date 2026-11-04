# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Export:** 1080×1920, 30 fps, at −14 LUFS. Save finished edits to `exports/` and push them so the owner can download from GitHub. Keep them under 100 MB: re-encode with `-crf 20 -preset slow` if needed.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
- **Seam:** the face dissolves softly into the B-roll (`seam_feather`). No hard colored divider line.
- **Captions:** word-by-word, all caps, Montserrat Black, sitting on the seam. Highlights alternate red `#E8231E` and yellow `#FFE11A`.
- **Sound effects stay restrained.** The owner found every-cut whooshes repetitive. Defaults in `build.py`:
  - B-roll swaps inside the split are silent.
  - A soft airy whoosh plays only on cuts to full-screen.
  - Mark only the biggest moment or two with `"hit": true` for the bass hit and flash.
  - Every cue gets a small random pitch variation.
- **Numbers and stats** get animated data graphics (`type: "data"`: counter, compare, bars, line, ring) with tick and land sounds. Run `suggest_data.py` on the transcript to find every number.
- **Things being talked about** get motion graphics (`type: "motion"`):
  - `stamp`: e.g. "FRAUD?"
  - `keyword`
  - `pin`: a place
  - `calendar`: months or seasons
  - `stopwatch`: race times
  - `wind`
  - `spotlight`: circle and arrow on a person in full-screen footage
  - `poll`: comment-bait ending
- **Never invent data.** Don't fake stats or poll percentages. If a value is interpreted (e.g. "23 mid" → 23.5), say so to the owner.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips** the owner provides go in as `type: "clip"` overlays, keyed with `key: "green"`/`"black"` or as alpha video.

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox share links. Download them with `?dl=1`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
3. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
4. **Write `plan.json`.** See `projects/charlotte-ehioghae/plan.json` for a full real example.
5. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
