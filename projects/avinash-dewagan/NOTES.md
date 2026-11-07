# Avinash Dewagan: 2nd at UIL 6A state as a sophomore (Nov 2026)

**Title (YouTube Shorts / TikTok):** Avinash Dewagan Is Just a Sophomore… and Ran 13:43 for 3 Miles 🤯
**Alternates:**
- This Texas Sophomore Just Took 2nd at State (14:39.8)
- 53 Seconds Faster in One Year — Avinash Dewagan Is Different

**Thumbnail** (3:4): `exports/thumbnails/avinash_dewagan_thumb.jpg`. It uses the owner's original race photo at native resolution, made by `thumbnail.py`.

**Export:** `exports/avinash_dewagan_tiktok.mp4` (1:12, crf 20).

## Inputs
These came from a Dropbox folder and are not committed.
- **Two talking heads (4K):**
  - **Clip B (10:21 PM):** the news intro ("Avinash Dewagan just delivered…"). It plays first.
  - **Clip A (10:15 PM):** the reaction ("Nah, he's actually different…"). It plays second, so the story runs news → reaction → future.
  - Each was tightened (B 39.0 → 35.0 s, A 42.0 → 37.2 s), then they were joined to 72.2 s.
- **Seven owner photos:**
  - The athletic.net and runfarusa live-results screenshots (1206×2622).
  - Five race and podium photos.
    - Three are 1206 px wide.
    - Two are **1206×804, below the 1080p rule**.
  - All five were AI-upscaled 2× (Real-ESRGAN general-x4v3) before use.
  - Full-screen shots use only the vertical photos: race, race, podium.
- **Online footage:** YouTube has the 2026 UIL 6A boys race (BryceMtn) and his Woodbridge race (Erik Boal Sports), but the download returned 403. Nothing was tried to get around it. See `footage_wanted.md`.

## Steps
0. **Match the two clips' loudness:** clip B was recorded at −17.8 LUFS and clip A at −12.1. Following the never-turn-down rule, B got one static +5.7 dB boost with a peak limiter (it lands at −14.1); A is untouched. The build then added the full-scale peak trim (−1.2 dB).
1. **Crop the face:** crop 2430×2160 at (670, 0), scale to 1440×1280.
2. **Fix the transcript:**
   - "Ivanage Deguan" → Avinash Dewagan.
   - "14, 30 something" → 14:30-something; "13, 40 something" → 13:40-something; "1343" → 13:43.

## Facts on screen (checked)
- **UIL 6A boys state 5K, Round Rock, Nov 2026:** 1. Ruel Newberry (Denton Guyer) 14:36.5, 2. Avinash Dewagan (Austin Vandegrift) 14:39.8, 3. Noah Garcia (El Paso Eastwood) 14:40.4. Sources: the live-results screenshot and Yahoo Sports.
- **2025 state as a freshman:** 17th, 15:32.7 (UIL / Statesman). That makes 52.9 s faster in 2026.
- **13:43 for 3 miles at the Woodbridge Classic:** the all-time sophomore class record (Vandegrift Voice, Oct 8, 2026).
- **Freshman track:** 3200m at the state meet, 7th in 9:23, a top-25 all-time mark for freshmen (Vandegrift Voice).

## Owner's wording vs. the record
- **"Top 25 in the nation as a freshman, from 9th graders to seniors":** the source says his freshman 3200 (9:23) was a top-25 *all-time freshman* mark, not a ranking against all grades. The board shows the sourced version; the captions keep his words.
- **"Most notorious performances":** kept as said. "Notorious" usually means infamous; he likely meant "historic".
