# Marcell Jacobs: the strange case (Nov 2026)

**Title (YouTube Shorts / TikTok), suggested:** Olympic Champ Hacked by His Teammate's Brother? The Marcell Jacobs Case
(vidIQ short-form score 84, 71 chars; matches the thumbnail. "marcell jacobs" ~3.5k searches/month; "100m" 57k, "olympics" 32k.)
Alternates (vidIQ score):
- Marcell Jacobs Won Gold… Then His Teammate's Brother Allegedly Hacked Him (scored 88 as "…Won Olympic Gold…", 81 chars; shortened here)
- Someone Allegedly Paid €10,000 to Hack the Olympic 100m Champion's Phone (scored 88 without "Allegedly"; keep it, it's an allegation)
- From 10.03 to 9.80… Was Marcell Jacobs Clean? (78)

**Thumbnail** (`exports/thumbnails/marcell_jacobs_viral_thumb.jpg` 3:4 / `_916.jpg` 9:16): rebuilt from his YouTube cover photo (Jacobs, hands on
head; used at native size, edges fading to black instead of a cut-out because rembg tore the dark arm), hook "OLYMPIC CHAMP / HACKED? / BY
TEAMMATE'S BROTHER", Polaroid of his Tokyo 9.80 celebration (still from his video). Filippo Tortu deliberately kept off the thumbnail.
Source: `thumb_viral/` (template now takes the hook lines as layout data).

## Source and cut
- Owner's YouTube video "The Strange Case of Marcell Jacobs" (Aug 2026, https://youtu.be/X6xEs2KnZHI, 10:17), file via Dropbox folder link,
  `raw/source.mp4` (1920x1078, not in git). All narration is his (no separate interview audio in this one).
- `cut_voice.py`: 18 ranges of his original voice, same plot order → 6:59. Removed the roadmap ("So today we're going through…"), "people
  weren't necessarily saying he cheated", Spazzini's sanction/appeal details, the 2022 titles run-down, the USB-drive chain, one of the two
  "$10,000" lines. Captions: `fix_captions.py` (10.03/9.95/9.94/9.84/9.80/9.85, Marcell, Kerley, Spazzini, Tortu, Pegoraro).
- Voice: house `polish` chain (owner-approved default).

## Visuals (owner: "a lot of vertical video and photo B-roll… really professional")
- His footage is already soft (YouTube-grade); a neural 2x upscale didn't make 9:16 crops sharp enough for full-screen (tested), so it
  plays in a square band at native size. Photos carry the vertical look: 52% of screen time.
  - Full-screen 9:16 (high-res Commons): Jacobs at the Paris 2024 final, Filippo Tortu ×3, Kerley, Paris 2024 finalists (Lyles, Thompson,
    Seville, Tebogo).
  - Near-full-screen 9:10 band (1080x1200, native size): Jacobs Belgrade 2022, with his child, Istanbul 2023, Rome 2024 medal,
    with President Mattarella, Budapest/Rome relays.
- Commons refuses original files (429) and only serves standard thumbnail sizes (1920/3840) to tools; photos 2800–3500 px wide come as
  1920 px, too small for full 9:16, hence the 9:10 band for them.
- Giacomo Tortu photo (owner's decision, Nov 9 2026): `photos/giacomo_tortu_corriereumbria.jpg`, the lead image of Corriere dell'Umbria's
  profile "Giacomo Tortu, chi è…" (no caption naming the person). Caveat told to the owner: his own YouTube video shows the same photo while
  saying Filippo is not accused, and it may be Filippo. Mitigations: always labelled "PER ITALIAN MEDIA · ALLEGED, NOT CONVICTED"; only on
  beats where his voice names Giacomo (0:49, 5:02, 6:26); Filippo appears only with "NOT ACCUSED"; the ending shows Jacobs, not a Tortu.
- Added facts (owner approved): closing "SINCE THEN (OCT 2025)" board: FIDAL tribunal banned Giacomo Tortu 36 months; the USB stick he got
  was empty; the tribunal said his doping suspicions had no factual basis (Jacobs never investigated for doping). Source: Il Post, 9 Oct 2025.

## Facts (checked; ANSA 9 Apr 2026, LaPresse)
- Jacobs: 100 m PB entering 2021 10.03 (2019); 9.95 Italian record (May 2021); Tokyo heat 9.94, semi 9.84, final 9.80 (Kerley 2nd 9.84);
  first Italian Olympic 100 m champion; Paris 2024 final 5th, 9.85.
- Equalize case: prosecutors allege Giacomo Tortu paid **€10,000** to hacker **Gabriele Pegoraro** for access to the phones of Jacobs, his
  coach, manager and nutritionist, covering **Sept 2020 – Aug 2021** (one Italian report says to Oct 2021). April 2026: 81 suspects named
  at the close of phase 2; he could face trial; allegations, not a conviction. Filippo Tortu is not under investigation.

## Where the owner's narration differs from the record (graphics show the record; his audio is unchanged)
- "$10,000" → it's €10,000 (euros).
- "September 2000 through August 2021" → September 2020.
- "Gabriel Pergraro/Progaro" → Gabriele Pegoraro.

## Export (Nov 9 2026)
- `exports/marcell_jacobs_tiktok_hq.mp4` (Git LFS): 7:10.6, 1080x1920, 30 fps, two-pass 7 Mbps, SSIM 0.996 vs master; audio copied (256k AAC).
  His voice: `polish` chain; the take measured -17.7 LUFS, so one static +3.7 dB boost to -14.0 LUFS with a limiter (peak -1.5 dBFS).
- 81 shots: 12 true full-screen photos, 69 in the framed band (near-full-screen 9:10 photo crops, his footage as a square band);
  photos fill 56% of the runtime. 64 graphics. 12 quiet whooshes on the full-screen cuts.
- build.py fix found on this edit: `fit: frame` segments used to count as full-screen, so no whooshes and only whip/glitch
  transitions; now band <-> full-screen cuts get the in/out transitions and the whoosh.
- Dropbox `/TikTok Exports/`: video + `marcell_jacobs_viral_thumb.jpg` + `_916.jpg`, content_hash verified on all three.
  Private link: https://www.dropbox.com/scl/fi/et6i5z2gi5pkvo2yvdqdo/marcell_jacobs_tiktok_hq.mp4?rlkey=wlmn69fylrcrrckyisysjj9fw&dl=0
