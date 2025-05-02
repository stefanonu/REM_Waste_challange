import os
import pytest
from predictor import predict
from run import download_with_ytdlp
# Resolve all paths relative to the root of the repo
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_ROOT = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "accent_classifier.pkl")
DATA_ROOT = "data"

def collect_test_files():
    test_cases = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attachment_path = os.path.join(current_dir, "data")

    for accent_dir in os.listdir(attachment_path):
        full_dir = os.path.join(attachment_path, accent_dir)
        if not os.path.isdir(full_dir):
            continue
        for file in os.listdir(full_dir):
            if file.endswith(".wav"):
                file_path = os.path.join(full_dir, file)
                expected = accent_dir.capitalize()
                test_cases.append((file_path, expected))
    return test_cases

@pytest.mark.parametrize("file_path, expected_label", collect_test_files())
def test_accent_prediction(file_path, expected_label):
    predicted_label, confidence = predict(file_path)
    assert predicted_label == expected_label, f"{file_path}: expected {expected_label}, got {predicted_label}"


@pytest.mark.parametrize("url, expected_label", [
    ("https://www.youtube.com/watch?v=H1KP4ztKK0A", "American"),
])
def test_accent_prediction_from_url(url, expected_label):
    video_path = download_with_ytdlp(url)
    assert os.path.exists(video_path), "Downloaded file missing."

    predicted_label, confidence = predict(video_path)

    os.remove(video_path)
    assert not os.path.exists(video_path), "Temp file was not deleted."

    assert predicted_label == expected_label, f"{url}: expected {expected_label}, got {predicted_label}"
