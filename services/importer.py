import os
import requests

from services.common import (
    save_product,
    slugify,
    safe_float,
    calculate_discount
)

AMAZON_API_URL = os.getenv("AMAZON_API_URL")
AMAZON_API_KEY = os.getenv("AMAZON_API_KEY")


def run_amazon_import():
    if not AMAZON_API_URL or not AMAZON_API_KEY:
        print("Amazon API configuration missing.")
        return

    headers = {
        "Authorization": f"Bearer {AMAZON_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        AMAZON_API_URL,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    products = data.get("products", [])

    inserted = 0
    updated = 0

    for item in products:
        external_id = str(item.get("asin") or item.get("id"))

        if not external_id or not item.get("affiliate_url"):
            continue

        current_price = safe_float(item.get("price"))
        original_price = safe_float(item.get("mrp"))

        product = {
            "source": "amazon",
            "external_id": external_id,
            "title": item.get("title", "Amazon Product"),
            "slug": slugify(f"amazon-{external_id}"),
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
            "store_name": "Amazon",
            "category_name": item.get("category", "Electronics")
        }

        result = save_product(product)

        if result == "inserted":
            inserted += 1
        else:
            updated += 1

    print({
        "platform": "amazon",
        "inserted": inserted,
        "updated": updated
    })


if __name__ == "__main__":
    run_amazon_import()