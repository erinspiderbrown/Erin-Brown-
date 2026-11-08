# Steve Prefontaine: the tragic death of America's greatest distance runner (Nov 2026)

**Title (YouTube Shorts / TikTok):** He Won a Race at Hayward… Hours Later, Steve Prefontaine Was Gone 💔
Alternates:
- Every American Record From 2K to 10K… and Steve Prefontaine Died at 24
- 0.8 Seconds From a Medal… The Steve Prefontaine Story
- If Pre Made It to Montreal '76… Was He Winning Gold?

## Format
- ~5:30, vertical 1080×1920. No talking head: the owner's default ElevenLabs voice narrates (approved Drummond recipe, see CLAUDE.md).
- Voice: flow "Steve Prefontaine voiceover (Drummond recipe)" `j3DrD1suS4c21E2NTzTa`, 8 sections (`script_sections.txt`), `eleven_v4`,
  stability 0.45 / similarity 0.85, `[calm] [relaxed] [Texas accent]` on every paragraph.
- Takes kept: 01a 02b 03a 04b 05b 06b 07b 08a. Rejected: 03b (repeats "it was his house" ×3 at the end), 08b ("24 years old" twice).
- Pace: opening 150 wpm over the first 20 s (Drummond ~164 steady). Section 03 read fast (~187 wpm, dense text), so its natural pauses got
  +0.32 s each instead of re-generating; other sections +0.1–0.22 s. 1.5 s breath between sections. Built by `assemble_voice.py` → `voice_master.wav` (5:29).
- **Reenactments (owner-approved budget, ~64k credits):** ElevenLabs `ltx-v2-fast`, 6 s each, no audio, flow `lkcp4S1Cw4Xvf55RVbbx`.
  8 at 4K (full-screen hero moments) + 12 at 1080p (framed middle band only, per the 1080p rule). Files in `reenact/`.
  - Dropped: `04_munich_lastturn` (garbled AI banner text). `06_memorial_rock` used for its first 2.5 s only (the push-in ends on a garbled sign).
  - Nothing on screen labels them as reenactments; they illustrate the story, and the facts come from the narration and graphics.
- Real photos: Wikimedia Commons (credits in `CREDITS.md`).

## Facts in the script (checked)
- Crash: just after midnight, 30 May 1975, Skyline Blvd near Hendricks Park, Eugene. His MGB convertible crossed the center line, hit a rock wall
  and overturned, pinning him. Age 24.
- Born 25 Jan 1951, Coos Bay, Oregon. Marshfield High, coach Walt McClure. Undefeated in cross country and track his junior and senior years.
- HS: mile 4:06.9 (Oregon HS record); 2 mile 8:41.5 (reported as a national HS record).
- University of Oregon under Bill Bowerman (Nike co-founder). 7 NCAA titles: 3 cross country, 4 three-mile/5000 (first to win 4 in one event).
  Never lost an NCAA race longer than a mile; lost only 3 college races in Eugene, all miles.
- Quote: "No one will ever win a 5,000-meter race by running an easy first two miles. Not against me."
- 1972 Olympic Trials (Eugene): American record 13:22.8 in the 5000.
- Munich 5000 final, 10 Sept 1972: Virén 13:26.4, Gammoudi 13:27.4, Stewart 13:27.6, **Prefontaine 4th 13:28.4** (0.8 s from bronze).
- AAU amateur rules; he took Nike shoes and gear and campaigned against the AAU.
- By 1975 he held every American record 2,000 m–10,000 m (7). 5000: 13:21.87 (Helsinki, 1974, said "thirteen twenty-one point nine");
  10,000: 27:43.6 (Eugene, 1974).
- Helped start the running club at the Oregon State Penitentiary; it still runs.
- Last race, 29 May 1975, Hayward Field: won the 5000 in 13:23.8; Frank Shorter 2nd. Party at Geoff Hollister's; after midnight he drove Shorter
  to Kenny Moore's, then headed home alone.
- Police reported BAC 0.16; Oregon's limit then was 0.15. Friends/family dispute it; some believe another car forced him off; police ruled that out.
- Legacy: Prefontaine Classic (since 1975); Pre's Rock memorial; films *Prefontaine* (1997) and *Without Limits* (1998); Nike HQ building named for him.
