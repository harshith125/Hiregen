from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    print("Database connection established and Beanie initialized.")
    yield
    # Shutdown logic (if any) can be placed here

app = FastAPI(
    title="HIREGEN API",
    description="Backend API for HIREGEN placement and internship analysis",
    version="0.1.0",
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as necessary for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import placement, analytics, community, learning, chat
app.include_router(placement.router, prefix="/api/records", tags=["Placement Records"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(community.router, prefix="/api/community", tags=["Community"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chatbot"])

@app.get("/")
async def root():
    return {"message": "Welcome to HIREGEN API - Phase 1 Backend Initialization"}
