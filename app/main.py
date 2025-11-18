from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jwt import InvalidTokenError
from pwdlib import PasswordHash
import jwt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.routes import login_router, wir_router, user_router
from app.routes.chroma_api import router as chroma_router
from app.routes.discipline_router import disciplineRouter as discipline
from app.db.main import initDB
from app.db import models
from app.core.env_settings import ENV_VARS
app = FastAPI(title="ChromaDB CRUD API")

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],       # You can restrict this to ['GET', 'POST'] if you want
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await initDB()


# app.include_router(chroma_router)
app.include_router(wir_router.wirRouter)
app.include_router(discipline)
app.include_router(login_router.router)
app.include_router(user_router.router)


class Token(BaseModel):
    accessToken: str
    tokenType: str

class TokenDate(BaseModel):
    username: str | None = None


oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")
passwordHash = PasswordHash.recommended()


def fakePasswordHasher(password: str):
    return "fakeHashed" + password


class TestUser(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None


class TestUserInDB(TestUser):
    hashedPassword: str


def verifyPassword(plainPassword, hashedPassword):
    return passwordHash.verify(plainPassword, hashedPassword)


def getPasswordHashed(password):
    return passwordHash.hash(password)


def getTestUser(db, username: str):
    if username in db:
        userDict = db[username]
        return TestUserInDB(**userDict)


def authenticateUser(fakeDB, username: str, password: str):
    user = getTestUser(fakeDB, username)
    if not user:
        return False
    if not verifyPassword(password, user.hashedPassword):
        return False
    return user


def createAccessToken(data: dict, expiresDelta: timedelta | None = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.now(timezone.utc) + expiresDelta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    toEncode.update({"exp": expire})
    encodeJWT = jwt.encode(toEncode, ENV_VARS.SECRET_KEY, algorithm=ENV_VARS.ALGORITHM)
    return encodeJWT


def getCurrentUser(token: Annotated[str, Depends(oauth2Scheme)]):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, ENV_VARS.SECRET_KEY, algorithms=[ENV_VARS.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentialsException
        tokenDate = TokenDate(username=username)
    except InvalidTokenError:
        raise credentialsException
    user = getTestUser(fakeUsersDB, username=tokenDate.username)
    if user is None:
        raise credentialsException
    return user


def getCurrentActiveUser(currentUser: Annotated[TestUser, Depends(getCurrentUser)]):
    if currentUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return currentUser


@app.post("/token")
async def login(formData: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticateUser(fakeUsersDB, formData.username, formData.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    accessTokenExpires = timedelta(minutes=ENV_VARS.ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(
        data={"sub": user.username}, expiresDelta=accessTokenExpires
    )
    return Token(accessToken=accessToken, tokenType="Bearer")


@app.get("/auth/me")
async def readUserMe(currentUser: Annotated[TestUser, Depends(getCurrentActiveUser)]):
    return currentUser


@app.get("/auth/me/items")
async def readOwnItems(currentUser: Annotated[TestUser, Depends(getCurrentActiveUser)]):
    return [{"item_id": "foo", "owner": currentUser.username}]