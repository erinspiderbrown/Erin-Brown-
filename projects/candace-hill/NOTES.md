# Candace Hill: did she finesse ASICS? (Nov 2026)

**Title (YouTube Shorts / TikTok):** She Ran 10.98 at 16 and Got a 10-Year Deal… Did She Finesse ASICS?

Alternates:
- 16 Years Old, 10.98, 10-Year ASICS Deal… Then She Never Ran Faster
- Candace Hill Got the Bag at 16. Did ASICS Lose the Bet?
- The Fastest High School Girl Ever Signed a 10-Year Deal. What Happened?

## Source
- **Voiceover:** 8 recordings from Dropbox `/Candace` (Candace 1, 2, pt 3, 4–8), assembled in order by `assemble_voice.py`.
  - Pauses over 0.62 s are shortened to 0.42 s, then the flub cuts and silence pass below bring it to 5:26.
  - Each part measured −15.4 to −19 LUFS, so each got one static lift to −14 with a limiter, as the house rule allows. No other processing, and nothing turned down.
- **No video:** the race clips (FloTrack, MileSplit), the news pages and YouTube couldn't be downloaded from the cloud session, so the edit is built from photos plus place scenes. See `footage_wanted.md`.
- **Photos:**
  - **Full-screen (sharp, never enlarged):**
    - NBC Sports / Getty portrait in her USA kit (4458×3007)
    - World Athletics flag shot at the 2015 World Youths (5215×3477)
    - AJC training shot (3000×1869)
    - World Athletics 2021 feature portrait (2800×1867)
  - **Split only:** the SI 10.98 finish (3000×1584) and the Refinery29 blocks shot.
  - **AI-upscaled (Real-ESRGAN), split only:** World Athletics' 2016 World U20 win, two 2015 Brooks PR shots, and the 2021 close-up.
- **Place scenes (`make_maps.py`):** Natural Earth outlines filled with the US / Colombia / Poland flags, with a city dot. Shoreline WA, Conyers GA, Cali, Bydgoszcz, California, Baton Rouge.

## v2: rebuilt around video (owner: "it didn't include any videos")
YouTube, FloTrack and MileSplit block downloads from the cloud, but Dailymotion mirrors several Candace Hill videos. These are now the top half of most of the split, AI-upscaled (Real-ESRGAN, 640 px input) because they're 720p or lower:

**The footage:**
- **beIN Sports / Express Xtra athlete profile (2016):** training, starts, runs, studying at home, coach Tony Carpenter, and the Cali 2015 race and flag celebration. The broadcast ticker is cropped off.
- **El País TV (Colombia), Cali 2015:** the race, the flag lap and the podium.
- **USATF 2016 junior-title interview** and **2017 goals interview:** used as B-roll only, without their audio.

**Soundbites cut into the voiceover**, each lip-synced in the top slot with the `podcast` mic badge:
- **A (after the intro), Candace:** "My name is Candace Hill. You don't know me yet, but you soon will."
- **B (after Cali), Candace:** "I cried, I really cried after my 100… wow, I'm a real world champion."
- **G (after the deal), Tony Carpenter:** "I think Candace Hill has the potential to be the greatest female sprinter ever, period."
- **C (after "missed four months"), Candace:** "…you need surgery and you'll be out for four months… dang… this is not going well."
  - Audio only, from a 288p interview, so it plays over training footage.
- **F (before the mental-health part), Tony Carpenter:** "the most important thing for her going to the next level is really on the mental side."

**Length:** 6:07 with the soundbites (5:26 without them).

**Races with no downloadable footage are animated race recreations** (`race_recreation.py`, labelled "RACE RECREATION" on screen; owner: "the videos that you don't have, just get creative"):
- **The 10.98 (Brooks PR 2015):** Hill against an 11.00 ghost runner, "the 11-second barrier". Used in the hook and again on "wasn't no fluke". Her real time; the ghost is a reference line, not a real runner.
- **2016 World U20 100 m final, Bydgoszcz:** all 8 finishers with official times (Hill 11.07, Swoboda 11.12, St Fort 11.18, Lansiquot 11.37, Rivera 11.59, Brier 11.60, Jasim 11.60, Ntia-Obong 11.79). Lane order isn't from the record, so it's marked "LANES ILLUSTRATIVE".
- The runner motion between start and finish is a sprint-curve model; only the finish times are real.
- **2024 Olympic Trials final:** real NBC broadcast footage (NBC Miami), in the split.

## Owner's flubs removed (`CUTS` in `assemble_voice.py`, then `tighten_voice.py`)
- **Part 3:** "ASICS ain't never *signed* the number" is cut. The restart "ASICS ain't never say the number" is kept.
- **Part 6:** hesitations before "Baton Rouge" (1.4 s), before "2024" and before "Olympic Trials" are cut.
- **Every silence over 0.7 s** (22 of them, including hesitations the transcriber hid inside long words) is shortened to 0.5 s.
  - That brings the video from 5:43 to 5:26.
- **Checked and left alone:**
  - "2017, 2018, 2019" in part 4 is clean, each burst checked separately.
  - Part 2 has one "sophomore", not two.
  - "Miles Smith" is how the owner said MileSplit; it's fixed in the captions only.

## Facts on screen (checked)
- **10.98 at the Brooks PR Invitational, Shoreline WA, June 2015, age 16:** the first high school girl under 11. (Wikipedia gives both June 20 and June 21.)
- **2015 World Youths, Cali:** 100 m 11.08 and 200 m 22.43, both golds.
- **Gatorade National Girls Track & Field Athlete of the Year, 2015.**
- **Signed with ASICS Dec 17, 2015, on a 10-year deal:** the youngest U.S. track athlete to turn pro.
  - The terms were never confirmed. MileSplit's source said six figures a year for 10 years with no reductions. ASICS also reportedly covered college tuition.
- **2016:**
  - Olympic Trials: 13th in the 100, 14th in the 200
  - World U20s, Bydgoszcz: 100 m gold in 11.07, plus 4x100 gold
- **2019 USA Championships:** 14th in the 100, 14th in the 200.
- **May 2021 World Athletics feature:** the "wrong decision" and "second-guessing" quotes, and her therapist on emotional issues becoming physical pain.
- **2021 Olympic Trials:** 100 m final, 11.23.
- **2024 Olympic Trials:** 100 m final, 7th in 11.00.
- **PBs still from 2015:** 10.98 and 22.43.

## Where the script differs from the record, or isn't verified
- **"2021 Trials… finals, 8th":** Wikipedia says 8th (11.23); Track & Field News lists her 9th. Hayward has 9 lanes. The board shows "100M FINAL 11.23" without a place.
- **"10.99 with a +2.5 wind, July 2021, California":** a 10.99 (2021) appears in her season list, but I couldn't confirm the meet or the wind reading.
- **"Only other sophomore to win Gatorade was Marion Jones":** not verified. It isn't shown as a graphic.
- **Not verified, voice only, no number on screen:**
  - "Five different coaching changes by 2023"
  - "Three years left on the deal in 2023"
  - "Pre-med"
- **"Miles Smith reported":** that's MileSplit, and the caption is corrected.
- **"When dated":** wind-aided (caption corrected).
