import colorsys
import math

from Labs.Lab3.util import CanvasUtils
from Labs.Lab3.Data import Data

from PyQt6.QtGui import QPainter, QColor

class Planet:
    parent: "Planet" = None
    min_color_value = 0
    max_color_value = 500

    def __init__(self, data: Data, name, size, mass, speed, distanceFromParent=None, startAngle=None):
        self.data = data

        self.children = []
        self.position = None
        # self.isCenterPlanet = False

        if name is not None:
            self.name = name

        self.size = 0
        if size is not None:
            self.size = size

        self.mass = 0
        if mass is not None:
            self.mass = mass

        self.speed = 0
        if speed is not None:
            self.speed = speed

        self.distanceFromParent = 0
        if distanceFromParent is not None:
            self.distanceFromParent = distanceFromParent

        self.angle = 0
        if startAngle is not None:
            self.angle = startAngle

    def getPosition(self):
        return self.position

    def getMass(self):
        return self.mass

    def getSize(self):
        return self.size

    def setAngle(self, angle):
        self.angle = angle
        return self

    def setMass(self, mass):
        self.mass = mass
        return self

    def setSize(self, size):
        self.size = size
        return self

    def getDensity(self):
        return self.mass / max(1, self.size)

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

    def __updateGraphics(self, painter: QPainter):  # Only after calculating the position
        if self.position is None:
            print("None position")
            return

        density = self.getDensity()
        color = CanvasUtils.interpolate_color(density, self.min_color_value, self.max_color_value)
        orbitOpacity = 20

        CanvasUtils.drawSphereAt(painter=painter, data=self.data, raw_pos=self.position, radius=self.size / 2, fill_color=color)

        if self.parent is not None:
            orbitColor = QColor(color.red(), color.green(), color.blue(), orbitOpacity)
            CanvasUtils.drawSphereAt(painter=painter, data=self.data, raw_pos=self.parent.position, radius=self.distanceFromParent, fill_color=QColor(0, 0, 0, 0), outline_color=orbitColor, outline_width=3)

        if self.data.drawPlanetInfo:
            # textColor = CanvasUtils.interpolate_color(density, self.min_color_value, self.max_color_value, saturation=10)
            text = f'{self.name}\nMass: {self.mass:.0f}\nDiameter: {self.size:.0f}\nDensity: {density:.0f}'
            CanvasUtils.drawTextAt(painter=painter, data=self.data, raw_pos=self.position, text=text, color=QColor('white'), outline_width=10, font_size=16, outline=True, outline_color=QColor(0, 255, 0))  # , size=(100, 70)

    def __calculatePositions(self):
        if self.parent is not None:
            self.position = (self.parent.position[0] + self.__getRelPosFromAngle()[0],
                             self.parent.position[1] + self.__getRelPosFromAngle()[1])

    def __updatePhysics(self):
        self.__calculatePositions()
        self.angle += self.speed * self.data.timeScale * self.data.deltaTime

    def updatePhysics(self):
        self.__updatePhysics()
        for child in self.children:
            child.updatePhysics()

    def updateGraphics(self, painter: QPainter):
        self.__updateGraphics(painter=painter)
        for child in self.children:
            child.updateGraphics(painter=painter)