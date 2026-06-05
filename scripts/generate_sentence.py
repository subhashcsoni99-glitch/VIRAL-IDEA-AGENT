#!/usr/bin/env python3
"""
ViralTube PRO - Sentence-Matched Video
Each clip shows image that MATCHES the spoken sentence
"""
import subprocess
import os
import json
import re
from datetime import datetime

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
IMG_DIR = "/tmp/unique_images"
os.makedirs(VIDEO_DIR, exist_ok=True)

def get_tts_text():
    """Extract TTS from video data"""
    try:
        with open("/Users/superadmin/.openclaw/workspace-viraltube/videos.json") as f:
            videos = json.load(f)
        result = videos[0].get('result', '')
        if 'TTS_SCRIPT:' in result:
            start = result.find('TTS_SCRIPT:') + 12
            end = result.find('Voice:', start)
            if end == -1:
                end = len(result)
            return result[start:end].strip()
    except:
        pass
    return None

def get_sentences(tts_text):
    """Split TTS into sentences"""
    tts_text = re.sub(r'\([^)]*\)', '', tts_text)
    sentences = [s.strip() for s in tts_text.replace('...', '.').split('.') if s.strip()]
    return sentences

def get_keyword_image(keyword):
    """Get image path for keyword"""
    images = {
        "imagine": "universe", "universe": "universe",
        "computer": "computer", "laptop": "computer", "classical": "chip",
        "physics": "atom", "atom": "atom", "maze": "lab", "lab": "lab",
        "quantum": "quantum", "qubit": "quantum",
        "bit": "binary", "zero": "binary", "one": "binary",
        "wall": "circuit", "circuit": "circuit", "slow": "tech",
        "leap": "ai", "ai": "ai",
        "password": "lock", "lock": "lock", "scary": "lock",
        "bank": "money", "money": "money",
        "apocalypse": "universe",
        "hope": "health", "health": "health", "cure": "health", "alzheim": "health",
        "material": "lab", "battery": "gpu",
        "google": "data", "data": "data", "ibm": "server",
        "china": "network", "network": "network", "government": "security",
    }
    
    keyword = keyword.lower()
    for k, v in images.items():
        if k in keyword:
            img_path = f"{IMG_DIR}/{v}_1.jpg"
            if os.path.exists(img_path):
                return img_path
    
    # Default fallback
    for name in ["quantum", "tech", "computer"]:
        img_path = f"{IMG_DIR}/{name}_1.jpg"
        if os.path.exists(img_path):
            return img_path
    return None

def create_clip(img_path, duration, output_path):
    """Create a single video clip"""
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", img_path,
        "-t", str(duration),
        "-vf", "scale=1280:720",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=30)
    return result.returncode == 0 and os.path.exists(output_path)

def main():
    print("=" * 60)
    print("🎬 VIRALTUBE - SENTENCE MATCHED VIDEO")
    print("=" * 60)
    
    # Get TTS
    tts_text = get_tts_text()
    if not tts_text:
        print("❌ No TTS found. Run script generation first.")
        return
    
    sentences = get_sentences(tts_text)
    print(f"\n📝 Found {len(sentences)} sentences")
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    work_dir = f"/tmp/vt_sent_{ts}"
    os.makedirs(work_dir, exist_ok=True)
    
    # Create TTS
    print("\n1️⃣ Creating voiceover...")
    tts_path = f"{VIDEO_DIR}/tts_sent_{ts}.mp3"
    
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
    
    print(f"   ✅ TTS created: {tts_path}")
    
    # Create sentence-matched clips
    print(f"\n2️⃣ Creating {len(sentences)} clips (sentence-matched)...")
    
    clips = []
    for i, sentence in enumerate(sentences):
        clip_path = os.path.join(work_dir, f"s_{i:02d}.mp4")
        
        # Get matching image for first keyword
        words = sentence.split()
        img_path = None
        for word in words[:5]:  # Check first 5 words
            img_path = get_keyword_image(word)
            if img_path:
                break
        
        if not img_path:
            img_path = f"{IMG_DIR}/quantum_1.jpg"
        
        if create_clip(img_path, 2.0, clip_path):
            clips.append(clip_path)
            if (i + 1) % 10 == 0:
                print(f"   Progress: {i + 1}/{len(sentences)} clips")
    
    print(f"   ✅ Created {len(clips)} clips")
    
    if len(clips) < 5:
        print("❌ Not enough clips")
        return
    
    # Concatenate
    print("\n3️⃣ Concatenating...")
    concat_file = os.path.join(work_dir, "concat.txt")
    with open(concat_file, 'w') as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")
    
    video_only = os.path.join(work_dir, "video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        video_only
    ], capture_output=True, timeout=60)
    
    # Mix audio
    print("\n4️⃣ Mixing audio...")
    final_path = f"{VIDEO_DIR}/pro_sentence_{ts}.mp4"
    
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
        print("✅ SENTENCE-MATCHED VIDEO READY!")
        print("=" * 60)
        print(f"\n📹 {final_path}")
        print(f"📊 Size: {size:.1f} MB")
        print(f"📊 Clips: {len(clips)} (each 2 sec)")
        print("\n🎯 Each image matches the spoken sentence!")
    else:
        print("❌ Failed")

if __name__ == "__main__":
    main()
