def recognize_gesture(results):

    if not results.multi_hand_landmarks:
        return "No Hand"

    hand = results.multi_hand_landmarks[0]

    landmarks = hand.landmark

    # Fingertips
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Finger joints
    index_pip = landmarks[6]
    middle_pip = landmarks[10]
    ring_pip = landmarks[14]
    pinky_pip = landmarks[18]

    fingers_up = 0

    if index_tip.y < index_pip.y:
        fingers_up += 1

    if middle_tip.y < middle_pip.y:
        fingers_up += 1

    if ring_tip.y < ring_pip.y:
        fingers_up += 1

    if pinky_tip.y < pinky_pip.y:
        fingers_up += 1

    # ---------- Open Palm ----------
    # ---------- Open Palm ----------
    if fingers_up == 4:
       return "HELLO 👋"

   # ---------- Thumbs Up ----------
    thumb_up = thumb_tip.y < landmarks[3].y

    other_fingers_down = (
        index_tip.y > index_pip.y and
        middle_tip.y > middle_pip.y and
        ring_tip.y > ring_pip.y and
        pinky_tip.y > pinky_pip.y
   )

    if thumb_up and other_fingers_down:
       return "GOOD 👍"

     #---------- Fist ----------
    if fingers_up == 0:
      return "STOP ✋"

    return "Hand Detected"