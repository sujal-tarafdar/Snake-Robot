import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==============================
# Snake Robot Twisting Motion
# ==============================

# Number of segments
NUM_SEGMENTS = 12

# Length of each segment
SEGMENT_LENGTH = 1

# Wave parameters
AMPLITUDE = 25           # degrees
PHASE_DIFF = np.pi / 6   # 30 degree phase shift
SPEED = 0.15

# Create figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Axis limits
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_zlim(-8, 8)

ax.set_title("Snake Robot Twisting Motion Simulation")

# Snake body line
line, = ax.plot([], [], [], 'o-', linewidth=3)

# ==============================
# Update Function
# ==============================

def update(frame):

    ax.view_init(elev=30, azim=frame * 0.5)

    x = [0]
    y = [0]
    z = [0]

    current_angle_h = 0
    current_angle_v = 0

    # Build snake body
    for i in range(NUM_SEGMENTS):

        # Horizontal wave
        theta_h = np.radians(
            AMPLITUDE * np.sin(SPEED * frame + i * PHASE_DIFF)
        )

        # Vertical wave
        theta_v = np.radians(
            AMPLITUDE * np.cos(SPEED * frame + i * PHASE_DIFF)
        )

        current_angle_h += theta_h
        current_angle_v += theta_v

        # Calculate next segment position
        dx = SEGMENT_LENGTH * np.cos(current_angle_h)
        dy = SEGMENT_LENGTH * np.sin(current_angle_h)
        dz = SEGMENT_LENGTH * np.sin(current_angle_v)

        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
        z.append(z[-1] + dz)

    # Update line data
    line.set_data_3d(x, y, z)

    return line,

# ==============================
# Animation
# ==============================

ani = FuncAnimation(
    fig,
    update,
    frames=500,
    interval=50,
    blit=False
)

plt.show()