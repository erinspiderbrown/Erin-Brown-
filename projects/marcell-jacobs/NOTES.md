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
- No free photo of Giacomo Tortu exists: name tags never sit on an unidentified person; when he's named, the screen shows Filippo labelled
  "NOT ACCUSED" or neutral footage.

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
