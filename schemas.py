from pydantic import BaseModel


# ---------- AUTH ----------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class MessageResponse(BaseModel):
    message: str


# ---------- SUMMARY ----------

class SummaryRow(BaseModel):
    category: str
    total_revenue: float
    top_product: str
    top_product_quantity_sold: int
