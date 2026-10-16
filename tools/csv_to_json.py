import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "manual_products.csv"
OUTPUT_FILE = PROJECT_ROOT / "manual_products.json"


def clean_text(value):
    return str(value or "").strip()


def to_float(value, default=0):
    value = clean_text(value).replace("₹", "").replace(",", "")

    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def to_bool(value):
    return clean_text(value).lower() in {
        "true",
        "yes",
        "1",
        "y"
    }


def to_variants(value):
    value = (value or "").strip()

    if not value:
        return []

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid variants JSON: {value}") from exc

    if not isinstance(parsed, list):
        raise ValueError(f"Variants must be a JSON array: {value}")

    variants = []

    for variant in parsed:
        attributes = {}

        if variant.get("color"):
            attributes["Color"] = str(variant["color"]).strip()

        if variant.get("size"):
            attributes["Size"] = str(variant["size"]).strip()

        variants.append({
            "attributes": attributes,
            "price": to_number(variant.get("price"), 0),
            "stock": to_number(variant.get("stock"), 0)
        })

    return variants

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid variants JSON: {value}"
        ) from error


def convert_csv_to_json():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {INPUT_FILE.name}"
        )

    products = []

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        required_columns = [
            "external_id",
            "title",
            "affiliate_url"
        ]

        if not reader.fieldnames:
            raise ValueError("CSV headers are missing.")

        missing_columns = [
            column
            for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                "Missing required CSV columns: "
                + ", ".join(missing_columns)
            )

        for row_number, row in enumerate(reader, start=2):
            external_id = clean_text(row.get("external_id"))
            title = clean_text(row.get("title"))
            affiliate_url = clean_text(row.get("affiliate_url"))

            if not external_id or not title or not affiliate_url:
                print(
                    f"Skipped row {row_number}: "
                    "external_id, title or affiliate_url missing."
                )
                continue

            products.append({
                "external_id": external_id,
                "title": title,
                "description": clean_text(row.get("description")),
                "image_url": clean_text(row.get("image_url")),
                "affiliate_url": affiliate_url,
                "source_product_url": clean_text(
                    row.get("source_product_url")
                ),
                "current_price": to_float(
                    row.get("current_price")
                ),
                "original_price": to_float(
                    row.get("original_price")
                ),
                "rating": to_float(row.get("rating")),
                "store_name": clean_text(
                    row.get("store_name")
                ) or "Partner Store",
                "category_name": clean_text(
                    row.get("category_name")
                ) or "Other",
                "is_featured": to_bool(
                    row.get("is_featured")
                ),
                "variants": to_variants(
                    row.get("variants")
                )
            })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            products,
            file,
            ensure_ascii=False,
            indent=2
        )

    print({
        "status": "success",
        "csv_file": INPUT_FILE.name,
        "json_file": OUTPUT_FILE.name,
        "products_converted": len(products)
    })

def to_number(value, default=0):
    if value is None or value == "":
        return default

    try:
        return float(str(value).replace(",", "").replace("₹", "").strip())
    except (TypeError, ValueError):
        return default
        variant_price = to_number(variant.get("price"), 0)

raw_variants = to_variants(row.get("variants", ""))

variants = []

for variant in raw_variants:
    attributes = {}

    if variant.get("color"):
        attributes["Color"] = str(variant["color"]).strip()

    if variant.get("size"):
        attributes["Size"] = str(variant["size"]).strip()

    if variant.get("storage"):
        attributes["Storage"] = str(variant["storage"]).strip()

    if variant.get("material"):
        attributes["Material"] = str(variant["material"]).strip()

    variants.append({
        "attributes": attributes,
        "price": to_number(variant.get("price"), 0),
        "stock": to_number(variant.get("stock"), 0)
    })

product = {
    "external_id": row["external_id"].strip(),
    "title": row["title"].strip(),
    "slug": row["slug"].strip(),
    "description": row.get("description", "").strip(),
    "image_url": row.get("image_url", "").strip(),
    "affiliate_url": row.get("affiliate_url", "").strip(),
    "source_product_url": row.get("source_product_url", "").strip(),
    "current_price": to_number(row.get("current_price"), 0),
    "original_price": to_number(row.get("original_price"), 0),
    "discount_percent": to_number(row.get("discount_percent"), 0),
    "rating": to_number(row.get("rating"), 0),
    "store_name": row.get("store_name", "").strip(),
    "is_active": row.get("is_active", "").strip().upper() == "TRUE",
    "is_featured": row.get("is_featured", "").strip().upper() == "TRUE",
    "category_id": get_category_id(row.get("category", "")),
    "variants": variants
}

if __name__ == "__main__":
    convert_csv_to_json()
