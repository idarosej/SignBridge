import cv2
import mediapipe as mp
import csv
import os

GESTURE = "stop"   # Change to hello, good, or stop

os.makedirs(f"dataset/{GESTURE}", exist_ok=True)

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

count = 0

while True:

    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Show count on screen
    cv2.putText(
        frame,
        f"Images: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press S to Save | Q to Quit",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )

    cv2.imshow("Collect Dataset", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        filename = f"dataset/{GESTURE}/{count}.jpg"
        cv2.imwrite(filename, frame)
        count += 1
        print(f"Saved image {count}")

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()