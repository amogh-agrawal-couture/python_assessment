from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import Base, engine, SessionLocal
from models import Product
from data_loader import load_csv

from routers.auth import router as auth_router
from routers.summary import router as summary_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # -------- STARTUP --------
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            load_csv(db)
    finally:
        db.close()

    yield

    # -------- SHUTDOWN --------
    # nothing to clean up


app = FastAPI(
    title="Python Assessment API",
    lifespan=lifespan,
)

# 🔥🔥🔥 THIS IS THE MISSING PART 🔥🔥🔥
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite frontend
    allow_credentials=True,                   # REQUIRED FOR COOKIES
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(summary_router)
