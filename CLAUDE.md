# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
  - **Upscales must not look blurry or distorted** (owner, Nov 23, 2026, all videos, all chats: "When you upscale photos and videos, make sure that they aren't really blurry or super distorted. Make them just good enough to where they meet the quality qualifications").
    - Always upscale from the original resolution. Never shrink a clip first to save time (the old "720p → 540×960" trick): it throws real detail away and comes out blurry.
    - Scale only to the size the slot needs (e.g. 1440×1280 top slot, 1080×960 split, 1080×1920 full-screen; photos cap at 3200 px), not beyond.
    - `editor/enhance.py` mixes the AI result with a plain Lanczos resize of the original (`--blend`, env `UPSCALE_BLEND`, default 0.6), so faces, hair and text keep their real texture instead of a waxy AI look. Don't push it to 1.0.
    - Check a full-resolution frame of every upscaled photo and clip (face, hands, text) before it goes in. If it still looks smeared or soft, flag it to the owner instead of using it.
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Use the owner's real voice with the approved light polish on every video.** The default is `voice_chain: "polish"` (owner, Nov 2026, after an A/B of his Felix/Tarmoh narration: "I like the way the voice sounds. Save that for all of my future videos").
  - The chain (in `build.py`): rumble filter below 60 Hz only, very gentle noise reduction (`afftdn nr=8`), soft de-ess, light 2:1 leveling. No EQ and no low cut: it measured *fuller* in the low end than the original.
  - **Hot phone takes** (owner, Nov 2026: "Why is the audio so loud of me talking and sound so echoed?"): his takes often come in around −10 LUFS and clip past 0 dBFS. `build.py` now repairs clipped peaks (`adeclip`) and trims the take to −24 LUFS *before* the polish, so the 2:1 compressor only touches peaks instead of squashing ~7 dB nonstop (which lifted the room echo). The static gain then brings it to −14. He approved this after the A/B in `projects/athlete-of-year/voice_before_after.mp3`. The render prints `voice input: … -> adeclip, volume before polish`.
  - Tell him when a take is clipping, and suggest recording a bit farther from the phone or in a softer room (rugs, curtains, a closet).
  - Don't make it stronger. Earlier, heavier processing (EQ, a 70 Hz+ high-pass, stronger noise reduction) made his voice "weird / muffled" and "took the bass out". Use `voice_chain: "original"` (untouched) only if he asks.
  - If you change anything in the voice path, send him a loudness-matched before/after (`projects/felix-tarmoh/voice_before_after.mp3` is the reference) before using it.
  - **Never turn the voice down below −14 LUFS.** A take that's already at or above −14 LUFS lands at −14 (the hot-take fix above); it's never made quieter than that.
    - One exception: if the take peaks right at 0 dBFS, it gets the minimum static trim to a −0.5 dBFS peak (about 0.5 dB, below audibility). ffmpeg's AAC encoder squashes full-scale audio (quieter, with crunch on the loudest words), and this headroom keeps the encode clean.
  - If the take is quieter than −14 LUFS, it gets one static volume boost up to −14, plus a peak limiter only in that case.
- **Full-screen shots must be sharp enough to monetize.** The owner rejected a soft opening shot.
  - A 16:9 1080p clip cropped to full-screen vertical gets enlarged about 1.8×, which looks soft. Don't use it full-screen.
  - Full-screen needs one of:
    - 4K landscape video (keep it at native 4K, don't downscale the intermediate)
    - vertical video at 1080×1920 or higher
    - a high-res photo (about 3000 px or more on the long side)
  - 1080p landscape clips go in the bottom half of the split only.
  - Check a full-resolution frame of every full-screen shot, especially the opening, before exporting.
- **Face look (owner, 18 Nov 2026): don't alter the talking head's quality at all.** He said: "besides the little darkened edges, don't alter the quality of the talking head video. It's already high quality and it doesn't need to be altered."
  - The only thing allowed on it is the dark-edge vignette (`vignette=PI/6`).
  - No sharpening (unsharp, cas), no denoise (hqdn3d), and no contrast, saturation, gamma or colour grade.
  - `build.py` drops any other filter put in `face_grade`.
  - This supersedes the older option-A cleanup (denoise, brighten, sharpen).
- **No filters or "looks" on the video** (owner, Nov 2026, on the Whelpton edit: "The filter that was put on this video is trash. Never do that again").
  - That edit used a custom `face_grade` (shadow-lifting curves, warm/cool colour shifts, a heavy off-centre vignette) plus `broll_grade: "cinematic"` (film colour grade).
  - Never use a custom `face_grade` or any `broll_grade` film look. Even if he asks for "cinematic", get cinematic from pacing, transitions, framing and photo push-ins, not a colour filter.
  - Only the vignette (see Face look above), which keeps his natural look.
- **B-roll shows the actual subject, never random people** (owner, Nov 2026, also on Whelpton).
  - Use footage and photos of the athlete being discussed: the owner's Dropbox clips first (he often adds the athlete's own training/lifting videos), then real photos of that athlete.
  - Photos of a star he name-checks (e.g. Usain Bolt) are fine.
  - No stock athletes, random meet/Olympic footage, other lifters or generic "sprinter" photos standing in for the subject. If there isn't enough, reuse the subject's clips with different framing and ask him for more.
  - If the subject's own footage shows numbers that contradict the script (e.g. lifts), show the real numbers and tell him.
