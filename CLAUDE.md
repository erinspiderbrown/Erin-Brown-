# TikTok editing: house rules

This repo holds the editing setup for the owner's TikTok sports/track videos. The tools are in `editor/` (see `editor/README.md`), and the house defaults are in `editor/style.json`.

## Hard rules
- **Length:** the final video is **at least 61 seconds** (1:01).
- **B-roll quality:** B-roll and photos must be **1080p or higher** on the short side. If something isn't, flag it to the owner and don't silently use it.
  - Never use sub-1080p footage full-screen. If the owner wants it used, keep it in the split and AI-upscale it first with `editor/upscale.py` (Real-ESRGAN general-x4v3; CPU, about 8 s per frame).
  - **Upscales must not look blurry or distorted (owner, Nov 23, 2026, all videos, all chats):** make them just good enough to meet the 1080 rule, no more.
    - Always upscale from the original resolution. Never shrink a clip first to save time: that throws real detail away and comes out blurry.
    - Scale only to the size the slot needs (e.g. 1440×1280 for the top slot, 1080×960 for the split), not beyond.
    - `upscale.py` mixes the AI result with a plain resize of the original (`UPSCALE_BLEND`, default 0.6), so faces, hair and text keep their real texture instead of a waxy, smeared AI look. Don't push it to 1.0.
    - Check a full-resolution frame of every upscaled photo and clip (face, hands, text) before it goes in. If it still looks smeared or soft, flag it to the owner instead of using it.
- **Full-screen B-roll covers the whole 9:16 frame.** No letterboxing, blurred fill or blank space. Use `focus` to keep the action in the crop.
- **Use the owner's original voice audio, untouched, on every video.** The default is `voice_chain: "original"`.
  - No EQ, no compression, no noise reduction: the owner said processing made his voice "weird / muffled" and "took the bass out".
  - **Never turn the voice down.** If the take is already at or above −14 LUFS, it passes through untouched: no gain and no limiter.
    - One exception: if the take peaks right at 0 dBFS, it gets the minimum static trim to a −0.5 dBFS peak (about 0.5 dB, below audibility). ffmpeg's AAC encoder squashes full-scale audio (quieter, with crunch on the loudest words), and this headroom keeps the encode clean.
  - If the take is quieter than −14 LUFS, it gets one static volume boost up to −14, plus a peak limiter only in that case.
  - Don't add voice processing back, or lower the voice, unless the owner asks for it.
