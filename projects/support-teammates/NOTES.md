# Support your teammates' content (Nov 2026)

**Title (YouTube Shorts / TikTok):** Athletes: Reposting Your Teammates Is Free… and It Pays Off 🤝
**Alternates:**
- You're One Handshake Away From a $1M Opportunity (Athletes, Listen)
- Why Every Track Athlete Should Repost Their Teammates

**Thumbnail** (3:4): `exports/thumbnails/support_teammates_thumb.jpg`. It's the GB women's 4×400 relay celebrating (Osaka 2007, Commons, CC BY 2.5) with "REPOST IT", made by `thumbnail.py`.

**Export:** `exports/support_teammates_tiktok.mp4` (1:09, crf 20, 65 MB).

## Inputs
- `raw/talking.mov`: a single 4K talking head, 73.2 s. It was tightened to 68.6 s, and the order was kept as recorded because it already reads logically: opportunity → support → how (repost, reshare, like, comment) → why (free, more eyes, handshake away) → costs nothing → call to action.
- **B-roll:**
  - The owner sent no B-roll, so the photos come from Wikimedia Commons: the GB 4×400 relay celebrating, plus the 400 m photos already credited on the 400-tips video. All are listed in `CREDITS.md`.
  - The owner's two NCAA photos are also used.
  - Commons rate-limited the search (HTTP 429), so no more photos were pulled.

## Steps
1. **Crop the face:** crop 2430×2160 at (715, 0), scale to 1440×1280, then run `tighten.py`.
2. **Voice:** −13.0 LUFS, so it's untouched except the full-scale peak trim (−0.5 dB).
3. **New motion graphic, `engage`:**
   - Social action buttons (repost, share, like, comment, save) light up on the spoken word, with a "+1" float.
   - No counts are shown, so nothing is invented.

## On-screen claims
- No stats. "$1M OPPORTUNITY" and "1 HANDSHAKE AWAY" are the owner's saying, shown as keywords and stamps, not as data.
- The comment bubbles are illustrative, not real quotes.
