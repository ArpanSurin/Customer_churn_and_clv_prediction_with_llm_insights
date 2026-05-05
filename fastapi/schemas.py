from datetime import date
from pydantic import BaseModel

class CustomerInput(BaseModel):
    customer_id: str
    age: int
    gender: str
    city: str
    customer_segment: str
    total_orders: int
    lifetime_spend: float
    total_returns: int
    avg_rating: float
    registration_date: date
    last_order_date: date
    total_ratings: int = 0
    email_available: int = 1
    phone_available: int = 1
    avg_discount_pct: float = 0.0
    avg_delivery_days: float = 0.0
    spend_per_order: float = 0.0
    avg_order_value: float = 0.0