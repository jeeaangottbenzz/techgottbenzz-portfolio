from .catalog import PRODUCTS_BY_ID
from .database import Database


async def enriched_cart(db: Database, user_id: int) -> list[dict]:
    result: list[dict] = []
    for row in await db.raw_cart(user_id):
        product = PRODUCTS_BY_ID.get(row["product_id"])
        if not product:
            continue
        result.append(
            {
                "product_id": product.id,
                "name": product.name,
                "sku": product.sku,
                "price": product.price,
                "stock": product.stock,
                "placeholder": product.placeholder,
                "quantity": row["quantity"],
            }
        )
    return result

