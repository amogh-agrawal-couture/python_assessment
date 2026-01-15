# data_loader.py

import pandas as pd
from sqlalchemy.orm import Session
from models import Product  # your SQLAlchemy model


def clean_products_csv(path="products_raw.csv") -> pd.DataFrame:
    """
    Reads the raw CSV, cleans it, and returns a DataFrame ready for DB insertion.
    """
    df = pd.read_csv(path)

    # Force numeric columns
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce")

    # Fill missing numeric values
    df["price"].fillna(df["price"].median(), inplace=True)
    df["quantity_sold"].fillna(df["quantity_sold"].median(), inplace=True)
    df["rating"] = df["rating"].fillna(df.groupby("category")["rating"].transform("mean"))
    df["review_count"].fillna(0, inplace=True)
    df["product_id"].ffill(inplace=True)

    # Drop any remaining NaNs
    df = df.dropna()

    # Convert to correct types for SQL
    df["quantity_sold"] = df["quantity_sold"].astype(int)
    df["review_count"] = df["review_count"].astype(int)
    df["product_id"] = df["product_id"].astype(int)

    # Optional: save cleaned CSV
    df.to_csv("products_clean.csv", index=False)

    return df


def load_csv(db: Session, path="products_raw.csv"):
    """
    Cleans the CSV and loads data into the database.
    """
    df = clean_products_csv(path)

    products = []
    for _, row in df.iterrows():
        product = Product(
            product_id=row["product_id"],
            product_name=row["product_name"],
            category=row["category"],
            price=row["price"],
            quantity_sold=row["quantity_sold"],
            rating=row["rating"],
            review_count=row["review_count"],
        )
        products.append(product)

    # Bulk insert
    db.bulk_save_objects(products)
    db.commit()
    print(f"Loaded {len(products)} products into the database.")
