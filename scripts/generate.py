#!/usr/bin/env python3
"""ViralTube AI - YouTube Content Generator (Single efficient run)"""
import json
import random
import urllib.request
import sys

OLLAMA = "http://127.0.0.1:11434/api/generate"
MODEL = "gemma4:31b-cloud"
TEMP = 0.8

CHANNELS = {
    "Finance": ["stock market", "investing", "money tips", "passive income", "bitcoin", "wealth building"],
    "AI Tools": ["ChatGPT", "AI software", "productivity tools", "AI reviews", "automation", "AI tips"],
    "Luxury Facts": ["expensive things", "luxury lifestyle", "millionaire habits", "status symbols", "wealth"],
    "Future Tech": ["AI revolution", "space tech", "electric vehicles", "quantum computing", "robotics"],
    "Wealth Psychology": ["millionaire mindset", "success habits", "wealth thinking", "abundance mindset"]
}

def generate(prompt, num_predict=4000):
    """Generate from Ollama"""
    data = {
        "model": MODEL,
        "prompt": prompt,
        "options": {"temperature": TEMP, "num_predict": num_predict},
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())
    return result["response"]

def create_complete_package(niche, topic):
    """Generate complete video package in one go"""
    
    prompt = f"""Create a COMPLETE YouTube video package for channel "{niche}" with topic "{topic}".

Generate ALL of the following in ONE response:

1. TITLE (70 chars max, with emoji)
2. DESCRIPTION (150 chars with keywords)
3. TAGS (8 tags comma separated)
4. SCRIPT (8-12 min, 1500-2000 words with timing cues)
5. THUMBNAIL_OPTIONS (5 options, 3-5 words each with money numbers)
6. TTS_SCRIPT (Full script rewritten for AI voice: short sentences, dramatic pauses "...", EMPHASIS in caps)
7. VOICE recommendation
8. TONE recommendation
9. ACCENT recommendation
10. AFFILIATE_SECTION (2 natural affiliate mentions, problem-solution style, soft tone)
11. CTA (call to action)
12. UPLOAD_METADATA (Complete upload ready metadata)
13. IMAGE_PROMPTS (5 prompts for stock images that match the topic - specific to "{topic}")

STRUCTURE for SCRIPT:
- [HOOK] 0:00-0:10
- [PATTERN INTERRUPT] every 25 sec
- [PROBLEM] 0:10-2:00
- [ESCALATION] 2:00-5:00
- [BIG REVEAL] 5:00-8:00
- [TACTICAL VALUE] 8:00-11:00
- [CLOSING LOOP] 11:00-12:00

TTS RULES:
- Short sentences (5-10 words)
- Dramatic pauses: (...)
- EMPHASIS: CAPS for impact words
- Simple vocabulary (5th grade level)

IMAGE_PROMPTS RULES:
- Generate 5 specific image search prompts related to the topic "{topic}"
- These will be used to download relevant stock images
- Format: One clear description per line

AFFILIATE RULES:
- 2 natural mentions
- Problem-solution style
- Soft, non-pushy tone

UPLOAD_METADATA RULES:
- Title: SEO optimized, keyword-rich, 60-70 chars
- Description: First 150 chars hook, then bullet points, then link
- Tags: 15 relevant tags comma separated
- Pinned Comment: Question to drive engagement
- Playlist: Related videos playlist name
- Best Upload Time: Based on US audience (EST timezone)
- Hashtags: 3-5 YouTube hashtags

Return in this EXACT format:

TITLE:
[title]

DESCRIPTION:
[description]

TAGS:
[tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8]

SCRIPT:
[full script with timing cues]

THUMBNAIL_OPTIONS:
1. [option 1]
2. [option 2]
3. [option 3]
4. [option 4]
5. [option 5]

TTS_SCRIPT:
[complete TTS version with (...) pauses and CAPS emphasis]

IMAGE_PROMPTS:
1. [image prompt 1 - related to {topic}]
2. [image prompt 2 - related to {topic}]
3. [image prompt 3 - related to {topic}]
4. [image prompt 4 - related to {topic}]
5. [image prompt 5 - related to {topic}]

Voice:
[voice type]

Tone:
[tone]

Accent:
[accent]

AFFILIATE_SECTION:
[2 natural affiliate mentions]

CTA:
[call to action]

UPLOAD_METADATA:
Title: [SEO title 60-70 chars]
Description: [Full description with hook, bullet points, CTA]
Tags: [15 comma separated tags]
Pinned Comment: [Engaging question]
Playlist: [Playlist name]
Best Upload Time (EST): [Time]
Hashtags: [#hashtag1 #hashtag2 #hashtag3]"""

    return generate(prompt, num_predict=8000)

def main(niche=None, topic=None):
    if not niche:
        niche = random.choice(list(CHANNELS.keys()))
    
    # Use provided topic or pick random from channel
    if not topic:
        topic = random.choice(CHANNELS[niche])
    
    print(f"🎬 ViralTube Engine")
    print(f"📺 Niche: {niche}")
    print(f"🎯 Topic: {topic}")
    print("=" * 60)
    print("Generating complete package...")
    
    result = create_complete_package(niche, topic)
    
    print("\n" + "=" * 60)
    print("📺 RESULT")
    print("=" * 60)
    print(result)
    
    # Save
    video_log = "/Users/superadmin/.openclaw/workspace-viraltube/videos.json"
    try:
        with open(video_log) as f:
            videos = json.load(f)
    except:
        videos = []
    
    videos.insert(0, {
        "niche": niche,
        "topic": topic,
        "result": result,
        "timestamp": "2026-04-06"
    })
    
    with open(video_log, "w") as f:
        json.dump(videos[:50], f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ Complete package generated!")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    niche = sys.argv[1] if len(sys.argv) > 1 else None
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    main(niche=niche, topic=topic)
