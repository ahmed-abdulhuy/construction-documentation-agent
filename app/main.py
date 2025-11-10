from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
import os
import sys
from app.chroma_api import router as chroma_router
from db.models import User
from db.main import initDB, getAsyncDB
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List


app = FastAPI(title="ChromaDB CRUD API")


# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],       # You can restrict this to ['GET', 'POST'] if you want
    allow_headers=["*"],
)
# app.include_router(chroma_router)

@app.on_event("startup")
async def on_startup():
    await initDB()

@app.get("/")
def readRoot():
    return {"message": "Welcome to the ChromaDB CRUD API"}

@app.post("/request/")
async def createRequest(user: User, session: AsyncSession = Depends(getAsyncDB)):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

