import uuid
from dataclasses import dataclass

from faker import Faker

fake = Faker()

CATEGORIES = [
    "Electronics", "Home & Kitchen", "Books", "Clothing",
    "Sports & Outdoors", "Toys & Games", "Beauty", "Grocery",
]


@dataclass
class Product:
    product_id: str
    name: str
    category: str
    price: float


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    country: str


def build_product_catalog(n: int = 200) -> list[Product]:
    return [
        Product(
            product_id=str(uuid.uuid4()),
            name=fake.catch_phrase(),
            category=fake.random_element(CATEGORIES),
            price=round(fake.random_int(min=499, max=29999) / 100, 2),
        )
        for _ in range(n)
    ]


def build_customer_pool(n: int = 500) -> list[Customer]:
    return [
        Customer(
            customer_id=str(uuid.uuid4()),
            name=fake.name(),
            email=fake.email(),
            country=fake.country_code(),
        )
        for _ in range(n)
    ]
