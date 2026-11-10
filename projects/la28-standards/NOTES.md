# LA28 entry standards: "athletes and fans are the dumbest" (Nov 10, 2026)

A long-form TikTok: 4:57, regular 9:16. Cinematic style: `"broll_grade": "cinematic"` (contrast, warm/cool split, vignette, grain), dissolves between full-screen shots, fade-through-black into each chapter, and slow push-ins on every photo.

## Inputs (not committed)
- `raw/talking_head.mov`: 4K, 5:11.
  - The voice was declipped: 38,798 flat tops.
  - Tightened to 4:57 (39 pauses). That needed the new low-memory `tighten.py`.
- `raw/photo.jpg`: the owner's LA28 standards chart (used as reference only).
- B-roll: Wikimedia Commons only (real photos and footage, free licences), plus reused 4K LA aerials and sprint clips from earlier projects.
  - Originals were rate-limited (HTTP 429), so photos came from Commons' cached 3840/1920 px thumbnails.
  - The Tokyo National Stadium photo only came at 1920 px, so it's enhanced to 4000 px with `enhance.py`.
  - Not obtainable (rate-limited originals): the Paris 2024 opening-ceremony horse video, two torch-relay clips, one Rio photo and the spikes photo. They're replaced with other ceremony and sprint shots.

## Josh Azzopardi
- Whisper skipped "Look at Josh Azzopardi from Australia. He's a 10.2, 10.3 guy." (about 4:17). I re-transcribed it in short chunks and spliced it in.
- Verified: he ran **10.41** in his 100 m heat at the Tokyo 2025 Worlds (6th, didn't advance). That's on screen as a stopwatch.
- **The crying interview was not found** in any coverage of Tokyo 2025 or his 2026 Commonwealth Games snub, which was an Instagram post. If it exists, it's broadcaster footage, which can't be pulled in. The owner can supply it.
- No photo of him is on Commons, so that section uses the Tokyo 2025 stadium and sprint footage.

## Data (all verified)
- **LA28 standards** (World Athletics, published Nov 10, 2026): 100 m 9.93, 200 m 19.95, 400 m 44.40, 800 m 1:43.00. **40% via standards, 60% via world rankings.**
- **"Old" standards:** the owner's 9.95 / "20 flat" / "44 mid" are the **Beijing 2027 Worlds** standards: 9.95 / 20.07 / 44.45. The graphics use the exact values, labelled "Worlds 2027".
  - Paris 2024 was 10.00 / 20.16 / 45.00 / 1:44.70.
  - The owner's "1:43.5" 800 m has no source match (Beijing 2027 is reported as 1:43), so there's no 800 m graphic.
- "High schoolers running 44.5" and "10.9 still gets in" are the owner's claims. They appear only as the keyword "HIGH SCHOOLERS", with no numbers.

## Structure
Hook (LA Coliseum, Rio opening ceremony) → PART 1: THE OLD STANDARDS → PART 2: THE OLDEST SPORT (Olympia, Greek vases, Discobolus) → PART 3: LA28 (100/200/400 m comparisons) → PART 4: THE 60% (opening ceremonies, ring) → PART 5: THE FANS → PART 6: EXHIBIT A (Azzopardi, 10.41) → THE BOTTOM LINE (poll "ARE THE LA28 STANDARDS TOO HARD?").

## Export
- The master is 680 MB.
- Shipped as a two-pass encode at 2.45 Mbps (`-tune film`), 97 MB. Side by side with the master, the difference is practically invisible.
- −13.5 LUFS.
- Thumbnail: `exports/la28_standards_thumb.jpg`, "9.93 TO QUALIFY?" / "LA28 STANDARDS" over the sprinter photo.

## B-roll credits (Wikimedia Commons)
> Photos/B-roll via Wikimedia Commons: Quintin Soloviev (CC BY 4.0); Ilgar Jafarov (CC BY-SA 4.0); Alexander Kachkaev (CC BY 2.0); Sgt. 1st Class Kula / U.S. Army (public domain); Ibex73 (CC BY 4.0); Dick Thomas Johnson (CC BY 2.0); Nick Webb (CC BY 2.0); dronepicr (CC BY 2.0); ArchaiOptix (CC BY-SA 4.0); Spurlock Museum (CC0); Livioandronico2013 (CC BY-SA 4.0); LeeMNichols (CC0); Chabe01 (CC BY-SA 4.0); Daieuxetdailleurs (CC BY 4.0); SprintsA11 (CC0); Oregon City High School (public domain); Habst (CC BY-SA 4.0); FISUTV (CC BY 3.0); World Athletics Championships 2015 (CC BY 3.0); the Dronalist (CC BY 3.0).
