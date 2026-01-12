# main.py
from fastapi import FastAPI
from database import Base, engine, SessionLocal
from models import Product
from data_loader import load_csv

from routers.auth import router as auth_router
from routers.summary import router as summary_router

app = FastAPI(title="Python Assessment API")

Base.metadata.create_all(engine)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    if db.query(Product).count() == 0:
        load_csv(db)
    db.close()

# 🚨 THIS is what makes signup appear
app.include_router(auth_router)
app.include_router(summary_router)
