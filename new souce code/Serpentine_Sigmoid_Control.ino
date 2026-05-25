/*
 * Serpentine_Sigmoid_Control.ino
 *
 * Implements the Sigmoid-improved head-stabilized amplitude control
 * and standard serpentine gaits for a 12-segment snake robot.
 * Designed for Arduino Mega 2560 and 12 dual-shaft servos.
 *
 * Pin Mapping:
 * - Servos s1 to s12: Pins 2 to 13
 * - Remote Control Inputs:
 *   - Pin 14: Forward
 *   - Pin 15: Reverse
 *   - Pin 16: Right Turn
 *   - Pin 17: Left Turn
 *
 * Stabilization:
 * - A Sigmoid dampening factor is applied to the head joints to stabilize
 *   a head-mounted camera or sensor:
 *   S(n) = 1 / (1 + exp(-a * (n - b)))
 *   where n is the joint index (1 to 12 from head to tail),
 *   a is the Sigmoid slope (default 1.0), and b is the number of restricted
 *   head joints (default 3.0).
 */

#include <Servo.h>
#include <math.h>

// Define servo objects for the snake segments (s1 = head, s12 = tail)
Servo s1;
Servo s2;
Servo s3;
Servo s4;
Servo s5;
Servo s6;
Servo s7;
Servo s8;
Servo s9;
Servo s10;
Servo s11;
Servo s12;

// Remote control pin mapping
const int forwardPin = 14;
const int reversePin = 15;
const int rightPin = 16;
const int leftPin = 17;

// Remote control state variables
int forwardVal = 0;
int reverseVal = 0;
int rightVal = 0;
int leftVal = 0;

// Serpentine motion control parameters
float lag = 0.5712;       // Phase lag between segments (radians)
int frequency = 1;        // Oscillation frequency multiplier
int amplitude = 40;       // Target gait amplitude (degrees)
int rightOffset = 5;      // Right turn steering offset (degrees)
int leftOffset = -5;      // Left turn steering offset (degrees)
int offset = 6;           // Calibration offset for the first three head servos
int delayTime = 7;        // Delay (ms) between loop updates (controls speed)
int startPause = 5000;     // Pause (ms) at startup for robot positioning

// Sigmoid-improved amplitude stabilization parameters
bool enableSigmoid = true; // Set to true to enable head stabilization
float sigmoidSlope = 1.0;  // Slope parameter 'a'
float sigmoidCenter = 3.0; // Center parameter 'b' (number of restricted head joints)

// Helper function to calculate the Sigmoid damping factor for joint n
float getSigmoidFactor(int jointIndex) {
  if (!enableSigmoid) {
    return 1.0;
  }
  // jointIndex is 1-based (s1 is 1, ..., s12 is 12)
  float n = (float)jointIndex;
  return 1.0 / (1.0 + exp(-sigmoidSlope * (n - sigmoidCenter)));
}

// Function to write angles to all 12 servos given current counter and turning offset
void writeSnakeAngles(float counterAngleRad, float currentTurnOffset) {
  // s1 to s12, phase multipliers: s1 has 5, s2 has 4, ..., s12 has -6
  // Angle formula: 90 + base_offset + turn_offset + S(n) * amplitude * cos(counterAngle + phase)
  
  float s1_ang = 90.0 + offset + currentTurnOffset + getSigmoidFactor(1) * amplitude * cos(counterAngleRad + 5.0 * lag);
  float s2_ang = 90.0 + offset + currentTurnOffset + getSigmoidFactor(2) * amplitude * cos(counterAngleRad + 4.0 * lag);
  float s3_ang = 90.0 + offset + currentTurnOffset + getSigmoidFactor(3) * amplitude * cos(counterAngleRad + 3.0 * lag);
  
  float s4_ang = 90.0 + currentTurnOffset + getSigmoidFactor(4) * amplitude * cos(counterAngleRad + 2.0 * lag);
  float s5_ang = 90.0 + currentTurnOffset + getSigmoidFactor(5) * amplitude * cos(counterAngleRad + 1.0 * lag);
  float s6_ang = 90.0 + currentTurnOffset + getSigmoidFactor(6) * amplitude * cos(counterAngleRad + 0.0 * lag);
  float s7_ang = 90.0 + currentTurnOffset + getSigmoidFactor(7) * amplitude * cos(counterAngleRad - 1.0 * lag);
  float s8_ang = 90.0 + currentTurnOffset + getSigmoidFactor(8) * amplitude * cos(counterAngleRad - 2.0 * lag);
  float s9_ang = 90.0 + currentTurnOffset + getSigmoidFactor(9) * amplitude * cos(counterAngleRad - 3.0 * lag);
  float s10_ang = 90.0 + currentTurnOffset + getSigmoidFactor(10) * amplitude * cos(counterAngleRad - 4.0 * lag);
  float s11_ang = 90.0 + currentTurnOffset + getSigmoidFactor(11) * amplitude * cos(counterAngleRad - 5.0 * lag);
  float s12_ang = 90.0 + currentTurnOffset + getSigmoidFactor(12) * amplitude * cos(counterAngleRad - 6.0 * lag);

  s1.write((int)round(s1_ang));
  s2.write((int)round(s2_ang));
  s3.write((int)round(s3_ang));
  s4.write((int)round(s4_ang));
  s5.write((int)round(s5_ang));
  s6.write((int)round(s6_ang));
  s7.write((int)round(s7_ang));
  s8.write((int)round(s8_ang));
  s9.write((int)round(s9_ang));
  s10.write((int)round(s10_ang));
  s11.write((int)round(s11_ang));
  s12.write((int)round(s12_ang));
}

