#!/usr/bin/env python3
"""ViralTube AI + Flux Image Generation - Integrated Pipeline"""
import json
import random
import urllib.request
import subprocess
import os
import re
import base64
import time
from datetime import datetime

OLLAMA = "http://127.0.0.1:11434/api/generate"
OLLAMA_IMG = "http://127.0.0.1:11434/api/generate"
SCRIPT_MODEL = "gemma4:31b-cloud"
IMAGE_MODEL = "x/flux2-klein"
TEMP = 0.8

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
IMG_DIR = "/tmp/unique_images_flux"
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

CHANNELS = {
    "Finance": ["stock market", "investing", "money tips", "passive income", "bitcoin", "wealth building"],
    "AI Tools": ["ChatGPT", "AI software", "productivity tools", "AI reviews", "automation", "AI tips"],
    "Luxury Facts": ["expensive things", "luxury lifestyle", "millionaire habits", "status symbols", "wealth"],
    "Future Tech": ["AI revolution", "space tech", "electric vehicles", "quantum computing", "robotics"],
    "Wealth Psychology": ["millionaire mindset", "success habits", "wealth thinking", "abundance mindset"]
}

def generate(prompt, model=SCRIPT_MODEL, num_predict=4000, timeout=300):
    """Generate from Ollama"""
    data = {
        "model": model,
        "prompt": prompt,
        "options": {"temperature": TEMP, "num_predict": num_predict},
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
        return result["response"]
    except Exception as e:
        print(f"   ⚠️ Generation error: {e}")
        return None

def generate_image(prompt, output_path, size=1024):
    """Generate image using Flux model via Ollama"""
    data = {
        "model": IMAGE_MODEL,
        "prompt": f"{prompt}, highly detailed, 4k, professional photography, cinematic lighting",
        "stream": False,
        "options": {"temperature": 0.8}
    }
    req = urllib.request.Request(
        OLLAMA_IMG,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read())
        
        if 'image' in result:
            img_data = base64.b64decode(result['image'])
            with open(output_path, 'wb') as f:
                f.write(img_data)
            size_mb = len(img_data) / 1024 / 1024
            return True, size_mb
        else:
            # Try response field
            if 'response' in result:
                print(f"   ⚠️ No image in response, got text instead")
            return False, 0
    except Exception as e:
        print(f"   ⚠️ Image gen failed: {e}")
        return False, 0

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
13. IMAGE_PROMPTS (5 prompts for AI image generation matching the topic "{topic}")

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
- Generate 5 specific image prompts for AI image generation
- Each prompt should be a vivid, detailed scene description
- Format: One clear, detailed prompt per line
- Focus on cinematic, 4k quality visual descriptions

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
1. [detailed image prompt 1]
2. [detailed image prompt 2]
3. [detailed image prompt 3]
4. [detailed image prompt 4]
5. [detailed image prompt 5]

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

def parse_image_prompts(result):
    """Extract IMAGE_PROMPTS from result"""
    prompts = []
    if 'IMAGE_PROMPTS:' in result:
        start = result.find('IMAGE_PROMPTS:') + 15
        end = result.find('Voice:', start)
        if end == -1:
            end = len(result)
        section = result[start:end].strip()
        # Parse numbered lines
        for line in section.split('\n'):
            line = line.strip()
            if line and line[0].isdigit():
                # Remove leading number and dot
                dot_idx = line.find('.')
                if dot_idx > 0 and dot_idx < 5:
                    prompt = line[dot_idx+1:].strip()
                    if prompt:
                        prompts.append(prompt)
    return prompts

def create_clip(img_path, duration, clip_path):
    """Create a single clip with Ken Burns animation and fade transitions"""
    # Clamp duration: max 10s, min 1s
    duration = max(1.0, min(10.0, duration))
    fade_out = max(0, duration - 0.3)
    
    # Ken Burns: slow zoom/pan - alternate between zoom-in and pan directions
    import random
    direction = random.choice(['zoom_in', 'zoom_out', 'pan_left', 'pan_right', 'pan_up', 'pan_down'])
    
    if direction == 'zoom_in':
        vf = f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(zoom+0.005,1.3)':d=25:s=1280x720,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out}:d=0.3"
    elif direction == 'zoom_out':
        vf = f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='max(zoom-0.005,1.0)':d=25:s=1280x720,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out}:d=0.3"
    elif direction == 'pan_left':
        vf = f"scale=1440:810:force_original_aspect_ratio=increase,crop=1280:720:x='min(x+2,160)':y='(ih-720)/2',zoompan=z=1.05:d=25:s=1280x720,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out}:d=0.3"
    elif direction == 'pan_right':
        vf = f"scale=1440:810:force_original_aspect_ratio=increase,crop=1280:720:x='max(x-2,0)':y='(ih-720)/2',zoompan=z=1.05:d=25:s=1280x720,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out}:d=0.3"
    elif direction == 'pan_up':
        vf = f"scale=1440:810:force_original_aspect_ratio=increase,crop=1280:720:x='(iw-1280)/2':y='min(y+2,90)',zoompan=z=1.05:d=25:s=1280x720,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out}:d=0.3"
    else:  # pan_down
        vf = f"scale=1440:810:force_original_aspect_ratio=increase,crop=1280:720:x='(iw-1280)/2':y='max(y-2,0)',zoompan=z=1.05:d=25:s=1280x720,fade=t=in:st=0:d=0.3,fade=t=out:st={fade_out}:d=0.3"
    
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", img_path,
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-r", "25",
        clip_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0 and os.path.exists(clip_path)