- **Low-res clips of the subject:** flag them first (see 6b). If he wants them used, `editor/enhance.py` (Real-ESRGAN, local CPU, no credits) upscales them.
  - Upscale from the clip's original resolution straight to the slot size (no shrinking first; see B-roll quality).
  - It takes about 5 s per frame, so enhance only the ranges you use, one job at a time.
- **Quality first** (owner, Nov 2026: "even the videos that were exported to Dropbox were very low quality … keep the quality really high"):
  - Intermediates: face crop and `tighten.py` at CRF 10 (24-bit audio); segments CRF 12; master `master_crf` 12 (style.json).
  - **Final export: x264 CRF 16, preset slow, no bitrate cap, audio copied** (`-c:v libx264 -crf 16 -preset slow -profile:v high -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart`). Big files go through Git LFS; don't squeeze to 100 MB or ~8 Mbps any more.
  - After changing the face source, clear the project's build cache (segments are cached by path, not content).
- **Export:** 1080×1920, 30 fps. Loudness is −14 LUFS, or louder if the owner's take is already louder (see above). Save finished edits to `exports/` and push them so the owner can download from GitHub. (Superseded: the old "under 100 MB, CRF 20 / 6–9 Mbps" export; see Quality first above.) Copy the audio (`-c:a copy`; the build writes 256k AAC) so the voice is never re-compressed.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
- **Seam:** a clear separation between the face and the B-roll, but soft: `seam_style: "soft"` gives a clean edge with a soft shadow band and a faint 2 px hairline.
  - The face must **not** blend or dissolve into the B-roll; the owner rejected `"blend"`.
  - No bold or colored divider line either; the owner rejected the red line.
- **Transitions: viral-style, on every video** (`editor/transitions.py`; auto-picked by `choose_transitions` in `build.py`):
  - **Into full-screen:** rotate zoom-through, whip-pan (left/up) and spin.
  - **`hit` segments:** flash or camera shake.
  - **Out of full-screen:** whip-down, zoom, whip-right or glitch.
  - **Full → full:** whip or glitch.
  - **B-roll swaps inside the split:** a bottom-half swipe with motion blur; the owner's face never moves.
  - **Overrides:** force one per segment with `"transition": "whip:left" | "zoom" | "spin" | "glitch" | "flash" | "shake" | "swipe:right" | "cut"`. Set `split_swipes: false` for plain cuts in the split.
  - Keep them varied, never the same transition twice in a row. Motion blur peaks briefly at the cut so both shots stay sharp.
- **Captions:** word-by-word, all caps, Montserrat Black, sitting on the seam. Highlights alternate red `#E8231E` and yellow `#FFE11A`.
- **Sound effects: few, quiet, spaced out.** The owner dislikes random loud sounds mid-sentence. `build.py` and the `style.json` defaults enforce this:
  - **Off:** `graphic_sfx: false`, so graphics and animations make no sound (no thuds, pops, ticks or clicks).
  - **Off:** `hit_sfx: false`, so there are no bass hits. `"hit": true` on a segment only picks the flash/shake transition.
  - **Off:** `extra_sfx_on: false`. Risers and long cinematic hits are banned outright (`BANNED_SFX`), in any video.
  - **Kept:** a quiet airy whoosh on cuts into and out of full-screen (`whoosh_level` 0.24), with small pitch variation. B-roll swaps inside the split are silent.
  - **Spaced out:** at least `sfx_min_gap` (3 s) between sound moments, and never the same sound file twice in a row.
  - The render prints the kept sound list (`SFX: …`). Check it.
  - Don't turn any of these back on unless the owner asks.
  - (History: the owner first found every-cut whooshes repetitive, then found graphic and impact sounds loud and random, and risers too loud and drawn out.)