void setup() {
  // Set remote control movement pins as inputs
  pinMode(forwardPin, INPUT);
  pinMode(reversePin, INPUT);
  pinMode(rightPin, INPUT);
  pinMode(leftPin, INPUT);

  // Initialize input pins to LOW state
  digitalWrite(forwardPin, LOW);
  digitalWrite(reversePin, LOW);
  digitalWrite(rightPin, LOW);
  digitalWrite(leftPin, LOW);

  // Attach servos to pins 2-13
  s1.attach(2);
  s2.attach(3);
  s3.attach(4);
  s4.attach(5);
  s5.attach(6);
  s6.attach(7);
  s7.attach(8);
  s8.attach(9);
  s9.attach(10);
  s10.attach(11);
  s11.attach(12);
  s12.attach(13);

  // Put snake robot in starting position (t = 0)
  writeSnakeAngles(0.0, 0.0);

  // Delay for physical setup and positioning
  delay(startPause);
}

void loop() {
  // Read inputs from remote control pins
  forwardVal = digitalRead(forwardPin);
  reverseVal = digitalRead(reversePin);
  rightVal = digitalRead(rightPin);
  leftVal = digitalRead(leftPin);

  // Forward motion logic
  if (forwardVal == HIGH) {
    for (int counter = 0; counter < 360; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      writeSnakeAngles(angleRad, 0.0);
      delay(delayTime);
    }
  }

  // Reverse motion logic
  if (reverseVal == HIGH) {
    for (int counter = 360; counter > 0; counter -= 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      writeSnakeAngles(angleRad, 0.0);
      delay(delayTime);
    }
  }

  // Right turn logic
  if (rightVal == HIGH) {
    // 1. Ramp up right turn offset over the first 10 degrees of oscillation
    for (int counter = 0; counter < 10; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      float turnOffset = 0.1 * (float)counter * (float)rightOffset;
      writeSnakeAngles(angleRad, turnOffset);
      delay(delayTime);
    }
    // 2. Maintain right turn offset during main oscillation cycle
    for (int counter = 11; counter < 350; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      writeSnakeAngles(angleRad, (float)rightOffset);
      delay(delayTime);
    }
    // 3. Ramp down right turn offset over the last 10 degrees
    for (int counter = 350; counter < 360; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      float turnOffset = 0.1 * (float)(360 - counter) * (float)rightOffset;
      writeSnakeAngles(angleRad, turnOffset);
      delay(delayTime);
    }
  }

  // Left turn logic
  if (leftVal == HIGH) {
    // 1. Ramp up left turn offset over the first 10 degrees of oscillation
    for (int counter = 0; counter < 10; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      float turnOffset = 0.1 * (float)counter * (float)leftOffset;
      writeSnakeAngles(angleRad, turnOffset);
      delay(delayTime);
    }
    // 2. Maintain left turn offset during main oscillation cycle
    for (int counter = 11; counter < 350; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      writeSnakeAngles(angleRad, (float)leftOffset);
      delay(delayTime);
    }
    // 3. Ramp down left turn offset over the last 10 degrees
    for (int counter = 350; counter < 360; counter += 1) {
      float angleRad = (float)frequency * (float)counter * 3.14159 / 180.0;
      float turnOffset = 0.1 * (float)(360 - counter) * (float)leftOffset;
      writeSnakeAngles(angleRad, turnOffset);
      delay(delayTime);
    }
  }
}
