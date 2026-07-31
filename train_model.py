import os
import cv2
import joblib
import numpy as np
import mediapipe as mp

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

X = []
y = []

dataset_path = "dataset"

print("Dataset path:", dataset_path)
print("Folders:", os.listdir(dataset_path))

for label in os.listdir(dataset_path):
    print("Reading:", label)

    folder = os.path.join(dataset_path, label)

    if not os.path.isdir(folder):
        continue

    for image_name in os.listdir(folder):

        image_path = os.path.join(folder, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            landmarks = []

            hand = results.multi_hand_landmarks[0]

            for lm in hand.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            X.append(landmarks)
            y.append(label)
print("Total samples:", len(X))
print("Labels:", len(y))

encoder = LabelEncoder()

y = encoder.fit_transform(y)

model = RandomForestClassifier(n_estimators=100)

model.fit(X, y)

joblib.dump(model, "models/gesture_model.pkl")
joblib.dump(encoder, "models/label_encoder.pkl")

print("✅ Model trained successfully!")