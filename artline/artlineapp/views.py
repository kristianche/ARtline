import cv2
import numpy as np
import mediapipe as mp
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import json
import base64
import os
from datetime import datetime
from pathlib import Path

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


WIDTH = 1560
HEIGHT = 780
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
COLORS = [(0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (128, 0, 128)]
color_names = {"black": 0, "red": 1, "green": 2, "blue": 3, "yellow": 4, "purple": 5}

canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
tracking = False
previous_points = []
color_index = 0  #
thickness = 5
eraser_mode = False


def get_screenshots_folder():
    """Returns the user's Screenshots folder path based on OS."""
    home = Path.home()

    if os.name == "nt":
        screenshots_folder = home / "Documents" / "Artline Pictures"
    else:
        screenshots_folder = home / "Documents" / "Artline Pictures"

    screenshots_folder.mkdir(parents=True, exist_ok=True)
    return str(screenshots_folder)


def air_drawing():
    global tracking, previous_points, canvas, color_index, thickness, eraser_mode

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
    ) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    index_x, index_y = int(index_tip.x * WIDTH), int(index_tip.y * HEIGHT)
                    thumb_x, thumb_y = int(thumb_tip.x * WIDTH), int(thumb_tip.y * HEIGHT)

                    if not tracking and abs(index_tip.y - thumb_tip.y) > 0.05:
                        tracking = True
                        previous_points = []

                    if tracking and abs(index_tip.y - thumb_tip.y) < 0.02:
                        tracking = False

                    if tracking:
                        previous_points.append((index_x, index_y))
                        if len(previous_points) > 1:
                            cv2.line(canvas, previous_points[-2], previous_points[-1],
                                     COLORS[color_index] if not eraser_mode else WHITE_COLOR, thickness)

                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            overlay = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
            _, jpeg = cv2.imencode('.jpg', overlay)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()


def home(request):
    global thickness, color_index, eraser_mode, canvas

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if "thickness" in data:
                thickness = data["thickness"]
            if "color_index" in data:
                color_index = data["color_index"]
            if "eraser_mode" in data:
                eraser_mode = data["eraser_mode"]

            if "clear_canvas" in data and data["clear_canvas"]:
                canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
                return JsonResponse({"status": "success", "message": "Canvas cleared!"})

            if "image" in data:
                image_data = data["image"]
                if not image_data:
                    return JsonResponse({"status": "error", "message": "No image data received"}, status=400)

                # Remove the base64 prefix (if exists)
                if image_data.startswith("data:image/png;base64,"):
                    image_data = image_data.split(",")[1]
                else:
                    return JsonResponse({"status": "error", "message": "Invalid image data format"}, status=400)

                try:
                    image_bytes = base64.b64decode(image_data)
                    print(len(image_bytes))
                    np_arr = np.frombuffer(image_bytes, np.uint8)
                    print(np_arr)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)

                    if img is None:
                        return JsonResponse({"status": "error", "message": "Failed to decode image data"}, status=400)

                    screenshots_folder = get_screenshots_folder()
                    print(screenshots_folder)

                    filename = f"drawing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = os.path.join(screenshots_folder, filename)

                    if not os.path.exists(screenshots_folder):
                        os.makedirs(screenshots_folder)

                    success = cv2.imwrite(filepath, img)
                    if success:
                        return JsonResponse({"status": "success", "message": "Drawing saved!", "filepath": filepath})
                    else:
                        return JsonResponse({"status": "error", "message": "Failed to save the image"}, status=500)

                except Exception as e:
                    return JsonResponse({"status": "error", "message": f"Error decoding image: {str(e)}"}, status=400)

            return JsonResponse(
                {"status": "success", "thickness": thickness, "color_index": color_index, "eraser_mode": eraser_mode})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return render(request, 'home.html',
                  {'width': WIDTH, 'height': HEIGHT, 'thickness': thickness, 'color_index': color_index,
                   'eraser_mode': eraser_mode})


def video_feed(request):
    return StreamingHttpResponse(air_drawing(), content_type='multipart/x-mixed-replace; boundary=frame')