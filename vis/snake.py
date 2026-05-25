import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# 12 Servo Snake Robot Simulation
# Based on Arduino Serpentine_Sigmoid_Control
# ==========================================

# -----------------------------
# PARAMETERS FROM ARDUINO CODE
# -----------------------------

NUM_SERVOS = 12

lag = 0.5712                 # phase lag
frequency = 1
amplitude = 25               # degrees
offset = 6                   # calibration offset

enableSigmoid = True
sigmoidSlope = 1.0
sigmoidCenter = 3.0

SEGMENT_LENGTH = 1.0

# Motion mode
MODE = "forward"
# Options:
# "forward"
# "reverse"
# "left"
# "right"
# "twisting"

# --------------------------------
# SIGMOID STABILIZATION FUNCTION
# --------------------------------

def get_sigmoid_factor(joint_index):

    if not enableSigmoid:
        return 1.0

    n = float(joint_index)

    return 1.0 / (1.0 + np.exp(
        -sigmoidSlope * (n - sigmoidCenter)
    ))

# --------------------------------
# CALCULATE SERVO ANGLES
# --------------------------------

def calculate_angles(counter_rad, turn_offset=0):

    angles = []

    phase_values = [
        5, 4, 3, 2, 1, 0,
        -1, -2, -3, -4, -5, -6
    ]

    for i in range(NUM_SERVOS):

        joint_index = i + 1

        sigmoid = get_sigmoid_factor(joint_index)

        angle = (
            90
            + turn_offset
            + sigmoid
            * amplitude
            * np.cos(counter_rad + phase_values[i] * lag)
        )

        angles.append(np.radians(angle - 90))

    return angles

# --------------------------------
# BUILD SNAKE BODY
# --------------------------------

def build_snake(angles, twisting=False):

    x = [0]
    y = [0]
    z = [0]

    yaw = 0
    pitch = 0

    for i, angle in enumerate(angles):

        # Alternate servo orientation
        if i % 2 == 0:
            yaw += angle
        else:
            pitch += angle

        # Twisting mode
        if twisting:
            roll_effect = 0.4 * np.sin(i * 0.5 + yaw)
        else:
            roll_effect = 0

        dx = SEGMENT_LENGTH * np.cos(yaw) * np.cos(pitch)
        dy = SEGMENT_LENGTH * np.sin(yaw) * np.cos(pitch)
        dz = SEGMENT_LENGTH * np.sin(pitch + roll_effect)

        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
        z.append(z[-1] + dz)

    return x, y, z

# --------------------------------
# MATPLOTLIB SETUP
# --------------------------------

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

line, = ax.plot([], [], [], 'o-', lw=4)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)

ax.set_title("12-Servo Snake Robot Simulation")

# --------------------------------
# ANIMATION UPDATE
# --------------------------------

def update(frame):

    ax.cla()

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

    ax.set_title(f"Snake Robot Motion : {MODE}")

    counter = np.radians(frame * frequency)

    turn_offset = 0

    twisting = False

    # -------------------
    # MOTION MODES
    # -------------------

    if MODE == "forward":
        counter_rad = counter

    elif MODE == "reverse":
        counter_rad = -counter

    elif MODE == "left":
        counter_rad = counter
        turn_offset = -5

    elif MODE == "right":
        counter_rad = counter
        turn_offset = 5

    elif MODE == "twisting":
        counter_rad = counter
        twisting = True

    else:
        counter_rad = counter

    # Calculate servo angles
    angles = calculate_angles(
        counter_rad,
        turn_offset
    )

    # Build snake body
    x, y, z = build_snake(
        angles,
        twisting
    )

    # Draw snake
    ax.plot(
        x,
        y,
        z,
        'o-',
        linewidth=4,
        markersize=8
    )

    # Camera rotation
    ax.view_init(
        elev=25,
        azim=frame * 0.5
    )

# --------------------------------
# RUN ANIMATION
# --------------------------------

ani = FuncAnimation(
    fig,
    update,
    frames=720,
    interval=30
)

plt.show()