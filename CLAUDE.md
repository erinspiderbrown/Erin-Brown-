# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Full-screen shots must be sharp enough to monetize.** The owner rejected a soft opening shot.
  - A 16:9 1080p clip cropped to full-screen vertical gets enlarged about 1.8×, which looks soft. Don't use it full-screen.
  - Full-screen needs one of:
    - 4K landscape video (keep it at native 4K, don't downscale the intermediate)
    - vertical video at 1080×1920 or higher
    - a high-res photo (about 3000 px or more on the long side)
  - 1080p landscape clips go in the bottom half of the split only.
  - Check a full-resolution frame of every full-screen shot, especially the opening, before exporting.
- **Export:** 1080×1920, 30 fps, at −14 LUFS. Save finished edits to `exports/` and push them so the owner can download from GitHub. Keep them under 100 MB: re-encode with `-crf 20 -preset slow`, or with a two-pass encode at about 9 Mbps if that's still too big.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
- **Seam:** a clear separation between the face and the B-roll, but soft: `seam_style: "soft"` gives a clean edge with a soft shadow band and a faint 2 px hairline.
  - The face must **not** blend or dissolve into the B-roll; the owner rejected `"blend"`.
  - No bold or colored divider line either; the owner rejected the red line.
- **Captions:** word-by-word, all caps, Montserrat Black, sitting on the seam. Highlights alternate red `#E8231E` and yellow `#FFE11A`.
- **Sound effects stay restrained.** The owner found every-cut whooshes repetitive. `build.py` enforces all of this:
  - Simple whooshes, swooshes and pops are fine.
  - **No risers or long cinematic hits, in any video.** The owner found them too loud and too drawn out. They're banned in `build.py` (`BANNED_SFX`), and `extra_sfx` can't add them back.
  - **Space the sounds out:** at least `sfx_min_gap` (3 s, in `style.json`) between sound moments, never one every 1–2 seconds. Hits and full-screen cuts take priority, and cues that crowd them are dropped. Each graphic gets one pop or thud, not one per word or state.
  - **Never the same sound twice in a row.** Consecutive transition sounds always use different files.
  - B-roll swaps inside the split are silent.
  - A soft airy whoosh plays only on cuts to full-screen.
  - Mark only the biggest moment or two with `"hit": true` for the short bass hit and flash.
  - Every cue gets a small random pitch variation.
  - The render prints the kept sound list (`SFX: …`). Check it.
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
  - `usmap`: states light up on a US map in time with the voice; `cross` puts a red X on a state
- **Never invent data.** Don't fake stats or poll percentages. If a value is interpreted (e.g. "23 mid" → 23.5), say so to the owner.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips are a standing request for future videos.** Plan short animated clips that illustrate what's being said, alongside the motion graphics. Examples: an animated track, a running-figure loop, a stopwatch or a globe spin.
  - Before each edit, list the animation moments you'd add and ask the owner to supply clips, or offer to generate them.
  - AI generation costs credits and the owner doesn't want an "AI look", so get approval first.
  - Clips go in as `type: "clip"` overlays: keyed with `key: "green"`/`"black"`, as alpha video, or full-frame as a B-roll segment.

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox share links. Download them with `?dl=1`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
3. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
4. **Write `plan.json`.** See `projects/charlotte-ehioghae/plan.json` for a full real example.
5. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
