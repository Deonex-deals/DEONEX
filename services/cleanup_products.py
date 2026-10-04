import os
from datetime import datetime, timedelta, timezone

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

DAYS_BEFORE_DEACTIVATION = int(
    os.getenv("PRODUCT_EXPIRY_DAYS", "30")
)
