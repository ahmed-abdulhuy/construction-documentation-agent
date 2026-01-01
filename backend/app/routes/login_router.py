from fastapi import APIRouter, Depends, Response, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main import getAsyncDB 
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from datetime import timedelta
from app.core.env_settings import ENV_VARS
from app.utils import db_utils
from app.core import security

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/access-token")
async def login_access_token(
    response: Response,
    session: Annotated[AsyncSession, Depends(getAsyncDB)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await db_utils.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Create access token
    access_expires = timedelta(minutes=ENV_VARS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(user.id, expires_delta=access_expires)

    # # Create refresh token
    # refresh_expires = timedelta(days=ENV_VARS.REFRESH_TOKEN_EXPIRE_DAYS)
    # refresh_token = security.create_refresh_token(user.id, expires_delta=refresh_expires)
    
    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,     # set to False for local development if needed
        samesite="lax",
        max_age=access_expires.seconds,
        path="/",
    )

    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=refresh_expires.seconds,
    #     path="/",
    # )


    return {"message": "Login successful"}
