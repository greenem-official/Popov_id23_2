from datetime import timedelta, datetime
from io import BytesIO

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, Form, File, Response
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.responses import StreamingResponse
from passlib.context import CryptContext
from jose import JWTError, jwt

import ImageOperations
from RequestTypes import BinarizationRequestModel, UserRegister, UserLogin

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# FastAPI
app = FastAPI()

# Конфигурация хешей и токенов
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["argon2", "pbkdf2_sha256"], deprecated="auto")


# БД
Base = declarative_base()

# Таблицы БД
class User(Base):
    __tablename__ = 'users'
    email = Column(String, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)


# Подключение к БД
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


# Эндпоинты

# Основной эндпоинт
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


@app.post("/auth/register")
async def register(registration_data: UserRegister):
    session = Session()

    existing_user = session.query(User).filter(User.email == registration_data.email).first()
    if existing_user:
        session.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(registration_data.password)
    db_user = User(email=registration_data.email, password_hash=hashed_password)

    session.add(db_user)
    session.commit()
    session.close()

    return {"message": "User created"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/auth/login")
async def login(login_data: UserLogin):
    session = Session()
    try:
        user = session.query(User).filter(User.email == login_data.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not pwd_context.verify(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_email": user.email
        }
    finally:
        session.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)
