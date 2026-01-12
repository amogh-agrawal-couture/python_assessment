# routers/summary.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd
import os

from database import get_db
from models import Product
from analysis import generate_summary
from auth import get_current_user
from schemas import SummaryRow

router = APIRouter(prefix="/summary", tags=["Summary"])

CSV_PATH = "summary.csv"


@router.get("/", response_model=list[SummaryRow])
def get_summary(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    df = pd.read_sql(db.query(Product).statement, db.bind)

    summary_df = generate_summary(df)

    # Ensure correct column names
    expected_cols = {
        "category",
        "total_revenue",
        "top_product",
        "top_product_quantity_sold",
    }
    if not expected_cols.issubset(summary_df.columns):
        raise HTTPException(
            status_code=500,
            detail="Summary dataframe columns mismatch",
        )

    summary_df.to_csv(CSV_PATH, index=False)

    return summary_df.to_dict(orient="records")


@router.get("/download")
def download_summary(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Regenerate CSV if missing
    if not os.path.exists(CSV_PATH):
        df = pd.read_sql(db.query(Product).statement, db.bind)
        summary_df = generate_summary(df)
        summary_df.to_csv(CSV_PATH, index=False)

    return FileResponse(
        CSV_PATH,
        media_type="text/csv",
        filename="summary.csv",
    )