- **Numbers and stats** get animated data graphics (`type: "data"`: counter, compare, bars, line, ring); they're silent by default. Run `suggest_data.py` on the transcript to find every number.
- **No big text that just repeats the captions** (owner, 25 Nov 2026, after the Yaseen Abdalla video, which is the last one made this way: "I don't like on the videos where the subtitles are there and then they put like big subtitles just replicating the same subtitles on the screen. Take away that for all future videos").
  - No `slam` or `keyword` whose text is the words he's saying at that moment (e.g. "BE FULLY AFRICAN", "CRABS IN A BUCKET", "GOOFY", "BORN IN THE USA").
  - Big on-screen text must add something the captions don't: a checked number, a result, a place or a name (`board`, `data`, `pin`, `stopwatch`, `poll`, `podcast` badge, etc.).
  - This overrides the `slam`/`keyword` density in the Jane and Yohan Blake formats below: fill those beats with data graphics, B-roll changes and punch-in zooms instead.
- **Things being talked about** get motion graphics (`type: "motion"`):
  - `slam`: kinetic punch text with a yellow marker bar on the key word (`hi`), e.g. "BIGGEST LIE". This replaces `stamp` (owner, Nov 2026: the red stamps are "too cliche"); the build turns any `stamp` into a `slam` unless a plan sets `stamps: true`.
  - `keyword`
  - `pin`: a place
  - `calendar`: months or seasons
  - `stopwatch`: race times
  - `wind`
  - `spotlight`: circle and arrow on a person in full-screen footage
  - `poll`: comment-bait ending
  - `padlock`: paywall
  - `subscription`: streaming screen swapping services, ending on "subscription required"
  - `tv`: TV switching on
  - `flow`: three-step icon chain; set `times` to land each step on the word
  - `bubbles`: generic reaction chat bubbles. These are illustrative, never presented as real quotes.
  - `usmap`: states light up on a US map in time with the voice; `cross` puts a red X on a state
  - `birthday`: cake with number candles and confetti
  - `podcast`: mic badge with a live waveform naming who's talking, for guest podcast clips
  - `board`: records board; rows of `event`, `value` and optional `tag`, with `times` landing each row on the word
  - `track`: one lap of a track with a clock counting to `value` (open 400 times)
- **Never invent data.** Don't fake stats or poll percentages. If a value is interpreted (e.g. "23 mid" → 23.5), say so to the owner.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips are a standing request for future videos.** Plan short animated clips that illustrate what's being said, alongside the motion graphics. Examples: an animated track, a running-figure loop, a stopwatch or a globe spin.
  - Before each edit, list the animation moments you'd add and ask the owner to supply clips, or offer to generate them.
  - AI generation costs credits and the owner doesn't want an "AI look", so get approval first.
  - As of Nov 2026 the owner's Higgsfield account is on the free plan with 10 credits. Its 1080p models need the Basic plan or higher, and the only clips 10 credits cover are 720p, which breaks the 1080p rule. Until that changes, hand-build animations as `motion` graphics.
  - Clips go in as `type: "clip"` overlays: keyed with `key: "green"`/`"black"`, as alpha video, or full-frame as a B-roll segment.

## Current reference format: the Jane Hedengren edit
**Start every new TikTok from this one** (owner, 15 Nov 2026: "I like the way that was edited. We're going to save that format and continue to grow from there").
- **Files:**
  - Plan: `projects/jane-hedengren/plan.json`, generated by `plan_builder.py`.
  - Notes: `NOTES.md`; also `CREDITS.md` and `footage_wanted.md`.
  - Export: `exports/jane_hedengren_tiktok_hq.mp4`.
  - Cover: `exports/thumbnails/jane_hedengren_thumb*.jpg`, made with the `thumb_short/` tool.
