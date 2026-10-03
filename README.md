# Deonex Deals

Deonex Deals एक premium affiliate deals website है जो multiple affiliate platforms और product APIs से products लाकर उन्हें Supabase database में store करती है, और Flask backend के माध्यम से live website पर दिखाती है।

Website में responsive premium layout, affiliate product listings, categories, product detail pages, Supabase authentication, contact form, feedback form, multiple API importers और Render Cron Jobs शामिल हैं।

---

## Features

- Premium and responsive UI
- Mobile पर 4-column product grid
- Desktop पर 6-column product grid
- Premium startup loading screen
- Home, category, product, about, contact और feedback pages
- Flask Python backend
- Supabase database integration
- Supabase user registration, login और logout
- Affiliate product redirect system
- Product categories
- Contact message storage
- Feedback storage
- Multiple API import support
- Manual JSON product import support
- Automatic product cleanup job
- Separate Render Cron Jobs for each affiliate platform
- GitHub to Render deployment support

---

## Tech Stack

| Technology | Use |
|---|---|
| Python | Backend language |
| Flask | Web framework |
| Gunicorn | Production WSGI server |
| Supabase | Database, Auth and PostgreSQL backend |
| HTML, CSS, JavaScript | Frontend |
| Render | Hosting and Cron Jobs |
| GitHub | Source code repository |
| Requests | External API calls |
| python-dotenv | Environment variable loading |

---

## Project Structure

```text
deonex-deals/
│
├── app.py
├── config.py
├── requirements.txt
├── render.yaml
├── .gitignore
├── .env.example
├── README.md
├── manual_products.json
│
├── services/
│   ├── __init__.py
│   ├── common.py
│   ├── import_amazon.py
│   ├── import_flipkart.py
│   ├── import_cuelinks.py
│   ├── import_admitad.py
│   ├── import_manual_products.py
│   └── cleanup_products.py
│
├── templates/
│   ├── base.html
│   ├── _product_card.html
│   ├── home.html
│   ├── category.html
│   ├── product.html
│   ├── about.html
│   ├── contact.html
│   ├── feedback.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── 404.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       ├── logo.png
│       ├── logo-dark.png
│       └── placeholder-product.jpg
│
├── database/
│   ├── schema.sql
│   ├── functions.sql
│   ├── policies.sql
│   └── demo_data.sql
│
└── docs/
    ├── API_SETUP.md
    ├── SUPABASE_SETUP.md
    ├── RENDER_DEPLOYMENT.md
    └── GITHUB_SETUP.md
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/deonex-deals.git](https://github.com/YOUR_GITHUB_USERNAME/deonex-deals.git)
cd deonex-deals
```

### 2. Create a Python virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Mac or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python packages

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

`.env.example` file को copy करके `.env` बनाएं।

Windows PowerShell:

```powershell
copy .env.example .env
```

Mac or Linux:

```bash
cp .env.example .env
```

अब `.env` में actual values भरें:

```env
SECRET_KEY=replace-with-a-long-random-secret

SUPABASE_URL=[https://your-project-id.supabase.co](https://your-project-id.supabase.co)
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_KEY=your-supabase-anon-key

SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

AMAZON_API_URL=
AMAZON_API_KEY=

FLIPKART_API_URL=
FLIPKART_API_KEY=

CUELINKS_API_URL=
CUELINKS_API_KEY=

ADMITAD_API_URL=
ADMITAD_API_KEY=

PRODUCT_EXPIRY_DAYS=30
```

> Important: `.env` को कभी GitHub पर upload या commit न करें।

### 5. Set up Supabase database

Supabase Dashboard खोलें:

```text
SQL Editor → New Query
```

इन SQL files को इसी order में run करें:

```text
1. database/schema.sql
2. database/functions.sql
3. database/policies.sql
4. database/demo_data.sql
```

### 6. Start the Flask application

```bash
python app.py
```

Website browser में खोलें:

```text
http://127.0.0.1:5000
```

---

## Supabase Setup

### Required values

Supabase Dashboard में:

```text
Project Settings → API
```

इन values को copy करें:

```text
Project URL
Publishable key / anon key
service_role key
```

### Key usage

| Key | Use |
|---|---|
| `SUPABASE_ANON_KEY` | Flask website public database access |
| `SUPABASE_KEY` | Existing Flask app compatibility |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-only API importer and Cron Jobs |

> Warning: `SUPABASE_SERVICE_ROLE_KEY` को कभी JavaScript, HTML, frontend, GitHub repository या public website पर expose न करें।

### Supabase Auth setup

Supabase Dashboard में:

```text
Authentication → Providers → Email
```

- Email provider enabled रखें
- Development testing में email confirmation optional है
- Production में email confirmation enable करने की सलाह दी जाती है

Render website live होने के बाद:

```text
Authentication → URL Configuration
```

यह URLs add करें:

```text
Site URL:
[https://your-render-service.onrender.com](https://your-render-service.onrender.com)

Redirect URLs:
[https://your-render-service.onrender.com](https://your-render-service.onrender.com)
```

---

## API Importers

Deonex Deals अलग-अलग platforms के लिए अलग importer scripts उपयोग करता है।

| Platform | Script | Suggested interval |
|---|---|---|
| Amazon | `services/import_amazon.py` | Every 6 hours |
| Flipkart | `services/import_flipkart.py` | Every 3 hours |
| Cuelinks | `services/import_cuelinks.py` | Twice daily |
| Admitad | `services/import_admitad.py` | Every 12 hours |
| Manual products | `services/import_manual_products.py` | When needed |
| Cleanup | `services/cleanup_products.py` | Daily |

