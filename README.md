## Setup

1. **Clone the repo and create a virtual environment**:
    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Install ffmpeg and yt-dlp** (required for audio handling):
    ```bash
    brew install ffmpeg yt-dlp  # on macOS
    ```
     ```bash
    sudo apt install ffmpeg yt-dlp # on Linux
    ```
      ```bash
    choco install ffmpeg # on Windows
    ```

## How to Use

### 1. Classify a local file (WAV or MP4):
```bash
python run.py path/to/file.wav
```

### 2. Classify a public video URL YouTube:
```bash
python run.py "https://www.youtube.com/watch?v=l8hpEvMW0oA"
```

## How it was implemented

1. I downloaded 4 long audio samples (1 per accent: American, British, Indian, Australian).
2. I split each into 10-second `.wav` chunks using `split_dataset.py`, creating a clean dataset.
3. `trainer.py` extracts MFCC features and trains a `RandomForestClassifier` on the segments.
4. `predictor.py` handles model inference, including `.mp4` audio extraction.
5. `run.py` serves as the CLI interface supporting both local paths and YouTube URLs.

## Running Tests
```bash
pytest
```

Tests cover:
- Local `.wav` and `.mp4` file predictions
- YouTube video URL predictions
- File cleanup and model confidence thresholds


> Dataset not included due to size.  
> But you can regenerate it by:
> 1. Running `dataset.py` to download 4 source videos
> 2. Running `split_dataset.py` to create segments
> 3. Running `trainer.py` to retrain the model
