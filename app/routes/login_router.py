from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main import getAsyncDB 
import uuid
from sqlmodel import select, Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from datetime import timedelta
from app.core.env_settings import ENV_VARS
from app.db.models import Token
from app.utils import db_utils
from app.core import security

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/access-token")
async def login_access_token(
    session: Annotated[AsyncSession, Depends(getAsyncDB)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await db_utils.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    print("\n\nAuthenticated user:", user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ENV_VARS.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
