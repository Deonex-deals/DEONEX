"""
Convert products.csv to products.json and upsert products to Supabase.

Expected CSV location:
products.csv  (repository root)

Expected CSV columns:
external_id,title,slug,description,image_url,affiliate_url,
source_product_url,current_price,original_price,discount_percent,
rating,store_name,is_active,is_featured,category,variants
"""

import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv

try:
    from supabase import create_client
except ImportError:
    create_client = None


BASE_DIR = Path(__file__).resolve().parents[1]

CSV_PATH = BASE_DIR / "products.csv"
JSON_PATH = BASE_DIR / "products.json"

load_dotenv(BASE_DIR / ".env")

SUPABASE_URL = (
    os.getenv("SUPABASE_URL")
    or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    or ""
).strip()

SUPABASE_SECRET_KEY = (
    os.getenv("SUPABASE_SECRET_KEY")
    or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    or ""
).strip()

SUPABASE_ANON_KEY = (
    os.getenv("SUPABASE_ANON_KEY")
    or os.getenv("SUPABASE_PUBLISHABLE_KEY")
    or ""
).strip()

supabase = None

if SUPABASE_URL and SUPABASE_SECRET_KEY and create_client:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)
        print("Supabase client connected successfully.")
    except Exception as error:
        print(f"Warning: Could not create Supabase client: {error}")
else:
    print("Supabase credentials not found. Database upsert will be skipped.")
    print(
        "Required environment variables: "
        "SUPABASE_URL and SUPABASE_SECRET_KEY"
    )


def to_number(value, default=0):
    """Convert '1,311', '₹368' or 368 into a number."""
    if value is None or value == "":
        return default

    try:
        number = float(
            str(value)
            .replace(",", "")
            .replace("₹", "")
            .replace("Rs.", "")
            .replace("Rs", "")
            .strip()
        )

        return int(number) if number.is_integer() else number
    except (TypeError, ValueError):
        return default


def to_boolean(value, default=False):
    """Convert TRUE/FALSE/true/false/1/0 into a boolean."""
    if value is None or value == "":
        return default

    return str(value).strip().lower() in ("true", "1", "yes", "y")


def make_slug(value):
    """Create a simple URL-friendly slug."""
    value = (value or "").strip().lower()

    replacements = {
        "&": "and",
        "/": "-",
        ",": "-",
        ".": "-",
        "(": "",
        ")": "",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = "-".join(value.split())

    return value or "other"


def normalize_variant(variant):
    """
    Normalize old and new variant formats.

    Old:
    {"color":"Black","size":"S","price":368}

    New:
    {"attributes":{"Color":"Black","Size":"S"},"price":368,"stock":10}
    """
    if not isinstance(variant, dict):
        return {
            "attributes": {},
            "price": 0,
            "stock": 0,
        }

    attributes = variant.get("attributes")

    if not isinstance(attributes, dict):
        attributes = {}

        if variant.get("color"):
            attributes["Color"] = str(variant["color"]).strip()

        if variant.get("size"):
            attributes["Size"] = str(variant["size"]).strip()

        if variant.get("storage"):
            attributes["Storage"] = str(variant["storage"]).strip()

        if variant.get("material"):
            attributes["Material"] = str(variant["material"]).strip()

        if variant.get("capacity"):
            attributes["Capacity"] = str(variant["capacity"]).strip()

    clean_attributes = {}

    for attribute_name, attribute_value in attributes.items():
        if attribute_value is None:
            continue

        attribute_value = str(attribute_value).strip()

        if attribute_value:
            clean_attributes[str(attribute_name).strip()] = attribute_value

    return {
        "attributes": clean_attributes,
        "price": to_number(variant.get("price"), 0),
        "stock": to_number(variant.get("stock"), 0),
    }


def to_variants(value):
    """Parse and normalize variants JSON from CSV."""
    value = (value or "").strip()

    if not value:
        return []

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid variants JSON: {value}. "
            'Use numeric price, for example {"price":1311}, '
            'not {"price":1,311}.'
        ) from error

    if not isinstance(parsed, list):
        raise ValueError(f"Variants must be a JSON array: {value}")

    return [normalize_variant(variant) for variant in parsed]


