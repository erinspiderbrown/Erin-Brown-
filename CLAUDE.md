# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
  - The owner wants low-res clips **enhanced**. Use `editor/enhance.py` (Real-ESRGAN, local CPU, no credits).
  - It makes 360p/540p clips and ~1200 px photos usable (photos become full-screen eligible).
  - For a soft 1080p clip, shrink it to 540×960 first, then upscale 4×.
  - Speed: about 5 s per 540×960 frame on this 4-core box. Enhance only the time ranges you use, and run one job at a time (parallel jobs just fight over the CPU).
  - Don't wait on jobs with busy-loops; use `sleep`.
- **Wikimedia Commons downloads:** full-size originals often get rate-limited (HTTP 429). Use the cached standard-width thumbnails (`/thumb/…/3840px-…` or `1920px-…`), and send a descriptive User-Agent with the repo URL. Don't hammer: pace downloads and back off.
- **Footage from broadcasters** (World Athletics/NBC interviews, ceremony broadcasts) is copyrighted. Don't pull it into videos. Find it, give the owner the link, and use free-licensed real footage instead.
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Full-screen shots must be sharp enough to monetize.** The owner rejected a soft opening shot.
  - A 16:9 1080p clip cropped to full-screen vertical gets enlarged about 1.8×, which looks soft. Don't use it full-screen.
  - Full-screen needs one of:
    - 4K landscape video (keep it at native 4K, don't downscale the intermediate)
    - vertical video at 1080×1920 or higher
    - a high-res photo (about 3000 px or more on the long side)
  - 1080p landscape clips go in the bottom half of the split only.
  - Check a full-resolution frame of every full-screen shot, especially the opening, before exporting.
- **The voice must sound clear, never muffled, in every video.** The owner rejected a muffled mix: a de-esser, noise reduction and a weak presence boost had halved the 5–10 kHz "air".
  - The default voice chain in `build.py` cuts low-mid mud and lifts clarity (1.8 kHz) and air (7.5 kHz shelf). It has no de-esser or noise reduction.
  - After every render, `build.py` runs `audio_check.py`, which compares the export's tone with the raw voice and warns `MUFFLED` if clarity, presence or air drops. Never ship with that warning.
- **Export:** 1080×1920, 30 fps, stereo audio, at −14 LUFS. Save finished edits to `exports/` and push them so the owner can download from GitHub. Keep them under 100 MB: re-encode with `-crf 20 -preset slow`, or with a two-pass encode at about 9 Mbps if that's still too big.
  - **Long-form (5 min+):** a two-pass encode at about 2.45 Mbps with `-tune film` fits under 100 MB and looked practically identical to the master on the LA28 video.
- **"Cinematic" requests:** set `"broll_grade": "cinematic"` in the plan.
  - Use `"transition": "fade"` on full-screen shots and `"fadeblack"` into chapter openers.
  - Prefer real high-res photos with slow push-ins.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
- **Seam:** a clear separation between the face and the B-roll, but soft: `seam_style: "soft"` gives a clean edge with a soft shadow band and a faint 2 px hairline.
  - The face must **not** blend or dissolve into the B-roll; the owner rejected `"blend"`.
  - No bold or colored divider line either; the owner rejected the red line.
- **Captions:** word-by-word, all caps, Montserrat Black, sitting on the seam. Highlights alternate red `#E8231E` and yellow `#FFE11A`.
- **Sound effects stay restrained.** The owner found every-cut whooshes repetitive. `build.py` enforces all of this:
  - Simple whooshes, swooshes and pops are fine.
  - **No risers or long cinematic hits, in any video.** The owner found them too loud and too drawn out. They're banned in `build.py` (`BANNED_SFX`), and `extra_sfx` can't add them back.
  - **Space the sounds out:** at least `sfx_min_gap` (3 s, in `style.json`) between sounds, never one every 1–2 seconds. The gap is measured between the closest actual sounds of two moments, so a late graphic pop counts. Hits and full-screen cuts take priority, and cues that crowd them are dropped. Each graphic gets one pop or thud, not one per word or state.
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
- **No name tags.** The owner doesn't like the name plate at the bottom of the opening. Don't use `type: "name"` in any video; `build.py` drops it. Introduce people with the captions, B-roll and other graphics instead.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips are a standing request for future videos.** Plan short animated clips that illustrate what's being said, alongside the motion graphics. Examples: an animated track, a running-figure loop, a stopwatch or a globe spin.
  - Before each edit, list the animation moments you'd add and ask the owner to supply clips, or offer to generate them.
  - AI generation costs credits and the owner doesn't want an "AI look", so get approval first.
  - Clips go in as `type: "clip"` overlays: keyed with `key: "green"`/`"black"`, as alpha video, or full-frame as a B-roll segment.

## What's working (performance notes)
- **Nov 2026, "The most embarrassing 400m I've ever seen?"** (`projects/noome-400`): 56.9K views in its first 1 day 20 h, #1 of the owner's last 10, **73.1% average viewed** on a 1:45 video, 1.3K likes.
- What it had:
  - A chaptered story: setup, then the owner's prediction, then the subject's own prediction in his own voice, then the race payoff.
  - A poll ending.
  - A question-style title with a strong claim.
- The owner's own cover for it: a close, sharp photo of the subject with the result as a two-line headline at the top ("RAN 50.8" / "IN THE 400M"), in bold italic with red, white and yellow text.
- For a running story (like the Noome series), match the covers so the videos read as a set on the profile.

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox share links. Download them with `?dl=1`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
   - Whisper can skip whole phrases (often names). Check for time gaps in `words.json`, then re-transcribe the gap in short chunks with `condition_on_previous_text=False` and splice in the words.
   - Whisper can mishear numbers ("50" heard as "15"). If a number contradicts the point being made, check it with the owner or the source they're quoting, and use the owner's own stats when they send them.
3. **Check the voice for clipping.** Phone recordings are often too hot: the owner's Nov 2026 take clipped on nearly every loud syllable, which sounds crunchy.
   - Run `editor/declip.py raw/talking_head.mov work/voice_declip.wav`. It rebuilds the flattened peaks and writes a float WAV.
   - Mux that WAV onto the cropped face video before tightening.
   - Keep the voice in float from here on: `tighten.py` writes `pcm_f32le`, and `build.py` gives it −6 dB of headroom first.
   - Don't fight leftover harshness by dulling the voice. Declipping fixes the cause.
4. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
5. **Structure the story.** For a follow-up or reaction, use chapter labels (`keyword` cards like "PART 1: THE 300"), and let the subject speak in their own words where there's an interview clip.
   - Splice it into the talking-head timeline: a gap in `face`, the clip's audio loudness-matched, and the words shifted. See `projects/noome-400/NOTES.md`.
6. **Write `plan.json`.** See `projects/charlotte-ehioghae/plan.json` for a full real example.
7. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.
8. **Every video gets a high-quality thumbnail** (TikTok cover, 1080×1920 JPG), saved as `exports/<name>_thumb.jpg` and pushed with the video.
   - Write `projects/<name>/thumbnail.json` and run `python3 editor/thumbnail.py thumbnail.json exports/<name>_thumb.jpg <scratch>/check.jpg`.
   - **The owner's preferred look** (shown on his best performer, and asked for again on LA28):
     - **A close, sharp photo of a star athlete** relevant to the topic (e.g. Noah Lyles or Gout Gout for sprint-standard videos) filling the frame. Not generic scenery, not an unrelated athlete.
     - **A two-line headline at the top:** bold slanted (`"slant": 10`) Anton, white with a black stroke, with the key number or word in yellow `#FFE11A` and a red `#E8231E` underline swoosh.
     - Lines take inline HTML spans for per-word colour; see `projects/la28-standards/thumbnail.json`.
   - **Photo:** free-licensed and real. If the athlete is small in the frame, crop the area the cover shows from the source and run it through `enhance.py` (downscale to about 675 px wide, then 4×) instead of zooming in the cover, which looks soft.
   - **Safe zones:** check the check image. Keep text out of the bottom 25% (caption/UI) and the right 140 px (buttons), and keep the text and the subject's face inside the centre 3:4 (y 240–1680), which is what the profile grid shows.
   - **Accuracy:** numbers on the thumbnail follow the "never invent data" rule too.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
