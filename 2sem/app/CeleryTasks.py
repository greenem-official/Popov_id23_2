from fastapi import HTTPException

import ImageOperations
from celery_app import app
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

@app.task
def process_image_async(contents, algorithm):
    try:
        logger.info(f"Starting task")

        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {"error": "Failed to decode image"}
        logger.info('img fine')

        output = ImageOperations.process_image(
            img,
            algorithm
        )

        if output is None:
            return {"error": "Algorithm not supported"}

        logger.info(f"Encoding task")
        # _, buf = cv2.imencode('.png', output)
        return {
            "status": "success",
            "image_data": output.hex()  # buf.tobytes()
        }
    except Exception as e:
        return {"error": str(e)}
