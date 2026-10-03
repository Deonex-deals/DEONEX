import os
import requests

from services.common import (
    save_product,
    slugify,
    safe_float,
    calculate_discount
)

CUELINKS_API_URL = os.getenv("CUELINKS_API_URL")
CUELINKS_API_KEY = os.getenv("CUELINKS_API_KEY")


def run_cuelinks_import():
    if not CUELINKS_API_URL or not CUELINKS_API_KEY:
        print("Cuelinks API configuration missing.")
        return

    headers = {
        "Authorization": f"Bearer {CUELINKS_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        CUELINKS_API_URL,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    products = data.get("products", [])

    inserted = 0
    updated = 0

    for item in products:
        external_id = str(item.get("id"))

        if not external_id or not item.get("affiliate_link"):
            continue

        current_price = safe_float(item.get("price"))
        original_price = safe_float(item.get("original_price"))

        product = {
            "source": "cuelinks",
            "external_id": external_id,
            "title": item.get("product_name", "Cuelinks Product"),
            "slug": slugify(f"cuelinks-{external_id}"),
            "description": item.get("description", ""),
            "image_url": item.get("image_url"),
            "affiliate_url": item.get("affiliate_link"),
            "source_product_url": item.get("product_url"),
            "current_price": current_price,
            "original_price": original_price,
            "discount_percent": calculate_discount(
                current_price,
                original_price
            ),
            "rating": safe_float(item.get("rating")),
            "store_name": item.get("store_name", "Cuelinks Partner"),
            "category_name": item.get("category", "Other")
        }

        result = save_product(product)

        if result == "inserted":
            inserted += 1
        else:
            updated += 1

    print({
        "platform": "cuelinks",
        "inserted": inserted,
        "updated": updated
    })


if __name__ == "__main__":
    run_cuelinks_import()