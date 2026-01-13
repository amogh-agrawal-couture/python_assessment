
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd
import os
from starlette import status
from database import get_db
from models import Product
from analysis import generate_summary
from auth import get_current_user
from schemas import SummaryRow

router = APIRouter(prefix="/summary", tags=["Summary"], dependencies=[Depends(get_current_user)])

CSV_PATH = "summary.csv"


@router.get("/", response_model=list[SummaryRow])
def get_summary(
    db: Session = Depends(get_db),
):
    df = pd.read_sql(db.query(Product).statement, db.bind)

    summary_df = generate_summary(df)

    expected_cols = {
        "category",
        "total_revenue",
        "top_product",
        "top_product_quantity_sold",
    }
    if not expected_cols.issubset(summary_df.columns):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Summary dataframe columns mismatch",
        )

    summary_df.to_csv(CSV_PATH, index=False)

    return summary_df.to_dict(orient="records")


@router.get("/download")
def download_summary(
    db: Session = Depends(get_db),
):
    if not os.path.exists(CSV_PATH):
        df = pd.read_sql(db.query(Product).statement, db.bind)
        summary_df = generate_summary(df)
        summary_df.to_csv(CSV_PATH, index=False)

    return FileResponse(
        CSV_PATH,
        media_type="text/csv",
        filename="summary.csv",
    )