- **Full-screen shots must be sharp enough to monetize.** The owner rejected a soft opening shot.
  - A 16:9 1080p clip cropped to full-screen vertical gets enlarged about 1.8×, which looks soft. Don't use it full-screen.
  - Full-screen needs one of:
    - 4K landscape video (keep it at native 4K, don't downscale the intermediate)
    - vertical video at 1080×1920 or higher
    - a high-res photo (about 3000 px or more on the long side)
  - 1080p landscape clips go in the bottom half of the split only.
  - Check a full-resolution frame of every full-screen shot, especially the opening, before exporting.
- **Export:** 1080×1920, 30 fps. Loudness is −14 LUFS, or louder if the owner's take is already louder (see above). Save finished edits to `exports/` and push them so the owner can download from GitHub. Keep them under 100 MB: re-encode the video with `-crf 20 -preset slow`, or with a two-pass encode at about 6–9 Mbps if that's still too big. Copy the audio (`-c:a copy`; the build writes 256k AAC) so the voice is never re-compressed.

## Style
- **Layout:** talking head on top, B-roll on the bottom most of the time, switching to full-screen B-roll for big moments.
- **Face look (owner, Nov 18, 2026): don't alter the talking head's quality at all.** It's already high quality. The only thing allowed on it is the dark-edge vignette (`face_grade: "vignette=PI/6"`): no sharpening/unsharp, no denoise, no contrast, saturation or colour grade. `build.py` drops any other filter put in `face_grade`. (He first disliked the reddish look from the old contrast and saturation grade, then on Nov 18 said the unsharp should not have been added either.)
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
  - **Epic mode** (`"transition_style": "epic"`, opt-in only): split B-roll swaps rotate through swipe, zoom, glitch and whip-up/down on the bottom half. It's not the default; the default is the Yohan Blake / Tebogo mix below.
  - Keep them varied, never the same transition twice in a row. Motion blur peaks briefly at the cut so both shots stay sharp.
- **Captions:** word-by-word, all caps, Montserrat Black, sitting on the seam. Highlights alternate red `#E8231E` and yellow `#FFE11A`.
- **Sound effects: few, quiet, spaced out.** The owner dislikes random loud sounds mid-sentence. `build.py` and the `style.json` defaults enforce this:
  - **Off:** `graphic_sfx: false`, so graphics and animations make no sound (no stamp thuds, pops, ticks or clicks).
  - **Off:** `hit_sfx: false`, so there are no bass hits. `"hit": true` on a segment only picks the flash/shake transition.
  - **Off:** `extra_sfx_on: false`. Risers and long cinematic hits are banned outright (`BANNED_SFX`), in any video.
  - **Kept:** a quiet airy whoosh on cuts into and out of full-screen (`whoosh_level` 0.24), with small pitch variation. B-roll swaps inside the split are silent.
  - **Spaced out:** at least `sfx_min_gap` (3 s) between sound moments, and never the same sound file twice in a row.
  - The render prints the kept sound list (`SFX: …`). Check it.
  - Don't turn any of these back on unless the owner asks.
  - (History: the owner first found every-cut whooshes repetitive, then found graphic and impact sounds loud and random, and risers too loud and drawn out.)
- **Numbers and stats** get animated data graphics (`type: "data"`: counter, compare, bars, line, ring); they're silent by default. Run `suggest_data.py` on the transcript to find every number.
- **Things being talked about** get motion graphics (`type: "motion"`):
  - `stamp`: e.g. "FRAUD?"
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
  - `neon`: glowing neon sign that flickers on (`text` with `|` for line breaks, `sub`, `icon`: bolt/plus/question/flame/check/arrow, `color`, `color2`, `frame`)
  - `raceplan`: a 400 m lap where a strategy's zones (`zones` of `from`/`to` metres, `label`, `color`) fill in as a runner dot goes round; the time stays "?" until `reveal`
  - `engage`: social action buttons (`items` of `icon` like/comment/repost/share/save plus `label`) light up on the spoken word (`times`), each with a "+1"; no counts are shown
  - `scoreboard`: clean LED stadium scoreboard (`title`, `clock`, `rows` of `place`, `name`, `team`, `time`; `hi` row glows). Use it to recreate a blurry real scoreboard, with the real times only.
  - `battery`: neon batteries draining (`rows` of `label`, `to` 0–1, `color`, `end` text). Illustrative only, never a measured value.
- **Never invent data.** Don't fake stats or poll percentages. If a value is interpreted (e.g. "23 mid" → 23.5), say so to the owner.
- **Punch-in zooms** on the talking head for emphasis (`zooms`).
- **Animation clips are a standing request for future videos.** Plan short animated clips that illustrate what's being said, alongside the motion graphics. Examples: an animated track, a running-figure loop, a stopwatch or a globe spin.
  - Before each edit, list the animation moments you'd add and ask the owner to supply clips, or offer to generate them.
  - AI generation costs credits and the owner doesn't want an "AI look", so get approval first.
  - As of Nov 2026 the owner's Higgsfield account is on the free plan with 10 credits. Its 1080p models need the Basic plan or higher, and the only clips 10 credits cover are 720p, which breaks the 1080p rule. Until that changes, hand-build animations as `motion` graphics.
  - Clips go in as `type: "clip"` overlays: keyed with `key: "green"`/`"black"`, as alpha video, or full-frame as a B-roll segment.

## Default editing method (from Nov 17, 2026): the v2 cinematic style
The owner said viewers called the old edits "regular Claude editing" with "stickers slapping on the screen" and asked to go "higher and more complex". He approved the Gift Bright test (`projects/gift-bright/`, `exports/gift_bright_v2style_test_hq.mp4`) and chose this style for the next video. **Use it for every video unless he asks for the old one.** It overrides the sticker-density and split-screen parts of the Yohan Blake method below; the fact-checking, story-arc, sound and voice rules still apply.
- **Layout (owner, Nov 17, 2026):** full-screen B-roll, FX shots and cards for the big moments. **Whenever it's back on the talking head, it's a split:** face on top, a high-quality photo or video underneath. No full-screen talking head (the `"face"` segment type exists but isn't used). Sub-1080 footage still stays in the split (AI-upscaled); render FX of it at `"frame": [1080, 960]` in `fx.json`.
- **FX shots** (`editor/cinefx.py`, driven by a project `fx.json`; each renders a finished 1080×1920 clip used as a `"nograde": true` full segment):
  - `freeze_pop`: the action freezes, the athlete is cut out with a white outline and glow, the background darkens and drifts, and the name/time sits above or behind them, with a gold sub-line.
  - `text_behind`: per-frame cutout, so a big title sits behind the moving athlete.
  - `parallax`: 2.5D push on a photo (athlete layer and background move separately); `subj_scale` < 1 leaves room for a title above the head.
  - `ramp`: real time into motion-interpolated slow motion.
  - `map_africa` (or similar maps): countries light up on the spoken word.
  - `progression`: numbers card (e.g. age 14 → age 15), times count **up**.
  - Keep titles clear of the head (check a frame); titles go above or behind the subject, never hidden.
- **No stickers:** no stamp/keyword/board/poll graphics by default (`"graphics": []`).
- **Captions:** `"caption_style": "cine"`: clean white Montserrat ExtraBold phrases that build word by word; key words (names, places, times, the punchline) in `caption_emph` punch in bigger in Anton gold (`caption_accent` `#FFC83D`). Lower third on full-screen shots, on the seam in the split; `cap_y` per segment moves them off on-screen labels.
- **Grade:** B-roll gets `broll_grade` (gentle contrast, warm highs, cool shadows, light vignette, **light** grain only: heavy grain turns to mush after TikTok's re-encode). The owner's face is never touched beyond the vignette: no unsharp, no grade (see Face look).
- **Transitions:** set per segment, mostly hard `cut`s, with a whip, zoom or glitch at act changes. No flash on every full-screen cut (`"flash": false`).
- **Sound:** the voice is untouched. Only a couple of quiet hits (via `meme_sfx`), on the freeze frames.
- **Watermarks:** remove burned-in repost text from clips (`delogo`) before using them.

## Previous default editing method: the Yohan Blake edit
**This is the default way to edit every TikTok from now on.** The owner reconfirmed this on Nov 6, 2026: every TikTok should match the Tebogo vs Lyles edit (`exports/tebogo_lyles_tiktok.mp4`, built in this style) unless he asks for something different.
- **No neon theme.** The owner rejected the neon look from the 30-second test and Breaking 21 edits: no `neon`/`battery` graphics, no neon caption colors, no per-video "epic" transition or sound overrides. Use the house red/yellow captions and this style's graphics. The owner called `exports/yohan_blake_tiktok.mp4` "perfect" and "probably the best video". Its plan is `projects/yohan-blake/plan.json` and its notes are in `projects/yohan-blake/NOTES.md`. Copy its structure, pacing, graphics and transitions unless the owner asks for something different.
- **Graphics and transitions:** the owner said both were "on point". Keep the same mix and density:
  - The auto-picked viral transitions, with no per-segment overrides.
  - A graphic on almost every beat (keywords, stamps, boards, bars, counters, a poll).
  - **No name tags.** The owner rejected the red-box `name` graphic (Nov 11, 2026) for every video; `name_tags: false` in `style.json` makes `build.py` skip them. Introduce a person with a `keyword`, the captions, or the `podcast` mic badge for a guest clip.
  - Don't thin them out or swap in new styles without asking.
- **Footage rights (owner, Nov 12, 2026):** for TikTok edits, use the real footage: broadcast race clips, news packages, interviews and athlete profiles, cut in as B-roll and soundbites. Don't use it in anything made for YouTube; YouTube versions need licensed or the owner's own footage. Credit the sources in `CREDITS.md`.
  - Where to get it from the cloud session: Dailymotion mirrors a lot of athlete profiles and interviews (search its API, download with yt-dlp), and some news sites embed downloadable video (NBC News, Fox News, ABC13).
  - YouTube, FloTrack and MileSplit block downloads here. Don't try to get around that; list those clips in `footage_wanted.md` for the owner to drop in Dropbox.
- **Pull relevant historical media online whenever the owner's footage doesn't cover the story.** That means photos of the athletes, races and moments being discussed. Use it even when he sends B-roll, if a moment he talks about isn't covered. See "When the owner sends only a talking head" below for sources and rules.
- **Story arc:** build the edit as an argument with a payoff.
  1. **Hook (0–15 s):** the subject full-screen, the claim as a `keyword` ("ALWAYS 2ND TO BOLT?"), a `stamp` on the punchline ("BIGGEST LIE"), and `bubbles` for "what people say online".
  2. **Context:** what's true about the subject, shown as data (an all-time `board`, a `pin` for where it happened, a `stamp` for the twist, e.g. "NOT A CHAMPIONSHIP").
  3. **Turn:** cut to full-screen on the key fact, with a `data` counter.
  4. **The real story:** each new person introduced in the voice/captions (or a `keyword`), then a `board` listing the evidence, one row landing on each spoken item (`times`).
  5. **Callback:** full-screen with the claim stamped again ("WRONG ERA?" → "LIE").
  6. **Proof:** actual results for each event the owner names (`bars` with real times, the subject's place in the name), with a stamp on each verdict ("4TH PLACE", "4TH AGAIN").
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

## Workflow
1. **Get the files.** Files over 30 MB come as Dropbox links.
   - Share links (`/scl/fi/...`): download with `?dl=1`.
   - Transfer links (`/transfer/...`): run `node editor/fetch_dropbox_transfer.js <url> <dir>`. You get a zip; unzip it into its own folder.
   - **Guest soundbites:** when the owner references someone's interview or podcast, cut the guest's best 15–25 s into the A-roll right after the owner introduces them. The guest's footage takes the top "speaker" slot, in the same 1440×1280 framing with any on-screen banners cropped off. Match its loudness to the owner's voice, and merge the guest's captions into the timeline. See `projects/flotrack-masai/`.
2. **Transcribe** with `transcribe.py … medium.en`, then fix names and numbers by hand (check bibs and graphics).
3. **Crop** the talking head to the top-half framing (1440×1280 intermediate), then run `tighten.py` to cut dead air. Check the result is still at least 61 s.
4. **Write `plan.json`.** Start from `projects/yohan-blake/plan.json`, the default editing method (see above).
5. **Render** with `python3 editor/build.py plan.json`, check sample frames, then export to `exports/` and push.
6. **Deliver to the owner's Dropbox** too: save every finished export to `/TikTok Exports/` in his Dropbox. He's connected it through the Composio connector (account "Erin Brown Track & Field").
   - Files over about 150 MB can't go through `DROPBOX_UPLOAD_FILE`. Use `DROPBOX_SAVE_URL` with the file's GitHub LFS URL (`https://media.githubusercontent.com/media/<owner>/<repo>/<branch>/exports/<file>`), so Dropbox fetches it server-side.
   - Check the returned `content_hash` against the local file (SHA-256 of the per-4 MB-block SHA-256s) before telling the owner it's there.
   - He can also put raw footage in his Dropbox and name the folder; read it from there instead of asking for share links.
7. **Write a title** for every video: a one-line, YouTube Shorts style hook (the owner asked for this on all of them).
   - Lead with a name people search plus the conflict or twist (e.g. "He Refused to Leave the Track… 11 Years Later, Track Banned Him").
   - Keep it under about 70 characters so it isn't cut off in the Shorts feed. One emoji at most.
   - No claim the video doesn't back up.
   - Put it at the top of the project's `NOTES.md` and give it to the owner with the finished video.
7b. **Send it to the owner's TikTok and Instagram** (set up Nov 12, 2026) through the vidIQ connector, once he approves the video:
   - **Track videos** (every chat) go to the TikTok account **"Erin Spider Brown"** (`platformAccountId` `_000ssAV0cJxYmcJ0XSxwm8rgS87rI5_tVPx`).
   - **GTA videos** (the GTA chat) go to TikTok **"6starfiles"** (`_000q3uBIYM4vO1HWm18pq2_3BVJbWI6uGec`). Never mix the two.
   - **Cover thumbnail on every upload (owner, Nov 12, 2026):** neither upload API takes a cover image, so build the upload copy with `editor/social_cover.sh <export> <thumb.jpg> <out> [bitrate]`. It puts the 9:16 cover as the first 0.1 s, which TikTok and Instagram use as the cover; the audio is copied untouched. Upload that copy, not the bare export.
   - **Track videos also go to Instagram @e.diamondz as a Trial Reel** (`vidiq_instagram_publish_reel`, account `29211548525143718`, `trialParams.graduationStrategy: "MANUAL"`, so he decides when to share it to followers; no AI label). Instagram takes at most 299 MB and 15 min, so upload a ~5 Mbps copy if the export is bigger.
   - **YouTube Shorts too (owner, Nov 13, 2026):** every TikTok video also goes to his main YouTube channel **The Erin Brown** (`UCiMHg3V2Q414zFIjb8PyTcg`) as a Short, using **the TikTok cut as-is**, news footage included. He chose this over the stock-only YouTube versions after being told about the copyright-claim risk; this overrides the "not for YouTube" line in Footage rights. Title = the video title + " #Shorts", category 17 (Sports). Ask him the privacy (he chose public for the NIL Short).
   - **Facebook Page too:** API-posted Instagram reels don't trigger Instagram's auto-share to Facebook, and trial reels go to non-followers only, so every Instagram video is also posted straight to his Facebook Page **E.Diamondz** (id `506309812910570`). vidIQ has no Facebook Page connected; post through the Composio facebook connection (account "Erin EDiamondz Brown") with `FACEBOOK_PUBLISH_PAGE_REEL` (`page_id`, `file_url` = the export's public GitHub LFS/raw URL, `description` = title plus hashtags, `video_state: PUBLISHED`). Before posting, check `FACEBOOK_LIST_PAGE_REELS` for a reel of the same length, so the same video isn't posted twice (another chat had to delete 6 duplicates on Nov 17).
   - Upload the export with `vidiq_video_upload` (`localFile` for files over 299 MB), then `vidiq_social_post_draft_create`. The caption is the title plus a few hashtags.
   - Owner's settings: `privacyLevel: PUBLIC_TO_EVERYONE` (**public**; owner, Nov 13, 2026: "make sure when you post the videos on TikTok that they're public and not private"), `allowComment: true`, `musicUsageConfirmed: true` (he accepted TikTok's terms).
   - **Standing approval (owner, Nov 17, 2026): "post it to TikTok, YouTube Shorts, Instagram trial reels, as well as Facebook. And do that for every TikTok that you create."** Once a video is finished and checked, post it to all four without asking again: TikTok public, YouTube Short public, Instagram trial reel (MANUAL), Facebook Page. Use the title plus hashtags as the caption, and send him the links. If he has asked to review a video first, wait for that.
   - **Reconfirmed (owner, Nov 24, 2026): "When a video is done, post automatically. You don't have to ask for my permission anymore. Just go ahead and post on all platforms."** Never stop to ask before posting a finished video. Post right away: if vidIQ suggests a later TikTok time for pacing, ignore it and post now (he asked for "right now" when one was scheduled on Nov 18).
   - Check `vidiq_social_post_status` until it's `completed`.
8. **Make a cover thumbnail** for every video in the style of the covers the owner currently uses (he sent examples on Nov 10, 2026, and rejected a split close-up and a plain photo with Anton text).
   - **Format:** 9:16, 1080×1920 JPG, saved to `exports/thumbnails/<video>_thumb.jpg`. Also save a 3:4 grid crop (`_thumb_3x4.jpg`), with everything important inside it. Deliver both to Dropbox with the video.
   - **Photos (owner, Nov 18, 2026):** official, high-quality photos of the athletes in the story only, e.g. press photos from the news articles (their lead images, at the largest size the site serves) or race photos he sends. **No screen grabs from videos, and never the owner himself.** Make it a designed graphic, not a plain photo.
   - **Design (owner, Nov 18, 2026: "the font sucks, the coloring sucks… make it eye-catching and high quality"):** magazine-poster layout, typeset in HTML and rendered with Playwright (see `projects/eat-some-food/cover/`). That means a cinematic grade with film grain, a small tracked kicker, a giant condensed headline *behind* the cut-out athlete, a clean skewed red slab for the key fact, and a gold quote line. No clip-art arrows or brush swipes on these.
   - **Background:** one sharp, full-bleed real photo (no AI images). The subject is cut out (rembg `u2net_human_seg`) and graded punchy, and the background is slightly blurred and darkened.
   - **Headline:** a big, bold, slanted headline in Montserrat Black: a white line over a yellow-gradient line, black stroke, drop shadow, with a tapered red brush swipe under it (e.g. "THE NEXT / BOLT?", "NO ARMS / NO LIMITS").
   - **Extras when they help the story:** a circle inset with a white/red ring and glow, a short red label tag, and a curved red arrow with a white outline pointing at the subject.
   - **Checks:** photos at native resolution, never enlarged. Faces, hands and gestures must not be cut off or covered.
   - **Example:** `projects/matthew-boling/thumbnail.py`.
- **Exports too big for GitHub's 100 MB limit at full quality** go through Git LFS (`exports/*_hq.mp4`). Measure SSIM against the master and keep it at 0.98 or higher, rather than squeezing under 100 MB and losing quality.

## Setup in a fresh session
Run `editor/setup.sh`. It installs faster-whisper and downloads the fonts and the Mixkit sound library into `editor/assets/`, which is gitignored. Node Playwright and Chromium render the graphics.
