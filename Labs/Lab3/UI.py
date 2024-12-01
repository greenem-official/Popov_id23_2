from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout, QSpacerItem, \
    QSizePolicy
from PyQt6.QtCore import Qt, QPoint, QRect, QSize

from Labs.Lab3.Data import Data
from Labs.Lab3.util.Debugging import color_map, DebuggableQWidget
from Labs.Lab3.util.StylesManager import StyleType, getStyle


class CirculatingButtonSwitch(DebuggableQWidget):
    def __init__(self, data: Data, optionsList, onValueChange=None, buttonStyle=None):
        super().__init__(data, 'debugAdvancedNumberWidget')
        self.data = data
        self.optionsList = optionsList
        self.index = -1
        self.onValueChange = onValueChange

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.btn = QPushButton('a')
        self.btn.clicked.connect(self.onButtonClicked)

        if buttonStyle is not None:
            self.btn.setStyleSheet(buttonStyle)

        self.onButtonClicked()

        self.layout.addWidget(self.btn)

    def getButton(self):
        return self.btn

    def updateIndex(self):
        self.index += 1
        if self.index >= len(self.optionsList):
            self.index = 0

    def getIndex(self):
        return self.index

    def onButtonClicked(self):
        self.updateIndex()
        self.btn.setText(self.optionsList[self.index])
        if self.onValueChange is not None:
            self.onValueChange(self.index)


class AdvancedNumberWidget(DebuggableQWidget):
    def __init__(self, data: Data, name, range, default, onValueChange=None):
        super().__init__(data, 'debugAdvancedNumberWidget')
        self.data = data

        self.funcOnRelease = onValueChange
        self.name = name

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(range[0], range[1])
        self.slider.setValue(default)
        # self.slider.setSingleStep(20)
        # self.slider.setPageStep(20)
        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.slider.valueChanged.connect(self.update_value)
        if self.funcOnRelease is not None:
            self.slider.valueChanged.connect(self.funcOnRelease)

        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.result_label)

        self.update_value(self.slider.value())
        # self.show()
        self.update()

    def getValue(self):
        return self.slider.value()

    def update_value(self, value):
        self.result_label.setText(f'{self.name}: {value}')


