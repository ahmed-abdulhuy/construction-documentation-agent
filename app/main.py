from app.routes import login_router, wir_router, user_router, chroma_api, discipline_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.main import initDB
from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
app = FastAPI(title="Kemit", version="0.1.0")

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


# app.include_router(chroma_api.router)
app.include_router(wir_router.wirRouter)
app.include_router(discipline_router.router)
app.include_router(login_router.router)
app.include_router(user_router.router)