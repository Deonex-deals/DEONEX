import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

    PRODUCT_API_URL = os.getenv("PRODUCT_API_URL", "")
    PRODUCT_API_KEY = os.getenv("PRODUCT_API_KEY", "")

    SITE_NAME = "Deonex Deals"