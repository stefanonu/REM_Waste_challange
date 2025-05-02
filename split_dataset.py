from pydub import AudioSegment
import os

ACCENTS = ["american", "british", "australian", "indian"]
INPUT_DIR = "downloads"
OUTPUT_DIR = "segments"
SEGMENT_LENGTH_MS = 10 * 1000  # 10 seconds

os.makedirs(OUTPUT_DIR, exist_ok=True)

for accent in ACCENTS:
    input_path = os.path.join(INPUT_DIR, f"{accent}.wav")
    if not os.path.exists(input_path):
        print(f"Skipping missing file: {input_path}")
        continue

    audio = AudioSegment.from_wav(input_path)
    duration_ms = len(audio)
    num_segments = duration_ms // SEGMENT_LENGTH_MS

    print(f"Splitting {accent}.wav into {num_segments} segments...")

    for i in range(num_segments):
        start = i * SEGMENT_LENGTH_MS
        end = start + SEGMENT_LENGTH_MS
        segment = audio[start:end]
        out_path = os.path.join(OUTPUT_DIR, f"{accent}_{i}.wav")
        segment.export(out_path, format="wav")
