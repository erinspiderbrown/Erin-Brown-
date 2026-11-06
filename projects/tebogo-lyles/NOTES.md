# Tebogo vs Lyles: "stop playing opossum" (Nov 2026)

**Title (YouTube Shorts / TikTok):** Noah Lyles Just Exposed the Olympic Champion's Pattern 👀
Thumbnail: `exports/thumbnails/tebogo_lyles_thumb.jpg` (Tebogo's side-eye from the Athletissima 2026 press conference on top, Lyles' peace sign at Paris 2024 below, "OPOSSUM?" on the seam; made by `thumbnail.py`).
Alternates:
- Tebogo Called Out the Field… Then Lyles Clapped Back
- "Stop Playing Opossum" — Noah Lyles Goes After Tebogo
- Is the Olympic 200m Champ Sandbagging? Noah Lyles Thinks So

Talking head (4K) with the owner's two photos and a screenshot of the Tebogo/Lyles tweets. Built in the default Yohan Blake style.

## Inputs
- `raw4/p1.jpg`: Tebogo and Bednarek, Paris 2024 200m final (2200×1489). Split only.
- `raw4/p2.jpg`: Lyles in a wheelchair after the Paris 200m. **768×1024, below the 1080p rule, so not used**; flagged to the owner.
- `raw4/tweet.jpg`: the X thread. Shown with the new `tweet` motion graphic: real screenshot cards drop in with a 3D tilt, a thread line draws down, and a highlighter sweeps the key line on the spoken words.
- Wikimedia Commons photos (2560 px thumbnails, capped at 3200): see `CREDITS.md`.

## Steps
1. Crop `crop=2430:2160:665:0`, scale to 1440×1280, `tighten.py` (89.6 s → 85.3 s).
2. Transcript fixes: "Le to boho" → Letsile Tebogo, "Kenny been there" → Kenny Bednarek, "no allows" → Noah Lyles (×2), "amen" → man, "shit" → sh*t (caption only).

## Facts on screen
- Paris 2024 men's 200m final: Tebogo 19.46 (gold), Bednarek 19.62 (silver), Lyles 19.70 (bronze). Official results.
- Name tags: "PARIS 2024 · SILVER" (Bednarek) and "BRONZE" (Lyles).
- Nothing on screen quantifies the owner's opinions ("sandbagged", "millions"); they're keywords and stamps only. No 2026 season times are shown.
- The opening chat bubbles are illustrative, not quotes.
