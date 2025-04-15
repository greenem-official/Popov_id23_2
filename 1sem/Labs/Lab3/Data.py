from Labs.Lab3.FrameUpdater import FrameUpdater


class Data:
    canvas = None
    navigation = None
    simulation = None
    meteorManager = None
    asteroidMenuWidget = None
    deltaTime = None
    debug = False
    drawPlanetInfo = False
    meteorMode = False
    renderWindowSize: tuple[int, int] = None

    mouseSensitivity = 1
    scrollSensitivity = 1

    def __init__(self, fps: int, size: tuple[int, int]):
        self.fps = fps
        self.frameUpdater = FrameUpdater(self)
        self.renderWindowSize = size
        self.timeScale = 3
