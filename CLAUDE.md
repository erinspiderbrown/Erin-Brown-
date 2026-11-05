# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
  - Never use sub-1080p footage full-screen. If the owner wants it used, keep it in the split and AI-upscale it first with `editor/upscale.py` (Real-ESRGAN general-x4v3; CPU, about 8 s per frame).
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Use the owner's original voice audio, untouched, on every video.** The default is `voice_chain: "original"`.
  - No EQ, no compression, no noise reduction: the owner said processing made his voice "weird / muffled" and "took the bass out".
  - **Never turn the voice down.** If the take is already at or above −14 LUFS, it passes through untouched: no gain and no limiter.
    - One exception: if the take peaks right at 0 dBFS, it gets the minimum static trim to a −0.5 dBFS peak (about 0.5 dB, below audibility). ffmpeg's AAC encoder squashes full-scale audio (quieter, with crunch on the loudest words), and this headroom keeps the encode clean.
  - If the take is quieter than −14 LUFS, it gets one static volume boost up to −14, plus a peak limiter only in that case.
  - Don't add voice processing back, or lower the voice, unless the owner asks for it.
- **Export:** 1080×1920, 30 fps. Loudness is −14 LUFS, or louder if the owner's take is already louder (see above). Save finished edits to `exports/` and push them so the owner can download from GitHub. Keep them under 100 MB: re-encode the video with `-crf 20 -preset slow` if needed (if that is still over 100 MB, use a two-pass encode at about 10.5 Mbps for a ~70 s video), and copy the audio (`-c:a copy`; the build writes 256k AAC) so the voice is never re-compressed.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
- **Face look:** no color grade on the talking head; the owner disliked the reddish look from the old contrast and saturation grade. Keep only the dark edges: `face_grade: "vignette=PI/6"` in `style.json`.
- **Seam:** a clear separation between the face and the B-roll, but soft: `seam_style: "soft"` gives a clean edge with a soft shadow band and a faint 2 px hairline.
  - The face must **not** blend or dissolve into the B-roll; the owner rejected `"blend"`.
  - No bold or colored divider line either; the owner rejected the red line.
- **Transitions: viral-style, on every video** (`editor/transitions.py`; auto-picked by `choose_transitions` in `build.py`):
  - **Into full-screen:** rotate zoom-through, whip-pan (left/up) and spin.
  - **`hit` segments:** flash or camera shake.
  - **Out of full-screen:** whip-down, zoom, whip-right or glitch.
  - **Full → full:** whip or glitch.
  - **B-roll swaps inside the split:** a bottom-half swipe with motion blur; the owner's face never moves.
  - **Overrides:** force one per segment with `"transition": "whip:left" | "zoom" | "spin" | "glitch" | "flash" | "shake" | "swipe:right" | "cut"`. Set `split_swipes: false` for plain cuts in the split.
  - Keep them varied, never the same transition twice in a row. Motion blur peaks briefly at the cut so both shots stay sharp.
- **Captions:** word-by-word, all caps, Montserrat Black, sitting on the seam. Highlights alternate red `#E8231E` and yellow `#FFE11A`.
- **No random loud sound effects mid-sentence.** The owner dislikes them. The defaults in `style.json` are:
  - **Off:** `graphic_sfx: false`, so graphics and animations make no sound (no stamp thuds, pops, ticks or clicks).
  - **Off:** `hit_sfx: false`, so there are no bass hits.
  - **Off:** `extra_sfx_on: false`, so there are no risers.
  - **Kept:** a quiet airy whoosh on cuts into and out of full-screen (`whoosh_level` 0.24), with small pitch variation. B-roll swaps inside the split are silent.
  - Don't turn any of these back on unless the owner asks. `"hit": true` on a segment now only adds the visual flash.
  - (History: the owner first found every-cut whooshes repetitive, then found graphic and impact sounds loud and random.)
- **Numbers and stats** get animated data graphics (`type: "data"`: counter, compare, bars, line, ring); they're silent by default. Run `suggest_data.py` on the transcript to find every number.
- **Things being talked about** get motion graphics (`type: "motion"`):
  - `stamp`: e.g. "FRAUD?"
  - `keyword`
  - `pin`: a place
  - `calendar`: months or seasons
  - `stopwatch`: race times
  - `wind`
  - `spotlight`: circle and arrow on a person in full-screen footage
  - `poll`: comment-bait ending
  - `padlock`: paywall
  - `subscription`: streaming screen swapping services, ending on "subscription required"
  - `tv`: TV switching on
  - `flow`: three-step icon chain; set `times` to land each step on the word
  - `bubbles`: generic reaction chat bubbles. These are illustrative, never presented as real quotes.
  - `board`: records board; rows of `event`, `value` and optional `tag`, with `times` landing each row on the word
  - `track`: one lap of a track with a clock counting to `value` (open 400 times)
  - `neon`: glowing neon sign that flickers on (`text` with `|` for line breaks, `sub`, `icon`: bolt/plus/question/flame/check/arrow, `color`, `color2`, `frame`)
  - `battery`: neon batteries draining (`rows` of `label`, `to` 0–1, `color`, `end` text). Illustrative only, never a measured value.
- **Never invent data.** Don't fake stats or poll percentages. If a value is interpreted (e.g. "23 mid" → 23.5), say so to the owner.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips are a standing request for future videos.** Plan short animated clips that illustrate what's being said, alongside the motion graphics. Examples: an animated track, a running-figure loop, a stopwatch or a globe spin.
  - Before each edit, list the animation moments you'd add and ask the owner to supply clips, or offer to generate them.
  - AI generation costs credits and the owner doesn't want an "AI look", so get approval first.
  - As of Nov 2026 the owner's Higgsfield account is on the free plan with 10 credits. Its 1080p models need the Basic plan or higher, and the only clips 10 credits cover are 720p, which breaks the 1080p rule. Until that changes, hand-build animations as `motion` graphics.
  - Clips go in as `type: "clip"` overlays: keyed with `key: "green"`/`"black"`, as alpha video, or full-frame as a B-roll segment.

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox links.
   - Share links (`/scl/fi/...`): download with `?dl=1`.
   - Transfer links (`/transfer/...`): run `node editor/fetch_dropbox_transfer.js <url> <dir>`. You get a zip; unzip it into its own folder.
   - **Guest soundbites:** when the owner references someone's interview or podcast, cut the guest's best 15–25 s into the A-roll right after the owner introduces them. The guest's footage takes the top "speaker" slot, in the same 1440×1280 framing with any on-screen banners cropped off. Match its loudness to the owner's voice, and merge the guest's captions into the timeline. See `projects/flotrack-masai/`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
3. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
4. **Write `plan.json`.** See `projects/charlotte-ehioghae/plan.json` for a full real example.
5. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
