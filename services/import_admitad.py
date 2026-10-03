import os
import requests

from services.common import (
    save_product,
    slugify,
    safe_float,
    calculate_discount
)

ADMITAD_API_URL = os.getenv("ADMITAD_API_URL")
ADMITAD_API_KEY = os.getenv("ADMITAD_API_KEY")


def get_products_from_admitad():
    if not ADMITAD_API_URL or not ADMITAD_API_KEY:
        print("Admitad API configuration missing. Import skipped.")
        return []

    headers = {
        "Authorization": f"Bearer {ADMITAD_API_KEY}",
        "Accept": "application/json"
    }

    response = requests.get(
        ADMITAD_API_URL,
        headers=headers,
        timeout=60
    )
    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        return (
            data.get("products")
            or data.get("results")
            or data.get("data")
            or []
        )

    if isinstance(data, list):
        return data

    return []


def run_admitad_import():
    products = get_products_from_admitad()

    inserted = 0
    updated = 0
    skipped = 0

    for item in products:
        external_id = str(
            item.get("id")
            or item.get("product_id")
            or item.get("offer_id")
            or ""
        ).strip()

        affiliate_url = (
            item.get("affiliate_url")
            or item.get("deeplink")
            or item.get("tracking_link")
            or item.get("url")
        )

        title = (
            item.get("name")
            or item.get("title")
            or item.get("product_name")
        )

        if not external_id or not title or not affiliate_url:
            skipped += 1
            continue

        current_price = safe_float(
            item.get("price")
            or item.get("sale_price")
            or item.get("current_price")
        )

        original_price = safe_float(
            item.get("old_price")
            or item.get("original_price")
            or item.get("mrp")
        )

        store_name = (
            item.get("shop_name")
            or item.get("store_name")
            or item.get("merchant_name")
            or "Admitad Partner"
        )

        product = {
            "source": "admitad",
            "external_id": external_id,
            "title": title,
            "slug": slugify(f"admitad-{external_id}"),
            "description": (
                item.get("description")
                or item.get("short_description")
                or ""
            ),
            "image_url": (
                item.get("image_url")
                or item.get("image")
                or item.get("picture")
            ),
            "affiliate_url": affiliate_url,
            "source_product_url": (
                item.get("product_url")
                or item.get("url")
            ),
            "current_price": current_price,
            "original_price": original_price,
            "discount_percent": calculate_discount(
                current_price,
                original_price
            ),
            "rating": safe_float(item.get("rating")),
            "store_name": store_name,
            "category_name": (
                item.get("category")
                or item.get("category_name")
                or "Other"
            ),
            "is_featured": False
        }

        try:
            result = save_product(product)

            if result == "inserted":
                inserted += 1
            else:
                updated += 1

        except Exception as error:
            skipped += 1
            print(f"Admitad product save failed: {title} | {error}")

    print({
        "platform": "admitad",
        "received": len(products),
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped
    })


if __name__ == "__main__":
    run_admitad_import()