# Jon Drummond: YouTube → vertical TikTok (Nov 2026)

The source is the owner's finished 16:9 YouTube edit ("Jon Drummond: He Wouldn't Leave The Track", 8:37, 1080p). It's voiceover with music, archive footage and widescreen motion graphics, and there's no talking head.

## Layout (`editor/vertical.py`)
- The full widescreen frame sits in the middle. It's scaled to 1180 wide with only the outer HUD corners trimmed, so it's never enlarged and stays sharp.
  - A full-screen 9:16 crop was tested and rejected: it cut every widescreen graphic in half and would have blown 1080p up 1.8×.
- Above the frame: a chapter header (title plus yellow subtitle) that animates in at each chapter.
- Below the frame: house-style word-by-word captions.
- At the bottom: a red progress bar and a "PART x / 11" label for retention on a long TikTok.

## Cut (8:37 → 6:41)
Cuts are at sentence boundaries, joined with 0.12 s crossfades:
- the "check it out" opener
- the Overbrook/JUCO bio
- the "where it ended" line in the hook
- the Sydney reaction aside (USATF statement, apology, emails, "my take")
- one restated rule detail
- the IAAF deadline detail
- the USATF CEO quote
- most of the closing recap

## Audio
The owner's mix is untouched. The cut measured −14.3 LUFS, so it gets a +0.3 dB static lift to −14 with a limiter. Nothing is turned down.

## Transcript fixes
- "John" → Jon
- "Gaye" → Gay
- "Maurice Green" → Greene
- "y 'all" and "eight -year" merged into single words
