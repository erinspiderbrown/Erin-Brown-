# Grant Grosvenor (Nov 2026)

Talking head about Grant Grosvenor (ex-Oregon NCAA champ, 33, back running sub-4) and the Nathan Green podcast clip.

## Inputs (not committed)
- `raw/face.mov`: 4K talking head (Dropbox).
- `raw/vidA.mp4`: Grant's Instagram post "Addressing Nathan Green slander": podcast audio over track footage, then Grant to camera. **720×1280, below the 1080p rule.** Has burned-in captions, so it's cropped to `[720,640,0,290]` to keep them out.
- `raw/vidB.mp4`: training montage. **720×1280, below the 1080p rule.** Used because it's the only training footage the owner sent.
- `raw/p1.jpg` (hurdles, 1206×1690), `raw/p2.jpg` (forest, 2000×3000), `raw/p4.webp` (Nathan Green, 2040×2031).
- `raw/p3.jpg`: Oregon relay photo, **1024×777, below the rule.** Used in the split only (not full-screen) because it's the 2016 photo the story needs.

## Steps
1. Crop the talking head (displays 3840×2160) to `crop=2430:2160:600:0`, scale to 1440×1280, `tighten.py` (110.7 s → 106.5 s).
2. `splice.py`: insert vidA 13.90–20.55 s (6.65 s of Nathan Green on the podcast) after "…was on a podcast" (69.50 s). The face video holds a frame there; it's covered by full-screen B-roll. Total 113.3 s.
3. Transcript fixes:
   - Name from the bib: Grosvenor (whisper heard "Grozier").
   - "NC double-a" → NCAA, "147" → 1:47, "358" → 3:58.
   - Two words are censored in the captions only (audio untouched).
4. `python3 ../../editor/build.py plan.json`, then a two-pass 6000k encode to `exports/grant_grosvenor_tiktok.mp4` (88 MB; CRF 20 was still 121 MB).

## Interpretations (tell the owner)
- "147" is shown as 1:47 with no event named (it's almost certainly 800 m, but he doesn't say so).
- In the podcast clip, "I deserve his NIL" is the reading in context; an isolated re-transcription heard "I deserve it".

## v2 (merged house style)
- Your original voice (no EQ, compression or denoise), with one gain to −14 LUFS.
- Viral transitions are auto-picked. Graphics are silent, there are no bass hits and no riser, and the only sounds are quiet full-screen whooshes at least 3 s apart.
- Full-screen shots are sharp sources only:
  - p2 (2000×3000) for the opening and the 3:58 moment (a tighter crop the second time).
  - p4 (2040×2031, shown at roughly native size) for the podcast.
  - The 720p vidB and vidA clips are in the bottom half only.
- "What does that say about you" is now a split shot with Nathan's photo and a face punch-in, because there's no third sharp full-screen source.
- The podcast clip stays at 6.6 s and on Nathan's photo, as the owner asked, rather than the 15–25 s guest-soundbite default. The podcast's own footage is 720p track B-roll with burned-in captions, so it can't fill the top "speaker" slot.
