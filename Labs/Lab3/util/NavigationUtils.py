from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent, QMouseEvent, QDragMoveEvent
from Labs.Lab3.Data import Data

class GlobalPositionData:
    position: tuple[float, float]
    scale: float
    # renderWindowSize: tuple[int, int]

    def __init__(self):
        self.position = (0, 0)
        self.scale = 1


class ControlsData:
    lastDragCoords: tuple[float, float] = None
    lastMousePos: tuple[float, float] = None
    state = 'released'

    # def __init__(self):
        # self.lastDragCoords = (0, 0)


class Navigation:
    def __init__(self, data: Data):
        self.data = data

        self.globalPositionData = GlobalPositionData()
        self.controlsData = ControlsData()

    def convertPosAbstractToDisplayX(self, raw_pos_x):
        if isinstance(raw_pos_x, float) or isinstance(raw_pos_x, int):
            return self.data.renderWindowSize[0] / 2 + (raw_pos_x - self.globalPositionData.position[0]) * self.globalPositionData.scale

    def convertPosAbstractToDisplayY(self, raw_pos_y):
        if isinstance(raw_pos_y, float) or isinstance(raw_pos_y, int):
            return self.data.renderWindowSize[1] / 2 + (raw_pos_y - self.globalPositionData.position[1]) * self.globalPositionData.scale

    def convertPosAbstractToDisplay(self, raw_pos):
        if isinstance(raw_pos, tuple) or isinstance(raw_pos, list):
            return (self.convertPosAbstractToDisplayX(raw_pos[0]), self.convertPosAbstractToDisplayY(raw_pos[1]))

    def convertPosDisplayToAbstractX(self, display_pos_x):
        if isinstance(display_pos_x, float) or isinstance(display_pos_x, int):
            return (display_pos_x - self.data.renderWindowSize[0] / 2) / self.globalPositionData.scale + self.globalPositionData.position[0]

    def convertPosDisplayToAbstractY(self, display_pos_y):
        if isinstance(display_pos_y, float) or isinstance(display_pos_y, int):
            return (display_pos_y - self.data.renderWindowSize[1] / 2) / self.globalPositionData.scale +self.globalPositionData.position[1]

    def convertPosDisplayToAbstract(self, raw_pos):
        if isinstance(raw_pos, tuple):
            return (self.convertPosDisplayToAbstractX(raw_pos[0]), self.convertPosDisplayToAbstractY(raw_pos[1]))

    def on_mousewheel(self, event: QWheelEvent):
        # if self.controlsData.lastMousePos is None:
        #     return
        # event.angleDelta().y()

        if self.data.scrollSensitivity == 0:
            return

        self.globalPositionData.scale = max(0.001, self.globalPositionData.scale + (
                    event.angleDelta().y() // 120) / 10 * self.data.scrollSensitivity)

        sign = 1 if event.angleDelta().y() >= 0 else -1
        offset_multiplier = 0.1
        # print(controlsData.lastMousePos[0] - globalPositionData.renderWindowSize[0] / 2)
        x_offset = (event.position().x() - self.data.renderWindowSize[0] / 2) * 1 / (
                    self.globalPositionData.scale ** 2) * offset_multiplier * sign
        y_offset = (event.position().y() - self.data.renderWindowSize[1] / 2) * 1 / (
                    self.globalPositionData.scale ** 2) * offset_multiplier * sign

        self.globalPositionData.position = (self.globalPositionData.position[0] + x_offset, self.globalPositionData.position[1] + y_offset)

    def on_mouse_movement(self, event: QMouseEvent):
        # print(event.buttons())
        self.controlsData.lastMousePos = (event.position().x(), event.position().y())
        # if event.buttons() == Qt.MouseButton.LeftButton:
        #     self.on_mouse_drag(event)

    def on_mouse_release(self, event: QMouseEvent):
        self.controlsData.lastDragCoords = None

    def on_mouse_click(self, event: QMouseEvent):
        self.controlsData.lastDragCoords = (event.position().x(), event.position().y())

    def on_mouse_drag(self, event: QMouseEvent):
        if self.controlsData.lastDragCoords is None:
            self.controlsData.lastDragCoords = (event.position().x(), event.position().y())
            # return

        offsets = (event.position().x() - self.controlsData.lastDragCoords[0], event.position().y() - self.controlsData.lastDragCoords[1])
        self.controlsData.lastDragCoords = (event.position().x(), event.position().y())

        sensitivityCoef = 1

        self.globalPositionData.position = (
            self.globalPositionData.position[0] - (offsets[0]) * self.data.mouseSensitivity * sensitivityCoef,
            self.globalPositionData.position[1] - (offsets[1]) * self.data.mouseSensitivity * sensitivityCoef
        )

    def on_mouse_left_click(self, event):
        self.controlsData.state = 'clicked'

    def on_mouse_left_release(self, event):
        self.controlsData.state = 'released'

    # def on_window_movement_resizing(self, event):
        # # print(event.widget, simulation.root, simulation.canvas, event.widget == simulation.root, event.widget == simulation.canvas)
        # # print(event.width, event.height)
        # if event.widget == self.simulation.root:
        #     self.globalPositionData.renderWindowSize = (event.width, event.height)
        #     # simulation.canvas.config(width=event.width, height=event.height)