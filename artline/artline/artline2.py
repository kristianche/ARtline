import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Canvas settings
CANVAS_SIZE = (480, 640)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (128, 0, 128)]  # Red, Green, Blue, Yellow, Purple
color_names = ["Red", "Green", "Blue", "Yellow", "Purple"]

canvas = np.ones((CANVAS_SIZE[0], CANVAS_SIZE[1], 3), dtype=np.uint8) * 255
strokes = []  # List to store strokes for undo feature
tracking = False
previous_points = []
color_index = 0  # Default color (Red)
thickness = 5
eraser_mode = False
brush_preview_radius = 20

cap = cv2.VideoCapture(0)

# Color buttons area and size
button_width = 100
button_height = 50
button_y = CANVAS_SIZE[0] - 60  # Position buttons at the bottom

def draw_buttons(frame):
    """Draw buttons for colors and highlight the selected one."""
    global color_index
    # Draw color buttons
    for i, color in enumerate(COLORS):
        button_x = 10 + i * (button_width + 10)
        # Highlight the selected button with a border
        if i == color_index:
            cv2.rectangle(frame, (button_x - 5, button_y - 5), (button_x + button_width + 5, button_y + button_height + 5), (255, 255, 255), 3)
        cv2.rectangle(frame, (button_x, button_y), (button_x + button_width, button_y + button_height), color, -1)
        cv2.putText(frame, color_names[i], (button_x + 10, button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLACK_COLOR, 2)

    # Draw eraser button
    cv2.rectangle(frame, (CANVAS_SIZE[1] - button_width - 10, button_y), (CANVAS_SIZE[1] - 10, button_y + button_height), (255, 255, 255), -1)
    cv2.putText(frame, "Eraser", (CANVAS_SIZE[1] - button_width - 5, button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLACK_COLOR, 2)

def is_point_in_button(x, y, button_x, button_y, button_width, button_height):
    """Check if the point (x, y) is inside the button."""
    return button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height

def draw_smooth_line(img, points, color, thickness):
    """Draw a smooth line using Catmull-Rom spline."""
    if len(points) < 2:
        return img
    for i in range(len(points) - 1):
        # Get points for Catmull-Rom spline
        p0 = points[i - 1] if i > 0 else points[i]  # Start point
        p1 = points[i]  # Control point
        p2 = points[i + 1] if i + 1 < len(points) else points[i]  # Control point
        p3 = points[i + 2] if i + 2 < len(points) else points[i + 1]  # End point

        # Calculate smooth curve points
        curve_points = []
        for t in np.linspace(0, 1, num=30):  # 30 interpolated points for smoothness
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t**2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t**3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t**2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t**3)
            curve_points.append((int(x), int(y)))

        # Draw the line between the points
        for j in range(len(curve_points) - 1):
            cv2.line(img, curve_points[j], curve_points[j + 1], color, thickness)

    return img

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

        frame = cv2.flip(frame, 1)  # Mirror effect
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract finger landmarks
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                index_x, index_y = int(index_tip.x * CANVAS_SIZE[1]), int(index_tip.y * CANVAS_SIZE[0])
                middle_x, middle_y = int(middle_tip.x * CANVAS_SIZE[1]), int(middle_tip.y * CANVAS_SIZE[0])
                thumb_x, thumb_y = int(thumb_tip.x * CANVAS_SIZE[1]), int(thumb_tip.y * CANVAS_SIZE[0])
                pinky_x, pinky_y = int(pinky_tip.x * CANVAS_SIZE[1]), int(pinky_tip.y * CANVAS_SIZE[0])

                # Gesture: Start tracking when index finger is far from thumb
                if not tracking and abs(index_tip.y - thumb_tip.y) > 0.05:
                    tracking = True
                    previous_points = []
                    print("🎨 Drawing Started!")

                # Gesture: Stop tracking when fingers come close
                if tracking and abs(index_tip.y - thumb_tip.y) < 0.02:
                    tracking = False
                    print("🛑 Drawing Stopped!")
                    strokes.append(canvas.copy())  # Save stroke for undo

                # Check if the user taps the color buttons
                for i in range(len(COLORS)):
                    button_x = 10 + i * (button_width + 10)
                    if is_point_in_button(index_x, index_y, button_x, button_y, button_width, button_height):
                        color_index = i
                        print(f"🎨 Switched to {color_names[color_index]}!")

                # Gesture: Activate eraser mode (if pinky & thumb touch)
                if abs(pinky_x - thumb_x) < 0.03 and abs(pinky_y - thumb_y) < 0.03:
                    eraser_mode = True
                    print("🧽 Eraser Activated!")
                else:
                    eraser_mode = False

                # Draw on canvas with smooth curve
                if tracking:
                    current_point = (index_x, index_y)
                    previous_points.append(current_point)

                    if len(previous_points) > 1:
                        # Draw smooth line between previous points
                        canvas = draw_smooth_line(canvas, previous_points, COLORS[color_index], thickness)
                else:
                    previous_points = []

                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Preview brush size
                if tracking:
                    cv2.circle(frame, (index_x, index_y), brush_preview_radius, COLORS[color_index], 2)

        # Draw color selection palette and highlight selected color
        draw_buttons(frame)

        # Overlay drawing on video
        overlay = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

        cv2.imshow('Artline', overlay)

        # Handle keypress
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit
            break
        elif key == ord('u'):  # Undo last stroke
            if strokes:
                canvas = strokes.pop()
                print("↩️ Undo Last Stroke!")
        elif key == ord('s'):  # Save drawing
            cv2.imwrite("air_drawing.png", canvas)
            print("📸 Drawing Saved!")
        elif key == ord('c'):  # Clear Canvas
            canvas = np.ones((CANVAS_SIZE[0], CANVAS_SIZE[1], 3), dtype=np.uint8) * 255
            strokes = []
            print("🧹 Canvas Cleared!")
        elif key == ord('+'):  # Increase thickness
            thickness += 1
            print(f"🖌️ Increased Brush Size: {thickness}")
        elif key == ord('-'):  # Decrease thickness
            if thickness > 1:
                thickness -= 1
            print(f"🖌️ Decreased Brush Size: {thickness}")

cap.release()
cv2.destroyAllWindows()


