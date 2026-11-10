# Matthew Boling: the downfall (Nov 2026)

**Title (YouTube Shorts / TikTok):** Matthew Boling Ran 9.98 at 18… So What Happened?

Alternates:
- They Called Him the Next Usain Bolt… 7 Years Later, Nobody Talks About Him
- "White Lightning" Was Supposed to Be the Next Bolt. What Happened?
- Matthew Boling: Downfall or Just Too Much Hype?
- 2x World Champion, 9.98, 19.92… Why Is Matthew Boling Forgotten?

## Source
The owner sent 8 voice-only recordings of the script (Dropbox, "Boling vid pt 1" … "Matt pt 7 (1)"). There's no talking head, so this is a documentary-style edit:
- **Full-screen:** high-res photos only (≥2560 px tall, never enlarged).
- **Split:** news footage on top, photos and footage on the bottom.

Story order: pt 1, part 2, pt 3–6, pt 7 (2025), pt 7 (1) (closing verdict).

## Audio (`assemble_voice.py`)
- The owner's voice is untouched: no EQ, compression or noise reduction.
- Pauses over 1.0 s are shortened to 0.65 s.
- Pt 1 was recorded hotter (−10.5 LUFS, peaking +0.8 dBFS). It gets only the minimum static trim to a −0.5 dBFS peak (−1.3 dB) and stays louder than −14.
- Parts 2–8 measured −14.6 to −15.6 LUFS. Each gets one static lift to −14 (+0.6 to +1.6 dB) with a peak limiter. Nothing is turned down.
- The finished voice track measures −13.9 LUFS with a −0.5 dBFS peak.

**Archival soundbites**, each set to about −16 LUFS so it sits just under the voice:
| Where | Clip |
|---|---|
| 0:00 | NBC Nightly News (2019): "He's a streak of lightning." |
| 0:45 | Boling to ABC13, the day after the 9.98: "My start was pretty good… keep pushing" |
| 1:57 | Boling to NBC: "Everything was super surreal. Like I didn't really know what I just did." |
| 2:00 | Chad Collier, his Strake Jesuit coach (NBC): "The bigger the stage, the bigger the performance." |
| 4:10 | Mark Boling, his dad (NBC): "If he says I'm going to the Olympics… I'll buy the tickets" |
| 5:33 | Boling to NBC: "I still have a lot of work to do if I want to get close to him" (Bolt) |

## Footage
- **NBC Nightly News**, "Track star goes from high school commencement to Olympic training" (2019, 1080p). Used in the split only, because 1080p landscape can't go full-screen.
- **Fox News / NFHS Network broadcast** of the 9.98 regional race (720p). AI-upscaled with `editor/upscale.py`; split only.
- **ABC13 Houston**: the @mgernander phone video of the 9.98 and the Boling interview (360p). AI-upscaled; split only.
- **Photos**: Wikimedia Commons; see `CREDITS.md`.

**Copyright:** the news clips are copyrighted broadcast footage, used briefly with commentary. That's a fair-use argument, not a license. TikTok/YouTube can still flag them. If a clip gets claimed, swap it for the matching Commons photo.

YouTube race footage (the 44.74 anchor, the 10.13, the 19.92, Budapest) can't be downloaded from the cloud session; see `footage_wanted.md`.

## Facts on screen (checked)
- **Apr 27, 2019:** 100 m, 9.98 (+4.2 m/s, wind-aided), UIL 6A Region III meet, Webster (Houston area). The real scoreboard was blurry, so it's rebuilt with its real results:
  - 1 Boling 9.98
  - 2 Lance Broome (Katy Seven Lakes) 10.27
  - 3 Dorian Hewitt (North Shore) 10.33
  - 4 Cameron Crowe (Cypress Ridge) 10.47
- **2019 UIL 6A state meet:**
  - 100 m 10.13, wind-legal U.S. high school record
  - Long jump state title 25'4.5" (wind-aided); PB 26'3.5" at the Texas Relays
  - 4x400 anchor split 44.74 from 20+ m back
- **2018–19 Gatorade National Boys Track & Field Player of the Year.**
- **2019 Pan Am U20s (San José, Costa Rica):** 100 m 10.11, 200 m 20.31, 4x100 38.62 (WU20R), 4x400 2:59.30 (WU20R).
- **2021:**
  - NCAA indoor 200 m champion, 20.19
  - Olympic Trials: 100 m 14th (semis), 200 m 9th (semis)
- **2022:**
  - 9.98 (+1.6) at the Tom Jones Memorial, Apr 16
  - 19.92 at the Georgia Tech Invitational, Apr 23
  - SEC 200 m champion, 20.01
  - NCAA 200 m 2nd, 20.13
  - USATF 200 m 6th, 20.15
- **2023:**
  - NCAA indoor 200 m champion, 20.12
  - NCAA outdoors: out in the semis
  - USATF 400 m 6th, 45.17
  - Budapest Worlds: mixed 4x400 gold in a world record 3:08.80 (3rd leg); ran the men's 4x400 heats, and the team took gold
- **Sept 2023:** turned pro; trains in South Carolina under Alleyne Francique.
- **2024:**
  - 400 m PB 44.84
  - World Indoor 4x400 silver
  - World Relays gold
  - Olympic Trials: 400 m final 8th (45.15; Quincy Hall won in 44.17); 200 m 9th, no final; not picked for Paris
- **2025 Grand Slam Track Philadelphia:** 200 m 7th (20.87), 400 m 5th (45.21).
- **PBs:** 9.98 / 19.92 / 44.84.

## Where the script differs from the record (owner, please check)
- **"Jumping 26 feet":** his state long-jump title was 25'4.5" (wind-aided). 26'3.5" was his PB at the Texas Relays. The graphic shows both.
- **"Gatorade National Athlete of the Year":** the award is Gatorade National *Boys Track & Field* Player of the Year. The graphic uses the real name.
- **"A couple weeks later he runs 19.92":** it was one week later (Apr 16 → Apr 23, 2022). The graphic says "1 week later".
- **2024 order:** the 44.84 PR came on July 19, after the Trials (June). The script implies it came before. The graphic just says "400M personal best · 2024".
- **"That year he ran 45.51":** I couldn't verify a 45.51 in 2025. 45.51 matches his 2021 indoor PB. Grand Slam Philly results show 45.21, which is what's on screen. The voice still says 45.51.
- **"The kid that ran 9.98 at 18… his best today is still 9.98":** true, but the 9.98 at 18 was wind-aided. His legal 9.98 came in 2022 at 21. The compare graphic labels them "AT 18 (WIND+)" and "TODAY (PB)".
- **"Two-time world champion":** both are relay golds; he ran the heats of the men's 4x400. The resume board says "RELAYS".

## Sources
- Wikipedia (Matthew Boling)
- Gatorade POY page
- MileSplit (44.74)
- LetsRun (2019 state meet)
- ESPN (turning pro)
- AJC (2024 Trials 8th)
- Watch Athletics and LetsRun (Grand Slam Philadelphia)
- World Athletics (mixed relay record ratified)
- Fox News broadcast scoreboard (Region III results)
