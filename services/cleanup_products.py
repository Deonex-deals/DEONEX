import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required."
    )

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)

DAYS_BEFORE_DEACTIVATION = int(
    os.getenv("PRODUCT_EXPIRY_DAYS", "30")
)


def deactivate_old_products():
    cutoff_date = (
        datetime.now(timezone.utc)
        - timedelta(days=DAYS_BEFORE_DEACTIVATION)
    ).isoformat()

    response = (
        supabase.table("products")
        .update({
            "is_active": False
        })
        .eq("is_active", True)
        .lt("last_synced_at", cutoff_date)
        .execute()
    )

    updated_count = len(response.data or [])

    print({
        "status": "cleanup_completed",
        "cutoff_date": cutoff_date,
        "deactivated_products": updated_count
    })


if __name__ == "__main__":
    deactivate_old_products()