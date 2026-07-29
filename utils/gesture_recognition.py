def recognize_gesture(results):
    """
    Very simple gesture recognition.
    """

    if not results.multi_hand_landmarks:
        return ""

    hand = results.multi_hand_landmarks[0]

    fingertips = [8, 12, 16, 20]

    fingers_up = 0

    for tip in fingertips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers_up += 1

    # Thumb
    if hand.landmark[4].x > hand.landmark[3].x:
        fingers_up += 1

    if fingers_up == 5:
        return "HELLO 👋"

    return "Hand Detected"