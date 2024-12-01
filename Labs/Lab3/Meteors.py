import math
from enum import Enum

from PyQt6.QtGui import QPainter, QMouseEvent, QColor

from Labs.Lab3.Data import Data
from Labs.Lab3.util import CanvasUtils


def calculateDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Meteor:
    __default_mass = 20
    __default_size = 20

    min_color_value = 0
    max_color_value = 500

    def __init__(self, data: Data, angle=None):
        self.data = data

        self.visible = True
        self.preparingMode = True
        self.speed = 0
        self.position = (0, 0)
        self.mass = self.__default_mass
        self.size = self.__default_size
        self.color = QColor('white')

        self.angle = 0
        if angle is not None:
            self.angle = angle

    def setPosition(self, position):
        self.position = position

    def setSpeed(self, speed):
        self.speed = speed

    def setMass(self, mass):
        self.mass = mass

    def setSize(self, size):
        self.size = size

    def setAngle(self, angle):
        self.angle = angle

    def getSize(self):
        return self.size

    def destroy(self):
        self.data.meteorManager.removeMeteor(self)

    def mergeWithPlanet(self, planet):
        planet.setMass(planet.getMass() + self.mass)
        planet.setSize(planet.getSize() + math.pow(self.size, 0.7))

        # print(CanvasUtils.interpolate_color(planet.getDensity(), self.min_color_value, self.max_color_value).hue())
        self.destroy()

    def checkCollisions(self):
        for planet in self.data.simulation.getAllPlanets():
            if calculateDistance(self.position, planet.getPosition()) < self.size / 2 + planet.getSize() / 2:
                self.mergeWithPlanet(planet)

    def __updatePhysics(self):
        self.position = CanvasUtils.getMovedPoint(self.position, self.angle, self.speed * self.data.timeScale * self.data.deltaTime)
        if abs(self.position[0]) > 4000 or abs(self.position[1]) > 4000:
            self.destroy()

        self.checkCollisions()

    def updatePhysics(self):
        self.__updatePhysics()

    def calculateColor(self):
        self.color = CanvasUtils.interpolate_color(self.mass / max(1, self.size), self.min_color_value,
                                                   self.max_color_value)

    def getColor(self):
        return self.color

    def __updateGraphics(self, painter: QPainter):
        if not self.visible:
            return

        # if self.preparingMode:
        #     self.color = QColor(255, 255, 255)
        # else:
        self.calculateColor()
        # print(self.mass / max(1, self.size), self.color.hue())
        CanvasUtils.drawSphereAt(painter=painter, data=self.data, raw_pos=self.position, radius=self.size / 2, fill_color=self.color,
                                 outline_color=QColor(255, 255, 255), outline_width=3)

    def updateGraphics(self, painter: QPainter):
        self.__updateGraphics(painter=painter)

    def setVisible(self, visible):
        self.visible = visible


class MouseState(Enum):
    PRESSED = 1
    DRAGGING = 2
    RELEASED = 3


class MeteorManager:
    lastPressLocation = (0, 0)
    curDirectionTargetPoint = None
    dragDistanceThreshold = 2
    min_drag_distance_to_draw_arrow = 5
    lastMeteorAngle = 0

    def __init__(self, data: Data):
        self.data = data
        self.mouseState = MouseState.RELEASED
        self.currentMeteor = None
        self.activeMeteors = []

    def setMeteorSpawnPoint(self, raw_pos):
        if self.currentMeteor is None:
            self.currentMeteor = Meteor(self.data)

        pos = self.data.navigation.convertPosDisplayToAbstract(raw_pos)
        self.currentMeteor.setPosition(pos)

        self.data.asteroidMenuWidget.onSpeedChange()
        self.data.asteroidMenuWidget.onMassChange()
        self.data.asteroidMenuWidget.onSizeChange()

    def getMouseEventPos(self, event: QMouseEvent):
        return (event.pos().x(), event.pos().y())

    def calculateAngle(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        delta_x = x2 - x1
        delta_y = y2 - y1

        angle_rad = math.atan2(delta_y, delta_x)
        angle_deg = math.degrees(angle_rad)

        angle_deg = (angle_deg + 360) % 360

        return angle_deg

    def onMousePressed(self, event: QMouseEvent):
        self.mouseState = MouseState.PRESSED
        self.lastPressLocation = self.data.navigation.convertPosDisplayToAbstract(self.getMouseEventPos(event))
        self.curDirectionTargetPoint = None
        self.setMeteorSpawnPoint((event.pos().x(), event.pos().y()))

    def onMouseReleased(self, event: QMouseEvent):
        pass
        # self.lastPressLocation = self.getMouseEventPos(event)
        # if self.mouseState == MouseState.PRESSED:
        #     self.setMeteorSpawnPoint((event.pos().x(), event.pos().y()))
        #     # create a meteor
        # elif self.mouseState == MouseState.DRAGGING:
        #     pass
        #     # direction thing

    def onMouseDragged(self, event: QMouseEvent):
        curPos = self.data.navigation.convertPosDisplayToAbstract(self.getMouseEventPos(event))
        # if calculateDistance(self.lastPressLocation, curPos) >= self.dragDistanceThreshold:
        self.mouseState = MouseState.DRAGGING
        self.curDirectionTargetPoint = curPos

    def launchCurMeteor(self, speed, mass):
        if self.currentMeteor is None or self.curDirectionTargetPoint is None:
            return

        if calculateDistance(self.lastPressLocation, self.curDirectionTargetPoint) >= self.dragDistanceThreshold:
            self.currentMeteor.setAngle(self.calculateAngle(self.lastPressLocation, self.curDirectionTargetPoint))
        else:
            self.currentMeteor.setAngle(self.currentMeteor.angle)
        self.lastMeteorAngle = self.currentMeteor.angle

        self.currentMeteor.setVisible(True)
        self.currentMeteor.setSpeed(speed)
        self.currentMeteor.setMass(mass)
        self.currentMeteor.preparingMode = False
        self.activeMeteors.append(self.currentMeteor)
        self.currentMeteor = None

    def removeMeteor(self, meteor):
        self.activeMeteors.remove(meteor)

    def onMeteorModeToggled(self):
        if self.currentMeteor is not None:
            self.currentMeteor.setVisible(self.data.meteorMode)

        # make currentMeteor visible or not

    def updatePhysics(self):
        for meteor in self.activeMeteors:
            meteor.updatePhysics()

    def updateGraphics(self, painter):
        if self.data.meteorMode:
            if self.currentMeteor is not None:
                self.currentMeteor.updateGraphics(painter)
                if self.curDirectionTargetPoint is not None:
                    if calculateDistance(self.lastPressLocation, self.curDirectionTargetPoint) > self.min_drag_distance_to_draw_arrow:
                        color = self.currentMeteor.getColor()
                        color.setAlpha(120)

                        CanvasUtils.drawArrowPointerAt(painter=painter, data=self.data, start_point_raw=self.lastPressLocation,
                                                       angle_degrees=self.calculateAngle(self.lastPressLocation, self.curDirectionTargetPoint),
                                                       length=100, originalSize=self.currentMeteor.getSize(), color=QColor('#77424245'), outlineColor=color, outlineWidth=2, long_side_ratio=5)
                        # CanvasUtils.drawLineAt(painter=painter, data=self.data,
                        #                        point1_raw=self.lastPressLocation, point2_raw=self.curDirectionTargetPoint,
                        #                        color=QColor(255, 255, 255), width=4)
                        # 424245 # 707cff
        for meteor in self.activeMeteors:
            meteor.updateGraphics(painter)