import random
import uuid
from datetime import datetime, timezone

from catalog import Customer, Product

# Rough funnel shape: everyone lands on the home page, most browse a few
# products, some add to cart, and a fraction of those actually check out.
SEARCH_PROBABILITY = 0.6
ADD_TO_CART_PROBABILITY = 0.35
CHECKOUT_PROBABILITY = 0.5


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_session(customer: Customer, catalog: list[Product]) -> tuple[list[dict], dict | None]:
    """Simulate one browsing session. Returns (clickstream_events, order_or_None)."""
    session_id = str(uuid.uuid4())
    events = [_clickstream_event(session_id, customer, "page_view", "home")]

    if random.random() < SEARCH_PROBABILITY:
        events.append(_clickstream_event(session_id, customer, "search", "search"))

    cart: list[tuple[Product, int]] = []
    for product in random.sample(catalog, k=random.randint(1, 5)):
        events.append(_clickstream_event(session_id, customer, "page_view", "product", product=product))
        if random.random() < ADD_TO_CART_PROBABILITY:
            qty = random.randint(1, 3)
            cart.append((product, qty))
            events.append(_clickstream_event(session_id, customer, "add_to_cart", "product", product=product))

    order = None
    if cart and random.random() < CHECKOUT_PROBABILITY:
        events.append(_clickstream_event(session_id, customer, "checkout_start", "checkout"))
        order = _order_event(customer, cart)
        events.append(_clickstream_event(session_id, customer, "purchase", "checkout", order_id=order["order_id"]))

    return events, order


def _clickstream_event(session_id, customer: Customer, event_type: str, page_type: str,
                        product: Product | None = None, order_id: str | None = None) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "session_id": session_id,
        "customer_id": customer.customer_id,
        "event_time": now_iso(),
        "event_type": event_type,
        "page_type": page_type,
        "product_id": product.product_id if product else None,
        "order_id": order_id,
    }


def _order_event(customer: Customer, cart: list[tuple[Product, int]]) -> dict:
    items = [
        {
            "product_id": product.product_id,
            "product_name": product.name,
            "category": product.category,
            "unit_price": product.price,
            "quantity": qty,
        }
        for product, qty in cart
    ]
    total = round(sum(i["unit_price"] * i["quantity"] for i in items), 2)
    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": customer.customer_id,
        "order_time": now_iso(),
        "status": "created",
        "items": items,
        "total_amount": total,
        "currency": "USD",
    }
