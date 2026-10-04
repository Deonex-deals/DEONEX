import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

    SUPABASE_URL = (
        os.getenv("SUPABASE_URL", "")
        .strip()
        .rstrip("/")
        .replace("/rest/v1", "")
        .replace("/auth/v1", "")
    )

    SUPABASE_PUBLISHABLE_KEY = (
        os.getenv("SUPABASE_PUBLISHABLE_KEY")
        or os.getenv("SUPABASE_KEY")
        or os.getenv("SUPABASE_ANON_KEY")
        or ""
    ).strip()

    SUPABASE_SECRET_KEY = (
        os.getenv("SUPABASE_SECRET_KEY")
        or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or ""
    ).strip()

    SITE_NAME = "Deonex Deals"
