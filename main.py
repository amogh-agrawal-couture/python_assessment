from fastapi import FastAPI
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

    yield  # 👈 app runs here

    # -------- SHUTDOWN --------
    # (nothing to clean up for now)


app = FastAPI(
    title="Python Assessment API",
    lifespan=lifespan
)

# Routers
app.include_router(auth_router)
app.include_router(summary_router)
