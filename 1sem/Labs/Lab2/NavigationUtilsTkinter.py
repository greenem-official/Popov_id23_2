class GlobalPositionData:
    position: tuple[int, int]
    scale: float
    renderWindowSize: tuple[int, int]

    def __init__(self):
        self.position = (0, 0)
        self.scale = 1


class ControlsData:
    lastDragCoords: tuple[int, int]
    lastMousePos: tuple[int, int]
    state = 'released'

    # def __init__(self):
        # self.lastDragCoords = (0, 0)


class Navigation():
    def __init__(self, simulation, renderWindowSize):
        self.globalPositionData = GlobalPositionData()
        self.controlsData = ControlsData()
        self.simulation = simulation
        self.globalPositionData.renderWindowSize = renderWindowSize

    def getIntPosScaled(self, raw_pos):
        # if isinstance(raw_pos, int) or isinstance(raw_pos, float):
        #     return int((raw_pos + globalPositionData.position) * globalPositionData.scale)
        # else:
        if isinstance(raw_pos, tuple):
            return int(self.globalPositionData.renderWindowSize[0] / 2 + (raw_pos[0] - self.globalPositionData.position[0]) * self.globalPositionData.scale),\
                int(self.globalPositionData.renderWindowSize[1] / 2 + (raw_pos[1] - self.globalPositionData.position[1]) * self.globalPositionData.scale)

    def on_mousewheel(self, event):
        self.globalPositionData.scale = max(0.001, self.globalPositionData.scale + (
                    event.delta / 120) / 10 * self.simulation.scrollSensitivity)

        sign = 1 if event.delta >= 0 else -1
        offset_multiplier = 0.1
        # print(controlsData.lastMousePos[0] - globalPositionData.renderWindowSize[0] / 2)
        x_offset = (self.controlsData.lastMousePos[0] - self.globalPositionData.renderWindowSize[0] / 2) * 1 / (
                    self.globalPositionData.scale ** 2) * offset_multiplier * sign
        y_offset = (self.controlsData.lastMousePos[1] - self.globalPositionData.renderWindowSize[1] / 2) * 1 / (
                    self.globalPositionData.scale ** 2) * offset_multiplier * sign

        self.globalPositionData.position = (self.globalPositionData.position[0] + x_offset, self.globalPositionData.position[1] + y_offset)

    def on_mouse_movement(self, event):
        self.controlsData.lastMousePos = (event.x, event.y)

    def on_mouse_drag(self, event):
        if self.controlsData.state == 'released':
            return
        elif self.controlsData.state == 'clicked':
            self.controlsData.lastDragCoords = (event.x, event.y)
            self.controlsData.state = 'dragging'
        elif self.controlsData.state == 'dragging':
            self.globalPositionData.position = (
            self.globalPositionData.position[0] - (event.x - self.controlsData.lastDragCoords[0]) * self.simulation.mouseSensitivity,
            self.globalPositionData.position[1] - (event.y - self.controlsData.lastDragCoords[1]) * self.simulation.mouseSensitivity
            )
        self.controlsData.lastDragCoords = (event.x, event.y)

    def on_mouse_left_click(self, event):
        self.controlsData.state = 'clicked'

    def on_mouse_left_release(self, event):
        self.controlsData.state = 'released'

    def on_window_movement_resizing(self, event):
        # print(event.widget, simulation.root, simulation.canvas, event.widget == simulation.root, event.widget == simulation.canvas)
        # print(event.width, event.height)
        if event.widget == self.simulation.root:
            self.globalPositionData.renderWindowSize = (event.width, event.height)
            # simulation.canvas.config(width=event.width, height=event.height)