import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "manual_products.csv"
OUTPUT_FILE = PROJECT_ROOT / "manual_products.json"


def to_float(value, default=0):
    try:
        return float(str(value).strip())
    except (ValueError, TypeError):
        return default


def to_bool(value):
    def to_variants(value):
    value = clean_text(value)

    if not value:
        return []

    try:
        variants = json.loads(value)

        if not isinstance(variants, list):
            raise ValueError("Variants must be a JSON list.")

        return variants

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid variants JSON: {value}"
        ) from error
    return str(value).strip().lower() in (
        "true",
        "yes",
        "1",
        "y"
    )


def convert_csv_to_json():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"File not found: {INPUT_FILE.name}"
        )

    products = []

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = [
            "external_id",
            "title",
            "affiliate_url",
            "current_price",
            "original_price",
            "rating",
            "store_name",
            "category_name",
            "is_featured"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                "Missing columns: " + ", ".join(missing_columns)
            )

        for row_number, row in enumerate(reader, start=2):
            external_id = row["external_id"].strip()
            title = row["title"].strip()
            affiliate_url = row["affiliate_url"].strip()

            if not external_id or not title or not affiliate_url:
                print(
                    f"Skipped row {row_number}: "
                    "external_id, title, or affiliate_url is missing."
                )
                continue

            product = {
                "external_id": external_id,
                "title": title,
                "description": row.get("description", "").strip(),
                "image_url": row.get("image_url", "").strip(),
                "affiliate_url": affiliate_url,
                "source_product_url": row.get(
                    "source_product_url",
                    ""
                ).strip(),
                "current_price": to_float(row.get("current_price")),
                "original_price": to_float(row.get("original_price")),
                "rating": to_float(row.get("rating")),
               "store_name": clean_text(
                     row.get("store_name")
               ) or "Partner Store",
               "category_name": clean_text(
                    row.get("category_name")
               ) or "Other",
              "is_featured": to_bool(
                      row.get("is_featured")),
              "variants": to_variants(
                   row.get("variants")
)
            }

            products.append(product)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=2)

    print({
        "status": "success",
        "input_file": INPUT_FILE.name,
        "output_file": OUTPUT_FILE.name,
        "products_converted": len(products)
    })


if __name__ == "__main__":
    convert_csv_to_json()
