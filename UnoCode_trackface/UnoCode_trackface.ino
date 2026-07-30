#include <Servo.h>

Servo myServo;  // Create a Servo object
int servoPin = 9;  // Connect Servo signal pin to D9
int position = 90;  // Start at the middle position

void setup() {
    Serial.begin(9600);  // Start serial communication
    myServo.attach(servoPin);
    myServo.write(position);  // Set initial position
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();  // Read incoming command

        if (command == 'U') {
            position += 10;  // Move up
            position = constrain(position, 0, 180);  // Limit range
            myServo.write(position);
            Serial.println("Moving Up");
        }
        else if (command == 'D') {
            position -= 10;  // Move down
            position = constrain(position, 0, 180);  // Limit range
            myServo.write(position);
            Serial.println("Moving Down");
        }
    }
}