# Supabase Setup for Deonex Deals

## 1. Create project

1. Supabase website पर account बनाएं
2. New Project पर click करें
3. Project name: `deonex-deals`
4. Strong database password रखें
5. Project create होने तक wait करें

## 2. Copy project credentials

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

## 3. Environment variables

Local `.env` file में:

```env
SUPABASE_URL=[https://your-project-id.supabase.co](https://your-project-id.supabase.co)
SUPABASE_ANON_KEY=your-publishable-or-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 4. Secret key usage

| Key | कहाँ use करें |
|---|---|
| `SUPABASE_ANON_KEY` | Flask public website queries |
| `SUPABASE_SERVICE_ROLE_KEY` | Render Cron Jobs और protected server-side importers |

`SUPABASE_SERVICE_ROLE_KEY` को कभी frontend, JavaScript, GitHub या public environment में expose न करें।

## 5. Run SQL files

Supabase Dashboard:

```text
SQL Editor → New Query
```

इन files को इसी order में run करें:

```text
1. database/schema.sql
2. database/functions.sql
3. database/policies.sql
4. database/demo_data.sql
```

## 6. Configure email authentication

Dashboard में:

```text
Authentication → Providers → Email
```

- Email provider enabled रखें
- Development testing के लिए Confirm Email off कर सकते हैं
- Production launch के लिए Confirm Email on रखें

## 7. Add Render website URL

Website Render पर live होने के बाद:

```text
Authentication → URL Configuration
```

यह values add करें:

```text
Site URL:
[https://your-render-service.onrender.com](https://your-render-service.onrender.com)

Redirect URLs:
[https://your-render-service.onrender.com](https://your-render-service.onrender.com)
```

Custom domain add करने के बाद उसे भी Site URL और Redirect URLs में add करें।

## 8. Verify setup

इन checks को करें:

- `categories` table में demo categories दिखें
- `products` table में demo products दिखें
- Website पर products दिखाई दें
- Register page से user signup हो
- Login page से user login हो
- Contact form `contacts` table में entry बनाए
- Feedback form `feedback` table में entry बनाए