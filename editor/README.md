# TikTok editor

Builds 1080×1920 TikTok edits in this style: talking head on top, B-roll on the bottom, switching to full-screen B-roll for big moments.

## Setup (once per machine)
    ./setup.sh            # installs faster-whisper, downloads fonts and the Mixkit SFX library

## Per video
1. Transcribe the talking-head take (word timings drive the captions):
       python3 transcribe.py raw/talking_head.mov 0 work/words.json
2. Write a plan (see `example_plan.json`): segments (split / full), B-roll sources and seek points, graphics.
3. Render:
       python3 build.py plan.json

## What it does
- **Layout:** split screen (face top, B-roll bottom, accent divider) and full-screen B-roll with smooth slide transitions and a punch-in.
- **Captions:** word-by-word highlights in Montserrat Black. The highlight color alternates between chunks using `caption_colors`.
- **Graphics:** stat cards with count-up numbers, and rank/name plates in the `accent` color.
- **Audio:** voice cleanup (high-pass, denoise, EQ, compression), mastered to −14 LUFS.
- **Sound effects:** Mixkit whooshes, impacts, pops and clicks. They rotate so none repeats back-to-back, and each one's peak lands exactly on its cut.
- **Quality rules:**
  - B-roll below 1080p (short side) is rejected.
  - Landscape clips that would need upscaling to fill the screen are shown sharp over a blurred fill.
  - Photos get a slow push-in.

SFX: Mixkit Sound Effects Free License (commercial use OK; files aren't committed, `setup.sh` downloads them).
Fonts: SIL Open Font License.
