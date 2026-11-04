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

## House style
`style.json` holds the defaults every plan inherits: colors, seam feather, sound level, minimums.

## Graphic types (`graphics` list in the plan)
| type | kinds / fields | use for |
|---|---|---|
| `data` | `counter`, `compare`, `bars`, `line`, `ring` | numbers and stats |
| `motion` | `stamp`, `keyword`, `pin`, `calendar`, `stopwatch`, `wind`, `spotlight`, `poll`, `padlock`, `subscription`, `tv`, `flow`, `bubbles`, `board`, `track` | things being talked about |
| `name` | `rank`, `name`, `sub` | introducing a person |
| `clip` | `src`, `t`, `dur`, `x`, `y`, `w`, `key: green\|black` | animation clips you supply (green-screen, black-background or alpha) |

Placement: `anchor` (`lower`/`upper`/`center`) or explicit `x`/`y`. `spotlight` takes subject coordinates `x`, `y`, `r` on the 1080×1920 frame.
Segments: `"hit": true` marks the one or two biggest full-screen moments (bass hit and flash). `"sfx": true` forces a whoosh on a quiet B-roll swap.

Renders are cached: unchanged segments and graphics are reused, so tweaks re-render fast.

## Transitions
`transitions.py` has these effects:
- `whip`: whip-pan with directional motion blur
- `zoom`: zoom-through
- `spin`
- `glitch`: RGB split plus jitter
- `flash`: white bloom
- `shake`: camera shake
- `swipe`: bottom-half whip for split B-roll swaps
- `cut`

Each is rendered as a short clip from the overlap between segments. `build.py` picks them automatically and varies them; override per segment with `"transition"`.

## What it does
- **Layout:** split screen (face top, B-roll bottom, separated by a soft seam: a clean edge, soft shadow and faint hairline. `seam_style: "blend"` is available but not the house look) and full-screen B-roll with smooth slide transitions, a punch-in and a flash frame.
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
- **Audio:** your original voice, untouched (one volume gain to −14 LUFS).
- **Sound effects:** Mixkit whooshes, impacts, pops and clicks. They rotate so none repeats back-to-back, and each one's peak lands exactly on its cut.
- **Quality rules:**
  - B-roll below 1080p (short side) is rejected.
  - Clips that have to be enlarged to fill the screen get extra sharpening.
  - Photos get a slow push-in.
  - Vertical or 4K footage looks best when used full-screen.

SFX: Mixkit Sound Effects Free License (commercial use OK; files aren't committed, `setup.sh` downloads them).
Fonts: SIL Open Font License.
