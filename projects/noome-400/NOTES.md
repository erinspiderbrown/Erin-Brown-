# Rylan Noome's 400 m: "embarrassed the entire sport" (Nov 2026)

A follow-up to `projects/rylan-noome` (his 35.3 300 m).

## Inputs (not committed)
- `raw/talking_head.mov`: 4K, 1:33.
- Owner's media:
  - `clip_430.mov`: the full 400 m race, vertical 1080×1920 at 60 fps, a soft phone zoom.
  - `clip_1031b.mov`: Noome's pre-race interview, 536×954.
  - `clip_1031a.mov`: him walking in, 360×640.
  - `photo_1.jpg`, `photo_2.jpg`: 1206 px wide.

## Enhancement (owner asked: "make sure the clips are high quality, even if you have to enhance")
`editor/enhance.py` (new) runs Real-ESRGAN general x4 v3 locally on CPU. It reconstructs detail; it isn't AI generation, and it uses no credits.

| output | from | result |
|---|---|---|
| `interview_hd.mp4` | interview 13.3–26.0 s, 536×954 | 1078×1920 |
| `arrived_hd.mp4` | walk-in, 360×640 | 1080×1920 |
| `noome_relay_hd.jpg`, `noome_blocks_hd.jpg` | 1206 px photos | about 2800–3000 × 4000 (full-screen eligible) |
| `race_start_hd.mp4` (0.5–6.5 s), `race_finish_hd.mp4` (34.5–51 s) | race clip | 540×960 → 4× → 1080×1920. Visibly cleaner than the soft original. |

- The middle of the race (the back straight) uses the original in the split, where it isn't enlarged.
- `race_card.mp4` and `butterfly_above.mp4` are reused from the earlier Noome video.

## Structure
| part | content |
|---|---|
| Hook | Enhanced full-screen photo, name card, "EMBARRASSING" |
| PART 1: THE 300 | Recap of the 35.3, the "too big?" stamp |
| PART 2: THE PREDICTIONS | The owner's 51.0, then **Noome's own words**: a 12.7 s insert from the enhanced interview ("I think I'm going to get sub-50 today…", and the calves question) |
| PART 3: THE 400 | Enhanced start, back straight in the split, "check engine light", enhanced finish from 300 m: "running backwards", "cinder blocks" |
| THE VERDICT | New Zealand pin, poll "WHAT DID HE RUN? SUB-50 / 51+" |

## Interview insert
- `work/face_story.mov` = talking head 0–37.05 s + 12.7 s gap (covered by the full-screen interview) + the rest of the talking head.
- The interview audio is declipped and loudness-matched to the owner's voice (+3.1 dB).
- `words_story.json` holds the captions, with the interview words placed in the gap and later words shifted by 12.7 s.
- Interview transcript fixes: "carbs" → CALVES, "street" → STRAIGHT.

## Data
- Name card: 100 m PB 10.48, age 20 (World Athletics).
- 35.3 and 51.0 are the owner's numbers from the previous video. "Sub-50" is Noome's own words.
- **His actual 400 m time isn't published anywhere I could find, and the owner doesn't say it, so no time is shown.** The poll asks viewers instead.

## Tool fixes this round
- `build.py`: if a video source is shorter than its segment (with the 0.15 s transition overlap), it holds the last frame and prints a NOTE. Before, the transition chain silently cut the video short, and the first render's picture stopped at 49.6 s.
- `enhance.py`: MKV intermediate, so an interrupted job stays readable.
