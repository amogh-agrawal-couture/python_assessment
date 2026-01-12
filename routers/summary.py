from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd

from database import get_db
from models import Product
from analysis import generate_summary
from auth import get_current_user

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)


@router.get("/")
def get_summary(
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    df = pd.read_sql(db.query(Product).statement, db.bind)
    summary_df = generate_summary(df)
    summary_df.to_csv("summary.csv", index=False)

    return summary_df.to_dict(orient="records")


@router.get("/download")
def download_summary(
    user: str = Depends(get_current_user)
):
    return FileResponse(
        "summary.csv",
        media_type="text/csv",
        filename="summary.csv"
    )
