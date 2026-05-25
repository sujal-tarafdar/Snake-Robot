"""
snake_controller.py
====================
Rolling locomotion controller for a 12-joint snake robot in Webots R2025a.

Joint layout (13 segments, 12 joints):
  Seg0 -[H0]- Seg1 -[V1]- Seg2 -[H2]- Seg3 -[V3]- Seg4 -[H4]- Seg5
       -[V5]- Seg6 -[H6]- Seg7 -[V7]- Seg8 -[H8]- Seg9 -[V9]- Seg10
       -[H10]- Seg11 -[V11]- Seg12

Rolling gait equations (Sidewinder / Rolling):
  θ_H(i, t) = A_H * sin(ω·t + φ·i)
  θ_V(i, t) = A_V * cos(ω·t + φ·i + π/2)

Where:
  A_H   = horizontal amplitude  (rad)
  A_V   = vertical  amplitude   (rad)
  ω     = angular frequency     (rad/s)
  φ     = spatial phase shift   (rad / joint-pair)
  i     = joint-pair index      (0..5)

The π/2 offset between H and V planes produces the characteristic
helical body wave that propels the snake forward.
"""

from controller import Robot
import math

# ─── Gait parameters ────────────────────────────────────────────────────────
A_H     = 0.6        # Horizontal amplitude  (rad)  ~34°
A_V     = 0.4        # Vertical   amplitude  (rad)  ~23°
OMEGA   = 1.8        # Angular frequency     (rad/s)
PHI     = math.pi / 3.0   # Spatial phase shift between consecutive H-V pairs

# ─── Robot initialisation ────────────────────────────────────────────────────
robot    = Robot()
timestep = int(robot.getBasicTimeStep())

# ─── Motor name lists ────────────────────────────────────────────────────────
# 12 motors total, alternating H / V, indexed 0-11
# Even indices → Horizontal joints (axis 0 1 0)
# Odd  indices → Vertical   joints (axis 1 0 0)
MOTOR_NAMES = [
    "motor_H_0",   # joint 0  – H
    "motor_V_1",   # joint 1  – V
    "motor_H_2",   # joint 2  – H
    "motor_V_3",   # joint 3  – V
    "motor_H_4",   # joint 4  – H
    "motor_V_5",   # joint 5  – V
    "motor_H_6",   # joint 6  – H
    "motor_V_7",   # joint 7  – V
    "motor_H_8",   # joint 8  – H
    "motor_V_9",   # joint 9  – V
    "motor_H_10",  # joint 10 – H
    "motor_V_11",  # joint 11 – V
]

SENSOR_NAMES = [
    "sensor_H_0",
    "sensor_V_1",
    "sensor_H_2",
    "sensor_V_3",
    "sensor_H_4",
    "sensor_V_5",
    "sensor_H_6",
    "sensor_V_7",
    "sensor_H_8",
    "sensor_V_9",
    "sensor_H_10",
    "sensor_V_11",
]

# ─── Initialise motors & sensors ─────────────────────────────────────────────
motors  = []
sensors = []

for name in MOTOR_NAMES:
    m = robot.getDevice(name)
    if m is None:
        print(f"[WARN] Motor not found: {name}")
        motors.append(None)
    else:
        # Position-control mode (default); velocity is limited in .wbt
        m.setPosition(0.0)
        motors.append(m)

for name in SENSOR_NAMES:
    s = robot.getDevice(name)
    if s is None:
        print(f"[WARN] Sensor not found: {name}")
        sensors.append(None)
    else:
        s.enable(timestep)
        sensors.append(s)

print("Snake robot controller initialised.")
print(f"  Motors active : {sum(1 for m in motors  if m is not None)}/12")
print(f"  Sensors active: {sum(1 for s in sensors if s is not None)}/12")
print(f"  Gait params   : A_H={A_H:.2f} rad, A_V={A_V:.2f} rad, ω={OMEGA:.2f} rad/s, φ={PHI:.3f} rad")

# ─── Helper ──────────────────────────────────────────────────────────────────

def rolling_gait(joint_idx: int, t: float) -> float:
    """
    Compute target angle for joint `joint_idx` at time `t`.

    Joints are paired as (H, V) = (0,1), (2,3), (4,5), (6,7), (8,9), (10,11).
    Pair index k = joint_idx // 2
    Within pair: 0 → Horizontal, 1 → Vertical
    """
    k         = joint_idx // 2          # pair index 0-5
    is_vert   = (joint_idx % 2 == 1)    # True for V joints
    phase_k   = k * PHI                 # spatial phase for this pair

    if is_vert:
        # Vertical plane wave (cosine, offset by π/2 relative to H)
        theta = A_V * math.cos(OMEGA * t + phase_k + math.pi / 2.0)
    else:
        # Horizontal plane wave (sine)
        theta = A_H * math.sin(OMEGA * t + phase_k)

    return theta


# ─── Main control loop ────────────────────────────────────────────────────────
step_count = 0

while robot.step(timestep) != -1:
    t = step_count * (timestep / 1000.0)   # simulation time in seconds

    for idx, motor in enumerate(motors):
        if motor is None:
            continue
        target = rolling_gait(idx, t)
        motor.setPosition(target)

    # Optional: print joint positions every ~1 second
    if step_count % (1000 // timestep) == 0:
        positions = []
        for s in sensors:
            if s is not None:
                positions.append(f"{s.getValue():+.3f}")
            else:
                positions.append("  N/A ")
        print(f"t={t:6.2f}s | " + " ".join(positions))

    step_count += 1
