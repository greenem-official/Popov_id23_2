import json
import math
import os.path

from PyQt6.QtGui import QColor

import CanvasUtils


class Simulation:
    def __init__(self, data):
        self.data = data

    def resetEverything(self):
        pass

    def updatePhysics(self):
        if self.data.waterDensity != 0:
            self.data.waterSpeed = math.sqrt(2*self.data.waterPressure/self.data.waterDensity + 2*self.data.g*self.data.elevationHeight)
            print('water speed:', self.data.waterSpeed)

            if self.data.simActive and not self.data.reachedLevel:
                self.data.waterHeightReal += self.data.waterSpeed * self.data.deltaTime * 1.0

            if self.data.waterHeightReal >= self.data.elevationHeight:
                self.data.waterHeightReal = self.data.elevationHeight
                self.data.reachedLevel = True


    def updateGraphics(self, painter):
        container_width = 600
        container_height = 300

        tube_width = 100
        tube_height = 400

        CanvasUtils.drawRectAtExact(painter=painter, data=self.data, raw_pos=(-container_width/2, container_height), raw_pos2=(container_width/2, 0),
                                    fill_color=QColor('#77424245'), outline_color=QColor('white'), outline_width=3)
        CanvasUtils.drawRectAtExact(painter=painter, data=self.data, raw_pos=(-tube_width/2, -500), raw_pos2=(tube_width/2, -500 + tube_height),
                                    fill_color=QColor('#77424245'), outline_color=QColor('white'), outline_width=3)
        if self.data.simActive and not self.data.reachedLevel:
            CanvasUtils.drawRectAtExact(painter=painter, data=self.data, raw_pos=(-tube_width/2, -500), raw_pos2=(tube_width/2, container_height),
                                        fill_color=QColor('#47bcff'), outline_color=None, outline_width=3)
        CanvasUtils.drawRectAtExact(painter=painter, data=self.data, raw_pos=(-container_width/2, container_height), raw_pos2=(container_width/2, container_height - self.data.waterHeightReal),
                                    fill_color=QColor('#47bcff'), outline_color=None, outline_width=3)
