# Render Deployment Guide

## Required GitHub files

```text
app.py
requirements.txt
render.yaml
services/
templates/
static/
database/
```

## 1. Create Render account

1. Render Dashboard खोलें
2. Continue with GitHub चुनें
3. GitHub repository access allow करें

## 2. Deploy web service

Render Dashboard:

```text
New + → Web Service
```

Repository: `deonex-deals`

Use these values:

| Setting | Value |
|---|---|
| Name | `deonex-deals-web` |
| Branch | `main` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Health Check Path | `/` |

## 3. Web service environment variables

```env
SECRET_KEY=long-random-secret-value
SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_ANON_KEY=your-anon-key
PYTHON_VERSION=3.12.7
```

If your existing app uses `SUPABASE_KEY`, add this too:

```env
SUPABASE_KEY=your-anon-key
```

## 4. Create API Cron Jobs

Create separate jobs so one failing API does not stop other imports.

### Amazon

```text
Name: deonex-amazon-sync
Build Command: pip install -r requirements.txt
Start Command: python -m services.import_amazon
Schedule: 5 */6 * * *
```

### Flipkart

```text
Name: deonex-flipkart-sync
Build Command: pip install -r requirements.txt
Start Command: python -m services.import_flipkart
Schedule: 15 */3 * * *
```

### Cuelinks

```text
Name: deonex-cuelinks-sync
Build Command: pip install -r requirements.txt
Start Command: python -m services.import_cuelinks
Schedule: 30 0,12 * * *
```

### Admitad

```text
Name: deonex-admitad-sync
Build Command: pip install -r requirements.txt
Start Command: python -m services.import_admitad
Schedule: 45 */12 * * *
```

### Cleanup

```text
Name: deonex-product-cleanup
Build Command: pip install -r requirements.txt
Start Command: python -m services.cleanup_products
Schedule: 0 18 * * *
```

## 5. Cron job variables

हर Cron Job में:

```env
SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
PYTHON_VERSION=3.12.7
```

और जिस platform का Cron Job है, उसी की API keys add करें।

Example: Amazon Cron Job:

```env
AMAZON_API_URL=[https://your-approved-api-endpoint.com](https://your-approved-api-endpoint.com)
AMAZON_API_KEY=your-api-key
```

## 6. Timezone note

Render Cron schedules UTC time में run होते हैं.

```text
IST = UTC + 5 hours 30 minutes
```

Example:

```text
0 18 * * *
```

यह UTC 18:00 पर चलेगा, जो IST 11:30 PM होता है।

## 7. Logs

Troubleshooting:

```text
Render Dashboard → Your Service → Logs
```

Check for:

- Missing environment variable
- Module not found
- API unauthorized / 401
- API rate limit / 429
- Supabase policy issue
- Invalid database key