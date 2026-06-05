#!/usr/bin/env python3
"""
ViralTube - Fixed String Formatting
"""
import subprocess
import os
import json
import re
from datetime import datetime

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
os.makedirs(VIDEO_DIR, exist_ok=True)

IMG_DIR = "/tmp/unique_images"

def create_clip(img_path, duration, clip_path):
    """Create a single clip with proper bash escaping"""
    fade_out = duration - 0.2
    vf = f"scale=1280:720,fade=t=in:st=0:d=0.2,fade=t=out:st={fade_out}:d=0.2"
    
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

def main():
    print("=" * 60)
    print("🎬 VIRALTUBE - FIXED")
    print("=" * 60)
    
    # Get images
    all_images = sorted([f for f in os.listdir(IMG_DIR) if f.endswith('.jpg')])
    print(f"\n📷 Images: {len(all_images)}")
    
    # Load data
    try:
        with open("/Users/superadmin/.openclaw/workspace-viraltube/videos.json") as f:
            videos = json.load(f)
        latest = videos[0]
        result = latest.get('result', '')
    except:
        print("❌ Failed to load video data")
        return
    
    # Extract TTS
    tts_text = ""
    if 'TTS_SCRIPT:' in result:
        start = result.find('TTS_SCRIPT:') + 12
        end = result.find('Voice:', start)
        if end == -1:
            end = len(result)
        tts_text = result[start:end].strip()
    
    if not tts_text:
        print("❌ No TTS found")
        return
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    work_dir = f"/tmp/vt_{ts}"
    os.makedirs(work_dir, exist_ok=True)
    
    # Create TTS
    print("\n1️⃣ Creating voiceover...")
    tts_path = f"{VIDEO_DIR}/tts_{ts}.mp3"
    
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
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return
    
    print(f"   ✅ TTS created")
    
    # Create segments
    phrases = tts_text.replace('...', '.').split('.')
    segments = []
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue
        words = len(phrase.split())
        duration = max(1.0, min(words * 0.25, 3.0))
        segments.append({'text': phrase[:20], 'duration': duration})
    
    print(f"\n2️⃣ Creating {len(segments)} clips...")
    
    # Create clips
    clips_created = 0
    for i, seg in enumerate(segments):
        img_index = i % len(all_images)
        img_path = os.path.join(IMG_DIR, all_images[img_index])
        clip_path = os.path.join(work_dir, f"clip_{i:04d}.mp4")
        
        if create_clip(img_path, seg['duration'], clip_path):
            clips_created += 1
        
        if (i + 1) % 20 == 0:
            print(f"   Progress: {i + 1}/{len(segments)} - {clips_created} clips")
    
    print(f"   ✅ Created {clips_created} clips")
    
    if clips_created < 5:
        print("❌ Not enough clips")
        return
    
    # Get all clips
    clips = sorted([f for f in os.listdir(work_dir) if f.endswith('.mp4')])
    
    # Concatenate
    print("\n3️⃣ Concatenating...")
    concat_file = f"{work_dir}/concat.txt"
    with open(concat_file, 'w') as f:
        for clip in clips:
            f.write(f"file '{work_dir}/{clip}'\n")
    
    video_only = f"{work_dir}/video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        video_only
    ], capture_output=True, timeout=120)
    
    # Mix audio
    print("\n4️⃣ Mixing audio...")
    final_path = f"{VIDEO_DIR}/pro_unique_{ts}.mp4"
    
    subprocess.run([
        "ffmpeg", "-y", "-i", video_only, "-i", tts_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        final_path
    ], capture_output=True, timeout=60)
    
    # Cleanup
    subprocess.run(["rm", "-rf", work_dir], capture_output=True)
    
    if os.path.exists(final_path):
        size = os.path.getsize(final_path) / 1024 / 1024
        print("\n" + "=" * 60)
        print("✅ VIDEO READY!")
        print("=" * 60)
        print(f"\n📹 {final_path}")
        print(f"📊 Size: {size:.1f} MB")
        print(f"📊 Clips: {clips_created}")
        print(f"📊 Unique images: {len(all_images)}")
    else:
        print("❌ Failed")

if __name__ == "__main__":
    main()
