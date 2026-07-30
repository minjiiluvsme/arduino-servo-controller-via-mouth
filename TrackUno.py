import time
import cv2
import mediapipe as mp
import numpy as np
import serial  # Import Serial library

# Initialize Serial Communication (Change 'COM7' to your Arduino port)
arduino = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # Wait for connection

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

last_change = time.time()

def send_command(direction):
    """Send command to Arduino to move servo motor"""
    global last_change
    if time.time() - last_change > 0.4:  # Cooldown to prevent rapid commands
        if direction == 'up':
            arduino.write(b'U')  # Send 'U'
            print("Servo Moving UP")
        elif direction == 'down':
            arduino.write(b'D')  # Send 'D'
            print("Servo Moving DOWN")
        last_change = time.time()

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("Error: Camera not accessible.")
    exit()

try:
    while True:
        success, img = cap.read()
        if not success:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(imgRGB)

        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:

                h, w, c = img.shape
                # Upper and lower lip points
                upper_lip = faceLms.landmark[13]
                lower_lip = faceLms.landmark[14]

                # Convert to pixel coordinates
                upper_y = int(upper_lip.y * h)
                lower_y = int(lower_lip.y * h)

                # Calculate mouth opening distance
                mouth_distance = abs(lower_y - upper_y)

                # Draw points and line
                cv2.circle(img, (int(upper_lip.x*w), upper_y), 4, (0,255,0), -1)
                cv2.circle(img, (int(lower_lip.x*w), lower_y), 4, (0,255,0), -1)
                cv2.line(img, (int(upper_lip.x*w), upper_y), (int(lower_lip.x*w), lower_y), (0,255,0), 2)

                # Thresholds → Adjust based on your camera distance
                if mouth_distance > 22:   # mouth open
                    send_command('up')
                elif mouth_distance < 16: # mouth closed
                    send_command('down')

        cv2.imshow("Mouth Control Tracker", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()
