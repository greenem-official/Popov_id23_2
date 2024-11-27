from tkinter import *
import time
import math
from Labs.Utils.NavigationUtils import *

def drawSphereAt(navigation: Navigation, canvas: Canvas, raw_pos, radius, outline='', width=1, fill=''):
    point1 = (navigation.getIntPosScaled((raw_pos[0] - radius, raw_pos[1] - radius)))
    point2 = (navigation.getIntPosScaled((raw_pos[0] + radius, raw_pos[1] + radius)))
    return canvas.create_oval(point1[0], point1[1], point2[0], point2[1],
                              outline=outline, width=width, fill=fill)


def drawCenteredText(navigation: Navigation, canvas: Canvas, raw_pos, text: str):
    textId = canvas.create_text(0, 0, text=text, anchor="nw", fill="white", font=("Arial", 14))
    xOffset = findXItemCenter(canvas, textId)
    extraOffset = (2, -8)
    xy = navigation.getIntPosScaled((raw_pos[0] + xOffset + extraOffset[0], raw_pos[1] + extraOffset[1]))
    canvas.move(textId, xy[0], xy[1])


def findXItemCenter(canvas, item):
    coords = canvas.bbox(item)
    xOffset = - ((coords[2] - coords[0]) / 2)
    return xOffset


class Planet:
    parent: "Planet" = None
    min_color_value = 0
    max_color_value = 100

    def __init__(self, name, size, density, speed, distanceFromParent=None):
        self.name = name
        self.size = size
        self.density = density
        self.speed = speed
        self.children = []
        self.position = None
        self.angle = 0
        self.distanceFromParent = distanceFromParent

        # self.linkToParent(parent)

    def setAngle(self, angle):
        self.angle = angle
        return self

    def __getRelPosFromAngle(self):
        angle_rad = -math.pi / 2 + (self.angle / 360) * (360 * math.pi / 180)
        x = self.distanceFromParent * math.cos(angle_rad)
        y = self.distanceFromParent * math.sin(angle_rad)
        return x, y

    def linkToParent(self, parentPlanet: "Planet", distance=None):
        if parentPlanet is None and self.parent is not None:
            self.parent.children.remove(self)
        if parentPlanet is not None:
            parentPlanet.children.append(self)

        self.parent = parentPlanet
        if distance is not None:
            self.distanceFromParent = distance
        return self

    def addChild(self, childPlanet: "Planet", distance=None):
        childPlanet.linkToParent(self, distance)
        return self

    def __interpolate_color(self, value):
        if value < self.min_color_value:
            value = self.min_color_value
        elif value > self.max_color_value:
            value = self.max_color_value

        normalized_value = 1 - (value - self.min_color_value) / (self.max_color_value - self.min_color_value)

        red = int(255 * (1 - normalized_value) + 128 * normalized_value)
        blue = int(60 * (1 - normalized_value) + 128 * normalized_value)
        green = int(20 * (1 - normalized_value) + 128 * normalized_value)

        hex_color = f'#{red:02X}{green:02X}{blue:02X}'
        return hex_color

    def __drawMyself(self, navigation: Navigation, canvas: Canvas, drawText):
        if self.position is None:
            print("None position")
            return

        color = self.__interpolate_color(self.density)
        drawSphereAt(navigation=navigation, canvas=canvas, raw_pos=self.position, radius=self.size / 2, fill=color, width=4)
        if drawText:
            drawCenteredText(navigation=navigation, canvas=canvas, raw_pos=self.position, text=self.name)

    def drawRecursively(self, navigation: Navigation, canvas: Canvas, timeScale, drawText):
        if self.parent is not None:
            self.position = (self.parent.position[0] + self.__getRelPosFromAngle()[0],
                             self.parent.position[1] + self.__getRelPosFromAngle()[1])
            self.angle += self.speed * timeScale

        self.__drawMyself(navigation=navigation, canvas=canvas, drawText=drawText)
        for child in self.children:
            child.drawRecursively(navigation=navigation, canvas=canvas, timeScale=timeScale, drawText=drawText)


class SolarSystemSimulation:
    def __init__(self, size, fps, timeScale, mouseSensitivity, scrollSensitivity, drawNames=False):
        self.navigation = Navigation(self, (size, size))

        self.__fps = fps
        self.mouseSensitivity = mouseSensitivity
        self.scrollSensitivity = scrollSensitivity
        self.timeScale = timeScale
        self.drawNames = drawNames
        self.__lastFrameTimestamp = time.time()
        self.__deltaTime = 0
        self.__mainPlanet = Planet('Sun', 40, 100, 0)
        self.__createPlanets()

        self.__root = Tk()
        self.__canvas = Canvas(self.__root, width=self.navigation.globalPositionData.renderWindowSize[0], height=self.navigation.globalPositionData.renderWindowSize[1], background='black')
        self.__canvas.pack(fill="both", expand=True)
        self.__registerBindings()

    @property
    def root(self):
        return self.__root

    @property
    def canvas(self):
        return self.__canvas

    def __registerBindings(self):
        self.__root.bind_all("<MouseWheel>", self.navigation.on_mousewheel)
        self.__root.bind_all("<Motion>", self.navigation.on_mouse_movement)
        self.__root.bind_all("<B1-Motion>", self.navigation.on_mouse_drag)
        self.__root.bind_all("<Button-1>", self.navigation.on_mouse_left_click)
        self.__root.bind_all("<ButtonRelease-1>", self.navigation.on_mouse_left_release)
        self.__root.bind_all("<Configure>", self.navigation.on_window_movement_resizing)

    def start(self):
        self.__drawFrame()
        self.__root.mainloop()

    def __createPlanets(self):
        self.__mainPlanet.position = (0, 0)
        self.__mainPlanet.addChild(
            Planet('A', 30, 10, 15, 80)
            .setAngle(120)
            .addChild(Planet('A_1', 15, 40, 20, 40))
        )

        self.__mainPlanet.addChild(
            Planet('B', 45, 60, 8, 140)
            .setAngle(-30)
            .addChild(Planet('B_1', 10, 40, 50, 90))
            .addChild(Planet('B_2', 25, 70, 20, 130))
        )

        self.__mainPlanet.addChild(
            Planet('C', 20, 25, 12, 190)
            .setAngle(90)
            .addChild(Planet('C_1', 15, 78, 50, 40))
            .addChild(
                Planet('C_2', 30, 42, 20, 140)
                .addChild(Planet('C_2_1', 10, 45, 35, 60))
            )
        )

    def __scheduleNextFrame(self):
        self.__root.after(int(1000 / self.__fps), self.__drawFrame)

    def __calculateTime(self):
        self.__deltaTime = time.time() - self.__lastFrameTimestamp
        self.__lastFrameTimestamp = time.time()

    def __drawPlanets(self):
        self.__mainPlanet.drawRecursively(navigation=self.navigation, canvas=self.__canvas, timeScale=self.timeScale, drawText=self.drawNames)

    def __drawFrame(self):
        self.__calculateTime()
        self.__canvas.delete('all')
        self.navigation.globalPositionData.renderWindowSize = (self.navigation.globalPositionData.renderWindowSize[0], self.navigation.globalPositionData.renderWindowSize[1])

        self.__drawPlanets()

        self.__scheduleNextFrame()


simulation = SolarSystemSimulation(size=800, fps=144, timeScale=0.05, mouseSensitivity=0.8, scrollSensitivity=0.8, drawNames=False)
try:
    simulation.start()
except KeyboardInterrupt:
    pass
