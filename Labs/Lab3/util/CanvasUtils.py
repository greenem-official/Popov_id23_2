import colorsys

from PyQt6.QtGui import QColor, QFont

from Labs.Lab3.Data import Data
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt


def drawSphereAt(painter: QPainter, data: Data, raw_pos, radius, fill_color, outline_color=None, outline_width=2):
    point1 = data.navigation.convertPosAbstractToDisplay((raw_pos[0] - radius, raw_pos[1] - radius))
    point2 = data.navigation.convertPosAbstractToDisplay((raw_pos[0] + radius, raw_pos[1] + radius))

    painter.setBrush(fill_color)

    if outline_color is None:
        painter.setPen(Qt.PenStyle.NoPen)
    else:
        painter.setPen(QPen(outline_color, outline_width))

    painter.drawEllipse(int(point1[0]), int(point1[1]), int(point2[0] - point1[0]), int(point2[1] - point1[1]))

def drawTextAt(painter: QPainter, data: Data, raw_pos, text, color=None, outline_width=2, font_size=14, outline=False, outline_color=None):
    if outline and outline_color is not None:
        drawTextAt(painter=painter, data=data, raw_pos=raw_pos, text=text, color=outline_color, outline_width=outline_width + 30, font_size=font_size, outline=False, outline_color=None)

    pos = data.navigation.convertPosAbstractToDisplay(raw_pos)

    if color is None:
        painter.setPen(Qt.PenStyle.NoPen)
    else:
        painter.setPen(QPen(color, outline_width))

    font = QFont()
    font.setPixelSize(font_size)
    painter.setFont(font)

    lines = text.splitlines()
    total_height = 0

    for line in lines:
        metrics = painter.fontMetrics()
        total_height += metrics.boundingRect(line).height()

    y_offset = -total_height / 2

    for line in lines:
        metrics = painter.fontMetrics()
        text_rect = metrics.boundingRect(line)
        x = pos[0] - text_rect.width() / 2
        y = pos[1] + metrics.ascent() / 2 - metrics.descent() + y_offset  # pos[1] + metrics.ascent() / 2 - metrics.descent() /2 + y_offset

        painter.drawText(int(x), int(y), int(text_rect.width()), int(text_rect.height()), Qt.AlignmentFlag.AlignCenter, line)
        y_offset += text_rect.height()

def drawLineAt(painter: QPainter, data: Data, point1_raw, point2_raw, color, width=2):
    point1 = data.navigation.convertPosAbstractToDisplay(point1_raw)
    point2 = data.navigation.convertPosAbstractToDisplay(point2_raw)

    painter.setPen(QPen(color, width, Qt.PenStyle.SolidLine))  # , Qt.PenStyle.RoundCap, Qt.PenStyle.RoundJoin

    painter.drawLine(int(point1[0]), int(point1[1]), int(point2[0]), int(point2[1]))
    # painter.drawLine((int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])))

def lerp(a, b, t):
    return a + (b - a) * t

def interpolate_color(value, min_value, max_value, saturation=55, brightness=80):
    if value < min_value:
        value = min_value
    elif value > max_value:
        value = max_value

    # Scaling value to [0, 1]
    normalized_value = (value - min_value) / (max_value - min_value)

    start_hue = 125
    end_hue = 180

    #  Green (125/360) in the beginning, goes through red (0) and to blue (180/360)
    hue = start_hue / 360 - normalized_value * (start_hue + end_hue) / 360
    hue = (hue + 1) % 1  # negative hue

    rgb = colorsys.hsv_to_rgb(hue, saturation / 100, brightness / 100)
    return QColor.fromRgbF(rgb[0], rgb[1], rgb[2])
    # return QColor.fromHslF(hue, saturation / 100, brightness / 100)

