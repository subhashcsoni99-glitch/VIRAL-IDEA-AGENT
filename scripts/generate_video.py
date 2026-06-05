#!/usr/bin/env python3
"""ViralTube Video Generator - WITH TOPIC-BASED IMAGES"""
import subprocess
import os
import sys
import json
from datetime import datetime

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
os.makedirs(VIDEO_DIR, exist_ok=True)

def download_image(url, output_path):
    """Download image from URL"""
    try:
        subprocess.run([
            "curl", "-s", "-L", "-o", output_path, url
        ], timeout=30)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except:
        return False

def get_images_for_topic(topic, niche="generic"):
    """Download stock images based on topic keywords"""
    images_dir = f"{VIDEO_DIR}/images"
    os.makedirs(images_dir, exist_ok=True)
    
    # Clear old images
    subprocess.run(["rm", "-f"] + [f"{images_dir}/img_{i}.jpg" for i in range(10)], shell=False)
    
    # Topic-based image URLs
    topic_lower = topic.lower()
    
    # Define image pools for different keywords
    image_pools = {
        "robotic": [
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1280",
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1280",
            "https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=1280",
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1280",
            "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=1280",
        ],
        "ollama": [
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1280",
            "https://images.unsplash.com/photo-1555949963-aa79dcee042c?w=1280",
            "https://images.unsplash.com/photo-1516110833967-0b5716ca1387?w=1280",
            "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1280",
            "https://images.unsplash.com/photo-1504639725590-34d0985008ef?w=1280",
        ],
        "ai": [
            "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1280",
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1280",
            "https://images.unsplash.com/photo-1555255707-c07966088b7b?w=1280",
            "https://images.unsplash.com/photo-1629875040248-aa393c0413e0?w=1280",
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1280",
        ],
        "quantum": [
            "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1280",
            "https://images.unsplash.com/photo-1635692206897-1eb7713a709f?w=1280",
            "https://images.unsplash.com/photo-1509228468518-1808ea13d5e2?w=1280",
        ],
        "finance": [
            "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1280",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1280",
            "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1280",
            "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1280",
        ],
        "wealth": [
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1280",
            "https://images.unsplash.com/photo-1560520653-9e0e4c49eb4c?w=1280",
            "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1280",
        ],
        "tech": [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1280",
            "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1280",
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1280",
        ],
    }
    
    # Generic fallback
    generic_images = [
        "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1280",
        "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1280",
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1280",
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1280",
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1280",
    ]
    
    # Find matching pools
    urls = []
    for keyword, pool in image_pools.items():
        if keyword in topic_lower:
            urls.extend(pool)
    
    # If no match, use generic
    if not urls:
        urls = generic_images
    else:
        # Dedupe and limit
        urls = list(dict.fromkeys(urls))[:5]
    
    downloaded = []
    for i, url in enumerate(urls):
        path = f"{images_dir}/img_{i}.jpg"
        if download_image(url, path):
            downloaded.append(path)
    
    return downloaded

def text_to_speech(script, output_path=None):
    """Convert text to speech"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/tts-{timestamp}.aiff"
    
    clean = script.replace('...', '... ')
    for emoji in ['📉', '📈', '💸', '🚀', '💰', '💼', '📘', '🤔']:
        clean = clean.replace(emoji, '')
    
    subprocess.run(["say", "-o", output_path, clean], capture_output=True)
    return output_path

def create_video_with_audio_and_images(audio_path, images, title, output_path=None):
    """Create final video"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/video-{timestamp}.mp4"
    
    if not images:
        return None
    
    # Get audio duration
    result = subprocess.run(
        ["afinfo", audio_path, "-json"],
        capture_output=True, text=True
    )
    try:
        audio_info = json.loads(result.stdout)
        duration = audio_info.get('format', {}).get('duration', 60)
    except:
        duration = 60
    
    # Create concat file
    concat_file = f"{VIDEO_DIR}/concat.txt"
    with open(concat_file, 'w') as f:
        for img in images:
            f.write(f"file '{img}'\n")
            f.write(f"duration {duration / len(images)}\n")
        f.write(f"file '{images[-1]}'\n")
    
    vf = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-i", audio_path,
        "-filter_complex", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-metadata", f"title={title}",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return output_path
    else:
        print(f"❌ Error: {result.stderr[:500]}")
        return None

def create_thumbnail(text, output_path=None):
    """Create thumbnail"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/thumbnail-{timestamp}.png"
    
    subprocess.run([
        "magick", "-size", "1280x720",
        "gradient:#0a0a0a-#1a1a2e",
        "-bordercolor", "#FFD700",
        "-border", "8",
        output_path
    ], capture_output=True)
    
    with open(output_path.replace('.png', '.txt'), 'w') as f:
        f.write(text)
    
    return output_path

def parse_result(result_text):
    """Parse generated result"""
    parts = {}
    
    if 'TITLE:' in result_text:
        start = result_text.find('TITLE:') + 7
        end = result_text.find('\n\n', start)
        parts['title'] = result_text[start:end].strip()
    
    if 'TTS_SCRIPT:' in result_text:
        start = result_text.find('TTS_SCRIPT:') + 12
        end = result_text.find('IMAGE_PROMPTS:', start) if 'IMAGE_PROMPTS:' in result_text else result_text.find('Voice:', start)
        parts['tts_script'] = result_text[start:end].strip()
    
    return parts

def generate_full_video(topic=None, niche=None):
    """Generate complete video with topic-based images"""
    print("=" * 60)
    print("🎬 VIRALTUBE VIDEO GENERATOR (TOPIC-BASED IMAGES)")
    print("=" * 60)
    
    # Load latest video
    video_log = "/Users/superadmin/.openclaw/workspace-viraltube/videos.json"
    try:
        with open(video_log) as f:
            videos = json.load(f)
        latest = videos[0]
        result_text = latest.get('result', '')
        topic = topic or latest.get('topic', 'video')
        niche = niche or latest.get('niche', 'Future Tech')
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    
    parts = parse_result(result_text)
    tts_script = parts.get('tts_script', '')
    title = parts.get('title', 'ViralTube Video')
    
    if not tts_script:
        print("❌ No TTS script found")
        return None
    
    print(f"\n📺 Topic: {topic}")
    print(f"📝 Title: {title}")
    
    # 1. Get relevant images
    print("\n1️⃣ Getting images for topic...")
    images = get_images_for_topic(topic, niche)
    
    for i, img in enumerate(images, 1):
        print(f"   {i}. {img}")
    
    # 2. TTS
    print("\n2️⃣ Converting to speech...")
    audio_path = text_to_speech(tts_script)
    print(f"   ✅ {audio_path}")
    
    # 3. Create video
    print("\n3️⃣ Creating video...")
    video_path = create_video_with_audio_and_images(audio_path, images, title)
    if video_path:
        print(f"   ✅ {video_path}")
    
    # 4. Thumbnail
    print("\n4️⃣ Creating thumbnail...")
    thumb_path = create_thumbnail(title)
    print(f"   ✅ {thumb_path}")
    
    print("\n" + "=" * 60)
    print("✅ VIDEO PACKAGE READY!")
    print("=" * 60)
    print(f"\n📹 Video: {video_path}")
    print(f"🎙️ Audio: {audio_path}")
    print(f"🖼️ Thumbnail: {thumb_path}")
    
    return {"video": video_path, "audio": audio_path, "thumbnail": thumb_path}

if __name__ == "__main__":
    niche = sys.argv[1] if len(sys.argv) > 1 else None
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    generate_full_video(topic=topic, niche=niche)
