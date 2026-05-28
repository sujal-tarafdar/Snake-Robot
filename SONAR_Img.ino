import serial
import pygame
import math

# =========================================
# SERIAL CONNECTION
# =========================================

arduino = serial.Serial(
    'COM3',      # CHANGE THIS
    115200
)

# =========================================0.
# PYGAME SETUP
# =========================================

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Snake Sonar Mapping"
)

clock = pygame.time.Clock()

# =========================================
# FONT
# =========================================

font = pygame.font.SysFont(
    "Arial",
    18
)

# =========================================
# RADAR CENTER
# =========================================

cx = WIDTH // 2
cy = HEIGHT - 50

# =========================================
# PERSISTENT POINT STORAGE
# =========================================

points = []

# =========================================
# MAIN LOOP
# =========================================

running = True

while running:

    # =====================================
    # CLEAR SCREEN
    # =====================================

    screen.fill((0, 0, 0))

    # =====================================
    # EVENTS
    # =====================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # =====================================
    # READ SERIAL
    # =====================================

    try:

        line = arduino.readline().decode().strip()

        # Expected format:
        # angle,distance

        angle, distance = line.split(',')

        angle = float(angle)
        distance = float(distance)

        # Ignore garbage values

        if distance > 0:

            # =================================
            # SCALE DISTANCE
            # =================================

            r = distance * 3

            # =================================
            # POLAR TO CARTESIAN
            # =================================

            rad = math.radians(angle)

            x = cx + r * math.cos(rad)

            y = cy - r * math.sin(rad)

            # =================================
            # STORE POINT
            # =================================

            points.append(
                (x, y, distance)
            )

    except:
        pass

    # =====================================
    # LIMIT HISTORY
    # =====================================

    if len(points) > 3000:

        points.pop(0)

    # =====================================
    # DRAW RADAR ARC
    # =====================================

    pygame.draw.circle(
        screen,
        (0, 80, 0),
        (cx, cy),
        150,
        1
    )

    pygame.draw.circle(
        screen,
        (0, 80, 0),
        (cx, cy),
        300,
        1
    )

    pygame.draw.circle(
        screen,
        (0, 80, 0),
        (cx, cy),
        450,
        1
    )

    # =====================================
    # DRAW ALL POINTS
    # =====================================

    for p in points:

        px = p[0]
        py = p[1]
        dist = p[2]

        # ---------------------------------
        # OBJECT POINT
        # ---------------------------------

        pygame.draw.circle(
            screen,
            (0,255,0),
            (int(px), int(py)),
            4
        )

        # ---------------------------------
        # DISTANCE LABEL
        # ---------------------------------

        label = font.render(
            f"{int(dist)}",
            True,
            (255,255,255)
        )

        screen.blit(
            label,
            (px + 6, py - 6)
        )

    # =====================================
    # RADAR CENTER POINT
    # =====================================

    pygame.draw.circle(
        screen,
        (255,0,0),
        (cx, cy),
        6
    )

    # =====================================
    # UPDATE DISPLAY
    # =====================================

    pygame.display.update()

    clock.tick(60)

# =========================================
# CLEANUP
# =========================================

pygame.quit()
arduino.close()