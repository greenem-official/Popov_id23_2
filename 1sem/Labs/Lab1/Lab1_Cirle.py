import math
import time
from tkinter import *

# Main settings
fps = 60
size = 600
radius = 200
speed = 0.14
direction = 1

# Start
root = Tk()
canvas = Canvas(root, width=size, height=size)
canvas.pack()

# Runtime variables
pos = 0
timestamp = time.time()
lastBallObj = None


def drawAt(pos, radius, outline='', width=1, fill=''):
    return canvas.create_oval(pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius, outline=outline,
                              width=width, fill=fill)


def setup():
    # Drawing the big circle
    drawAt((size / 2, size / 2), radius, outline='gray', width=10)


def animate():
    global pos
    global timestamp
    global lastBallObj

    # Clearing old ball
    canvas.delete(lastBallObj)

    # Calculating ball angle in radians
    angle_rad = -math.pi / 2 + pos * (360 * math.pi / 180)
    x = size / 2 + radius * math.cos(angle_rad)
    y = size / 2 + radius * math.sin(angle_rad)

    # Drawing the ball and remembering it
    lastBallObj = drawAt((x, y), 20, fill='red', outline='black', width=5)

    # Moving the position
    deltaTime = time.time() - timestamp
    pos += speed * direction * deltaTime
    timestamp = time.time()

    # Repeating the steps with a set interval based on set FPS
    root.after(int(1000 / fps), animate)


# The game loop logic
setup()
animate()
root.mainloop()
