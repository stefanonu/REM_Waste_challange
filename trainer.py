import os
import librosa
import numpy as np
import pickle
from glob import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

SEGMENT_DIR = "segments"
AUDIO_FILES = glob(os.path.join(SEGMENT_DIR, "*.wav"))

X, y = [], []

print(f"[INFO] Loading {len(AUDIO_FILES)} audio segments...")

for file_path in AUDIO_FILES:
    label = os.path.basename(file_path).split("_")[0]
    y_raw, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y_raw, sr=sr, n_mfcc=13)
    features = np.mean(mfcc.T, axis=0)
    X.append(features)
    y.append(label.capitalize())

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

print("\n[INFO] Classification Report:")
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save model + encoder
os.makedirs("models", exist_ok=True)
with open("models/accent_classifier.pkl", "wb") as f:
    pickle.dump(clf, f)
with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ Model and label encoder saved to 'models/'")
