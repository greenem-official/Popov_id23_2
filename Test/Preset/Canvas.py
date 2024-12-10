from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPainter, QColor

from Data import Data
from Simulation import Simulation
from UI import UIWidget
from NavigationUtils import Navigation
from FrameUpdater import FrameUpdater


class Canvas(QWidget):
    def __init__(self, data: Data):
        super().__init__()
        self.data = data

        self.data.canvas = self
        self.data.navigation = Navigation(self.data)
        self.data.frameUpdater = FrameUpdater(self.data)
        self.data.simulation = Simulation(self.data)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        ui = UIWidget(self.data)
        self.mainLayout.addWidget(ui)
        ui.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def update_physics(self):
        self.data.simulation.updatePhysics()

    def update_graphics(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor(40, 40, 40))  # Background
        self.data.simulation.updateGraphics(painter)  # Objects

        painter.end()
