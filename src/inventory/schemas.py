from ninja import Schema
from decimal import Decimal
from typing import Optional


class MaterialOut(Schema): # displaying, method GET
    id: int
    name: str
    unit_price: Decimal
    unit: str
    quantity: Decimal


class MaterialIn(Schema): # writing, method POST
    name: str
    unit_price: Decimal
    unit: str
    quantity: Decimal


class ChangeMaterial(Schema): # partial changing, uses for PATCH
    name: Optional[str] = None
    unit_price: Optional[Decimal] = None
    unit: Optional[str] = None
    quantity: Optional[Decimal] = None