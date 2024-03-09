from typing import Union
from pydantic import BaseModel
from schema.customer import Customer

from schema.product import Product

class Order(BaseModel):
    id: int
    customer_id: Union[int, Customer]
    items: list[int]
    status: str = "pending"

class OrderCreate(BaseModel):
    customer_id: int
    items: list[int | Product]

orders = [
    Order(id=1, customer_id=1, items=[1, 2])
]