# Allyson Felix vs Jeneba Tarmoh: the 2012 dead heat (Nov 2026)

**Title (YouTube Shorts / TikTok):** Allyson Felix Kept the Spot… Jeneba Tarmoh Lost Her Olympics 💔
Alternates:
- They Tied to the Thousandth… Then USATF Wanted a Coin Toss
- Jeneba Tarmoh Did the Victory Lap… Then They Took It Back
- Allyson Felix: Two-Faced or Ambitious? 🤔
- Same Coach, Same Time, One Spot: Felix vs Tarmoh 2012
- 11.068 vs 11.068… and the Olympic Spot Came Down to an Email
- Was Allyson Felix Wrong for Keeping That Olympic Spot?

**Thumbnail v2 (viral, owner's YouTube style):** `exports/thumbnails/felix_tarmoh_viral_thumb.jpg` (3:4) / `_916.jpg` (9:16), rebuilt from
his YouTube thumbnail: "BIGGEST / SNAKE / IN TRACK?" (green #8DF02A + glowing white, Anton), Felix bust (Commons "Allyson Felix Doha 2012.jpg",
CC BY 2.0) on black, Polaroid of Felix + Tarmoh embracing at the Trials cropped from his thumbnail (only ~110 px there; straightened, FSRCNN 4×,
soft at inset size). Swap in a sharp frame from the race footage when it arrives. Source: `thumb_viral/`.

**Thumbnail v1** (`exports/thumbnails/felix_tarmoh_thumb.jpg` / `_916.jpg`): Felix cut out of "Allyson Felix Doha 2012.jpg" (Commons, CC BY 2.0)
with a red rim over Hayward Field at dusk ("Hayward Field 6-4-11.JPG"). No free photo of Tarmoh exists on Commons/Flickr; add her behind
Felix from a frame of the owner's footage once it arrives.

Source: the owner's YouTube video "Allyson Felix: Two-Faced or Ambitious?" (Sept 2024, https://youtu.be/td5bQpV9gP4, 11:15).
This TikTok retells it in ~5:25 in his default ElevenLabs voice, facts checked.

## Export
- `exports/felix_tarmoh_tiktok_hq.mp4` (Git LFS): 6:51, 1080×1920, 30 fps, 7 Mbps 2-pass, SSIM 0.997 vs master, −14.1 LUFS / −1.4 dBTP.
- Dropbox `/TikTok Exports/`: `felix_tarmoh_tiktok_hq.mp4` (content_hash a45a1680… matches), `felix_tarmoh_viral_thumb_v2.jpg` and
  `felix_tarmoh_viral_thumb_916_v2.jpg` (sharper Polaroid; hashes match). The earlier `felix_tarmoh_viral_thumb*.jpg` and `felix_tarmoh_thumb*.jpg` are older versions.
- Voice: owner-approved light polish (`voice_chain: "polish"`, now the house default) after a before/after (`voice_before_after.mp3`).
- v1 had two clipped cards ("RAN THE 4X100 HEATS (STILL GOT…", "WANTED THE 100 + 200"); shortened in v2.

## The cut (real voice + real footage)
- Source: the owner's 2024 YouTube video file (Dropbox share, 11:14, 1920x1080), `raw/source.mp4` (not in git).
- `cut_voice.py` keeps 22 ranges of his ORIGINAL audio, same plot order, untouched (25 ms fades at cuts only): 6:47.8 + 3 s poll hold.
  Removed: channel plugs (intro/outro), "critics argued" / "most damaging" repetition, the Michael Johnson lobby clip, most of the closing moral.
  Kept: Tarmoh "blackballed" cold open (podcast), the race + reversal, USATF's Jill Geer announcement, golden-girl setup, Tarmoh's ESPN interview
  (~80 s), Nike clout / roles-reversed, "that's politics" + "blackballed" (podcast), runoff or coin toss, harassment + walk-away, London.
- `plan_builder.py`: his video plays in sync in a 4:3 framed band (native 1440x1080 crop, no upscale); real stills from the same video fill the
  panels (photo finish, race, the Tarmoh/Felix photo, Felix bib, ESPN set, podcast, Jill Geer, Kersee); one full-screen Hayward Field photo.
  63 graphics (results board 10.92/10.96/11.068/11.068, stopwatch 11.068, tiebreak board, London board, name tags, stamps, poll).
- Captions: his transcript re-timed to the cut, names fixed (Allyson, Jeneba Tarmoh, USATF, Tianna).

## Where the owner's 2024 narration differs from the record (flag, not changed: it's his voice)
- "both clocked 11.06": official 11.068 for both (graphics show 11.068).
- "multiple Olympic medals in the 200 and 400": before 2012 Felix had 200 m silvers (2004, 2008) and 4x400 gold (2008); the "400" is the relay.
- "harassed… threats": not independently verified; it's his account.
- His video says Tarmoh was replaced in the final; true. The graphic adds that she still received a 4x100 gold medal for running the heats.

## Direction change (owner, Nov 8)
- Use the owner's REAL voice from his 2024 video (not ElevenLabs), real footage/interviews of Felix and Tarmoh (faces OK), Tarmoh's
  interview soundbites, lots of real video, ≤ 7:00, same plot. Generic AI reenactments are no longer the plan; no credit top-up needed.
- Waiting on the owner's files in Dropbox `/Felix Tarmoh/` (see `footage_wanted.md`).
- The ElevenLabs takes/flows below are kept only as a fallback.

## Status (ElevenLabs draft, superseded)
- Voice: flow `4LlukseKRsgRiOUAzkpV`, 8 sections × 2 takes (Drummond recipe). Draft picks 01b 02a 03a 04a 05a 06b 07a 08a, assembled by
  `assemble_voice.py` (+0.22–0.4 s per natural pause, 1.5 s breaths) → 5:25. Section 05 reads at 213 wpm in both takes: re-voice after top-up.
- Reenactments: flow `1kAbw3V5Z9CqtozGX0gV`. ElevenLabs plan quota (496,500) ran out after 6 of 20 started (Nov 8). Owner is topping up.
  - Usable: 03_victory_lap (4K), 08_finish_legs (4K), 10_officials (1080p); 02_lean_at_line only cropped above the Olympic rings (band).
  - Redo after top-up: 07_relay_night (garbled "London 2012" banner), 09_photo_finish_monitor (shows two men).
  - Not yet generated: 01, 04, 05, 06 (4K) and 11–20 (1080p). Prompts avoid identifiable faces of the real athletes.

## Facts in the script (checked)
- 23 June 2012, Hayward Field, US Olympic Trials 100 m final: Jeter 10.92, Madison 10.96; Felix and Tarmoh both 11.068 (shown 11.07).
  Tarmoh was first placed 3rd, did the victory lap and press conference; officials reviewed the photo and announced a dead heat that night.
- USATF had no tie-break rule for the last spot; it announced a runoff-or-coin-toss procedure, resolved after the 200 m.
- 30 June: Felix won the Trials 200 m in 21.69 (PB, meet record).
- Runoff set for Mon 2 July, 5 p.m. (NBC). That morning Tarmoh emailed USATF via her agent: "I am no longer running the 100m dash in the Olympic Games";
  "My heart was not at peace with running." Felix: "The situation has been difficult for everyone involved."
- Tarmoh's quotes (her later interview, as used in the owner's video): not comfortable with a runoff or coin toss; felt Felix "said one thing and did
  another"; told she'd be "blackballed" if she spoke.
- Shared coach Bobby Kersee. Tarmoh: born 1989 (22 at the Trials), San Jose, Texas A&M, turned pro with Nike. Felix: world 200 m champion 2005/07/09.
- London: Felix 100 m 5th (10.89 PB), 200 m gold (21.88, after silvers in 2004 and 2008), 4x100 gold (WR 40.82), 4x400 gold.
  Tarmoh: relay reserve, ran 2nd leg of the 4x100 heats, left off the final, still received a gold medal.
- Later: Felix retired with 11 Olympic medals (7 gold), most of any US track athlete. Tarmoh: 10.93 in 2013, US 200 m champion 2014.

## Where the script differs from the owner's 2024 video
- Adds that Tarmoh received a 4x100 gold medal for running the heats (his video says only that she was replaced in the final).
- Leaves out the "Michael Johnson in the lobby" remark (only Tarmoh's recollection; can't be checked).
- "If it was the other way around… ain't nobody lookin' at no photo again" is the owner's opinion from his video, said as opinion.
