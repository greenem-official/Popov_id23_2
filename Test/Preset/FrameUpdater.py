import time

from PyQt6.QtCore import QTimer


class FrameUpdater:
    def __init__(self, data):
        self.data = data
        self.paused = False

        self.lastFrameTimestamp = time.time()
        self.data.deltaTime = 0
        self.data.timeSinceStart = 0
        self.data.realTime = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def update_frame(self):
        self.__calculateTime()
        if not self.paused:
            self.data.canvas.update_physics()
        self.data.canvas.update_graphics()

    def __calculateTime(self):
        self.data.deltaTime = time.time() - self.lastFrameTimestamp
        self.lastFrameTimestamp = time.time()

        self.data.timeSinceStart += self.data.deltaTime
        self.data.realTime = time.time()

    def change_fps(self, new_fps):
        self.data.fps = new_fps
        self.timer.setInterval(1000 // self.data.fps)

    def getPaused(self):
        return self.paused

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def togglePause(self):
        self.paused = not self.paused