def get_or_create_category(category_name):
    """
    Find a category by name or slug.
    If it does not exist, create it automatically and return its ID.
    """
    category_name = (category_name or "Other").strip()

    if not category_name:
        category_name = "Other"

    if not supabase:
        raise ValueError(
            "Supabase client is not configured, so category cannot be created."
        )

    slug = make_slug(category_name)

    # 1. Search by exact/case-insensitive name
    response = (
        supabase
        .table("categories")
        .select("id,name,slug")
        .ilike("name", category_name)
        .limit(1)
        .execute()
    )

    if response.data:
        category = response.data[0]
        print(
            f"Category found by name: {category['name']} "
            f"(ID: {category['id']})"
        )
        return category["id"]

    # 2. Search by slug
    response = (
        supabase
        .table("categories")
        .select("id,name,slug")
        .eq("slug", slug)
        .limit(1)
        .execute()
    )

    if response.data:
        category = response.data[0]
        print(
            f"Category found by slug: {category['name']} "
            f"(ID: {category['id']})"
        )
        return category["id"]

    # 3. Try to create the missing category
    print(f"Category not found. Creating category: {category_name}")

    try:
        insert_response = (
            supabase
            .table("categories")
            .insert(
                {
                    "name": category_name,
                    "slug": slug,
                }
            )
            .execute()
        )

        if insert_response.data:
            category = insert_response.data[0]
            print(
                f"Category created: {category['name']} "
                f"(ID: {category['id']})"
            )
            return category["id"]

    except Exception as error:
        print(
            f"Warning: Could not insert category '{category_name}': {error}. "
            "Trying to find it again."
        )

    # 4. Final retry by name or slug
    response = (
        supabase
        .table("categories")
        .select("id,name,slug")
        .or_(f"name.ilike.{category_name},slug.eq.{slug}")
        .limit(1)
        .execute()
    )

    if response.data:
        category = response.data[0]
        print(
            f"Category found after retry: {category['name']} "
            f"(ID: {category['id']})"
        )
        return category["id"]

    raise ValueError(f"Could not create or find category: {category_name}")


def build_product(row, row_number):
    """Convert one CSV row into a clean product dictionary."""
    external_id = (row.get("external_id") or "").strip()
    title = (row.get("title") or "").strip()

    if not external_id:
        raise ValueError("external_id is required")

    if not title:
        raise ValueError("title is required")

    slug = (row.get("slug") or "").strip()

    if not slug:
        slug = make_slug(title)

    category_name = (row.get("category") or "").strip() or "Other"

    current_price = to_number(row.get("current_price"), 0)
    original_price = to_number(row.get("original_price"), 0)
    discount_percent = to_number(row.get("discount_percent"), 0)

    if discount_percent == 0 and original_price > current_price > 0:
        discount_percent = round(
            ((original_price - current_price) / original_price) * 100
        )

    category_id = get_or_create_category(category_name)

    return {
        "external_id": external_id,
        "title": title,
        "slug": slug,
        "description": (row.get("description") or "").strip(),
        "image_url": (row.get("image_url") or "").strip(),
        "affiliate_url": (row.get("affiliate_url") or "").strip(),
        "source_product_url": (row.get("source_product_url") or "").strip(),
        "current_price": current_price,
        "original_price": original_price,
        "discount_percent": discount_percent,
        "rating": to_number(row.get("rating"), 0),
        "store_name": (row.get("store_name") or "").strip(),
        "is_active": to_boolean(row.get("is_active"), True),
        "is_featured": to_boolean(row.get("is_featured"), False),
        "category_id": category_id,
        "variants": to_variants(row.get("variants", "")),
    }


def read_products_from_csv():
    """Read and validate all product rows from CSV."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    products = []

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header row")

        required_columns = {
            "external_id",
            "title",
            "slug",
            "image_url",
            "affiliate_url",
            "current_price",
            "original_price",
            "discount_percent",
            "rating",
            "store_name",
            "is_active",
            "is_featured",
            "category",
            "variants",
        }

        missing_columns = required_columns - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                "Missing required CSV columns: "
                + ", ".join(sorted(missing_columns))
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                product = build_product(row, row_number)
            except Exception as error:
                raise ValueError(f"Row {row_number}: {error}") from error

            products.append(product)

    return products


def write_products_json(products):
    """Write clean product data to products.json."""
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

    with JSON_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(
            products,
            json_file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Created JSON file: {JSON_PATH}")
    print(f"Total products written: {len(products)}")


def upsert_products_to_supabase(products):
    if not supabase:
        print("Supabase is not configured. Skipping database upsert.")
        return

    for product in products:
        database_product = {
            "external_id": product["external_id"],
            "title": product["title"],
            "slug": product["slug"],
            "description": product["description"],
            "image_url": product["image_url"],
            "affiliate_url": product["affiliate_url"],
            "source_product_url": product["source_product_url"],
            "current_price": product["current_price"],
            "original_price": product["original_price"],
            "discount_percent": product["discount_percent"],
            "rating": product["rating"],
            "store_name": product["store_name"],
            "is_active": product["is_active"],
            "is_featured": product["is_featured"],
            "category_id": product["category_id"],
            "variants": product["variants"],
        }

        existing = (
            supabase
            .table("products")
            .select("id")
            .eq("external_id", product["external_id"])
            .limit(1)
            .execute()
        )

        if existing.data:
            product_id = existing.data[0]["id"]

            (
                supabase
                .table("products")
                .update(database_product)
                .eq("id", product_id)
                .execute()
            )

            print(f"Updated product: {product['external_id']}")
        else:
            (
                supabase
                .table("products")
                .insert(database_product)
                .execute()
            )

            print(f"Inserted product: {product['external_id']}")


def convert_csv_to_json():
    print(f"Reading CSV file: {CSV_PATH}")

    products = read_products_from_csv()

    if not products:
        print("Warning: No products found in CSV file.")
        return

    write_products_json(products)
    upsert_products_to_supabase(products)

    print("CSV to JSON conversion completed successfully.")


if __name__ == "__main__":
    convert_csv_to_json()
