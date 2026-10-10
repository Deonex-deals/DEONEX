from datetime import datetime
from functools import wraps
import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from supabase import create_client, Client

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

if not app.config["SUPABASE_URL"]:
    raise RuntimeError("SUPABASE_URL is missing.")

if not app.config["SUPABASE_PUBLISHABLE_KEY"]:
    raise RuntimeError(
        "SUPABASE_PUBLISHABLE_KEY is missing. "
        "Add it in Render Environment Variables."
    )

supabase: Client = create_client(
    app.config["SUPABASE_URL"],
    app.config["SUPABASE_PUBLISHABLE_KEY"]
)

supabase_admin = None

if app.config["SUPABASE_SECRET_KEY"]:
    supabase_admin = create_client(
        app.config["SUPABASE_URL"],
        app.config["SUPABASE_SECRET_KEY"]
    )

print({
    "supabase_url_present": bool(app.config["SUPABASE_URL"]),
    "publishable_key_present": bool(app.config["SUPABASE_PUBLISHABLE_KEY"]),
    "publishable_key_prefix": app.config["SUPABASE_PUBLISHABLE_KEY"][:16],
    "secret_key_present": bool(app.config["SUPABASE_SECRET_KEY"]),
    "secret_key_prefix": app.config["SUPABASE_SECRET_KEY"][:10],
    "admin_client_created": supabase_admin is not None
})


def current_user():
    return session.get("user")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user():
            flash("Dashboard देखने के लिए पहले login करें।", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view


@app.context_processor
def inject_global_data():
    categories = []
    try:
        response = supabase.table("categories").select("*").order("name").execute()
        categories = response.data or []
    except Exception:
        categories = []

    return {
        "site_name": app.config["SITE_NAME"],
        "nav_categories": categories,
        "logged_user": current_user()
    }


@app.route("/")
def home():
    try:
        featured_response = (
            supabase.table("products")
            .select("*, categories(name, slug)")
            .eq("is_active", True)
            .eq("is_featured", True)
            .order("created_at", desc=True)
            .limit(12)
            .execute()
        )

        latest_response = (
            supabase.table("products")
            .select("*, categories(name, slug)")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .limit(12)
            .execute()
        )

        categories_response = (
            supabase.table("categories")
            .select("*")
            .order("name")
            .limit(12)
            .execute()
        )

        return render_template(
            "home.html",
            featured_products=featured_response.data or [],
            latest_products=latest_response.data or [],
            categories=categories_response.data or []
        )
    except Exception as error:
        flash(f"Database connection issue: {error}", "danger")
        return render_template(
            "home.html",
            featured_products=[],
            latest_products=[],
            categories=[]
        )


@app.route("/category/<slug>")
def category(slug):
    category_response = (
        supabase.table("categories")
        .select("*")
        .eq("slug", slug)
        .limit(1)
        .execute()
    )

    if not category_response.data:
        abort(404)

    selected_category = category_response.data[0]

    products_response = (
        supabase.table("products")
        .select("*")
        .eq("category_id", selected_category["id"])
        .eq("is_active", True)
        .order("created_at", desc=True)
        .execute()
    )

    return render_template(
        "category.html",
        category=selected_category,
        products=products_response.data or []
    )


@app.route("/product/<slug>")
def product(slug):
    product_response = (
        supabase.table("products")
        .select("*")
        .eq("slug", slug)
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    if not product_response.data:
        abort(404)

    product = product_response.data[0]

    related_response = (
        supabase.table("products")
        .select("*")
        .eq("category_id", product["category_id"])
        .eq("is_active", True)
        .neq("id", product["id"])
        .limit(6)
        .execute()
    )

    return render_template(
        "product.html",
        product=product,
        related_products=related_response.data or []
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, subject, message]):
            flash("कृपया सभी fields भरें।", "danger")
            return redirect(url_for("contact"))

        try:
            if supabase_admin is None:
                raise RuntimeError(
                    "Admin database client missing. "
                    "Add SUPABASE_SECRET_KEY in Render Environment."
                )

            supabase_admin.table("contacts").insert({
                "name": name,
                "email": email,
                "subject": subject,
                "message": message
            }).execute()

            flash("आपका संदेश सफलतापूर्वक भेज दिया गया है।", "success")

        except Exception as error:
            flash(f"Message save नहीं हो सका: {error}", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        rating = request.form.get("rating", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, rating, message]):
            flash("कृपया सभी fields भरें।", "danger")
            return redirect(url_for("feedback"))

        try:
            if supabase_admin is None:
                raise RuntimeError(
                    "Admin database client missing. "
                    "Add SUPABASE_SECRET_KEY in Render Environment."
                )

            supabase_admin.table("feedback").insert({
                "name": name,
                "email": email,
                "rating": int(rating),
                "message": message
            }).execute()

            flash("Feedback के लिए धन्यवाद।", "success")

        except Exception as error:
            flash(f"Feedback save नहीं हो सका: {error}", "danger")

        return redirect(url_for("feedback"))

    return render_template("feedback.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if len(name) < 2 or not email or len(password) < 6:
            flash("नाम, valid email और कम से कम 6 characters का password दें।", "danger")
            return redirect(url_for("register"))

        try:
            result = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": name
                    }
                }
            })

            if result.user:
                flash(
                    "Registration successful. अगर Supabase email confirmation enabled है तो email verify करें, फिर login करें।",
                    "success"
                )
                return redirect(url_for("login"))

            flash("Registration पूरा नहीं हो सका।", "danger")
        except Exception as error:
            flash(f"Registration error: {error}", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        try:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if result.user:
                session["user"] = {
                    "id": result.user.id,
                    "email": result.user.email,
                    "name": (
                        result.user.user_metadata.get("full_name")
                        if result.user.user_metadata
                        else result.user.email
                    )
                }

                flash("Welcome back! Login successful.", "success")
                return redirect(request.args.get("next") or url_for("dashboard"))

            flash("Invalid email या password।", "danger")
        except Exception:
            flash("Login failed. Email/password या email verification check करें।", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    session.clear()
    flash("आप successfully logout हो गए हैं।", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/go/<product_id>")
def affiliate_redirect(product_id):
    response = (
        supabase.table("products")
        .select("affiliate_url")
        .eq("id", product_id)
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    if not response.data:
        abort(404)

    product = response.data[0]

    try:
        supabase.table("products").update({
            "clicks": 1
        }).eq("id", product_id).execute()
    except Exception:
        pass

    return redirect(product["affiliate_url"])


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
    
@app.template_filter("to_price")
def to_price(value):
    try:
        number = float(str(value).replace(",", "").replace("₹", "").strip())
        return f"{number:,.0f}"
    except (TypeError, ValueError):
        return value

if __name__ == "__main__":
    app.run(debug=True)
