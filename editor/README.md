# TikTok editor

Builds 1080×1920 TikTok edits in this style: talking head on top, B-roll on the bottom, switching to full-screen B-roll for big moments.

## Setup (once per machine)
Needs ffmpeg, Python 3, and Node with Playwright and Chromium.

    ./setup.sh            # installs faster-whisper, downloads fonts and the Mixkit SFX library

## Per video
Rules: the final video must be **at least 61 seconds**, and all B-roll must be **1080p or higher**.

1. Transcribe the talking-head take (word timings drive the captions):
       python3 transcribe.py raw/talking_head.mov 0 work/words.json medium.en
1b. Crop a 4K or landscape talking head to the top-half framing first (1440×1280 works well), then cut the dead air:
       python3 tighten.py work/face.mov work/words.json work/face_tight.mov work/words_tight.json
2. Write a plan (see `example_plan.json`): segments (split / full), B-roll sources and seek points, graphics.
3. Find every stat worth animating:
       python3 suggest_data.py work/words.json
4. Render:
       python3 build.py plan.json

## What it does
- **Layout:** split screen (face top, B-roll bottom, accent divider) and full-screen B-roll with smooth slide transitions, a punch-in and a flash frame.
- **Full frame:** full-screen B-roll always fills the whole 9:16 frame, with no bars, blur fill or blank space. `focus: [x, y]` (0–1) picks the crop point so the action stays in frame.
- **Face zooms:** `zooms: [[start, end, scale]]` punches in on you for emphasis.
- **Data graphics** (`"type": "data"`) are rendered in Chromium as transparent overlays:
  - `counter`: a big number counting up with motion blur and a progress bar.
  - `compare`: a head-to-head with the winner's bar glowing and a delta badge.
  - `bars`: a ranked list.
  - `line`: a chart that draws on, with a final-value callout.
  - `ring`: a percent gauge.

  Each one gets its own sound design: a whoosh in, data ticks as the numbers move, and a pop and bass hit when the number lands.
- **Captions:** word-by-word highlights in Montserrat Black. The highlight color alternates between chunks using `caption_colors`.
- **Graphics:** stat cards with count-up numbers, and rank/name plates in the `accent` color.
- **Audio:** voice cleanup (high-pass, denoise, EQ, compression), mastered to −14 LUFS.
- **Sound effects:** Mixkit whooshes, impacts, pops and clicks. They rotate so none repeats back-to-back, and each one's peak lands exactly on its cut.
- **Quality rules:**
  - B-roll below 1080p (short side) is rejected.
  - Clips that have to be enlarged to fill the screen get extra sharpening.
  - Photos get a slow push-in.
  - Vertical or 4K footage looks best when used full-screen.

SFX: Mixkit Sound Effects Free License (commercial use OK; files aren't committed, `setup.sh` downloads them).
Fonts: SIL Open Font License.
