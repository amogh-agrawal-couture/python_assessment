from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd
import os
from starlette import status
from database import get_db
from models.models import Product
from analysis import generate_summary
from utils.auth import get_current_user
from schemas.schemas import SummaryRow

router = APIRouter(prefix="/summary", tags=["Summary"], dependencies=[Depends(get_current_user)])

CSV_PATH = "summary.csv"
EXPECTED_COLS = {"category", "total_revenue", "top_product", "top_product_quantity_sold"}

def _ensure_summary(db: Session) -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            if not df.empty and EXPECTED_COLS.issubset(df.columns):
                return df
        except Exception:
            pass

    products_df = pd.read_sql(db.query(Product).statement, db.bind)
    summary_df = generate_summary(products_df)

    if not EXPECTED_COLS.issubset(summary_df.columns):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid summary columns")

    summary_df.to_csv(CSV_PATH, index=False)
    return summary_df

@router.get("/", response_model=list[SummaryRow])
def get_summary(db: Session = Depends(get_db)):
    return _ensure_summary(db).to_dict(orient="records")


@router.get("/download")
def download_summary(db: Session = Depends(get_db)):
    _ensure_summary(db)
    return FileResponse(CSV_PATH, media_type="text/csv", filename="summary.csv")