- **What it is:** the Yohan Blake method below, applied to a ~1:10 hot take.
  - **Freeze-frame pop-outs** introduce each person: the subject with a yellow glow, the rival with a red glow.
  - **Full-screen** at about 5 turns (hook, rival, the twist, "top runner now", payoff), with `hit` on the 2–3 biggest.
  - **`slam`s** on the punchlines.
  - **`board`s** for the evidence: results top 3, records, the season so far.
  - A **`poll`** ending.
  - Auto-picked viral transitions.
  - The `polish` voice chain with the hot-take fix.
  - Default face cleanup only, **no filter**.
  - Real photos of the actual athletes (Commons), and every number checked.
  - The NOTES list where his wording differs from the record.
  - CRF 16 HQ export.
- **Growing from it:** keep this structure and density. Change one thing at a time when he asks, and record each change here so the format keeps evolving from Jane, not from older edits.

## Default editing method: the Yohan Blake edit
**This is the default way to edit every TikTok from now on.** The owner called `exports/yohan_blake_tiktok.mp4` "perfect" and "probably the best video". Its plan is `projects/yohan-blake/plan.json` and its notes are in `projects/yohan-blake/NOTES.md`. Copy its structure, pacing, graphics and transitions unless the owner asks for something different.
- **Graphics and transitions:** the owner said both were "on point". Keep the same mix and density:
  - The auto-picked viral transitions, with no per-segment overrides.
  - A graphic on almost every beat (keywords, slams, boards, bars, counters, a poll).
  - **No name tags** (owner, Nov 2026: "those little red name tag[s] at the bottom, I don't like that. Let's exclude those"). The build skips `name` graphics unless a plan sets `name_tags: true`. Introduce a person with a **freeze-frame pop-out** instead (`editor/freeze.py`): the shot freezes with a flash, the background drops dark and desaturated, and the athlete pops out with a white edge and glow. Use it as a full-screen segment (see `FRZ()` in `projects/bright/plan_builder.py`); `pick` selects the athlete when several are in frame (choose a frame where they're clear of others).
  - Don't thin them out or swap in new styles without asking.
- **Pull relevant historical media online whenever the owner's footage doesn't cover the story.** That means photos of the athletes, races and moments being discussed. Use it even when he sends B-roll, if a moment he talks about isn't covered. See "When the owner sends only a talking head" below for sources and rules.
- **Story arc:** build the edit as an argument with a payoff.
  1. **Hook (0–15 s):** the subject full-screen (freeze pop-out on their first mention), the claim as a `keyword` ("ALWAYS 2ND TO BOLT?"), a `slam` on the punchline ("BIGGEST LIE"), and `bubbles` for "what people say online".
  2. **Context:** what's true about the subject, shown as data (an all-time `board`, a `pin` for where it happened, a `slam` for the twist, e.g. "NOT A CHAMPIONSHIP").
  3. **Turn:** cut to full-screen on the key fact, with a `data` counter.
  4. **The real story:** a freeze pop-out for each new person, then a `board` listing the evidence, one row landing on each spoken item (`times`).
  5. **Callback:** full-screen with the claim slammed again ("WRONG ERA?" → "LIE").
  6. **Proof:** actual results for each event the owner names (`bars` with real times, the subject's place in the name), with a slam on each verdict ("4TH PLACE", "4TH AGAIN").
  7. **Ending:** `poll` on the core question ("BORN IN THE WRONG ERA? YES / NO").
- **Pacing:**
  - A graphic on almost every beat, about every 3–5 s.
  - A new B-roll shot every 4–7 s.
  - Full-screen at each act turn (4–5 per video), with `hit` on the two biggest.
  - Punch-in zooms on the owner's rhetorical questions ("Where was he?").
- **Facts on screen:** the owner's claims are backed by real, checked numbers: official times and places, all-time ranks. Never invent data. List every added fact in the project NOTES, and tell the owner where his wording differs from the record.
- **When the owner sends only a talking head:**
  - Pull B-roll from Wikimedia Commons: freely licensed photos of the athletes and races, ≥2800 px.
    - Search by category and by file name.
    - Download slowly, because Commons rate-limits.
    - Bake in EXIF orientation, and cap photos at 3200 px for render speed.
  - Write `CREDITS.md` (CC BY / CC BY-SA need a caption credit) and tell the owner the caption line.
  - YouTube race footage can't be downloaded from the cloud session (bot check; don't try to get around it). List the official uploads in `footage_wanted.md` so the owner can send them; they'd go in the bottom half.
  - Full-screen photos must be vertical or large enough to crop to 9:16 sharply. A wide landscape photo crops to an awkward slice, so use it in the split only.
- **Graphic layout limits (learned on this edit):**
  - `board` rows: keep `event` to about 20 characters, and only use `tag` on short rows, or the value gets clipped.
  - `bars`: at most 4 rows in the split. For 5+ results, use a `board` (rows like "5 · YOHAN BLAKE", with a `tag`).
  - Check a frame after each data graphic lands, plus the full-screen shots, before exporting.

## Converting one of the owner's YouTube videos to a TikTok (learned on Felix/Tarmoh, Nov 2026)
- Source = his original video file (he shares it via Dropbox). Keep his real voice (`polish` chain), the same plot order, ≤ 7:00: cut channel plugs, repeated commentary and long closing morals (`projects/felix-tarmoh/cut_voice.py`).
- Keep the interview/soundbite clips that are inside his video (they're the strongest moments).
- **More vertical, full-screen visuals** (owner: "more vertical images and videos should have been included", while keeping it high quality). On Felix/Tarmoh almost every shot was his 1080p footage in the framed middle band; that read as too boxed-in.
  - Aim for roughly half the runtime full-screen, alternating with the framed band every ~5–8 s.
  - Full-screen still has to be sharp: high-res photos (≥ 3000 px long side, from Commons), vertical video, or 4K. His 1080p landscape footage stays in the framed band.
  - Put the full-screen shots on the big beats (hook, each act turn, verdicts) and on every new person.
- Rebuild his YouTube thumbnail as the TikTok cover (step 8).

## ElevenLabs narration (when the owner asks for his AI voice instead of a talking head)
**This is the owner's DEFAULT VOICE for all his YouTube and TikTok videos** (approved Nov 2026: "I like that one. Set that as the default voice"). Always use this recipe. Don't improvise the model, settings or format. The owner asked "why can't you be consistent with the voices?", so match this exactly every time.
- **Approved results:**
  - The Jon Drummond YouTube voiceover.
  - The final Asafa Powell video (`exports/asafa_powell_tiktok_hq.mp4`, Asafa v3).
- **Reference flows** (read a node with `creative_get_flow_node` if in doubt):
  - "Jon Drummond documentary voiceover" (`EwtCtvyEoktyTmEPgx7r`), nodes labelled "V4 0x … (natural, consistent)".
  - "Asafa Powell voiceover (Drummond recipe)" (`W4Hc1NpmegUzmpwft2jt`), with its script in `projects/asafa-powell/script_v4_sections.txt`.
- **Assembly** (as on Asafa v3):
  - Generate 2 takes per section.
  - Transcribe them and keep the take that stays in dialect, says every line and doesn't rush its first seconds.
  - Join sections with about 1.5 s of breath.
  - If the video must reach a length, lengthen about 15 of the longest in-section pauses by about 0.4 s.
- **Mix:** set `voice_chain: "original"` in the plan for ElevenLabs narration. The clone was approved as generated (Drummond, Asafa v3); the `polish` default is for his real recordings.
- **Voice:** his clone "Erin Brown" (`voice_id` `dk6cvd5UilZRrcpZ7dNK`).
- **Model and settings:** `eleven_v4`, `voice_settings` `{"stability": 0.45, "similarity": 0.85}`. Nothing else.
- **Tags:** every paragraph starts with `[calm] [relaxed] [Texas accent]`. Put `[pause]` before big beats.
- **Spelling:** write it the way he talks, in his urban Texas dialect:
  - "Aight, so check it out", "lemme tell y'all", "'Cause", "nah, mane", "damn near a hour", "they was", "4 by 1"
  - dropped g's: "leavin'", "standin'", "lookin'"
  - phonetic name spellings where needed ("Drummund")
- **Length:** seven-ish short sections of about 900–1,900 characters, each its own node. That keeps the delivery steady, where one long take speeds up.
- **Pace check:** the approved Drummond read runs about **164 wpm, steady from the first second**, with pauses averaging about 0.6 s. Measure each take, and reject any whose first 30 s is noticeably faster than the rest.
Learned on the Asafa Powell video (Nov 2026); details in `projects/asafa-powell/NOTES.md`:
- **Asafa v1:** `eleven_v4`, default settings, no tags, dialect script. It was "really decent", but **too fast at the beginning** (182 wpm in the first 30 s).
- **What he rejected:**
  - A proper, newscaster-style script: "doesn't sound like how I would talk".
  - An enthusiastic, "too proper" open.
  - `eleven_multilingual_v2` with stability 0.75 and style 0 (Asafa v2): he called it "horrible". Don't use that model or those settings for him.
- **Script:** write it in his **urban Texas dialect**, modelled on his real transcripts (Klan, Yohan Blake, Drummond, 200m):
  - phrases like "Man, let me tell y'all", "he ain't even make it to the final", "Where he finish? Fifth.", "Make it make sense", "they was", "4x1", "worlds"
  - times said the track way ("nine seventy-four")
  - keep it conversational and calm, not performed
- **Words the voice mangles:** "Mane" came out as "May-nay", and "fr" came out as "far". Avoid them, or check every take's transcript and cut them.
- **Limits:** ElevenLabs takes at most 5,000 characters per generation, so split long scripts at a section break. Transcribe every take and keep the one that stays in dialect; some takes drift ("how *are* you", "*Meh*").

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox links.
   - Share links (`/scl/fi/...`): download with `?dl=1`.
   - Transfer links (`/transfer/...`): run `node editor/fetch_dropbox_transfer.js <url> <dir>`. You get a zip; unzip it into its own folder.
   - **Guest soundbites:** when the owner references someone's interview or podcast, cut the guest's best 15–25 s into the A-roll right after the owner introduces them. The guest's footage takes the top "speaker" slot, in the same 1440×1280 framing with any on-screen banners cropped off. Match its loudness to the owner's voice, and merge the guest's captions into the timeline. See `projects/flotrack-masai/`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
3. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
4. **Write `plan.json`.** Start from `projects/jane-hedengren/plan.json` (the current reference format), built on the Yohan Blake method (see above).
5. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.
6. **Deliver to the owner's Dropbox** too: save every finished export to `/TikTok Exports/` in his Dropbox. He's connected it through the Composio connector (account "Erin Brown Track & Field").
   - Files over about 150 MB can't go through `DROPBOX_UPLOAD_FILE`. Use `DROPBOX_SAVE_URL` with the file's GitHub LFS URL (`https://media.githubusercontent.com/media/<owner>/<repo>/<branch>/exports/<file>`), so Dropbox fetches it server-side.
   - Check the returned `content_hash` against the local file (SHA-256 of the per-4 MB-block SHA-256s) before telling the owner it's there.
   - He can also put raw footage in his Dropbox and name the folder; read it from there instead of asking for share links.
6b. **Post every finished video to YouTube Shorts and Instagram without asking; the owner posts TikTok himself** (owner, Nov 2026: "post them on all three places … don't ask again", then, after the API-posted TikToks looked "really low" quality: TikTok goes back to him).
   - Via vidIQ (`vidiq_video_upload` → `vidiq_social_post_draft_create` + `vidiq_social_post_publish`; `vidiq_instagram_publish_reel` for the trial reel).
   - **TikTok: do NOT post it.** TikTok re-compresses uploads sent through its posting API; the app's "Upload HD" option is only in the app. Deliver the export to Dropbox `/TikTok Exports/` as usual and give him the caption to paste. He posts it on "Erin Spider Brown" from the app with "Upload HD" on.
   - **YouTube Short:** "The Erin Brown" (@theerinbrowntv, `UCiMHg3V2Q414zFIjb8PyTcg`), public, category 17 (Sports), `#Shorts` in the description, the video title as the YouTube title.
   - **Instagram trial reel:** @e.diamondz (`29211548525143718`), `trialParams.graduationStrategy: MANUAL`.
   - **Facebook Page "E.Diamondz"** (id `506309812910570`, the Page linked to @e.diamondz): post every finished video there too, with the same caption as the Instagram reel.
     - Use the Composio Facebook connector, connected 17 Nov 2026: `FACEBOOK_CREATE_VIDEO_POST` with `file_url` set to the export's GitHub LFS media URL. vidIQ has no Facebook Page connected.
     - Then check `FACEBOOK_GET_GRAPH_OBJECT` (fields `permalink_url,status`) until `video_status` is ready, and record the link.
     - Alternative that posts it as a Page **Reel** (used by the "TikTok editing 2" chat, confirmed working on the Whelpton video): `FACEBOOK_PUBLISH_PAGE_REEL` with `page_id` `506309812910570`, `file_url` = the export's direct URL (GitHub LFS media URL), `description` = title + hashtags, `video_state` `PUBLISHED`. It returns `video_id` with `upload_success`/`finish_success` true.
   - Caption: the title + one line + `#track #trackandfield` + topic tags. Never the "6starfiles" TikTok or the "GTA 6 Ernie" YouTube channel.
   - Record the post links in the project NOTES.
   - **Low-res sources:** tell him BEFORE the edit when any of his clips/photos are under 1080p (they look soft once enlarged) and ask for better versions or offer to find some.
7. **Write a title** for every video: a one-line, YouTube Shorts style hook (the owner asked for this on all of them).
   - Lead with a name people search plus the conflict or twist (e.g. "He Refused to Leave the Track… 11 Years Later, Track Banned Him").
   - Keep it under about 70 characters so it isn't cut off in the Shorts feed. One emoji at most.
   - No claim the video doesn't back up.
   - Put it at the top of the project's `NOTES.md` and give it to the owner with the finished video.
8. **Thumbnail for every video.**
   - **CURRENT STYLE (owner, 18 Nov 2026), which overrides everything below for short videos.** He made his own Shea Foster cover and said: "Use this thumbnail instead. Simple, high quality. And I want my thumbnails in the future to look like this."
     - Reference: `projects/shea-foster/owner_thumbnail.png` (also `exports/thumbnails/shea_foster_thumb_owner.jpg`, 1086×1448, 3:4).
     - **One real, sharp photo of the subject** fills the frame: a race/candid moment with the real background softly out of focus, and natural, warm, bright colour.
       - No cut-outs, no white outlines or glows, no photo cards, no caution tape, no headline text, no number boxes.
     - **One symbolic inset:** a circle with a thick red `#E8231E` border and a speech-bubble tail pointing at the subject's head.
       - Inside it, a sharp real photo of an object that tells the story: a judge's gavel for a ban, a stopwatch for a time, a syringe for doping, a measuring tape for a jump standard.
       - It sits top-right, over sky or background, never over a face.
     - **Simple and high quality:** sharp at full size, no screen grabs, the owner only if he supplies a HQ photo of himself.
     - Make 3:4 (1080×1440, his format) plus a 9:16 version for the upload cover (same layout, more background above and below).
     - The "designed graphic" layered style and the text-hook covers below are **superseded** for short videos. Keep them only for reference or if he asks.
   - Older guidance (superseded where it conflicts with the above). Style depended on length (owner, Nov 2026: "only want to use that [viral] style of thumbnail when I'm making the longer 5-minute plus documentary style videos"):
   - **5+ minute documentary-style videos:** the VIRAL thumbnail below.
   - **Shorter videos (TikToks under ~5 min):** a bright SHORT-FORM viral cover, NOT the dark cut-out style (owner, Nov 2026, on the Gift Bright cut-out: "That thumbnail is trash. It has no viral or virality in it").
     - Bright and saturated, never dark/moody grading. One 2–4 word hook in Anton, yellow `#FFE11A` with a thick black outline ("15 YEARS OLD", "HE'S ONLY 15").
     - The key number in a red `#E8231E` box with a white border ("10.28").
     - **Real photos with their real backgrounds, slightly blurred** (owner, 17 Nov 2026, on the LA28 cover: "Never use screen grab photos from videos when you make these thumbnails. I shouldn't be in the thumbnail unless it's a high quality image. Use real images with real backgrounds that are slightly blurred. But the green background is ridiculous.").
       - Use a sharp, high-res real photo of the athlete (Commons or his own photos), never a frame grabbed from a video.
       - Keep the photo's own background (stadium, track), blurred a little (depth-of-field look) so the athlete stands out sharp in front.
       - **No color-burst/rays backgrounds** (the green/purple burst is banned).
       - **The owner only goes in the cover if he supplies a high-quality photo of himself.** Never cut him out of his talking-head video.
       - **Make it a designed graphic, not a photo with text** (owner, 18 Nov 2026: "Make a more complex thumbnail. That looks too simple. It looks like no effort was put into making that. Make it a real graphic and do that for all of the thumbnails"). Every cover is layered:
         - The athlete cut out large (`rembg`, `u2net_human_seg` keeps raised arms), with a white edge, a warm rim glow and a drop shadow.
         - Behind them, their own real photo's background with the athlete painted out (no ghost) and blurred: `editor/cover_bg.py photo.jpg bg.jpg`.
         - 2–3 tilted white photo cards of the evidence (other athletes, the race, the moment), each with a short Anton caption carrying a checked fact ("MEN'S TJ: 7", "PARIS: WITHDREW"), and a red ring on the person in the card.
         - A two-line headline: a white kicker over a huge yellow word with a 3D extrude, plus a red ribbon sub-line.
         - A story graphic: caution tape ("BANNED · 4 YEARS", "CUT THE EVENT?"), a number badge ("8.30 M"), or an object drawn in SVG (an EPO vial).
         - Template: `projects/shea-foster/thumb_pro/` (`thumb.html` element types bg/subj/card/text/ribbon/tape/stamp/vial, `layouts.json`, `render.js`). Second example: `projects/cut-events/thumb_pro/`. Render 9:16 and 3:4.
       - This supersedes the older "huge face cut-out over a bright color burst" and "his face cut-out in a corner" options. Tool: `projects/cut-events/thumb_real/`.
     - Cover any burned-in captions/logos. Cut-outs at or below ~1.1× source size.
     - Tool: `projects/bright/thumb_short/` (`thumb.html`, `layouts.json`, `render.js`); render 9:16 and 3:4.
   - **VIRAL thumbnail, in the owner's YouTube-thumbnail style** (owner, Nov 2026: the plain cut-outs "aren't appeasing to an audience… they aren't viral thumbnails"; "look into the YouTube thumbnails and convert it into a TikTok thumbnail, high quality").
   - **Style (from his YouTube thumbnails, e.g. "Allyson Felix: Two-Faced or Ambitious?"):** black background, the subject's face big and close (cut out of a real, sharp photo, bust fading into black), a bold 2–4 word hook in Anton, stacked: lines in green `#8DF02A` with the key word huge in glowing white (e.g. "BIGGEST / SNAKE / IN TRACK?"), and a tilted white Polaroid inset showing the other person or the key moment.
   - If the owner already made a YouTube thumbnail for the story, rebuild THAT design (same words, colors, inset) at full resolution; never just upscale the 640×480 YouTube image.
   - **Tool:** `projects/felix-tarmoh/thumb_viral/` (`thumb.html` + `render.js`, Playwright at 2× then downscaled). Copy it per video and change the text, photos and layout numbers.
   - Make both: 9:16 (1080×1920, keep the key content inside the middle 1080×1440) and 3:4 (1080×1440, laid out separately).
   - For 5+ min documentaries, the cut-out style below is also the fallback when no hook text fits.
   - **Cut-out style (shorter videos):** Save `exports/thumbnails/<video>_thumb.jpg` (3:4, 1080×1440, the profile-grid cover) and `<video>_thumb_916.jpg` (9:16 upload cover), and deliver both to Dropbox with the video.
   - **Tool:** `editor/thumb_cutout.py spec.json`. Cut subjects out with `rembg` (`isnet-general-use`, local, no credits), then clean the mask (threshold alpha > 150 and feather) to drop semi-transparent leftovers.
   - **Look:** the key athlete(s) cut out of **real photos**, layered over a real, darkened and graded background tied to the story (a stadium or venue).
     - The main subject is big and front-and-center, with a white outline, a colored glow and a drop shadow.
     - The second person sits behind, with a contrasting glow color.
     - On busts, use `fade_bottom` and `soft_below` so the torso fades into the background and ragged clothing edges never show.
   - **Reference:** `projects/asafa-powell/thumb_spec.json` and `exports/thumbnails/asafa_powell_thumb.jpg` (Powell front, blue rim; Bolt behind, gold glow; the Bird's Nest at night).
   - **Text:** viral thumbnails carry the bold hook text (see above); plain cut-out fallbacks have none.
   - Real photos only: no AI-generated images, nothing that looks AI. Never enlarge a cut-out past about 1.1× its source. The background can be soft and graded.
   - Check at full size: faces sharp, no halos or torn edges, no heads or hands cut off, and both sizes composed.
- **Exports too big for GitHub's 100 MB limit at full quality** go through Git LFS (`exports/*_hq.mp4`). Measure SSIM against the master and keep it at 0.98 or higher, rather than squeezing under 100 MB and losing quality.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
