#!/bin/bash
# ViralTube - Shell Script (macOS compatible)

VIDEO_DIR="$HOME/Videos/viraltube"
IMG_DIR="/tmp/unique_images"
EDGE_TTS="/Users/superadmin/Library/Python/3.9/bin/edge-tts"
mkdir -p "$VIDEO_DIR"

echo "============================================================"
echo "🎬 VIRALTUBE - SHELL VERSION"
echo "============================================================"

# Get images
ALL_IMAGES=$(ls "$IMG_DIR"/*.jpg 2>/dev/null | sort)
IMAGE_COUNT=$(echo "$ALL_IMAGES" | grep -c "^" || echo 0)
echo ""
echo "📷 Images: $IMAGE_COUNT"

# Load video data
if [ ! -f "$HOME/.openclaw/workspace-viraltube/videos.json" ]; then
    echo "❌ No video data found"
    exit 1
fi

# Extract TTS from JSON
TTS_TEXT=$(python3 -c "
import json, re
with open('$HOME/.openclaw/workspace-viraltube/videos.json') as f:
    videos = json.load(f)
    result = videos[0].get('result', '')
    if 'TTS_SCRIPT:' in result:
        start = result.find('TTS_SCRIPT:') + 12
        end = result.find('Voice:', start)
        if end == -1:
            end = len(result)
        print(result[start:end].strip())
" 2>/dev/null)

if [ -z "$TTS_TEXT" ]; then
    echo "❌ No TTS found"
    exit 1
fi

TS=$(date +'%Y%m%d-%H%M%S')
WORK_DIR="/tmp/vt_$TS"
mkdir -p "$WORK_DIR"

# Create TTS
echo ""
echo "1️⃣ Creating voiceover..."

CLEAN_TTS=$(echo "$TTS_TEXT" | sed 's/[📉📈💸🚀💰💼📘🤔🎬⚡✨💡🔥\]\[]//g' | sed 's/\[[^]]*\]//g' | tr -s ' ')
echo "$CLEAN_TTS" > /tmp/tts.txt

"$EDGE_TTS" -f /tmp/tts.txt --write-media "$VIDEO_DIR/tts_$TS.mp3" -v en-GB-RyanNeural

if [ ! -f "$VIDEO_DIR/tts_$TS.mp3" ]; then
    echo "❌ TTS failed"
    exit 1
fi

echo "   ✅ TTS created"

TTS_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_DIR/tts_$TS.mp3" 2>/dev/null)
echo "   Duration: ${TTS_DUR}s"

# Create segments file
> /tmp/segments.txt
echo "$TTS_TEXT" | tr '.' '\n' | while read phrase; do
    phrase=$(echo "$phrase" | xargs)
    [ -z "$phrase" ] && continue
    words=$(echo "$phrase" | wc -w)
    duration=$(echo "scale=1; if($words * 0.25 > 3) 3 else if($words * 0.25 < 1) 1 else $words * 0.25" | bc)
    echo "$duration:$phrase" >> /tmp/segments.txt
done

SEGMENT_COUNT=$(wc -l < /tmp/segments.txt 2>/dev/null || echo 0)
echo ""
echo "2️⃣ Creating $SEGMENT_COUNT clips..."

# Create clips
CLIP_NUM=0
CLIPS_CREATED=0

while IFS=: read -r duration phrase; do
    [ -z "$duration" ] && continue
    
    IMG_INDEX=$((CLIP_NUM % IMAGE_COUNT))
    IMG=$(echo "$ALL_IMAGES" | sed -n "$((IMG_INDEX + 1))p")
    CLIP="$WORK_DIR/clip_$(printf '%04d' $CLIP_NUM).mp4"
    
    fade_out=$(echo "$duration - 0.2" | bc)
    
    ffmpeg -y -loop 1 -i "$IMG" -t "$duration" \
        -vf "scale=1280:720,fade=t=in:st=0:d=0.2,fade=t=out:st=${fade_out}:d=0.2" \
        -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p -r 25 \
        "$CLIP" 2>/dev/null
    
    [ -f "$CLIP" ] && CLIPS_CREATED=$((CLIPS_CREATED + 1))
    
    [ $((CLIP_NUM % 20)) -eq 0 ] && [ $CLIP_NUM -gt 0 ] && \
        echo "   Progress: $CLIP_NUM/$SEGMENT_COUNT - $CLIPS_CREATED clips"
    
    CLIP_NUM=$((CLIP_NUM + 1))
done < /tmp/segments.txt

echo "   ✅ Created $CLIPS_CREATED clips"

[ "$CLIPS_CREATED" -lt 5 ] && echo "❌ Not enough clips" && exit 1

# Concatenate
echo ""
echo "3️⃣ Concatenating..."

ls "$WORK_DIR"/clip_*.mp4 | sort > "$WORK_DIR/concat.txt"
sed -i '' "s|^|file '$WORK_DIR/|g" "$WORK_DIR/concat.txt"

ffmpeg -y -f concat -safe 0 -i "$WORK_DIR/concat.txt" \
    -c:v libx264 -preset fast -crf 20 \
    "$WORK_DIR/video.mp4" 2>/dev/null

# Mix audio
echo ""
echo "4️⃣ Mixing audio..."

FINAL="$VIDEO_DIR/pro_unique_$TS.mp4"

ffmpeg -y -i "$WORK_DIR/video.mp4" -i "$VIDEO_DIR/tts_$TS.mp3" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$FINAL" 2>/dev/null

# Cleanup
rm -rf "$WORK_DIR" /tmp/segments.txt

if [ -f "$FINAL" ]; then
    SIZE=$(ls -lh "$FINAL" | awk '{print $5}')
    echo ""
    echo "============================================================"
    echo "✅ VIDEO READY!"
    echo "============================================================"
    echo ""
    echo "📹 $FINAL"
    echo "📊 Size: $SIZE"
    echo "📊 Clips: $CLIPS_CREATED"
    echo "📊 Unique images: $IMAGE_COUNT"
else
    echo "❌ Failed"
fi
