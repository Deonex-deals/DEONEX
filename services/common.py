import os
import re
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()

SUPABASE_SECRET_KEY = (
    os.getenv("SUPABASE_SECRET_KEY")
    or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    or ""
).strip()

if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_SECRET_KEY are required."
    )

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


def slugify(value):
    value = str(value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def safe_float(value, default=0):
    try:
        return float(value or default)
    except (ValueError, TypeError):
        return default


def calculate_discount(current_price, original_price):
    current_price = safe_float(current_price)
    original_price = safe_float(original_price)

    if original_price > current_price and original_price > 0:
        return round(((original_price - current_price) / original_price) * 100)

    return 0


def get_or_create_category(category_name):
    category_name = category_name or "Other"
    category_slug = slugify(category_name)

    category = (
        supabase.table("categories")
        .select("id")
        .eq("slug", category_slug)
        .limit(1)
        .execute()
    )

    if category.data:
        return category.data[0]["id"]

    new_category = (
        supabase.table("categories")
        .insert({
            "name": category_name,
            "slug": category_slug,
            "description": f"Best offers in {category_name}"
        })
        .execute()
    )

    return new_category.data[0]["id"]


def save_product(product):
    category_id = get_or_create_category(product["category_name"])

    payload = {
        "category_id": category_id,
        "title": product["title"],
        "slug": product["slug"],
        "description": product.get("description", ""),
        "image_url": product.get("image_url"),
        "affiliate_url": product["affiliate_url"],
        "source_product_url": product.get("source_product_url"),
        "current_price": product.get("current_price", 0),
        "original_price": product.get("original_price", 0),
        "discount_percent": product.get("discount_percent", 0),
        "rating": product.get("rating", 0),
        "store_name": product.get("store_name", "Partner Store"),
        "source": product["source"],
        "external_id": product["external_id"],
        "is_active": True,
        "last_synced_at": datetime.now(timezone.utc).isoformat()
    }

    existing = (
        supabase.table("products")
        .select("id")
        .eq("source", product["source"])
        .eq("external_id", product["external_id"])
        .limit(1)
        .execute()
    )

    if existing.data:
        (
            supabase.table("products")
            .update(payload)
            .eq("id", existing.data[0]["id"])
            .execute()
        )
        return "updated"

    supabase.table("products").insert(payload).execute()
    return "inserted"
