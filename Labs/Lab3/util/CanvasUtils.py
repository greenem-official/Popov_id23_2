import colorsys
import math

from PyQt6.QtGui import QColor, QFont, QBrush

from Labs.Lab3.Data import Data
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint


def qpointToTuple(point: QPoint):
    return (point.x(), point.y())

def tupleToQpoint(point):
    return QPoint(point[0], point[1])

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


def drawArrowPointerAt(painter: QPainter, data: Data, start_point_raw, angle_degrees, length, originalSize, color, outlineColor, outlineWidth=2, long_side_ratio=5):
    start_point_converted = data.navigation.convertPosAbstractToDisplay(start_point_raw)
    originalSize = originalSize * 1

    start_point = QPoint(int(start_point_converted[0]), int(start_point_converted[1]))

    angle_radians = math.radians(angle_degrees)

    long_side_size = originalSize
    base_side_size = originalSize * long_side_ratio

    mid_point_raw = getMovedPoint(start_point_converted, angle_radians, base_side_size, alreadyRadians=True)
    mid_point = QPoint(int(mid_point_raw[0]), int(mid_point_raw[1]))

    # mid_point = QPoint(int(start_point.x() + length * math.cos(angle_radians)),
    #                    int(start_point.y() + length * math.sin(angle_radians)))

    # print(f"start_point: {start_point.x()}, {start_point.y()}")
    # print(f"mid_point: {mid_point.x()}, {mid_point.y()}")

    # base_length = length * base_length_ratio
    angle_left = angle_radians + math.pi / 4
    angle_right = angle_radians - math.pi / 4

    # print(angle_left, angle_right)

    left_point_raw = getMovedPoint((start_point.x(), start_point.y()), angle_left, long_side_size, alreadyRadians=True)
    left_point = QPoint(int(left_point_raw[0]), int(left_point_raw[1]))

    right_point_raw = getMovedPoint((start_point.x(), start_point.y()), angle_right, long_side_size, alreadyRadians=True)
    right_point = QPoint(int(right_point_raw[0]), int(right_point_raw[1]))

    # left_point = QPoint(int(mid_point.x() + base_length / 2 * math.cos(angle_left)),
    #                     int(mid_point.y() + base_length / 2 * math.sin(angle_left)))
    # right_point = QPoint(int(mid_point.x() + base_length / 2 * math.cos(angle_right)),
    #                      int(mid_point.y() + base_length / 2 * math.sin(angle_right)))

    # print(f"left_point: {left_point.x()}, {left_point.y()}")
    # print(f"right_point: {right_point.x()}, {right_point.y()}")

    polygon = [mid_point, left_point, right_point]
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

def getMovedPoint(point, angle, distance, alreadyRadians=False):
    x, y = point

    if not alreadyRadians:
        angle_radians = math.radians(angle)
    else:
        angle_radians = angle

    dx = distance * math.cos(angle_radians)
    dy = distance * math.sin(angle_radians)

    new_x = x + dx
    new_y = y + dy

    return (new_x, new_y)

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

