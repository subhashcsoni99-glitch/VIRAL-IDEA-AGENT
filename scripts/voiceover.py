#!/usr/bin/env python3
"""ViralTube Voiceover - Convert TTS script to audio"""
import subprocess
import os
import sys
from datetime import datetime

def generate_voiceover(script, output_path=None, voice=None):
    """Convert TTS script to audio using Mac say command"""
    
    if not output_path:
        video_dir = os.path.expanduser("~/Videos/viraltube")
        os.makedirs(video_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{video_dir}/voiceover-{timestamp}.aiff"
    
    print(f"🎙️ Generating voiceover...")
    print(f"📁 Output: {output_path}")
    
    # Clean script for speech
    clean_script = script.replace('...', '... ')
    clean_script = clean_script.replace('📉', '')
    clean_script = clean_script.replace('📈', '')
    clean_script = clean_script.replace('💸', '')
    clean_script = clean_script.replace('🚀', '')
    clean_script = clean_script.replace('💰', '')
    clean_script = clean_script.replace('💼', '')
    clean_script = clean_script.replace('📘', '')
    clean_script = clean_script.replace('🤔', '')
    
    # Use specified voice or default Alex (good for narration)
    voice_flag = []
    if voice:
        voice_flag = ["-v", voice]
    
    # Generate audio
    cmd = ["say", "-o", output_path] + voice_flag + [clean_script]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Get duration
        duration_cmd = subprocess.run(
            ["afinfo", output_path],
            capture_output=True,
            text=True
        )
        for line in duration_cmd.stdout.split('\n'):
            if 'Duration' in line:
                print(f"⏱️ Duration: {line.split(':')[1].strip()}")
                break
        
        print(f"✅ Voiceover saved to: {output_path}")
        return output_path
    else:
        print(f"❌ Error: {result.stderr}")
        return None

def list_voices():
    """List available Mac voices"""
    result = subprocess.run(["say", "-v"], capture_output=True, text=True)
    print("Available voices:")
    print(result.stdout)

if __name__ == "__main__":
    # Get script from stdin or argument
    script = sys.argv[1] if len(sys.argv) > 1 else None
    
    if script == "--list":
        list_voices()
    elif script:
        voice = sys.argv[2] if len(sys.argv) > 2 else None
        generate_voiceover(script, voice=voice)
    else:
        print("Usage:")
        print("  python3 voiceover.py 'script text' [voice]")
        print("  python3 voiceover.py --list  # List available voices")
