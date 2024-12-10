import colorsys
import math

from PyQt6.QtGui import QColor, QFont, QBrush
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint

from Data import Data


def qpointToTuple(point: QPoint):
    return (point.x(), point.y())

def tupleToQpoint(point):
    return QPoint(int(point[0]), int(point[1]))

def drawSphereAt(painter: QPainter, data: Data, raw_pos, radius, fill_color, outline_color=None, outline_width=2, displaySpaceAlready=False):
    if not displaySpaceAlready:
        point1 = data.navigation.convertPosAbstractToDisplay((raw_pos[0] - radius, raw_pos[1] - radius))
        point2 = data.navigation.convertPosAbstractToDisplay((raw_pos[0] + radius, raw_pos[1] + radius))
    else:
        point1 = (raw_pos[0] - radius, raw_pos[1] - radius)
        point2 = (raw_pos[0] + radius, raw_pos[1] + radius)

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


def drawArrowPointerAt(painter: QPainter, data: Data, start_point_raw, angle_degrees, originalSize, originalSpeed, color, outlineColor, outlineWidth=2):
    start_point_converted = data.navigation.convertPosAbstractToDisplay(start_point_raw)
    originalSize = data.navigation.convertDistanceAbstractToDisplay(originalSize * 1)

    angle = math.radians(angle_degrees)
    angle_perpendicular = angle + math.pi / 2

    offset_distance = math.pow(originalSize, 0.9)
    base_side_size = originalSize
    long_side_size = originalSize * math.sqrt(originalSpeed / 10)

    mid_point_raw = offsetPoint(start_point_converted, angle, offset_distance, alreadyRadians=True)

    side_point_1 = offsetPoint(mid_point_raw, angle_perpendicular, base_side_size / 2, alreadyRadians=True)
    side_point_2 = offsetPoint(mid_point_raw, angle_perpendicular, - base_side_size / 2, alreadyRadians=True)
    last_point = offsetPoint(mid_point_raw, angle, long_side_size, alreadyRadians=True)

    polygon = [tupleToQpoint(side_point_1), tupleToQpoint(side_point_2), tupleToQpoint(last_point)]
    painter.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))
    painter.setPen(QPen(outlineColor, outlineWidth))
    painter.drawPolygon(polygon)

    # drawSphereAt(painter, data, data.navigation.convertPosDisplayToAbstract(qpointToTuple(left_point)), radius=10,
    #              fill_color=QColor(255, 0, 0))
    # drawSphereAt(painter, data, data.navigation.convertPosDisplayToAbstract(qpointToTuple(right_point)), radius=10,
    #              fill_color=QColor(255, 0, 0))
    # drawSphereAt(painter, data, data.navigation.convertPosDisplayToAbstract(qpointToTuple(mid_point)), radius=10,
    #              fill_color=QColor(255, 0, 0))

def drawLineAt(painter: QPainter, data: Data, point1_raw, point2_raw, color, width=2):
    point1 = data.navigation.convertPosAbstractToDisplay(point1_raw)
    point2 = data.navigation.convertPosAbstractToDisplay(point2_raw)

    painter.setPen(QPen(color, width, Qt.PenStyle.SolidLine))  # , Qt.PenStyle.RoundCap, Qt.PenStyle.RoundJoin

    painter.drawLine(int(point1[0]), int(point1[1]), int(point2[0]), int(point2[1]))
    # painter.drawLine((int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])))

def offsetPoint(point, angle, distance, alreadyRadians=False):
    x, y = 0, 0
    if isinstance(point, tuple) or isinstance(point, list):
        x, y = point
    elif isinstance(point, QPoint):
        x = point.x()
        y = point.y()

    if not alreadyRadians:
        angle_radians = math.radians(angle)
    else:
        angle_radians = angle

    dx = distance * math.cos(angle_radians)
    dy = distance * math.sin(angle_radians)

    new_x = x + dx
    new_y = y + dy

    if isinstance(point, tuple) or isinstance(point, list):
        return (new_x, new_y)
    elif isinstance(point, QPoint):
        return QPoint(int(new_x), int(new_y))  # loses precision!!!

def lerp(a, b, t):
    return a + (b - a) * t

def interpolate_color_saturation(value, min_value, max_value, hue=0, brightness=80):
    normalized_value = (value - min_value) / (max_value - min_value)

    rgb = colorsys.hsv_to_rgb(hue, normalized_value, brightness / 100)
    return QColor.fromRgbF(rgb[0], rgb[1], rgb[2])

def interpolate_color(value, min_value, max_value, saturation=55, brightness=80, justSaturationMode=False):
    if value < min_value:
        value = min_value
    elif value > max_value:
        value = max_value

    if justSaturationMode:
        return interpolate_color_saturation(value=value, min_value=min_value, max_value=max_value, brightness=brightness)

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

