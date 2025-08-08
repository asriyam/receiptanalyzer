from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ReceiptItem(BaseModel):
    name: str = Field(description="Name or description of the purchased item")
    quantity: int = Field(description="Number of items purchased", ge=1)
    unit_price: float = Field(description="Price per individual item", ge=0)
    total_price: float = Field(description="Total price for this line item (quantity × unit_price)", ge=0)

class ReceiptData(BaseModel):
    merchant_name: str = Field(description="Name of the store or merchant")
    merchant_address: Optional[str] = Field(None, description="Physical address of the merchant if visible")
    date: str = Field(description="Receipt date in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Receipt time in HH:MM format if visible")
    items: list[ReceiptItem] = Field(description="List of all purchased items with their details")
    subtotal: float = Field(description="Subtotal before tax", ge=0)
    tax_amount: float = Field(description="Total tax amount charged", ge=0)
    tax_rate: Optional[float] = Field(None, description="Tax rate as percentage (e.g., 8.5 for 8.5%)", ge=0, le=100)
    total_amount: float = Field(description="Final total amount paid", ge=0)
    payment_method: Optional[str] = Field(None, description="Payment method used (e.g., CASH, CARD, CREDIT, DEBIT)")
    receipt_number: Optional[str] = Field(None, description="Receipt or transaction number if visible")