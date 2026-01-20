import pandas as pd

def generate_summary(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate revenue for each transaction
    df["revenue"] = df["price"] * df["quantity_sold"]

    rows = []
    for category, g in df.groupby("category"):
        # Identify the product with the highest sales volume in the group
        top = g.loc[g["quantity_sold"].idxmax()]

        rows.append({
            "category": category,
            "total_revenue": round(g["revenue"].sum(), 2),
            "top_product": top["product_name"],
            "top_product_quantity_sold": int(top["quantity_sold"])
        })

    # Return a structured summary table
    return pd.DataFrame(rows)