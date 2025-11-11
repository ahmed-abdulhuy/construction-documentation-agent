from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
import sys
from routes.chroma_api import router as chroma_router
from routes.wir_router import wirRouter as wir
from routes.discipline_router import disciplineRouter as discipline
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.main import initDB
from db import models
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
app.include_router(wir)
app.include_router(discipline)