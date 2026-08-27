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
    global confidence

    global gesture_history
    global gesture_counts
    global total_gestures
    global highest_confidence
    global session_start

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
                landmarks.extend([
                    lm.x,
                    lm.y,
                    lm.z
                ])

            # AI Prediction
            prediction = model.predict([landmarks])

            # Prediction Confidence
            probabilities = model.predict_proba([landmarks])

            confidence = max(probabilities[0]) * 100

            # Track highest confidence
            if confidence > highest_confidence:
                highest_confidence = confidence

            current_prediction = encoder.inverse_transform(
                prediction
            )[0]

            # ---------------------------
            # Stable Prediction
            # ---------------------------

            if current_prediction == last_prediction:

                prediction_count += 1

            else:

                last_prediction = current_prediction
                prediction_count = 1

            # ---------------------------
            # Confirm Gesture
            # ---------------------------

            if prediction_count >= 5 and gesture != current_prediction:

                gesture = current_prediction

                speak(gesture)

                # Add to history
                gesture_history.append(gesture)

                if len(gesture_history) > 5:
                    gesture_history.pop(0)

                # Update statistics
                gesture_counts[gesture] = (
                    gesture_counts.get(gesture, 0) + 1
                )

                total_gestures += 1

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

        else:

            # No hand detected
            gesture = "No Hand Detected"

            last_prediction = ""
            prediction_count = 0
            confidence = 0

            # IMPORTANT:
            # Do NOT reset statistics here.
            # Do NOT reset gesture history here.

        # ---------------------------
        # Display Gesture
        # ---------------------------

        cv2.putText(
            frame,
            gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # ---------------------------
        # Display Confidence
        # ---------------------------

        cv2.putText(
            frame,
            f"Confidence: {confidence:.1f}%",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        # ---------------------------
        # Encode Frame
        # ---------------------------

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

gesture = "No Hand Detected"

confidence = 0

gesture_history = []

gesture_counts = {}

total_gestures = 0

highest_confidence = 0

session_start = time.time()

last_prediction = ""

prediction_count = 0
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

@app.route("/stats")
def get_stats():

    most_detected = "None"

    if gesture_counts:
        most_detected = max(
            gesture_counts,
            key=gesture_counts.get
        )

    # Calculate session duration
    session_duration = int(time.time() - session_start)

    return {
        "total": total_gestures,
        "most_detected": most_detected,
        "highest_confidence": round(highest_confidence, 1),
        "different_gestures": len(gesture_counts),
        "session_duration": session_duration
    }
@app.route("/reset-session", methods=["POST"])
def reset_session():

    global gesture
    global confidence
    global gesture_history
    global gesture_counts
    global total_gestures
    global highest_confidence
    global last_prediction
    global prediction_count
    global session_start

    gesture = "No Hand Detected"
    confidence = 0

    gesture_history.clear()
    gesture_counts.clear()

    total_gestures = 0
    highest_confidence = 0

    last_prediction = ""
    prediction_count = 0

    session_start = time.time()

    return {
        "success": True,
        "message": "Session reset successfully"
    }
@app.route("/history")
def history():
    return {
        "history": gesture_history
    }

@app.route("/message")
def get_message():

    if gesture_history:
        message = " ".join(gesture_history)
    else:
        message = "No message yet"

    return {
        "message": message
    }

@app.route("/speak-message", methods=["POST"])
def speak_message():

    if not gesture_history:
        return {
            "success": False,
            "message": "No message to speak"
        }

    message = " ".join(gesture_history)

    threading.Thread(
        target=speak,
        args=(message,),
        daemon=True
    ).start()

    return {
        "success": True,
        "message": message
    }

@app.route("/clear-message", methods=["POST"])
def clear_message():

    global gesture_history

    gesture_history.clear()

    return {
        "success": True,
        "message": "Message cleared"
    }
@app.route("/confidence")
def get_confidence():
    return {
        "confidence": round(confidence,1)
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