class AsteroidMenu(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.data.asteroidMenuWidget = self

        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel('Meteor Creation Tool')
        title.setStyleSheet(getStyle(StyleType.SectionTitle))
        # title.setStyle(QStyle('SectionTitle'))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.modeSwitchButton = None
        self.modeSwitchButton = CirculatingButtonSwitch(data, ['Disabled', 'Enabled'], onValueChange=self.onAsteroidModeChange)
        self.speedWidget = AdvancedNumberWidget(data, 'Speed', (1, 400), 150, onValueChange=self.onSpeedChange)
        self.massWidget = AdvancedNumberWidget(data, 'Mass', (1, 5000), 50, onValueChange=self.onMassChange)
        self.sizeWidget = AdvancedNumberWidget(data, 'Diameter', (5, 100), 20, onValueChange=self.onSizeChange)
        launchBtn = QPushButton('Launch')

        launchBtn.clicked.connect(self.onLaunchBtnPressed)

        layout.addWidget(title)
        layout.addWidget(self.modeSwitchButton)
        layout.addWidget(self.speedWidget)
        layout.addWidget(self.massWidget)
        layout.addWidget(self.sizeWidget)
        layout.addWidget(launchBtn)

        self.update()
        self.onSpeedChange(self.speedWidget.getValue())
        self.onMassChange(self.massWidget.getValue())

    def onLaunchBtnPressed(self):
        if self.data.meteorManager is not None:
            self.data.meteorManager.launchCurMeteorAuto()

    def onSpeedChange(self, value=None):
        if value is None:
            value = self.speedWidget.getValue()
        if self.data.meteorManager is not None and self.data.meteorManager.currentMeteor is not None:
            self.data.meteorManager.currentMeteor.setSpeed(value)

    def onMassChange(self, value=None):
        if value is None:
            value = self.massWidget.getValue()
        if self.data.meteorManager is not None and self.data.meteorManager.currentMeteor is not None:
            self.data.meteorManager.currentMeteor.setMass(value)

    def onSizeChange(self, value=None):
        if value is None:
            value = self.sizeWidget.getValue()
        if self.data.meteorManager is not None and self.data.meteorManager.currentMeteor is not None:
            self.data.meteorManager.currentMeteor.setSize(value)

    def onAsteroidModeChange(self, index):
        if index == 0:
            self.data.meteorMode = False
            if self.modeSwitchButton is not None:
                self.modeSwitchButton.getButton().setProperty('feature_active', None)
                self.modeSwitchButton.getButton().style().unpolish(self.modeSwitchButton.getButton())
                self.modeSwitchButton.getButton().style().polish(self.modeSwitchButton.getButton())
        elif index == 1:
            self.data.meteorMode = True
            if self.modeSwitchButton is not None:
                self.modeSwitchButton.getButton().setProperty('feature_active', True)
                self.modeSwitchButton.getButton().style().unpolish(self.modeSwitchButton.getButton())
                self.modeSwitchButton.getButton().style().polish(self.modeSwitchButton.getButton())
        self.data.meteorManager.onMeteorModeToggled()


class SpecialControlWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        title = QLabel('Inspect')
        title.setStyleSheet(getStyle(StyleType.SectionTitle))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        debugVisualsButton = QPushButton('Data')
        debugVisualsButton.clicked.connect(self.onDebugVisualsBtnClicked)

        debugButton = QPushButton('Layout')
        debugButton.clicked.connect(self.onDebugBtnClicked)

        layout.addWidget(debugVisualsButton)
        layout.addWidget(debugButton)

    def onDebugBtnClicked(self):
        self.data.debug = not self.data.debug

    def onDebugVisualsBtnClicked(self):
        self.data.drawPlanetInfo = not self.data.drawPlanetInfo


class GeneralControlWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.pause_button = None
        self.pause_button = CirculatingButtonSwitch(data, ['Pause', 'Paused'], onValueChange=self.onPauseStateChange)
        layout.addWidget(self.pause_button)

        reset_view_button = QPushButton('Reset View')
        reset_view_button.clicked.connect(self.onResetViewButtonClicked)
        layout.addWidget(reset_view_button)

        reset_simulation_button = QPushButton('Reset Simulation')
        reset_simulation_button.clicked.connect(self.onResetSimulationButtonClicked)
        layout.addWidget(reset_simulation_button)

        visualTitle = QLabel('Visual')
        visualTitle.setStyleSheet(getStyle(StyleType.SectionTitle))
        visualTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(visualTitle)

        self.fpsWidget = AdvancedNumberWidget(data=data, name="FPS", range=(1, 240), default=144, onValueChange=self.onFpsSliderRelease)
        layout.addWidget(self.fpsWidget)

        self.timescaleWidget = AdvancedNumberWidget(data=data, name="Time Scale", range=(1, 999), default=50, onValueChange=self.onTimeScaleSliderRelease)
        layout.addWidget(self.timescaleWidget)

        sensitivityTitle = QLabel('Sensitivity')
        sensitivityTitle.setStyleSheet(getStyle(StyleType.SectionTitle))
        sensitivityTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sensitivityTitle)

        self.movementSensitivityWidget = AdvancedNumberWidget(data=data, name="Movement", range=(-5, 10), default=0, onValueChange=self.onMovementSensitivityChange)
        layout.addWidget(self.movementSensitivityWidget)

        self.scalingSensitivityWidget = AdvancedNumberWidget(data=data, name="Scaling", range=(-5, 10), default=0, onValueChange=self.onScalingSensitivityChange)
        layout.addWidget(self.scalingSensitivityWidget)

    def onPauseStateChange(self, index):
        if index == 0:
            self.data.frameUpdater.unpause()
        if index == 1:
            self.data.frameUpdater.pause()
        if self.pause_button is not None:
            self.pause_button.getButton().setProperty('feature_active', (True if self.data.frameUpdater.getPaused() else None))
            self.pause_button.getButton().style().unpolish(self.pause_button.getButton())
            self.pause_button.getButton().style().polish(self.pause_button.getButton())

    def onFpsSliderRelease(self):
        self.data.frameUpdater.change_fps(self.fpsWidget.getValue())

    def onTimeScaleSliderRelease(self):
        self.data.timeScale = self.timescaleWidget.getValue() / 50 * 3

    def onMovementSensitivityChange(self):
        self.data.mouseSensitivity = max(0, 1 + self.movementSensitivityWidget.getValue() / 5)
        # print('movement', self.data.mouseSensitivity)

    def onScalingSensitivityChange(self):
        self.data.scrollSensitivity = max(0, 1 + self.scalingSensitivityWidget.getValue() / 5)
        # print('scaling', self.data.scrollSensitivity)

    def onResetViewButtonClicked(self):
        self.data.navigation.globalPositionData.position = (0, 0)
        self.data.navigation.globalPositionData.scale = 1

    def onResetSimulationButtonClicked(self):
        self.data.simulation.resetEverything()


class LeftWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugVbox')
        self.data = data

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        topWidget = GeneralControlWidget(data)
        bottomWidget = SpecialControlWidget(data)

        layout.addWidget(topWidget)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        layout.addWidget(bottomWidget)

        topWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        bottomWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


class RightWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugVbox')
        self.data = data

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(AsteroidMenu(data))
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)


class UIWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugHBox')
        self.data = data
        self.ignoreMouse = False

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        leftWidget = LeftWidget(data)
        rightWidget = RightWidget(data)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        leftWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        rightWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        layout.addWidget(leftWidget)
        layout.addItem(spacer)
        layout.addWidget(rightWidget)

    def isPosInsideOfRect(self, pos: QPoint, rect: QRect):
        return rect.contains(pos)
        # return (rect.x() <= pos.x() <= rect.x() + rect.width() and
        #         rect.y() <= pos.y() <= rect.y() + rect.height())
