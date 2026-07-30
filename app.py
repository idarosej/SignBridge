from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
from utils.gesture_recognition import recognize_gesture

app = Flask(__name__)

# Global gesture text
gesture = "No Hand Detected"

# Open webcam
camera = cv2.VideoCapture(0)

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


def generate_frames():
    global gesture

    while True:
        success, frame = camera.read()

        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Recognize gesture
        gesture = recognize_gesture(results)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        else:
            gesture = "No Hand Detected"

        cv2.putText(
            frame,
            gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )


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


if __name__ == "__main__":
    app.run(debug=True)