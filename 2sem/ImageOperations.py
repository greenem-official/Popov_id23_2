import io
import time

import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from BinarizationAlgorythms import *


def image_to_base64(image_path):
    image = Image.open(image_path)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str

def base64_to_image(base64_str):
    image_data = base64.b64decode(base64_str)
    np_array = np.frombuffer(image_data, np.uint8)

    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image

def binarize(image):
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    return binary

def process_image(image, algorythm: str):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # binary = binarize(gray)

    if algorythm == 'otsu':
        binary = otsu_binarization(image)
    elif algorythm == 'bradley_roth':
        binary = bradley_roth_binarization(image, window_size=25, k=0.1)
    else:
        return None

    _, buffer = cv2.imencode(".png", binary)
    bytes_img = buffer.tobytes()

    return bytes_img


if __name__ == "__main__":
    pass
    # input_enc = image_to_base64("client/images/image.jpg")
    #
    # start = time.perf_counter()
    # output_enc = process_image_from_base64(input_enc, "otsu")
    # end = time.perf_counter()
    # print(f"Время выполнения: {end - start:.6f} секунд")
    #
    # img = Image.open(io.BytesIO(base64.decodebytes(bytes(output_enc, "utf-8"))))
    # img.save("client/images/debug_result.png")
