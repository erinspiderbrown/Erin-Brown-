# Flotrack paywall / Masai Russell (Nov 2026)

A reference project for the **guest soundbite** workflow.

## Inputs
These came in a Dropbox Transfer zip and are not committed:
- `talking_head.mov`: 4K, 74.3 s.
- `podcast.mp4`: 1080p, 59.6 s.
- `photo1.jpg`, `photo2.jpg` and `photo3.jpg`: Masai photos, all at least 1080 px on the short side.

## Steps
1. **Crop the face:** crop 2000×1778 at (880, 170), scale to 1440×1280, then run `tighten.py` (74.3 s → 71.6 s).
2. **Soundbite:** take podcast 32.75–37.95 s and 40.15–59.6 s, crop to 956×850 at (482, 0) to remove the lower-third banner, scale to 1440×1280, and raise by +2.6 dB to match the owner's voice.
3. **A-roll:** you 0–18.86 s, then soundbite A, then soundbite B, then you from 18.86 s to the end. Total 96.3 s.
4. **Captions:** podcast words shifted into the timeline; "flow track" merged to "Flotrack".
5. **Podcast as B-roll:** use crop `[1920,850,0,0]` to drop the banner.

## Notes
- All animations were hand-built `motion` graphics: `padlock`, `subscription`, `tv`, `flow` and `bubbles`. The owner asked for AI clips, but Higgsfield's free plan can't make 1080p video.
- The bubble texts are generic illustrative reactions, not real quotes.
