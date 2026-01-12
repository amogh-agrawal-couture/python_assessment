from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from models import Product
from data_loader import load_csv

from routers.auth import router as auth_router
from routers.summary import router as summary_router

app = FastAPI(title="Python Assessment API")

# ✅ CORS (REQUIRED for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Load CSV on startup
@app.on_event("startup")
def startup():
    db = SessionLocal()
    if db.query(Product).count() == 0:
        load_csv(db)
    db.close()

# ✅ Routers
app.include_router(auth_router)
app.include_router(summary_router)
