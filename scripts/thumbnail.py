#!/usr/bin/env python3
"""ViralTube Thumbnail Generator using ImageMagick (No font required)"""
import subprocess
import os
import sys
from datetime import datetime

VIDEO_DIR = os.path.expanduser("~/Videos/viraltube")
os.makedirs(VIDEO_DIR, exist_ok=True)

def create_thumbnail(text, output_path=None, bg_color1="#0a0a0a", bg_color2="#1a1a2e"):
    """Create thumbnail with gradient background (text added via Canva later)"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/thumbnail-{timestamp}.png"
    
    # Create gradient background
    cmd = [
        "magick", "-size", "1280x720",
        f"gradient:{bg_color1}-{bg_color2}",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Save text to file for reference
        txt_file = output_path.replace('.png', '.txt')
        with open(txt_file, 'w') as f:
            f.write(text)
        print(f"✅ Thumbnail: {output_path}")
        print(f"📝 Text file: {txt_file}")
        return output_path
    else:
        print(f"❌ Error: {result.stderr}")
        return None

def create_thumbnail_with_border(text, output_path=None):
    """Create thumbnail with gold border accent"""
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_path = f"{VIDEO_DIR}/thumbnail-{timestamp}.png"
    
    # Create gradient with border
    cmd = [
        "magick", "-size", "1280x720",
        "gradient:#0a0a0a-#1a1a2e",
        "-bordercolor", "#FFD700",
        "-border", "10",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        txt_file = output_path.replace('.png', '.txt')
        with open(txt_file, 'w') as f:
            f.write(text)
        print(f"✅ Thumbnail: {output_path}")
        print(f"📝 Text file: {txt_file}")
        return output_path
    return None

def main():
    text = sys.argv[1] if len(sys.argv) > 1 else "Wealth Building 101"
    
    # Create thumbnail
    path = create_thumbnail_with_border(text)
    
    if not path:
        create_thumbnail(text)

if __name__ == "__main__":
    main()
