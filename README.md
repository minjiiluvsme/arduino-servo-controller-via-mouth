# Mouth Gesture Controlled Servo Motor
This project uses Python, OpenCV, and MediaPipe Face Mesh to detect mouth movements in real time. When the mouth opens or closes, the Python application sends commands through serial communication to an Arduino Uno, which controls a servo motor accordingly.
Features

Real-time mouth tracking using MediaPipe Face Mesh
Live webcam detection with OpenCV
Serial communication between Python and Arduino
Servo motor rotates based on mouth opening and closing
Built-in command cooldown to prevent rapid servo movement

Requirements
Python Environment

Python 3.7 or later
OpenCV
MediaPipe
NumPy
PySerial

Install requirements using:
pip install opencv-python mediapipe numpy pyserial

