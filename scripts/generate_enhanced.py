#!/usr/bin/env python3
"""ViralTube Enhanced - Professional Video Generator"""
import subprocess
import os
import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
import random

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
os.makedirs(VIDEO_DIR, exist_ok=True)

TTS_PATH = "/Users/superadmin/Library/Python/3.9/bin/edge-tts"

# Free background music (royalty-free)
MUSIC_URLS = [
    "https://cdn.pixabay.com/audio/2022/03/15/audio_8cb749d484.mp3",  # Cinematic
    "https://cdn.pixabay.com/audio/2022/01/18/audio_d0c6ff2a9e.mp3",  # Ambient
    "https://cdn.pixabay.com/audio/2021/11/25/audio_d633989fbd.mp3",  # Uplifting
]

def download_file(url, path):
    """Download file"""
    try:
        subprocess.run(["curl", "-s", "-L", "-o", path, url], timeout=60, check=True)
        return os.path.exists(path) and os.path.getsize(path) > 1000
    except:
        return False

def get_topic_images(topic):
    """Get relevant stock images for topic"""
    images_dir = f"{VIDEO_DIR}/images"
    os.makedirs(images_dir, exist_ok=True)

    # Clear old
    for f in os.listdir(images_dir):
        os.remove(f"{images_dir}/{f}")

    # Image URLs by keyword
    topic_images = {
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
        ],
        "open claw": [
            "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1280",
            "https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=1280",
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1280",
        ],
    }

    topic_lower = topic.lower()
    urls = []
    for keyword, pool in topic_images.items():
        if keyword in topic_lower:
            urls.extend(pool)

    if not urls:
        urls = topic_images["ai"]

    urls = list(dict.fromkeys(urls))[:5]

    downloaded = []
    for i, url in enumerate(urls):
        path = f"{images_dir}/img_{i}.jpg"
        if download_file(url, path):
            downloaded.append(path)

    return downloaded

def text_to_speech_edge(text, output_path, voice="en-GB-RyanNeural"):
    """Convert text to speech using Edge TTS"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/tts-{timestamp}.mp3"

    # Clean text
    clean = text.replace('...', '... ')
    clean = re.sub(r'[📉📈💸🚀💰💼📘🤔🎬⚡✨💡🔥]', '', clean)
    clean = re.sub(r'\([^)]*\)', '', clean)  # Remove parentheticals
    clean = re.sub(r'\[.*?\]', '', clean)  # Remove brackets
    clean = re.sub(r'\s+', ' ', clean).strip()

    # Write to temp file
    with open("/tmp/tts_text.txt", "w") as f:
        f.write(clean)

    try:
        subprocess.run([
            TTS_PATH,
            "-f", "/tmp/tts_text.txt",
            "--write-media", output_path,
            "-v", voice
        ], timeout=120, check=True)
        return output_path
    except Exception as e:
        print(f"Edge TTS failed: {e}, trying say...")
        subprocess.run(["say", "-o", output_path.replace('.mp3', '.aiff'), clean])
        return output_path.replace('.mp3', '.aiff')

def get_audio_duration(path):
    """Get audio duration"""
    try:
        result = subprocess.run(
            ["afinfo", path, "-json"],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        return data.get('format', {}).get('duration', 60)
    except:
        return 60

def download_music():
    """Download background music"""
    music_path = f"{VIDEO_DIR}/music.mp3"
    for url in MUSIC_URLS:
        if download_file(url, music_path):
            return music_path
    return None

def create_motion_video(audio_path, images, title, output_path=None):
    """Create video with motion effects, Ken Burns, and music"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/video-{timestamp}.mp4"

    if not images:
        return None

    duration = get_audio_duration(audio_path)
    num_images = len(images)
    duration_per = duration / num_images

    # Create motion image sequence with Ken Burns
    motion_dir = f"{VIDEO_DIR}/motion"
    os.makedirs(motion_dir, exist_ok=True)

    print(f"   Creating motion effects ({num_images} images, {duration_per:.1f}s each)...")

    for i, img in enumerate(images):
        # Create Ken Burns effect: slow zoom + pan
        effects = [
            # Slow zoom in
            f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoom=5:mode=bicubic",
            # Slow zoom out
            f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoom=5:mode=bicubic",
            # Pan left
            f"scale=1920:1080,crop=1280:720:0:180",
            # Pan right
            f"scale=1920:1080,crop=1280:720:640:180",
            # Zoom in center
            f"scale=1600:900,crop=1280:720:160:90",
        ]

        effect = effects[i % len(effects)]
        motion_path = f"{motion_dir}/motion_{i}.mp4"

        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", img,
            "-t", str(duration_per),
            "-vf", effect,
            "-c:v", "libx264", "-preset", "fast", "-tune", "stillimage",
            "-pix_fmt", "yuv420p",
            motion_path
        ]
        subprocess.run(cmd, capture_output=True)

    # Get motion files
    motion_files = sorted([f"{motion_dir}/{f}" for f in os.listdir(motion_dir) if f.endswith('.mp4')])

    if not motion_files:
        print("   ❌ Motion generation failed")
        return None

    # Create concat file
    concat_file = f"{VIDEO_DIR}/concat.txt"
    with open(concat_file, 'w') as f:
        for mf in motion_files:
            f.write(f"file '{mf}'\n")

    # Download music
    print("   🎵 Adding background music...")
    music_path = download_music()

    # Build filter for video with music
    if music_path:
        # Mix audio: reduce music volume, place under voiceover
        filter_complex = (
            "[0:a][1:a]amix=inputs=2:duration=first:weights=0.3 1[aout]"
        )
        audio_input = f"-i {music_path}"
        audio_filter = "-filter_complex [0:a][1:a]amix=inputs=2:duration=first:weights=0.3 1[aout] -map 0:v -map [aout]"
    else:
        audio_input = ""
        audio_filter = "-c:a copy"

    # Final video: concat images + add audio
    temp_video = f"{VIDEO_DIR}/temp_video.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", audio_path,
    ] + (["-i", music_path] if music_path else []) + [
        "-filter_complex",
        "[0:v]scale=1280:720:force_original_aspect_ratio=decrease," 
        "pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,fps=30[v]",
        "-map", "[v]" + ("[aout]" if music_path else ""),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        temp_video
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"   ❌ Video error: {result.stderr[-300:]}")
        # Fallback
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_file,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-shortest",
            output_path
        ]
        subprocess.run(cmd, capture_output=True)
    else:
        subprocess.run(["mv", temp_video, output_path])

    return output_path if os.path.exists(output_path) else None

