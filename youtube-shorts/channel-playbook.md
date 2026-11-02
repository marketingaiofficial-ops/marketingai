# Faceless 3D Explainer Shorts: Channel Playbook

Reference channel: [Zack D. Films](https://m.youtube.com/@zackdfilms). We study its format; we never copy its videos, characters or branding.

## 1. What the reference channel does (research, Nov 2026)

Figures come from public stats trackers (vidIQ, VidAnalyze). They are estimates, not official numbers.

| Metric | Value |
|---|---|
| Subscribers | ~29.3–29.4M |
| Lifetime views | ~81B |
| Public videos | ~4,100 since June 2021, roughly 3 uploads/day |
| Avg. views per video | ~19.7M (tracker estimate) |

### The format formula
1. **Format:** vertical Shorts, 30–60 s, with realistic 3D CGI. There is no presenter and no face cam.
2. **Hook in the first second:** narration over the most dramatic visual. The pattern is "This man is about to…", "Here's what happens if…" or "This is how…".
3. **Curiosity gap:** the narrator states something surprising, then explains it step by step, usually showing the inside of the body or object.
4. **One idea per video,** told as a micro-story with a twist or payoff at the end.
5. **Calm, confident male narration.** The pacing is fast but never rushed, with short sentences.
6. **Evergreen topics:**
   - The human body: "what happens to your body if…"
   - Survival and safety hacks
   - Strange history: disasters and odd inventions
   - How everyday things work
   - Myth-busting
7. **Volume:** several uploads a day. The look stays consistent, so each video is instantly recognisable.

## 2. Our channel: positioning

Body science and survival explainers in 3D, where every video teaches one thing that could save your life or blow your mind.

Name ideas (check that the handle is free before choosing):
- **Inside Out 3D**
- **BodyGlitch**
- **What Really Happens**
- **Curio3D**
- **The Hidden Why**

Brand rules:
- **Voice:** ElevenLabs "Viraj – Dramatic TV Narration" (voice_id `3Dfn3iRttMKWMoZ2tEFU`), model `eleven_v4`. Use the same voice on every video for brand recognition.
- **Look:** clean 3D render style, saturated colour-coding and the same caption style everywhere:
  - O₂ = cyan
  - CO₂ = amber
  - danger = red
  - key fact = yellow
- **Captions:** Inter Display Black, uppercase, 1–4 words per chunk, centred at y≈1395 (inside the Shorts safe zone).
- **No logo bug, no "subscribe" pleas inside the video.** Let the loop do the work.

## 3. Episode structure (55–62 s)

| Beat | Time | Purpose |
|---|---|---|
| Hook | 0–5 s | Most dramatic visual plus "This man is about to…" |
| Setup | 5–14 s | What the person does (the mistake or situation) |
| Mechanism | 14–30 s | Inside-the-body or inside-the-object explanation with colour-coded HUD |
| Escalation | 30–44 s | Consequences build: meters, heartbeat, tension |
| Climax | 44–48 s | The moment, with silence or impact |
| Name it | 48–54 s | Big title card of the concept |
| Takeaway | 54–61 s | 1–2 rules. End cleanly so the Short loops. |

Script length is 140–150 words for about 60 s with the Viraj voice.

## 4. Production pipeline (what is in this repo)

1. **Script:** write the beats above and fact-check every claim.
2. **Voiceover:** ElevenLabs `creative_generate_speech`, then pick the best take.
3. **Word timings:** ElevenLabs Scribe (`creative_transcribe_audio`) produces `assets/words.json`.
4. **SFX:** ElevenLabs text-to-sound covers ambience, whooshes, heartbeat, impacts and breathing. Keep one take each.
5. **Visuals:** a procedural 3D-style renderer in `ep01-shallow-water-blackout/render/engine.py`. It provides:
   - an underwater pool with perspective floor, caustics and god rays
   - "clay 3D" characters
   - glossy organs and molecules
   - HUD panels, captions and grading
6. **Edit and timeline:** `render/ep01.py` defines the scenes, transitions, captions synced to the word timings, and parallel rendering.
7. **Sound design:** `render/mix_audio.py` builds the score, places the SFX, ducks the music, and runs loudnorm to -14 LUFS.
8. **Mux:** the final MP4 is 1080×1920, 30 fps, H.264 with AAC audio.

Upgrade path: with credits on Higgsfield (Seedance / Kling image-to-video), or with the full ElevenLabs connector, generated CGI clips can replace or augment the procedural scenes. The timeline, captions, VO and mix pipeline stay the same.

## 5. Next 20 episode ideas (same niche, all original)

1. What happens to your body if you hold in a sneeze
2. Why you should never jump into cold water (cold shock response)
3. What a rip current does, and the one way out (swim parallel)
4. Why "stop, drop and roll" works
5. What happens inside your ear when you go too deep underwater
6. Why carbon monoxide kills silently
7. What happens to your body in a lightning strike, and the 30/30 rule
8. Why you shouldn't pull out a stabbed object
9. What happens to your eyes when you look at a solar eclipse
10. Why choking victims can't cough, and the Heimlich manoeuvre
11. What happens to your body in an elevator free-fall
12. Why hypothermia makes people take their clothes off (paradoxical undressing)
13. What altitude sickness does to your brain
14. Why you should never heat honey or water in a sealed container
15. What happens if you swallow a magnet (or two)
16. Why your ears pop on a plane
17. What a concussion does inside the skull
18. Why you should never touch someone being electrocuted
19. What happens to your body when you donate blood
20. Why drowning doesn't look like drowning (instinctive drowning response)

## 6. Upload checklist (per Short)
- **Title:** under 60 characters, curiosity plus a stake, e.g. "Why strong swimmers black out underwater 😳".
- **Description:** 1–2 lines explaining the fact, a safety line if relevant, 3–5 hashtags (#shorts #science #3danimation + topic).
- **Cover frame:** pick the hook frame (subject plus red target ring).
- **Pinned comment:** a question that invites answers ("Did you know this? 👇").
- **Cadence target:** start at 1 per day, scale to 2–3 per day once the pipeline is templated.
