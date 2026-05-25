/*
 * Concertina_Control.ino
 *
 * Implements Concertina gait motion for a 12-segment snake robot
 * based on alternating odd/even segment phase oscillations.
 *
 * Pin Mapping:
 * - Servos 0 to 11: Pins 2 to 13
 * - Remote Control Inputs:
 *   - Pin 14: Forward (Runs the concertina motion)
 *   - Pin 15: Reverse (Runs the concertina motion with reversed phase timing)
 *   - Pin 16: Right Turn
 *   - Pin 17: Left Turn
 *
 * Center calibration:
 * - Servo 2 is calibrated at 180 degrees, while all other servos are centered at 90 degrees.
 * - Dynamic safety limits are applied around each servo's center position.
 */

#include <Servo.h>

Servo servo[12];

// Center positions (preserves your specific offset calibration)
int center[12] = {
  90, 90, 180, 90, 90, 90,
  90, 90, 90, 90, 90, 90
};

float t = 0;

// Wave parameters
float speedWave = 0.15;
float amplitude = 20;

// Timing control
unsigned long lastSwitch = 0;
bool oddPhase = true;
int phaseDelay = 2000;   // 2 sec switch interval

// Remote control pin mapping
const int forwardPin = 14;
const int reversePin = 15;
const int rightPin = 16;
const int leftPin = 17;

void setup() {
  Serial.begin(9600);
  Serial.println("Snake Robot Starting Concertina Motion...");

  // Initialize remote control pins as inputs
  pinMode(forwardPin, INPUT);
  pinMode(reversePin, INPUT);
  pinMode(rightPin, INPUT);
  pinMode(leftPin, INPUT);

  digitalWrite(forwardPin, LOW);
  digitalWrite(reversePin, LOW);
  digitalWrite(rightPin, LOW);
  digitalWrite(leftPin, LOW);

  // Attach servos 0 to 11 to pins 2 to 13
  for (int i = 0; i < 12; i++) {
    servo[i].attach(2 + i);
    servo[i].write(center[i]);

    Serial.print("Servo ");
    Serial.print(i);
    Serial.print(" attached to pin ");
    Serial.println(2 + i);
  }

  lastSwitch = millis();
}

void loop() {
  // Read inputs from remote control pins
  int forwardVal = digitalRead(forwardPin);
  int reverseVal = digitalRead(reversePin);
  int rightVal = digitalRead(rightPin);
  int leftVal = digitalRead(leftPin);

  // If any movement pin is active, or if you want autonomous continuous mode,
  // execute the concertina wave calculations.
  // (Remove "|| true" if you only want the robot to move when remote buttons are pressed)
  if (forwardVal == HIGH || reverseVal == HIGH || rightVal == HIGH || leftVal == HIGH || true) {
    
    // Adjust phase progression direction if reversing
    if (reverseVal == HIGH) {
      t -= speedWave;
    } else {
      t += speedWave;
    }

    // Switch between odd and even phase
    if (millis() - lastSwitch > phaseDelay) {
      oddPhase = !oddPhase;
      lastSwitch = millis();

      if (oddPhase)
        Serial.println("ODD PHASE ACTIVE");
      else
        Serial.println("EVEN PHASE ACTIVE");
    }

    // Move all servos
    for (int i = 0; i < 12; i++) {
      float pos = center[i];

      // Steering adjustment offsets
      float turnOffset = 0;
      if (rightVal == HIGH) {
        turnOffset = 10.0; // Apply offset to turn right
      } else if (leftVal == HIGH) {
        turnOffset = -10.0; // Apply offset to turn left
      }

      // ---------------- ODD PHASE ----------------
      if (oddPhase) {
        // Move odd indexed servos together
        if (i % 2 == 1) {
          pos += amplitude * sin(t) + turnOffset;
        }
      }
      // ---------------- EVEN PHASE ----------------
      else {
        // Move even indexed servos together
        if (i % 2 == 0) {
          pos += amplitude * sin(t) + turnOffset;
        }
      }

      // Limit motion:
      // Note: Since servo[2] has a center of 180 degrees, a static constraint of [60, 120]
      // would block its movement. We use dynamic safety limits centered around each joint's center.
      float minLimit = (center[i] == 180) ? 140.0 : 60.0;
      float maxLimit = (center[i] == 180) ? 180.0 : 120.0;
      pos = constrain(pos, minLimit, maxLimit);

      // Write servo angle
      servo[i].write((int)round(pos));

      // Debug print (throttled to avoid flooding serial buffer)
      if (i == 0 || i == 1 || i == 2) {
        Serial.print("Servo ");
        Serial.print(i);
        Serial.print(" Position: ");
        Serial.println(pos);
      }
    }
    
    Serial.println("----------------------");
  } else {
    // Return all joints to center position when idle
    for (int i = 0; i < 12; i++) {
      servo[i].write(center[i]);
    }
  }

  delay(20);
}