def create_thumbnail(title):
    """Create animated thumbnail with text"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output = f"{VIDEO_DIR}/thumbnail-{timestamp}.png"

    # Create gradient background
    subprocess.run([
        "magick", "-size", "1280x720",
        "gradient:#1a1a2e-#16213e",
        "-font", "Helvetica-Bold",
        "-pointsize", "72",
        "-fill", "white",
        "-gravity", "center",
        f"-annotate", "+0+0", title[:60],
        "-bordercolor", "#FFD700", "-border", "10",
        output
    ], capture_output=True)

    return output

def create_animated_intro(images, duration=5):
    """Create animated intro with text overlay"""
    if not images:
        return None

    intro_path = f"{VIDEO_DIR}/intro.mp4"
    img = images[0]

    # Create slow zoom intro
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", img,
        "-t", str(duration),
        "-vf", "scale=1920:1080,zoompan=z='min(zoom+0.001,1.5)':d=125:s=1280x720",
        "-c:v", "libx264", "-preset", "fast", "-tune", "stillimage",
        "-pix_fmt", "yuv420p",
        intro_path
    ]
    subprocess.run(cmd, capture_output=True)

    return intro_path if os.path.exists(intro_path) else None

def parse_script(result_text):
    """Parse TTS script from result"""
    if 'TTS_SCRIPT:' in result_text:
        start = result_text.find('TTS_SCRIPT:') + 12
        end = result_text.find('IMAGE_PROMPTS:', start)
        if end == -1:
            end = result_text.find('Voice:', start)
        return result_text[start:end].strip()
    return None

def generate_enhanced_video(topic=None, niche=None):
    """Generate professional video"""
    print("=" * 60)
    print("🎬 VIRALTUBE ENHANCED (Motion + Music + Edge TTS)")
    print("=" * 60)

    # Load latest
    video_log = "/Users/superadmin/.openclaw/workspace-viraltube/videos.json"
    try:
        with open(video_log) as f:
            videos = json.load(f)
        latest = videos[0]
        result_text = latest.get('result', '')
        topic = topic or latest.get('topic', 'video')
        niche = niche or latest.get('niche', 'Future Tech')
    except:
        print("❌ No video data found. Run generate.py first!")
        return None

    title = "Local AI Robots: Ollama + Open Claw Guide! 🤖"
    if 'TITLE:' in result_text:
        start = result_text.find('TITLE:') + 7
        end = result_text.find('\n', start)
        title = result_text[start:end].strip()

    tts_script = parse_script(result_text)
    if not tts_script:
        print("❌ No TTS script found")
        return None

    print(f"\n📺 Topic: {topic}")
    print(f"📝 Title: {title}")

    # 1. Images
    print("\n1️⃣ Downloading topic images...")
    images = get_topic_images(topic)
    for i, img in enumerate(images, 1):
        print(f"   {i}. {os.path.basename(img)}")

    # 2. Voice (Edge TTS)
    print("\n2️⃣ Creating voiceover (Edge TTS - Microsoft Neural)...")
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    audio_path = f"{VIDEO_DIR}/tts-{timestamp}.mp3"
    audio_path = text_to_speech_edge(tts_script, audio_path)
    print(f"   ✅ {audio_path}")

    # 3. Motion video with music
    print("\n3️⃣ Creating motion video with background music...")
    video_path = create_motion_video(audio_path, images, title)
    if video_path:
        print(f"   ✅ {video_path}")

    # 4. Thumbnail
    print("\n4️⃣ Creating thumbnail...")
    thumb_path = create_thumbnail(title)
    print(f"   ✅ {thumb_path}")

    print("\n" + "=" * 60)
    print("✅ ENHANCED VIDEO PACKAGE READY!")
    print("=" * 60)
    print(f"\n📹 Video: {video_path}")
    print(f"🎙️ Audio: {audio_path}")
    print(f"🖼️ Thumbnail: {thumb_path}")

    return {"video": video_path, "audio": audio_path, "thumbnail": thumb_path}

if __name__ == "__main__":
    niche = sys.argv[1] if len(sys.argv) > 1 else None
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    generate_enhanced_video(topic=topic, niche=niche)
