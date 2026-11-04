# Taiju Goto (Nov 2026)

## Inputs
These came in a Dropbox folder link and are not committed:
- `talking.mov`: 4K, 73.4 s.
- `photo_flag.jpg`: 1080×1350. Goto in a Japan flag, with a Track Gazette "47.93 · U18 World Record" graphic baked in.
- `photo_timer.jpg`: 2048×1365. Goto next to the 45.33 timer.
- `photo_tweet.jpg`: 1170×1416. Screenshot of the Track & Field Gazette post. This is the source for every stat on screen.
- `race720.mov`: 52 s of phone footage from the stands, **1280×720**. **Not used**: it's below the 1080p rule and the owner hasn't approved it.

## Steps
1. **Crop the face:** crop 2430×2160 at (700, 0), scale to 1440×1280 at 30 fps. The face fills more of this frame than in earlier takes, so the crop is wider.
2. **Transcribe:** `medium.en`.
3. **Fix the transcript by hand:**
   - "Godo" → Goto.
   - "147" → 47.
   - "45 3" → 45.3, "13 6" → 13.6, "48 0 0" → 48.00.
4. **Cut the repeat:** the take opened with "47.9 in the 400 hurdles" twice. The first one (5.35–8.25 s) was cut.
5. **Tighten:** `tighten.py`, 70.5 s → 64.6 s.
6. **Render:** `python3 ../../editor/build.py plan.json`. The build output is 103 MB, so it was re-encoded with `-crf 20 -preset slow` to 65.6 MB.

## Data notes
- On-screen values are the precise ones from the Gazette post: 47.93, 45.33, 13.63 and 20.40. The owner said them rounded: 47.9, 45.3, 13.6, 20.4.
- The "48.5 / 48 flat" from earlier in the year is the owner's recollection. It stays in the captions only, with no data graphic.
- Record tags: 400mH 47.93 is the **World U18 record** and 400m 45.33 is the **Asian U18 record**, both per the Gazette post. The owner's line "the under-18 record in all those events for Japan" is shown only as a keyword ("UNDER-18 RECORDS"), not tagged on each event.

## New motion graphics (hand-built)
- `board`: a records board. Rows of event, time and an optional tag slide in, and `times` lands each row on the spoken word.
- `track`: a runner dot laps an oval while a clock counts up to `value`, then the label pops in. Used for "one lap = open 400".
