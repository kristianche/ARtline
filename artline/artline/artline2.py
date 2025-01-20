import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

CANVAS_SIZE = (480, 640)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

canvas = np.ones((CANVAS_SIZE[0], CANVAS_SIZE[1], 3), dtype=np.uint8) * 255
tracking = False
previous_point = None

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                thumb_x, thumb_y = int(thumb_tip.x * CANVAS_SIZE[1]), int(thumb_tip.y * CANVAS_SIZE[0])
                index_x, index_y = int(index_tip.x * CANVAS_SIZE[1]), int(index_tip.y * CANVAS_SIZE[0])

                if not tracking and thumb_y - index_y > 40:
                    tracking = True
                    print("Tracking started!")

                if tracking and thumb_y - index_y < 10:
                    tracking = False
                    print("Tracking stopped!")
                    # Save the canvas
                    cv2.imwrite("tracked_contour.png", canvas)
                    print("Contour saved to 'tracked_contour.png'")

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if tracking:
                    current_point = (index_x, index_y)
                    if previous_point:
                        cv2.line(canvas, previous_point, current_point, BLACK_COLOR, 2)
                    previous_point = current_point
                else:
                    previous_point = None

        overlay = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

        cv2.imshow('Tracked Contour', overlay)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
