# Is Noah Lyles a better 200 m runner than Usain Bolt? (Nov 2026)

## Inputs (not committed)
- `raw/talking_head.mov`: 4K (3840×2160 after rotation), 1:41, Dropbox folder link. No B-roll was supplied.
- `broll/`: all found on Wikimedia Commons, and all ≥1080p, so this plan runs the build's normal resolution check (no `skip_res_check`).
  - Every full-screen shot is a high-res photo: Bolt's pose, his portrait, the Rio 200 m win, the Jamaica flag and Gatlin.
  - The 1080p race clips are used in the split only.

## Steps
1. Crop the talking head to 2430×2160 at (585, 0) and scale to 1440×1280.
2. Declip the voice: 4,835 flat tops, 5,488 peaks rebuilt. Mux it onto the face, then `tighten.py`: 100.6 s → 93.2 s (20 pauses cut).
3. Transcript fixes:
   - "Noah laws" / "No allows" → NOAH LYLES.
   - "Justin gallon" → GATLIN.
   - "Johan" → YOHAN (Blake).
   - One swear softened in the captions only.
   - **"he's done it 15 times" is left as heard, and needs the owner's check** (see Data).
4. `python3 ../../editor/build.py plan.json`, then export at CRF 20 (91 MB, −14.6 LUFS).

## Data (no invented numbers)
- **Sub-20 200 m races (v2):** from the list the owner sent ("Most sub-20 200m races · men · all-time · all conditions", graphic by @Romar Asugao).
  - Lyles **50**, Bednarek **45**, Bolt **34**.
  - The owner confirmed he says "50" (Whisper heard "15"), and the caption is corrected.
  - The bars recreate the numbers. The list image itself isn't shown, because it's someone else's design and photo.
- **Bolt:** 200 m world record 19.19 (Berlin 2009). Olympic 200 m golds 2008, 2012, 2016.
- **Lyles:** 0 Olympic 200 m golds (bronze at Tokyo 2020, held in 2021, and Paris 2024). He has world 200 m titles, but the graphic only shows Olympic golds, which is what the owner says.
- **Gatlin:** Olympic 100 m 2004, World 100 and 200 m 2005, World 100 m 2017 (shown as the chips 2004 · 2005 · 2017).
- **Blake:** 200 m PB 19.26 (Brussels Diamond League, 2011).
  - Note for the owner: Blake *was* 2011 world 100 m champion, so "nothing to show for it" is a little strong. That's his opinion, and it isn't shown on screen.

## B-roll credits (Wikimedia Commons)
Paste this in the caption or a pinned comment:

> Photos/B-roll via Wikimedia Commons: Fernando Frazão/Agência Brasil (CC BY 3.0 BR); Arian Zwegers (CC BY 2.0); Neil (CC BY 2.0); Aeltegop (CC BY 4.0); jenaragon94 (CC BY 2.0); Kent Capture (CC BY 2.0); Ludovic Péron (CC BY-SA 3.0); Dickelbers (CC BY-SA 4.0); FISUTV (CC BY 3.0); World Athletics Championships 2015 (CC BY 3.0).

| file | Commons source | author | license |
|---|---|---|---|
| bolt_pose.jpg, bolt_finish.jpg | Bolt conquista tricampeonato também nos 200 metros … ffz-0001 / ffz-8112 (Rio 2016) | Fernando Frazão/Agência Brasil | CC BY 3.0 BR |
| bolt_portrait.jpg | Brussels, Memorial Van Damme, Usain Bolt (14697330331).jpg | Arian Zwegers | CC BY 2.0 |
| bolt_close.jpg | Usain Bolt (9394476568).jpg | Neil | CC BY 2.0 |
| lyles_paris.jpg, lyles_start.jpg | Noah Lyles - JO 03.08.2024.jpg; Noah Lyles JO 03.08.2024.jpg | Aeltegop | CC BY 4.0 |
| lyles_usatf_race.jpg, lyles_usatf.jpg | USATF day 2 2018 (28092336797 / 42963236801) | jenaragon94 | CC BY 2.0 |
| gatlin.jpg | Justin Gatlin-Men's 100m Final-London 2012 Olympics (8374272018).jpg | Kent Capture | CC BY 2.0 |
| blake_race.jpg, blake_close.jpg | Brussels, Memorial Van Damme, Yohan Blake (7957000656).jpg; Yohan Blake Memorial Van Damme 2012.jpg | Arian Zwegers | CC BY 2.0 |
| blake_portrait.jpg | Athletissima 2012 - Yohan Blake (2).jpg | Ludovic Péron | CC BY-SA 3.0 |
| jamaica_flag.jpg | Flag of Jamaica 03.jpg | Dickelbers | CC BY-SA 4.0 |
| univ200.mp4 | Athletics Men's 200 Final - 27th Summer Universiade 2013 - Kazan (RUS).webm | FISUTV | CC BY 3.0 |
| beijing100.mp4 | Shelly Ann Fraser Pryce wins - World Athletics Championships BEIJING 2015.webm | World Athletics Championships 2015 | CC BY 3.0 |

## v2 (owner feedback)
- **Audio was muffled.** The tone check showed 5–10 kHz air halved (0.33 → 0.15) and extra low end, caused by the de-esser, noise reduction and reduced presence EQ.
  - New default voice chain: low-mid cut and clarity/air lift.
  - The voice is now brighter than the raw recording: clarity 17.9 → 20.8, presence 2.9 → 4.9, air 0.28 → 0.41.
  - `audio_check.py` now runs after every render.
- **Stats:** the "15" caption is now "50", and the bars show Lyles 50 · Bednarek 45 · Bolt 34 (all conditions).
- The California and Rylan Noome videos were re-rendered with the same clear voice chain.
