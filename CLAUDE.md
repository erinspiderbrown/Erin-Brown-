# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Use the owner's original voice audio, untouched, on every video.** The default is `voice_chain: "original"`.
  - No EQ, no compression, no noise reduction: the owner said processing made his voice "weird / muffled" and "took the bass out".
  - **Never turn the voice down.** If the take is already at or above −14 LUFS, it passes through untouched: no gain and no limiter.
    - One exception: if the take peaks right at 0 dBFS, it gets the minimum static trim to a −0.5 dBFS peak (about 0.5 dB, below audibility). ffmpeg's AAC encoder squashes full-scale audio (quieter, with crunch on the loudest words), and this headroom keeps the encode clean.
  - If the take is quieter than −14 LUFS, it gets one static volume boost up to −14, plus a peak limiter only in that case.
  - Don't add voice processing back, or lower the voice, unless the owner asks for it.
- **Full-screen shots must be sharp enough to monetize.** The owner rejected a soft opening shot.
  - A 16:9 1080p clip cropped to full-screen vertical gets enlarged about 1.8×, which looks soft. Don't use it full-screen.
  - Full-screen needs one of:
    - 4K landscape video (keep it at native 4K, don't downscale the intermediate)
    - vertical video at 1080×1920 or higher
    - a high-res photo (about 3000 px or more on the long side)
  - 1080p landscape clips go in the bottom half of the split only.
  - Check a full-resolution frame of every full-screen shot, especially the opening, before exporting.
- **Export:** 1080×1920, 30 fps. Loudness is −14 LUFS, or louder if the owner's take is already louder (see above). Save finished edits to `exports/` and push them so the owner can download from GitHub. Keep them under 100 MB: re-encode the video with `-crf 20 -preset slow`, or with a two-pass encode at about 6–9 Mbps if that's still too big. Copy the audio (`-c:a copy`; the build writes 256k AAC) so the voice is never re-compressed.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
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
- **Sound effects: few, quiet, spaced out.** The owner dislikes random loud sounds mid-sentence. `build.py` and the `style.json` defaults enforce this:
  - **Off:** `graphic_sfx: false`, so graphics and animations make no sound (no stamp thuds, pops, ticks or clicks).
  - **Off:** `hit_sfx: false`, so there are no bass hits. `"hit": true` on a segment only picks the flash/shake transition.
  - **Off:** `extra_sfx_on: false`. Risers and long cinematic hits are banned outright (`BANNED_SFX`), in any video.
  - **Kept:** a quiet airy whoosh on cuts into and out of full-screen (`whoosh_level` 0.24), with small pitch variation. B-roll swaps inside the split are silent.
  - **Spaced out:** at least `sfx_min_gap` (3 s) between sound moments, and never the same sound file twice in a row.
  - The render prints the kept sound list (`SFX: …`). Check it.
  - Don't turn any of these back on unless the owner asks.
  - (History: the owner first found every-cut whooshes repetitive, then found graphic and impact sounds loud and random, and risers too loud and drawn out.)
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
  - `usmap`: states light up on a US map in time with the voice; `cross` puts a red X on a state
  - `birthday`: cake with number candles and confetti
  - `podcast`: mic badge with a live waveform naming who's talking, for guest podcast clips
  - `board`: records board; rows of `event`, `value` and optional `tag`, with `times` landing each row on the word
  - `track`: one lap of a track with a clock counting to `value` (open 400 times)
- **Never invent data.** Don't fake stats or poll percentages. If a value is interpreted (e.g. "23 mid" → 23.5), say so to the owner.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips are a standing request for future videos.** Plan short animated clips that illustrate what's being said, alongside the motion graphics. Examples: an animated track, a running-figure loop, a stopwatch or a globe spin.
  - Before each edit, list the animation moments you'd add and ask the owner to supply clips, or offer to generate them.
  - AI generation costs credits and the owner doesn't want an "AI look", so get approval first.
  - As of Nov 2026 the owner's Higgsfield account is on the free plan with 10 credits. Its 1080p models need the Basic plan or higher, and the only clips 10 credits cover are 720p, which breaks the 1080p rule. Until that changes, hand-build animations as `motion` graphics.
  - Clips go in as `type: "clip"` overlays: keyed with `key: "green"`/`"black"`, as alpha video, or full-frame as a B-roll segment.

## Default editing method: the Yohan Blake edit
**This is the default way to edit every TikTok from now on.** The owner called `exports/yohan_blake_tiktok.mp4` "perfect" and "probably the best video". Its plan is `projects/yohan-blake/plan.json` and its notes are in `projects/yohan-blake/NOTES.md`. Copy its structure, pacing, graphics and transitions unless the owner asks for something different.
- **Graphics and transitions:** the owner said both were "on point". Keep the same mix and density:
  - The auto-picked viral transitions, with no per-segment overrides.
  - A graphic on almost every beat (name tags, keywords, stamps, boards, bars, counters, a poll).
  - Don't thin them out or swap in new styles without asking.
- **Pull relevant historical media online whenever the owner's footage doesn't cover the story.** That means photos of the athletes, races and moments being discussed. Use it even when he sends B-roll, if a moment he talks about isn't covered. See "When the owner sends only a talking head" below for sources and rules.
- **Story arc:** build the edit as an argument with a payoff.
  1. **Hook (0–15 s):** the subject full-screen with a name tag, the claim as a `keyword` ("ALWAYS 2ND TO BOLT?"), a `stamp` on the punchline ("BIGGEST LIE"), and `bubbles` for "what people say online".
  2. **Context:** what's true about the subject, shown as data (an all-time `board`, a `pin` for where it happened, a `stamp` for the twist, e.g. "NOT A CHAMPIONSHIP").
  3. **Turn:** cut to full-screen on the key fact, with a `data` counter.
  4. **The real story:** a name tag for each new person, then a `board` listing the evidence, one row landing on each spoken item (`times`).
  5. **Callback:** full-screen with the claim stamped again ("WRONG ERA?" → "LIE").
  6. **Proof:** actual results for each event the owner names (`bars` with real times, the subject's place in the name), with a stamp on each verdict ("4TH PLACE", "4TH AGAIN").
  7. **Ending:** `poll` on the core question ("BORN IN THE WRONG ERA? YES / NO").
- **Pacing:**
  - A graphic on almost every beat, about every 3–5 s.
  - A new B-roll shot every 4–7 s.
  - Full-screen at each act turn (4–5 per video), with `hit` on the two biggest.
  - Punch-in zooms on the owner's rhetorical questions ("Where was he?").
- **Facts on screen:** the owner's claims are backed by real, checked numbers: official times and places, all-time ranks. Never invent data. List every added fact in the project NOTES, and tell the owner where his wording differs from the record.
- **When the owner sends only a talking head:**
  - Pull B-roll from Wikimedia Commons: freely licensed photos of the athletes and races, ≥2800 px.
    - Search by category and by file name.
    - Download slowly, because Commons rate-limits.
    - Bake in EXIF orientation, and cap photos at 3200 px for render speed.
  - Write `CREDITS.md` (CC BY / CC BY-SA need a caption credit) and tell the owner the caption line.
  - YouTube race footage can't be downloaded from the cloud session (bot check; don't try to get around it). List the official uploads in `footage_wanted.md` so the owner can send them; they'd go in the bottom half.
  - Full-screen photos must be vertical or large enough to crop to 9:16 sharply. A wide landscape photo crops to an awkward slice, so use it in the split only.
- **Graphic layout limits (learned on this edit):**
  - `board` rows: keep `event` to about 20 characters, and only use `tag` on short rows, or the value gets clipped.
  - `bars`: at most 4 rows in the split. For 5+ results, use a `board` (rows like "5 · YOHAN BLAKE", with a `tag`).
  - Check a frame after each data graphic lands, plus the full-screen shots, before exporting.

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox links.
   - Share links (`/scl/fi/...`): download with `?dl=1`.
   - Transfer links (`/transfer/...`): run `node editor/fetch_dropbox_transfer.js <url> <dir>`. You get a zip; unzip it into its own folder.
   - **Guest soundbites:** when the owner references someone's interview or podcast, cut the guest's best 15–25 s into the A-roll right after the owner introduces them. The guest's footage takes the top "speaker" slot, in the same 1440×1280 framing with any on-screen banners cropped off. Match its loudness to the owner's voice, and merge the guest's captions into the timeline. See `projects/flotrack-masai/`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
3. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
4. **Write `plan.json`.** Start from `projects/yohan-blake/plan.json`, the default editing method (see above).
5. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
