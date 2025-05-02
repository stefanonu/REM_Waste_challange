import argparse
import os
import tempfile
import subprocess
from predictor import predict

def download_with_ytdlp(url):
    tmp_dir = tempfile.mkdtemp()
    output_template = os.path.join(tmp_dir, "video.%(ext)s")

    command = [
        "yt-dlp",
        "-f", "mp4/best",
        "-o", output_template,
        url
    ]
    print(f"[INFO] Downloading video from: {url}")
    subprocess.run(command, check=True)

    for file in os.listdir(tmp_dir):
        if file.endswith(".mp4") or file.endswith(".webm"):
            return os.path.join(tmp_dir, file)

    raise RuntimeError("Failed to download valid video")

def classify(input_path_or_url):
    if input_path_or_url.startswith("http"):
        video_path = download_with_ytdlp(input_path_or_url)
    else:
        if not os.path.exists(input_path_or_url):
            raise FileNotFoundError(f"File not found: {input_path_or_url}")
        video_path = input_path_or_url

    predict(video_path)

    if input_path_or_url.startswith("http"):
        os.remove(video_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Classify English accent from an audio/video file or Loom URL.",
        epilog="Example: python run.py ./audio.mp4 OR python run.py https://loom.com/share/xyz"
    )
    parser.add_argument("input", help="Path to local video/audio file OR Loom URL")

    args = parser.parse_args()

    classify(args.input)
