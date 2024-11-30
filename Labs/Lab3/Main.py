import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent, QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow
import logging

from Labs.Lab3.Canvas import Canvas
from Labs.Lab3.Data import Data
from Labs.Lab3.util import StylesManager


class MainWindow(QMainWindow):
    def __init__(self, data: Data):
        super().__init__()
        self.data = data

        self.setWindowTitle("Simulation")
        self.setGeometry(100, 100, data.renderWindowSize[0], data.renderWindowSize[1])

        canvas = Canvas(data)
        self.setCentralWidget(canvas)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def resizeEvent(self, event: QResizeEvent):
        self.data.renderWindowSize = (event.size().width(), event.size().height())

    def wheelEvent(self, event):
        # if not self.data.meteorMode:
        self.data.navigation.on_mousewheel(event)

    def isLeftClicked(self, event: QMouseEvent):
        return Qt.MouseButton.LeftButton in event.buttons()

    def isMiddleClicked(self, event: QMouseEvent):
        return Qt.MouseButton.MiddleButton in event.buttons()

    def mousePressEvent(self, event: QMouseEvent):
        # if self.isLeftClicked(event) and not self.data.meteorMode or self.isMiddleClicked(event) and self.data.meteorMode:
        if self.isMiddleClicked(event):
            self.data.navigation.on_mouse_click(event)
        elif self.isLeftClicked(event) and self.data.meteorMode:
            self.data.meteorManager.onMousePressed(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.data.meteorMode:
            self.data.navigation.on_mouse_release(event)
        elif self.data.meteorMode:
            self.data.meteorManager.onMouseReleased(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        # if self.isLeftClicked(event) and not self.data.meteorMode or self.isMiddleClicked(event) and self.data.meteorMode:
        if self.isMiddleClicked(event):
            self.data.navigation.on_mouse_drag(event)
        elif self.isLeftClicked(event) and self.data.meteorMode:
            self.data.meteorManager.onMouseDragged(event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    StylesManager.init()
    data = Data(fps=144, size=(1500, 800))

    app = QApplication(sys.argv)
    app.setStyleSheet(StylesManager.load_style('data/styles/style.css'))

    window = MainWindow(data)
    window.show()
    try:
        app.exec()
    except Exception as e:
        logging.error(f"Exception: {e}")
