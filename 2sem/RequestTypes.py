from pydantic import BaseModel, EmailStr


class BinarizationRequestModel(BaseModel):
    image: str
    algorithm: str | None = None

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
