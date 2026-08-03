from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import joblib
import threading
import win32com.client
import time

app = Flask(__name__)

# ===========================
# Load AI Model
# ===========================
model = joblib.load("models/gesture_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")

# ===========================
# Windows Speech
# ===========================


last_spoken = ""
gesture = "No Hand Detected"

last_prediction = ""
prediction_count = 0

speech_busy = False
last_spoken = ""

def speak(text):
    global speech_busy
    global last_spoken

    if text == "No Hand Detected":
        last_spoken = ""
        return

    if text == last_spoken:
        return

    if speech_busy:
        return

    last_spoken = text

    def run():
        global speech_busy

        speech_busy = True

        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)

        speech_busy = False

    threading.Thread(target=run, daemon=True).start()


# ===========================
# Webcam
# ===========================
camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# ===========================
# MediaPipe
# ===========================
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


# ===========================
# Camera Stream
# ===========================
def generate_frames():
    global gesture
    global last_prediction
    global prediction_count

    confidence = 0
    while True:

        success, frame = camera.read()

        if not success:
            print("Camera read failed")
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            landmarks = []

            for lm in hand.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            prediction = model.predict([landmarks])

            probabilities = model.predict_proba([landmarks])

            confidence = max(probabilities[0]) * 100

            current_prediction = encoder.inverse_transform(prediction)[0]


            if current_prediction == last_prediction:
                prediction_count += 1
            else:
                last_prediction = current_prediction
                prediction_count = 1

            if prediction_count >= 5 and gesture != current_prediction:
                
                
                gesture = current_prediction  
                speak(gesture)      
                gesture_history.append(gesture)

                if len(gesture_history) > 5:
                    gesture_history.pop(0)

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

        else:

            gesture = "No Hand Detected"
            last_prediction = ""
            prediction_count = 0
            gesture_history = []

        cv2.putText(
            frame,
            gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
                frame,
                f"Confidence: {confidence:.1f}%",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
        )
        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

# ===========================
# Flask Routes
# ===========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sign")
def sign():
    return render_template("sign.html")


@app.route("/speech")
def speech():
    return render_template("speech.html")


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/gesture")
def get_gesture():
    return gesture

@app.route("/history")
def history():
    return {
        "history": gesture_history
    }

# ===========================
# Run Application
# ===========================

if __name__ == "__main__":

    print("=" * 50)
    print("🤟 SignBridge AI Started")
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)

    app.run(
        debug=True,
        threaded=True
    )