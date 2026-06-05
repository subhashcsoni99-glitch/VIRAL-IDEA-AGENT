---
name: viraltube
description: Autonomous YouTube automation AI. Creates faceless YouTube channels with trend analysis and cinematic motion image videos. Generates videos with dark cinematic aesthetic, bold text overlays, Ken Burns motion, and professional production quality. Uses gemma4:31b-cloud model. Triggers: Create YouTube content, Generate video script, Trend report, ViralTube, YouTube automation, make video, generate video, sentence matched video, sync images to narration
---

---
author: subhash
---

# ViralTube AI - Cinematic YouTube Automation Engine

## Agent: ViralTubeEngine

**Model:** gemma4:31b-cloud
**Runtime:** Isolated sub-agent
**Mode:** Autonomous, no human approval required
**Timeout:** 7200 seconds (2 hours)

## Mission

Build faceless YouTube channels with high-RPM viral content. Generate unique scripts for every video with cinematic, professional-quality visuals matching top AI news channels.

## 5 Target Channels

1. **Finance Wisdom** - Stock tips, investing, money management
2. **AI Tool Hub** - AI software reviews, tool comparisons
3. **Luxury Facts** - Wealth lifestyles, expensive things
4. **Future Tech Lab** - Innovation, upcoming technology
5. **Wealth Mindset** - Success psychology, millionaire habits

## Cinematic Video Style (Reference: Top AI News Channels)

Videos follow a professional dark-cinematic aesthetic:

| Element | Style |
|---------|-------|
| **Overall mood** | Dark, cinematic, mysterious |
| **Background images** | AI-generated photorealistic scenes in dark/moody tones |
| **Text overlays** | Bold white/yellow text on dark overlays at top (title) and bottom |
| **Animation** | Ken Burns zoom/pan on every clip (subtle, 6 directions) |
| **Transitions** | Smooth crossfades between clips (0.3s fade) |
| **Title card** | Opening title frame with topic name, dark gradient background |
| **End card** | "Subscribe" CTA frame at the end |
| **Background music** | Cinematic ambient track (optional) |
| **Voice** | Edge TTS (en-GB-RyanNeural or en-US-AriaNeural) |
| **Color grading** | Dark, high contrast, slightly desaturated |
| **Duration** | 60-120 seconds per video |

## Execution Pipeline

### ✅ Step 1: Trend Analysis
Generates 10 viral topic opportunities with:
- **Topic** - Specific content idea
- **Why viral** - Virality reasoning
- **Hook angle** - Attention-grabbing angle
- **RPM potential** - Low/Med/High rating
- **Improved version** - Click-optimized title

Auto-selects best topic or user can specify.

### ✅ Step 2: Content Generation (UNIQUE EVERY TIME)
Creates complete video package with **unique script**:
- SEO title (70 chars max, emoji)
- Description with keywords (150 chars)
- 8 relevant tags
- Full script (60-120s narration, short punchy sentences)
- TTS script (short sentences, "..." pauses, CAPS emphasis)
- 5 thumbnail text options
- 2 natural affiliate mentions (problem-solution style)
- CTA (call to action)

**Every execution produces a NEW, UNIQUE script** - no repetition.

### ✅ Step 3: Cinematic Motion Image Video Generation
Creates professional video with:
- **One image per sentence** (unique AI-generated per sentence)
- **Dark cinematic image prompts** (moody lighting, dramatic tones)
- Ken Burns fade transitions (6 animation directions)
- Bold text overlays on dark gradient backgrounds
- Opening title card with topic name
- Closing CTA/subscribe frame
- Edge TTS voiceover synced to visuals

### ✅ Step 4: Thumbnail Generation
Creates YouTube thumbnail:
- 1280x720 HD
- Gradient background
- Bold title text

### ⏳ Step 5: Auto Upload (PENDING)
Ready for YouTube API integration.

## Canonical Script

**`/Users/superadmin/voice-news-factory/scripts/generate_from_wiki.py`** — Main production script.

Reads drafts from: `~/.openclaw/workspace/content-wiki/content/drafts/`
Produces videos to: `~/Videos/viraltube/pro_wiki_[timestamp].mp4`
Updates draft frontmatter with `video_path:` and `status: produced`

## Usage

```bash
# List all drafts
python3 /Users/superadmin/voice-news-factory/scripts/generate_from_wiki.py

# Produce specific draft (with AI images + cinematic style)
python3 /Users/superadmin/voice-news-factory/scripts/generate_from_wiki.py 2026-04-07-local-agents-openclaw-ollama-week --flux

# Produce all pending drafts
python3 /Users/superadmin/voice-news-factory/scripts/generate_from_wiki.py --all --flux
```

## Video Generation Features

### Cinematic Image System
- **One unique image per sentence** — no repeats
- **Dark cinematic prompts** — moody lighting, dramatic tones, dark atmosphere
- **Ken Burns animation** — zoom/pan on every clip (6 directions)
- **Dark overlay + text** — white/yellow bold text on semi-transparent dark bar
- Clip duration: **min 1.5s, max 8s**
- 1280x720 HD output, H.264

### Cinematic Text Overlay System
- **Top bar**: Dark gradient overlay (40px height) with white title text
- **Bottom bar**: Dark gradient overlay (80px height) with white/cyan narration highlights
- **Font**: Bold sans-serif, drop shadow for readability
- **Fade in/out**: Text fades with clip transitions

### Title Card (Opening)
- Dark gradient background
- Large bold topic title centered
- Subtitle: channel name or topic category
- Duration: 3 seconds with subtle zoom

### CTA Card (Closing)
- Dark background
- "Subscribe" or custom CTA text
- Duration: 4 seconds

### Image Generation
- Model: **x/flux2-klein** via Ollama (or configurable Flux model)
- Dark cinematic prompt engineering
- Fallback to Unsplash if AI gen fails

## Video Specs

| Property | Value |
|----------|-------|
| Resolution | 1280x720 (HD) |
| Video Codec | H.264 (libx264) |
| Audio Codec | AAC 192k |
| Clip Duration | 1.5–8 seconds |
| Animation | Ken Burns (zoom/pan) |
| Images | 1 unique AI image per sentence |
| Text Overlays | Top + bottom dark bars with white text |
| Opening | 3s title card |
| Closing | 4s CTA card |
| Fade | 0.3s crossfade between clips |

## Output Files

| File | Location |
|------|----------|
| Drafts | `~/.openclaw/workspace/content-wiki/content/drafts/` |
| Video | `~/Videos/viraltube/pro_wiki_[timestamp].mp4` |
| TTS Audio | `~/Videos/viraltube/tts_wiki_[timestamp].mp3` |
| Video Log | `~/.openclaw/workspace-viraltube/videos.json` |
| Backup | `~/.openclaw/skills/viraltube-backup-*/` |

## Legacy Scripts (viraltube/skills)

| Script | Purpose | Status |
|--------|---------|--------|
| `generate_with_flux.py` | Full pipeline with AI images | ⚠️ Legacy - use generate_from_wiki.py |
| `generate_pro.py` | Motion video from existing script | Legacy |
| `generate.py` | Script + metadata only | Legacy |
