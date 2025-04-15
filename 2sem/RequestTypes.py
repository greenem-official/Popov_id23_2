from pydantic import BaseModel

class BinarizationRequestModel(BaseModel):
    image: str
    algorithm: str | None = None