def main(niche=None, topic=None):
    if not niche:
        niche = random.choice(list(CHANNELS.keys()))
    
    if not topic:
        topic = random.choice(CHANNELS[niche])
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    print("=" * 60)
    print("🎬 VIRALTUBE + FLUX IMAGE GENERATION")
    print("=" * 60)
    print(f"📺 Niche: {niche}")
    print(f"🎯 Topic: {topic}")
    print(f"🖼️ Image Model: {IMAGE_MODEL}")
    print("=" * 60)
    
    # Step 1: Generate script
    print("\n1️⃣ Generating video script...")
    result = create_complete_package(niche, topic)
    
    if not result:
        print("❌ Script generation failed")
        return
    
    print("   ✅ Script generated")
    
    # Step 2: Generate images with Flux
    print(f"\n2️⃣ Generating images with {IMAGE_MODEL}...")
    prompts = parse_image_prompts(result)
    
    if not prompts:
        print("   ⚠️ No image prompts found, using topic as prompt")
        prompts = [topic] * 5
    
    print(f"   📝 {len(prompts)} prompts to generate")
    
    # Clear old images
    subprocess.run(["rm", "-rf", IMG_DIR], capture_output=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    
    generated_images = []
    for i, p in enumerate(prompts[:5]):
        print(f"   🎨 Generating image {i+1}/5...")
        img_path = os.path.join(IMG_DIR, f"flux_{i+1}.png")
        
        success, size_mb = generate_image(p, img_path)
        if success:
            print(f"   ✅ Image {i+1}: {size_mb:.1f} MB")
            generated_images.append(img_path)
        else:
            print(f"   ❌ Image {i+1} failed")
        
        time.sleep(1)  # Rate limit
    
    all_images = sorted([f for f in os.listdir(IMG_DIR) if f.endswith('.png')])
    print(f"   📊 Total images for video: {len(all_images)}")
    
    if len(all_images) < 3:
        print("❌ Not enough images generated")
        return
    
    # Step 3: Create TTS
    print("\n3️⃣ Creating voiceover...")
    tts_text = ""
    if 'TTS_SCRIPT:' in result:
        start = result.find('TTS_SCRIPT:') + 12
        end = result.find('Voice:', start)
        if end == -1:
            end = len(result)
        tts_text = result[start:end].strip()
    
    if not tts_text:
        print("❌ No TTS found in script")
        return
    
    tts_path = f"{VIDEO_DIR}/tts_flux_{ts}.mp3"
    
    # Clean text for TTS
    clean = re.sub(r'[📉📈💸🚀💰💼📘🤔🎬⚡✨💡🔥\]\[]', '', tts_text)
    clean = re.sub(r'\([^)]*\)', '', clean)
    clean = re.sub(r'\[.*?\]', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()[:4000]
    
    with open("/tmp/tts.txt", "w") as f:
        f.write(clean)
    
    try:
        subprocess.run([
            "/Users/superadmin/Library/Python/3.9/bin/edge-tts",
            "-f", "/tmp/tts.txt",
            "--write-media", tts_path,
            "-v", "en-GB-RyanNeural"
        ], timeout=120, check=True)
        print("   ✅ TTS created")
    except Exception as e:
        print(f"   ❌ TTS failed: {e}")
        return
    
    # Step 4: Create video clips
    print("\n4️⃣ Creating motion video...")
    work_dir = f"/tmp/vt_flux_{ts}"
    os.makedirs(work_dir, exist_ok=True)
    
    # Split TTS into segments
    phrases = tts_text.replace('...', '.').split('.')
    segments = []
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue
        words = len(phrase.split())
        # Clamp duration: max 10s, min 1s
        duration = max(1.0, min(10.0, words * 0.3))
        segments.append({'text': phrase[:25], 'duration': duration})
    
    print(f"   📊 {len(segments)} segments to create")
    
    # KEY FIX: Each segment gets a UNIQUE image (no immediate repeat)
    img_pool_size = len(all_images)
    prev_img_index = -1
    clips_created = 0
    
    for i, seg in enumerate(segments):
        # Pick a unique image, avoiding immediate repeat
        if img_pool_size > 1:
            available = [idx for idx in range(img_pool_size) if idx != prev_img_index]
            img_index = random.choice(available)
        else:
            img_index = 0
        prev_img_index = img_index
        img_path = os.path.join(IMG_DIR, all_images[img_index])
        clip_path = os.path.join(work_dir, f"clip_{i:04d}.mp4")
        
        if create_clip(img_path, seg['duration'], clip_path):
            clips_created += 1
        
        if (i + 1) % 20 == 0:
            print(f"   Progress: {i+1}/{len(segments)} clips")
    
    print(f"   ✅ Created {clips_created} clips")
    
    if clips_created < 3:
        print("❌ Not enough clips created")
        return
    
    # Step 5: Concatenate clips
    print("\n5️⃣ Concatenating clips...")
    clips = sorted([f for f in os.listdir(work_dir) if f.endswith('.mp4')])
    
    concat_file = f"{work_dir}/concat.txt"
    with open(concat_file, 'w') as f:
        for clip in clips:
            f.write(f"file '{work_dir}/{clip}'\n")
    
    video_only = f"{work_dir}/video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        video_only
    ], capture_output=True, timeout=180)
    
    # Step 6: Mix with audio
    print("\n6️⃣ Adding audio...")
    final_path = f"{VIDEO_DIR}/pro_flux_{ts}.mp4"
    
    subprocess.run([
        "ffmpeg", "-y", "-i", video_only, "-i", tts_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        final_path
    ], capture_output=True, timeout=60)
    
    # Cleanup
    subprocess.run(["rm", "-rf", work_dir], capture_output=True)
    
    # Save result
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
        "timestamp": datetime.now().strftime('%Y-%m-%d'),
        "images": "flux",
        "video_path": final_path
    })
    
    with open(video_log, "w") as f:
        json.dump(videos[:50], f, indent=2)
    
    # Output
    if os.path.exists(final_path):
        size = os.path.getsize(final_path) / 1024 / 1024
        print("\n" + "=" * 60)
        print("🎉 VIDEO READY - WITH FLUX IMAGES!")
        print("=" * 60)
        print(f"\n📹 Video: {final_path}")
        print(f"📊 Size: {size:.1f} MB")
        print(f"🖼️ Images: {len(generated_images)} AI-generated")
        print(f"📝 Clips: {clips_created}")
    else:
        print("❌ Video creation failed")

if __name__ == "__main__":
    import sys
    niche = sys.argv[1] if len(sys.argv) > 1 else "Future Tech"
    topic = sys.argv[2] if len(sys.argv) > 2 else "robotics ollama openclaw"
    main(niche=niche, topic=topic)
