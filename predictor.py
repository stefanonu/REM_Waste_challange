import sys
import os
import librosa
import numpy as np
import pickle
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
    return audio_path

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0).reshape(1, -1)

def load_model_and_encoder():
    with open("models/accent_classifier.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/label_encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
    return model, encoder

def predict(accent_file):
    ext = os.path.splitext(accent_file)[1].lower()
    if ext == ".mp4":
        print(f"[INFO] Extracting audio from {accent_file}")
        audio_path = extract_audio(accent_file)
    else:
        audio_path = accent_file

    features = extract_features(audio_path)
    model, encoder = load_model_and_encoder()

    probs = model.predict_proba(features)[0]
    pred_idx = np.argmax(probs)
    accent = encoder.inverse_transform([pred_idx])[0]
    confidence = probs[pred_idx] * 100

    print(f"\nPredicted Accent: {accent}")
    print(f"Confidence: {confidence:.2f}%")
    return accent, confidence 
