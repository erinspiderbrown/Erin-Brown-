# 400 tips for a high school senior (reply to WTFQuincy) (Nov 2026)

**Title (YouTube Shorts / TikTok):** How I Went From 56 to 48 in the 400 by Changing One Thing 🏃
**Alternates:**
- 5 Ways to Run the 400… Only One Got Me Under 49
- High Schoolers: Stop Running the 400 Like This

A talking head replying to a comment, in the house style (Yohan Blake / Tebogo).

## Inputs
- `raw/talking.mov`: 4K, 143.7 s.
- `raw/photo.jpg`: the WTFQuincy comment screenshot (1206×280). It's shown with the `tweet` card graphic, and the highlighter sweeps "me in the 400 as a senior in highschool".
- **Race videos:** the owner linked two, the first 49 (2018 SW AAU Region 18 qualifier, 400m, 15–16 boys) and the 47.1 Conference Final on YouTube.
  - YouTube returned 403 on the media download from the cloud session. Per the house rule, nothing was tried to get around it.
  - The owner was asked to add the files to Dropbox. **When they arrive, they go in the split at the attempt-4 (≈79–92 s) and attempt-5 (≈94–108 s) sections.**
- **B-roll meanwhile:** Wikimedia Commons 400 m photos (see `CREDITS.md`) plus the owner's two NCAA photos.

## Steps
1. **Crop the face:** crop 2000×1778 at (890, 330), scale to 1440×1280, then run `tighten.py` (143.7 s → 135.4 s).
2. **Fix the transcript:**
   - "WTF Quincy" → WTFQuincy, "down pack" → down pat, "175 180" → "175, 180".
   - "49 5" → 49.5, "48 for" → 48.4 (interpreted, see below).
   - "shit" → SH*T in the captions.
3. **New motion graphic, `raceplan`:** a 400 m lap where the coloured zones of each strategy fill in as a runner dot goes round, with the time revealed as he says it.

## Numbers on screen (all as the owner said them)
- Attempts 1–5: 56, 54, 53, 49.5, 48.4. Attempt 4 is his first sub-50 and attempt 5 his first sub-49.
- **"48 for" is interpreted as 48.4.** Confirm with the owner.
- The race-plan zone splits (HARD 0–150, SHUT IT DOWN 150–250, HIT IT 250–400; PUSH 0–180, CHILL 180–200, HIT IT 200–400, etc.) are drawn from his description of each plan.
