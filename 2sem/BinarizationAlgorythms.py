import cv2
import numpy as np

def __grayscale_image(image):
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    return gray

def otsu_binarization(image):
    gray = __grayscale_image(image)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary

def bradley_roth_binarization(image, window_size=15, k=0.15):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    integral = cv2.integral(gray)
    h, w = gray.shape

    half_window = window_size // 2

    binary = np.zeros((h, w), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            y1 = max(0, y - half_window)
            x1 = max(0, x - half_window)
            y2 = min(h, y + half_window + 1)
            x2 = min(w, x + half_window + 1)

            # Суммарная яркость прямоугольника окна
            area = integral[y2, x2] - integral[y1, x2] - integral[y2, x1] + integral[y1, x1]
            # Соотношение этой яркости на число пикселей там, т.е. средняя яркость на пиксель (* обратное k)
            threshold = area / ((y2 - y1) * (x2 - x1)) * (1 - k)

            if gray[y, x] >= threshold:
                binary[y, x] = 255

    return binary
