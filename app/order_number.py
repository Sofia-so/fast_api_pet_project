from uuid import uuid4
from datetime import datetime

def generate_order_number():
    return f"ORD-{datetime.now():%Y%m%d}-{uuid4().hex[:6].upper()}"
