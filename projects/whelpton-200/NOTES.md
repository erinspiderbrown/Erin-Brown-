# "6'5 and ran 21.04?" Tiaan Whelpton's 200m (Nov 14, 2026), cinematic

## Inputs (not committed)
- `raw/talking_head.mov`: 4K, 1:59, dim lighting. No clipping (declip found 0 flat tops).
- Owner footage of Whelpton, all AI-enhanced with `enhance.py`:
  - `clip_a.mov`: the race, 640×360. Enhanced 22–34.3 s to 1920×1080; used in the split only.
  - `clip_a.mp4`: celebration, 720×900. Enhanced to 1536×1920, which is full-screen eligible.
  - `photo_a.jpg` (1440×1799) and `photo_b.jpg` (World Indoors, 1206×834): enhanced to ~4000 px.

## Talking head ("cinematic", fixing the lighting)
- Crop 2430:2160:745:0 → 1440×1280, then tighten: 118.9 → 103.7 s.
- Custom `face_grade` in the plan:
  - lifts shadows and mids with a curve, so the face is brighter;
  - warmer mids and a slight cool shadow;
  - light denoise and sharpen;
  - an off-centre vignette that darkens the backdrop.
- `broll_grade: cinematic`, fades on full-screen shots, and fade-to-black into the 200m section and the Whelpton reveal.

## Facts (verified)
- **Whelpton 200m: 21.04**, heat 3 win, Open Meeting #4, Hamilton, 14 Nov 2026 (Athletics NZ rankings, anzrankings.org.nz).
- **100m PB 10.10** (legal; Feb 2025 and Feb 2026). **10.01 wind-aided**, ITM Christchurch, 21 Feb 2026.
- **Bolt's height:** 6'5" (1.95 m).
- **Not verified:**
  - Whelpton at 6'5". His coach only says he's tall "like Usain Bolt was".
  - The bench 300 / squat 800 / clean 600 numbers.
  - These are shown as the owner's questions ("BENCH 300?"), never as data. The thumbnail avoids the height.
- **Owner's own stats:** 20.8 twice last season (sprained ankle; stress fractures in both shins).

## Transcript fixes
- "Teon Welton" → TIAAN WHELPTON.
- "10 -2" → 10.2; "20 .8" → 20.8; "Twenty-one" → 21.
- "bitch" softened to B*TCH in captions only.
- ~49 s: "20 point hurt" is left as heard; it was confirmed twice with a re-transcribe.

## Credits (Wikimedia Commons)
> Photos/B-roll via Wikimedia Commons:
> - 2025 Skelton Gym Powerlifting Competition (video and photos, US DoD, public domain)
> - 1st Lt. Nsikakabasi Ndem barbell squats (public domain)
> - Usain Bolt (broll3 set)
> - London 2012 200m heat 1 start (CC BY 2.0)
> - Glasgow Indoor Grand Prix (CC BY 2.0)
> - 2017 Canada Summer Games blocks (CC BY 2.0)
> - "Get set" (CC BY-SA 4.0)
> - Fractured tibia/fibula X-ray (CC BY-SA 3.0)
> - US Navy shin-splints photo (public domain)
> - Nike Vaporfly Next% photo, HK (CC BY-SA 4.0)
> - FISUTV Universiade 200m (CC BY 3.0)
> - Stopwatch and HS sprint photos (see `projects/california-sprints/NOTES.md`)
