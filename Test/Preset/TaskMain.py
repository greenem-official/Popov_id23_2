import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent, QMouseEvent, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow

from Canvas import Canvas
from Data import Data
from util import StylesManager


class MainWindow(QMainWindow):
    def __init__(self, data: Data):
        super().__init__()
        self.data = data

        self.setWindowTitle("Task")
        self.setGeometry(100, 100, data.renderWindowSize[0], data.renderWindowSize[1])

        canvas = Canvas(data)
        self.setCentralWidget(canvas)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def resizeEvent(self, event: QResizeEvent):
        self.data.renderWindowSize = (event.size().width(), event.size().height())

    def wheelEvent(self, event):
        self.data.navigation.on_mousewheel(event)

    def isLeftClicked(self, event: QMouseEvent):
        return Qt.MouseButton.LeftButton in event.buttons()

    def isMiddleClicked(self, event: QMouseEvent):
        return Qt.MouseButton.MiddleButton in event.buttons()

    def mousePressEvent(self, event: QMouseEvent):
        if self.isMiddleClicked(event):
            pass
        elif self.isLeftClicked(event):
            pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        pass

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isMiddleClicked(event):
            pass
        elif self.isLeftClicked(event):
            pass

    def keyReleaseEvent(self, event: QKeyEvent):
        if Qt.Key.Key_Return == event.key():
            pass


def load_style(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
    StylesManager.init()
    data = Data(fps=144, size=(1500, 800))

    app = QApplication(sys.argv)
    app.setStyleSheet(StylesManager.load_style('data/styles/style.css'))

    window = MainWindow(data)
    window.show()
    try:
        app.exec()
    except Exception as e:
        print(f"Exception: {e}")
