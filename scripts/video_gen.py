#!/usr/bin/env python3
"""ViralTube Full Video Generator - TTS + Video from text"""
import subprocess
import os
import sys
import json
from datetime import datetime

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
os.makedirs(VIDEO_DIR, exist_ok=True)

def text_to_speech(script, output_path=None):
    """Convert text to speech using macOS say command"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/tts-{timestamp}.aiff"
    
    # Clean script
    clean = script.replace('...', '... ')
    for emoji in ['📉', '📈', '💸', '🚀', '💰', '💼', '📘', '🤔', '✨', '🔥', '⭐']:
        clean = clean.replace(emoji, '')
    
    # Generate audio
    subprocess.run(["say", "-o", output_path, clean], capture_output=True)
    print(f"🎙️ TTS: {output_path}")
    return output_path

def create_video_from_audio(audio_path, title, output_path=None, bg_color="black"):
    """Create video with title text using ffmpeg (slideshow style)"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/video-{timestamp}.mp4"
    
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
    
    # Create video from audio duration
    # Use ffmpeg to create video with title frame
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c={bg_color}:s=1280x720:d={duration}",
        "-i", audio_path,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-metadata", f"title={title}",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"🎬 Video: {output_path}")
        return output_path
    else:
        print(f"❌ Error: {result.stderr[:500]}")
        return None

def create_thumbnail(text, output_path=None):
    """Create thumbnail image"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/thumbnail-{timestamp}.png"
    
    # Create thumbnail with ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=1280x720",
        "-vf", f"drawtext=text='{text}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-frames:v", "1",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"🖼️ Thumbnail: {output_path}")
        return output_path
    else:
        print(f"❌ Error: {result.stderr[:500]}")
        return None

def generate_full_video(tts_script, title, thumbnail_text):
    """Generate complete video package"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    print("=" * 50)
    print("🎬 VIRALTUBE VIDEO GENERATOR")
    print("=" * 50)
    
    # 1. TTS Audio
    print("\n1️⃣ Converting text to speech...")
    audio_path = text_to_speech(tts_script)
    
    # 2. Video
    print("\n2️⃣ Creating video...")
    video_path = create_video_from_audio(audio_path, title)
    
    # 3. Thumbnail
    print("\n3️⃣ Creating thumbnail...")
    thumb_path = create_thumbnail(thumbnail_text)
    
    print("\n" + "=" * 50)
    print("✅ VIDEO PACKAGE READY!")
    print("=" * 50)
    print(f"\n📹 Video: {video_path}")
    print(f"🎙️ Audio: {audio_path}")
    print(f"🖼️ Thumbnail: {thumb_path}")
    
    return {
        "video": video_path,
        "audio": audio_path,
        "thumbnail": thumb_path,
        "title": title
    }

def main():
    tts_script = sys.argv[1] if len(sys.argv) > 1 else None
    title = sys.argv[2] if len(sys.argv) > 2 else "ViralTube Video"
    thumbnail = sys.argv[3] if len(sys.argv) > 3 else "Wealth Building 101"
    
    if not tts_script:
        print("Usage: python3 video_gen.py 'tts_script' 'title' 'thumbnail_text'")
        print("\nOr generate from videos.json:")
        video_log = "/Users/superadmin/.openclaw/workspace-viraltube/videos.json"
        if os.path.exists(video_log):
            with open(video_log) as f:
                videos = json.load(f)
            if videos:
                latest = videos[0]
                result = latest.get('result', '')
                # Parse result for TTS script
                if 'TTS_SCRIPT:' in result:
                    tts_start = result.find('TTS_SCRIPT:') + 12
                    tts_end = result.find('Voice:', tts_start) if 'Voice:' in result else tts_start + 500
                    tts_script = result[tts_start:tts_end].strip()
                    
                    title_start = result.find('TITLE:') + 7
                    title_end = result.find('\n\n', title_start)
                    title = result[title_start:title_end].strip()
                    
                    generate_full_video(tts_script, title, title)
                    return
    
    if tts_script:
        generate_full_video(tts_script, title, thumbnail)
    else:
        print("No TTS script provided")

if __name__ == "__main__":
    main()
