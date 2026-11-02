# Ep01: "Shallow Water Blackout"

A 61 s vertical Short (1080×1920, 30 fps) with an ElevenLabs voiceover, a procedural 3D-style render, synced captions and full sound design.

Final file: `out/ep01_shallow_water_blackout.mp4`

## Upload copy

**Title options**
- Why strong swimmers black out underwater 😳
- Never do this before swimming underwater
- This is why you should never hold your breath alone

**Description**
> Breathing fast before a dive doesn't load you up with oxygen. It flushes out CO₂, the thing that tells your brain to breathe. Your oxygen can run out before the alarm ever goes off. This is shallow water blackout.
> Never hyperventilate before going underwater, and never hold your breath alone.
> #shorts #science #swimming #3danimation #watersafety

## Script (voice: ElevenLabs "Viraj – Dramatic TV Narration", eleven_v4)

| Time | Line | Visual |
|---|---|---|
| 0.0 | This man is about to black out underwater… and he has no idea. | Underwater tracking shot, red target ring on the swimmer |
| 5.4 | Before diving in, he breathes really fast, over and over. | Hologram body with lungs pumping at 4× speed |
| 10.1 | He thinks he's loading up on oxygen, so he can stay under longer. | O₂ molecules streaming into the lungs |
| 14.3 | But he's not. Fast breathing barely adds any oxygen. | Blood vessel; RBCs already full; meter 97%→98% |
| 18.6 | Instead, it flushes carbon dioxide out of his blood. | CO₂ molecules leave the vessel; CO₂ meter drops |
| 22.5 | And here's the problem. Your urge to breathe isn't triggered by low oxygen… | Brain with "breathing alarm"; low-O₂ signal crossed out |
| 27.4 | …it's triggered by rising carbon dioxide. | CO₂ signal fires; alarm flashes "BREATHE!" |
| 30.4 | So as he swims, his oxygen keeps falling… but the alarm… never goes off. | Swimmer with HUD: O₂ falling, CO₂ below alarm line, alarm silent |
| 37.7 | He feels completely fine. Then, without any warning… his brain simply shuts down. | Close-up; heartbeat; desaturation; tunnel vision; cut to black |
| 44.9 | No struggle. No splash. No cry for help. | Swimmer limp, sinking; last bubbles escape |
| 48.6 | This is called shallow water blackout. It can happen to even the strongest swimmers. | Title slam: SHALLOW / WATER / BLACKOUT |
| 54.4 | So never hyperventilate before going underwater… and never, ever hold your breath alone. | Two rule cards; two swimmers together |

Fact basis: hyperventilation lowers blood CO₂ (hypocapnia) but adds little oxygen, because arterial blood is already ~97–99% saturated. The drive to breathe is mainly CO₂-driven, so the breathing urge is delayed while O₂ falls until loss of consciousness (hypoxic blackout). See for example the CDC MMWR (2011) report on hazardous underwater breath-holding behaviors.

## Rebuild

```bash
pip install numpy opencv-python-headless scipy pillow
cd render
python3 ep01.py preview /tmp 0.6 25 44     # preview frames
python3 ep01.py render 4                    # -> out/video_noaudio.mp4
python3 mix_audio.py                        # -> out/mix.wav (-14 LUFS)
ffmpeg -i ../out/video_noaudio.mp4 -i ../out/mix.wav -c:v libx264 -crf 18 -preset slow \
       -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart ../out/ep01_shallow_water_blackout.mp4
```

## Assets
- `assets/audio/voiceover.mp3`: ElevenLabs TTS (Take A of 2)
- `assets/words.json`: ElevenLabs Scribe word timings, which drive captions and scene timing
- `assets/audio/sfx_*.mp3`: ElevenLabs text-to-sound effects
- ElevenLabs flow with all generations: https://elevenlabs.io/app/flows/BlfK39iSHZRClaIXjwMR
