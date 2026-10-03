import os
import requests

from services.common import (
    save_product,
    slugify,
    safe_float,
    calculate_discount
)

FLIPKART_API_URL = os.getenv("FLIPKART_API_URL")
FLIPKART_API_KEY = os.getenv("FLIPKART_API_KEY")


def run_flipkart_import():
    if not FLIPKART_API_URL or not FLIPKART_API_KEY:
        print("Flipkart API configuration missing.")
        return

    headers = {
        "Authorization": f"Bearer {FLIPKART_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        FLIPKART_API_URL,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    products = data.get("products", [])

    inserted = 0
    updated = 0

    for item in products:
        external_id = str(item.get("product_id"))

        if not external_id or not item.get("affiliate_url"):
            continue

        current_price = safe_float(item.get("selling_price"))
        original_price = safe_float(item.get("mrp"))

        product = {
            "source": "flipkart",
            "external_id": external_id,
            "title": item.get("title", "Flipkart Product"),
            "slug": slugify(f"flipkart-{external_id}"),
            "description": item.get("description", ""),
            "image_url": item.get("image_url"),
            "affiliate_url": item.get("affiliate_url"),
            "source_product_url": item.get("product_url"),
            "current_price": current_price,
            "original_price": original_price,
            "discount_percent": calculate_discount(
                current_price,
                original_price
            ),
            "rating": safe_float(item.get("rating")),
            "store_name": "Flipkart",
            "category_name": item.get("category", "Other")
        }

        result = save_product(product)

        if result == "inserted":
            inserted += 1
        else:
            updated += 1

    print({
        "platform": "flipkart",
        "inserted": inserted,
        "updated": updated
    })


if __name__ == "__main__":
    run_flipkart_import()