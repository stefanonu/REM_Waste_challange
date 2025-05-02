import subprocess

def download_audio(accent: str, url: str, output_dir: str = "downloads"):
    output_template = f"{output_dir}/{accent}.%(ext)s"
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "wav",
        "-o", output_template,
        url
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Downloaded {accent} audio to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {accent} from {url}")
        print(e)

# Example usage
accent_urls = {
    "american": "https://www.youtube.com/watch?v=H1KP4ztKK0A",
    "british": "https://www.youtube.com/watch?v=FyyT2jmVPAk",
    "australian": "https://www.youtube.com/watch?v=66aG5P0kQpU",
    "indian": "https://www.youtube.com/watch?v=ryP8_MPFyUw"
}

for accent, url in accent_urls.items():
    download_audio(accent, url)

