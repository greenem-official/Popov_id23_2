from tkinter import *
import time
import math


def drawAt(canvas: Canvas, pos, radius, outline='', width=1, fill=''):
    return canvas.create_oval(pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius,
                                     outline=outline, width=width, fill=fill)

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

    def __drawMyself(self, canvas: Canvas):
        if self.position is None:
            print("None position")
            return

        color = self.__interpolate_color(self.density)
        drawAt(canvas=canvas, pos=self.position, radius=self.size/2, fill=color, width=4)

    def drawRecursively(self, canvas: Canvas, timeScale):
        if self.parent is not None:
            self.position = (self.parent.position[0] + self.__getRelPosFromAngle()[0], self.parent.position[1] + self.__getRelPosFromAngle()[1])
            self.angle += self.speed * timeScale

        self.__drawMyself(canvas)
        for child in self.children:
            child.drawRecursively(canvas, timeScale)

class SolarSystemSimulation:
    def __init__(self, size, fps, timeScale):
        self.__size = size
        self.__fps = fps
        self.timeScale = timeScale
        self.__lastFrameTimestamp = time.time()
        self.__deltaTime = 0
        self.__mainPlanet = Planet('L0', 40, 100, 0)
        self.__createPlanets()

        self.__root = Tk()
        self.__canvas = Canvas(self.__root, width=self.__size, height=self.__size)
        self.__canvas.pack()

    def start(self):
        self.__drawFrame()
        self.__root.mainloop()

    def __createPlanets(self):
        self.__mainPlanet.position = (self.__size/2, self.__size/2)
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
        self.__mainPlanet.drawRecursively(self.__canvas, self.timeScale)

    def __drawFrame(self):
        self.__calculateTime()
        self.__canvas.delete('all')

        self.__drawPlanets()

        self.__scheduleNextFrame()


simulation = SolarSystemSimulation(size=700, fps=60, timeScale=0.2)
simulation.start()
