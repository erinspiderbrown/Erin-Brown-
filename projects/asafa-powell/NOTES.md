# Asafa Powell: fastest man without an individual gold (Nov 2026)

**Title (YouTube Shorts / TikTok):** 97 Times Under 10 Seconds… and Asafa Powell Never Won Individual Gold 💔
Alternates:
- He Broke the 100m World Record 4 Times… But Couldn't Win When It Counted
- Asafa Powell Ran 9.74 in the HEATS… and Still Never Won Gold
- The Fastest Man Alive, Until the Lights Came On: The Asafa Powell Story

## Owner feedback on the narration (most recent first)
- **v3: APPROVED.** "Okay, I like that one. Set that as the default voice used for my YouTube videos and my TikTok videos." This is now the house default (see CLAUDE.md, ElevenLabs narration). It's in `exports/` and Dropbox.
  - Redone with the **approved Jon Drummond recipe** read straight from his ElevenLabs flow `EwtCtvyEoktyTmEPgx7r`. That means `eleven_v4`, stability 0.45, similarity 0.85, `[calm] [relaxed] [Texas accent]` on every paragraph, `[pause]` before beats, dropped g's, and 7 short sections (`script_v4_sections.txt`, flow `W4Hc1NpmegUzmpwft2jt`).
  - Owner: "The last two just weren't it… In the John Drummond video, that was much better. Why can't you be consistent?"
  - Measured pace: Drummond holds 164 wpm from the first second. Asafa v1 opened at 182 wpm, v2 at 194 wpm.
- **v2** (`eleven_multilingual_v2`, stability 0.75, style 0, script `script_v3_part*.txt`, calmer delivery plus stadium/crowd/reporter beds): **"horrible"**. This is the version currently in `exports/` and Dropbox.
- **v1** (`eleven_v4`, default settings, dialect script `script_v2_part*.txt`): **slightly too fast at the beginning, then "really decent"**. This is the reference for future ElevenLabs narration. It's in git history at commit 097f953 (`exports/asafa_powell_tiktok_hq.mp4`) and can be restored.
- The first, too-proper script (`old/`) was rejected before it was used.
- The owner said not to proceed further on this video for now.

## Format
- **Length:** 5:34, vertical 1080×1920, full-screen photos the whole way.
- **No talking head:** the owner's ElevenLabs voice ("Erin Brown", `eleven_v4`) narrates, at his request.
- **Script:** written in the owner's own dialect and slang, modelled on his real transcripts (Klan, Yohan Blake, Drummond, 200m):
  - phrases like "Man, let me tell y'all", "he ain't even make it to the final", "Where he finish? Fifth.", "Make it make sense"
  - times said the track way ("nine seventy-four"), "4x1", "worlds"
- **Script files:**
  - `script_v2_part1.txt` and `script_v2_part2.txt`: split because ElevenLabs takes at most 5,000 characters per generation.
  - `old/`: the first, too-proper version, which the owner rejected.
- **Takes used:** part 1 take A and part 2 take B. The other takes slipped out of dialect ("how *are* you", "*Meh*, let me tell y'all", "*they're* supposed to be").
- **Pauses:** 19 natural pauses at section breaks were lengthened by 0.75 s for dramatic beats and to clear 5:30.
- **Voice level:** the ElevenLabs master is about -24 LUFS. The build raises it to -14 with a peak limiter, the house path for quiet takes.

## Framing (owner's rule)
Only **individual** World Championship / Olympic golds count. Commonwealth Games, the circuit and other meets are not presented as titles.
- Relay golds are real, so the script mentions them (Berlin 2009 anchor, Rio 2016 lead-off) but treats them as not the one that counts.
- The Beijing 2008 4x1 gold was stripped in 2017 after Nesta Carter's retest.
- **Correction to the owner's brief:** Powell's best individual global finishes were two **bronzes** (Osaka 2007, Berlin 2009), not silver.

## Facts on screen (checked)
- **Sub-10 runs:** 97, the most ever. His last came 1 Sept 2016. *(NBC Sports, Wikipedia)*
- **World records (all at regular meets):**
  - 9.77 Athens, 14 Jun 2005
  - =9.77 Gateshead, 11 Jun 2006
  - =9.77 Zurich, 18 Aug 2006
  - 9.74 Rieti, 9 Sep 2007. This came in the **heats**; he won the final in 9.78.
- **Global 100m record:**
  - 2003 Paris worlds: false start in the quarterfinal, DQ.
  - 2004 Athens Olympics: 5th, 9.94.
  - 2005 Helsinki worlds: missed with a groin injury.
  - 2007 Osaka worlds: bronze, 9.96. Gay 9.85 won and Atkins (his cousin, BAH) took silver in 9.91.
  - 2008 Beijing Olympics: 5th, 9.95. Bolt 9.69, Thompson 9.89, Dix 9.91.
  - 2009 Berlin worlds: bronze, 9.84. Bolt 9.58, Gay 9.71.
  - 2011 Daegu worlds: withdrew (groin).
  - 2012 London Olympics: crossed last in 11.99. He is officially 7th after Tyson Gay's results were annulled; "dead last" is still true.
  - 2015 Beijing worlds: 7th in the final.
- **2008 season:** first man to run sub-10 fifteen times in one season. His lifetime best was 9.72 in Lausanne on 2 Sep 2008, 17 days after the Olympic final ("like two weeks later").
- **Bolt's record:** Bolt took the WR at 9.72 in New York on 31 May 2008.
- **Relays:**
  - Berlin 2009 4x1 gold, Powell anchoring.
  - Rio 2016 Olympic 4x1 gold, Powell leading off the final (Powell, Blake, Ashmeade, Bolt, 37.27).
- **Quotes:**
  - Powell after Osaka: "When Tyson came on and gave me a little bit of pressure I just panicked."
  - Michael Johnson on Osaka: "You could see him thinking, I'm losing it, I'm losing it, and he just gave up."
  - Powell after Beijing: "I've got no idea why I'm always winning on the circuit but then finishing fifth at the Olympics."
- **2013 doping case:** positive test for oxilofrine, which he said came from a supplement. JADCO banned him for 18 months; CAS cut it to 6.
- **Beijing relay gold:** stripped in 2017 when Nesta Carter's retest came back positive.
- **Family:** born in Spanish Town, the youngest of six sons, and both parents are ministers. Brother Michael was shot dead in a New York taxi in 2002, and brother Vaughn died of a heart attack about a year later. Coach Stephen Francis at MVP from 2001.
- **"9.72 or faster" board (all-time list as of July 2026):** Bolt 9.58, Gay 9.69, Blake 9.69, Powell 9.72. Bolt, Gay (2007) and Blake (2011) all won individual world/Olympic 100m titles; Powell is the only one without one.

## Media
High-res photos from Wikimedia Commons (credits in `CREDITS.md`).
- **Downloads:** 3840 px renditions where available, never enlarged past native size.
- **Video:** no freely licensed Powell race video exists on Commons. YouTube can't be downloaded from the cloud session. Pexels (4K stock) is blocked until the owner fixes the key format.