### Test importers locally

```bash
python -m services.import_amazon
python -m services.import_flipkart
python -m services.import_cuelinks
python -m services.import_admitad
python -m services.import_manual_products
python -m services.cleanup_products
```

### Manual product import

`manual_products.json` में products add करें:

```json
[
  {
    "external_id": "manual-demo-001",
    "title": "Premium Smart Watch",
    "description": "Fitness tracker with calling support.",
    "image_url": "[https://example.com/product-image.jpg](https://example.com/product-image.jpg)",
    "affiliate_url": "[https://example.com/your-affiliate-link](https://example.com/your-affiliate-link)",
    "source_product_url": "[https://example.com/original-product-page](https://example.com/original-product-page)",
    "current_price": 2499,
    "original_price": 4999,
    "rating": 4.4,
    "store_name": "Partner Store",
    "category_name": "Electronics",
    "is_featured": true
  }
]
```

फिर run करें:

```bash
python -m services.import_manual_products
```

---

## Render Deployment

### Web Service configuration

Render Dashboard में:

```text
New + → Web Service
```

इन settings का उपयोग करें:

| Setting | Value |
|---|---|
| Name | `deonex-deals-web` |
| Branch | `main` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Health Check Path | `/` |

### Web Service environment variables

```env
SECRET_KEY=your-long-random-secret
SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_KEY=your-supabase-anon-key
PYTHON_VERSION=3.12.7
```

### Render Cron Jobs

Create separate Cron Jobs for each API importer.

| Name | Start command | Schedule (UTC) |
|---|---|---|
| `deonex-amazon-sync` | `python -m services.import_amazon` | `5 */6 * * *` |
| `deonex-flipkart-sync` | `python -m services.import_flipkart` | `15 */3 * * *` |
| `deonex-cuelinks-sync` | `python -m services.import_cuelinks` | `30 0,12 * * *` |
| `deonex-admitad-sync` | `python -m services.import_admitad` | `45 */12 * * *` |
| `deonex-product-cleanup` | `python -m services.cleanup_products` | `0 18 * * *` |

Each Cron Job needs:

```env
SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
PYTHON_VERSION=3.12.7
```

Platform-specific jobs need only their own API credentials.

Example for Amazon Cron Job:

```env
AMAZON_API_URL=[https://your-approved-api-endpoint.com](https://your-approved-api-endpoint.com)
AMAZON_API_KEY=your-amazon-api-key
```

### Render schedule timezone

Render Cron Jobs UTC timezone में चलती हैं।

```text
IST = UTC + 5 hours 30 minutes
```

Example:

```text
0 18 * * *
```

यह UTC 18:00 पर run होगा, जो IST 11:30 PM है।

---

## GitHub Upload Rules

GitHub पर ये files upload करें:

```text
app.py
config.py
requirements.txt
render.yaml
README.md
.env.example
services/
templates/
static/
database/
docs/
manual_products.json
```

GitHub पर ये files upload न करें:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
SUPABASE_SERVICE_ROLE_KEY
API keys
Passwords
```

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial Deonex Deals affiliate website"
git branch -M main
git remote add origin [https://github.com/YOUR_GITHUB_USERNAME/deonex-deals.git](https://github.com/YOUR_GITHUB_USERNAME/deonex-deals.git)
git push -u origin main
```

---

## Security Checklist

- Keep `.env` in `.gitignore`
- Never upload real API keys to GitHub
- Never expose `SUPABASE_SERVICE_ROLE_KEY` in frontend code
- Use only approved affiliate APIs or product feeds
- Follow Amazon, Flipkart, Cuelinks, Admitad and other partner platform policies
- Do not scrape websites without explicit permission
- Add affiliate disclosure to website footer and product pages
- Show price and availability disclaimer

---

## Database Files

Run database files in this exact order:

```text
database/schema.sql
database/functions.sql
database/policies.sql
database/demo_data.sql
```

| File | Purpose |
|---|---|
| `schema.sql` | Categories, products, contacts, feedback and sync log tables |
| `functions.sql` | Product click function and automatic updated_at trigger |
| `policies.sql` | Row Level Security policies |
| `demo_data.sql` | Demo categories and products |

---

## Affiliate Disclosure

Deonex Deals may use affiliate links. When users click a product deal, they may be redirected to a partner website.

Users do not pay extra because of affiliate links. Deonex Deals may earn a commission on qualifying purchases. Prices, offers and product availability can change at any time on the partner website.

---

## Troubleshooting

### Website shows database connection error

Check:

```text
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_KEY
```

are correctly set in `.env` or Render Environment Variables.

### API importer does not save products

Check:

```text
SUPABASE_SERVICE_ROLE_KEY
Platform API URL
Platform API key
API response field mapping
Supabase product table
Render Cron Job logs
```

### Render deployment fails

Check:

```text
requirements.txt exists
Build Command = pip install -r requirements.txt
Start Command = gunicorn app:app
app.py exists in root directory
Environment variables are correctly added
```

### Login is not working

Check Supabase Dashboard:

```text
Authentication → Providers → Email
Authentication → URL Configuration
```

Ensure email provider is enabled and the Render URL is added.

---

## Future Improvements

- Admin dashboard for product management
- Product search and filters
- Wishlist system
- Price history tracking
- Product price-drop alerts
- Email newsletter integration
- Telegram deal alerts
- WhatsApp channel alerts
- SEO sitemap generation
- Custom domain
- Analytics dashboard
- Coupon code system
- AI-powered product recommendations

---

## License

This project is created for Deonex Deals. Before commercial use, verify the license terms of all third-party APIs, libraries, product images and affiliate platforms.
