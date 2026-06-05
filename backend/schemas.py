from datetime import date, datetime

from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=8, max_length=20)


class ClientOut(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ClientListItem(ClientOut):
    balance: float


class PurchaseCreate(BaseModel):
    client_id: int
    product: str = Field(min_length=2, max_length=120)
    value: float = Field(gt=0)
    purchase_date: date


class PurchaseOut(BaseModel):
    id: int
    client_id: int
    product: str
    value: float
    purchase_date: date
    created_at: datetime
    client_name: str


class PurchaseCreateResponse(BaseModel):
    purchase: PurchaseOut
    current_balance: float
    receipt_text: str


class DashboardOut(BaseModel):
    total_clients: int
    total_purchases: int
    total_open_amount: float
    overdue_clients: int