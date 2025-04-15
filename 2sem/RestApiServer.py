import base64
from io import BytesIO

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, Form, File, Response
from starlette.responses import StreamingResponse

import ImageOperations
from RequestTypes import BinarizationRequestModel

app = FastAPI()

@app.post("/binary_image")
async def binary_image(
    image: UploadFile = File(...),
    algorithm: str = Form("bradley_roth")
):
    try:
        contents = await image.read()

        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        output = ImageOperations.process_image(
            img,
            algorithm
        )

        if output is None:
            raise HTTPException(
                status_code=400,
                detail="Algorithm not supported"
            )

        return StreamingResponse(
            BytesIO(output),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=binarized_image.png"}
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)
