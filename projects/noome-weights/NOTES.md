# Rylan Noome, part 3: 50.8 in the 400, then the weight room (Nov 2026)

Follows `projects/rylan-noome` (the 300 m) and `projects/noome-400` (the race).

## Inputs (not committed)
- `raw/talking_head.mov`: 4K, 1:47. Voice declipped: 8,269 flat tops, 9,220 peaks rebuilt. Tightened 107.3 s → 102.1 s.
- `race_400.mov`: byte-identical to the noome-400 race clip, so I reused its Real-ESRGAN-enhanced `race_start_hd`/`race_finish_hd` (no re-upscale).
- `clip_nov08.mov`: Noome's power clean, vertical 1080×1920 at 60 fps, sharp at native res (used full-screen without enhancement).
- `photo_a.jpg` (1206×1629, blocks) and `photo_b.jpg` (2048×1365, high-kick warm-up): both enhanced to 4000 px with `enhance.py`.
- Also reused from noome-400: `race_card.mp4`, `race_full.mp4`, `arrived_hd.mp4`, `noome_relay_hd.jpg`.

## Structure
| part | content |
|---|---|
| Hook | Full-screen power clean, "DEEP TROUBLE?" |
| PART 1: THE 300 | Race card, 35.3 stopwatch, warm-up photo, "REDEMPTION?" |
| PART 2: THE 400 | Enhanced start, then the full-screen finish, 50.8 stopwatch, and prediction 51.0 vs result 50.8 |
| PART 3: THE WEIGHT ROOM | Gym clip, "TOO STRONG?", "1.5 DAYS LATER", full-screen clean, 135 KG counter |
| THE VERDICT | "STRONG, NOT FAST", poll "SHOULD HE CUT THE WEIGHTS? YES / NO" |

No name tag (owner rule).

## Data
- **50.8** (his 400 m) and the **51.0** prediction are the owner's numbers.
- **135 kg** power clean is the owner's number. The **≈298 lb** is my conversion (135 × 2.2046 = 297.6), and the owner says "around 300 pounds".
- The muscle-mass/lactic-acid point is the owner's opinion. It's in the voiceover only, with no graphic.
- Captions: "Ryland noon" → RYLAN NOOME, two swears softened.

## Freezes caught by the short-clip check
- `race_card` was too short for the 4.4–16.9 s segment (it would have frozen for 2.4 s). The relay photo now takes over at 12.0 s.
- The last race-card segment now starts from 0.
