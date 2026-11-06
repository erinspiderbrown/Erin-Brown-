# LSU 131, Texas Southern 22 (Nov 2026)

## Inputs
- `raw/talking_head.mov`: 4K, 87.6 s (Dropbox). This was the only file; all B-roll was sourced.

## B-roll (Wikimedia Commons, all 1080p or higher; credit required where noted)
Game footage:
- `game1-7.mp4`: 6.5 s cuts from "Superliga Femenina - Caribeñas Vs. Costaneras" (Venezuelan women's league broadcast, 1080p, public domain). They're cropped `[1920,880,0,0]` to hide the scoreboard bar.
- These are generic women's basketball, never presented as LSU or Texas Southern.
- `stef.webm`: "Stef hits foul line jumper against Penn State" by Sphilbrick, CC BY-SA 3.0.
- `adelphi.webm`: "Adelphi University Women's Basketball - Day in the Life" by GKess Films, CC BY 3.0.

Photos:
- `pmac.jpg`: LSU's Dale Brown-Sue Gunter Court (PMAC) by Spatms, CC BY-SA 4.0.
- `lsu01/05/19.jpg`: Kentucky vs LSU Lady Tigers (Jan 1, 2026) by Gold Broth, CC BY-SA 4.0. They show LSU's home court, not the Texas Southern game.
- `wnba1/2/4/25.jpg`: 2024 WNBA Finals Game 1 by Kew Gardens 613, CC BY-SA 4.0.
- `kids1/3.jpg`: "Basketball gateway to youth mentoring program" by Cpl. Paul Peterson (USMC), public domain.
- `umd3.jpg`: University of Maryland Women's Basketball Practice by MD Comptroller, CC BY 2.0. umd1 and umd2 aren't used because they show a public official.

## Facts on screen (checked: LSU Reveille, Bleacher Report, Yahoo Sports, ClutchPoints)
- Final 131–22, Nov 5, 2026. The 109-point margin is the largest in Division I history, beating Baylor's 140–32 win over Winthrop (108) in 2016.
- 2nd quarter: 40–0.
- Texas Southern: 38 turnovers, 8 of 55 from the field.
- The 50, 60 and 80 counters are the owner's hypotheticals, labelled "Losing by" with his quotes.
- "10 ON 5?" is his joke, shown as a question, not data.

## Steps
1. Transcribe with large-v3. Fixes: "slam-dunking", "three-point", "y'all". Swears are censored in captions only (f*ck, sh*t); the audio is untouched.
2. Crop the face to 2000×1778 at (863, 250), scale to 1440×1280, then run `tighten.py` (87.6 s → 82.4 s).
3. New motion kind `scoreboard`: arena LED board counts up to the final, with a FINAL lamp and a margin slam.
4. Render, then re-encode at `-crf 20` plus a `-crf 24` phone copy.

## Title
- **Recommended:** LSU beat Texas Southern by 109 points… how?? 😳
- Alt: 131–22. Is women's basketball even real?
- Alt: The biggest blowout in D1 history makes no sense

Caption:
LSU beat Texas Southern by 109 points… how?? 😳 #LSU #womensbasketball #collegebasketball #ncaa #blowout
B-roll: Wikimedia Commons (Gold Broth, Spatms, Kew Gardens 613, Sphilbrick, GKess Films, MD Comptroller)
