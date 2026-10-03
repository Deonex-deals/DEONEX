import json
from pathlib import Path

from services.common import (
    save_product,
    slugify,
    safe_float,
    calculate_discount
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANUAL_PRODUCTS_FILE = PROJECT_ROOT / "manual_products.json"


def load_manual_products():
    if not MANUAL_PRODUCTS_FILE.exists():
        print(f"Manual product file not found: {MANUAL_PRODUCTS_FILE}")
        return []

    with open(MANUAL_PRODUCTS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("manual_products.json must contain a JSON list.")

    return data


def run_manual_import():
    products = load_manual_products()

    inserted = 0
    updated = 0
    skipped = 0

    for index, item in enumerate(products, start=1):
        title = str(item.get("title", "")).strip()
        affiliate_url = str(item.get("affiliate_url", "")).strip()

        if not title or not affiliate_url:
            skipped += 1
            print(f"Skipped manual product at index {index}: title or affiliate_url missing.")
            continue

        external_id = str(
            item.get("external_id")
            or item.get("id")
            or slugify(title)
        )

        current_price = safe_float(item.get("current_price"))
        original_price = safe_float(item.get("original_price"))

        product = {
            "source": "manual",
            "external_id": external_id,
            "title": title,
            "slug": slugify(f"manual-{external_id}"),
            "description": item.get("description", ""),
            "image_url": item.get("image_url"),
            "affiliate_url": affiliate_url,
            "source_product_url": item.get("source_product_url"),
            "current_price": current_price,
            "original_price": original_price,
            "discount_percent": item.get(
                "discount_percent",
                calculate_discount(current_price, original_price)
            ),
            "rating": safe_float(item.get("rating")),
            "store_name": item.get("store_name", "Partner Store"),
            "category_name": item.get("category_name", "Other"),
            "is_featured": bool(item.get("is_featured", False))
        }

        try:
            result = save_product(product)

            if result == "inserted":
                inserted += 1
            else:
                updated += 1

        except Exception as error:
            skipped += 1
            print(f"Manual product save failed: {title} | {error}")

    print({
        "platform": "manual",
        "received": len(products),
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped
    })


if __name__ == "__main__":
    run_manual_import()