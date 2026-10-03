# GitHub Setup Guide

## 1. Create repository

1. GitHub पर login करें
2. ऊपर plus icon पर click करें
3. New repository चुनें
4. Repository name: `deonex-deals`
5. Public या Private choose करें
6. Create repository click करें

## 2. Do not upload secrets

इन files को GitHub में commit न करें:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
```

`.gitignore` file में यह जरूर रखें:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
.DS_Store
```

## 3. Upload using Git commands

Project folder terminal में खोलें:

```bash
git init
git add .
git commit -m "Initial Deonex Deals project"
git branch -M main
git remote add origin [https://github.com/YOUR_GITHUB_USERNAME/deonex-deals.git](https://github.com/YOUR_GITHUB_USERNAME/deonex-deals.git)
git push -u origin main
```

`YOUR_GITHUB_USERNAME` को अपने actual GitHub username से replace करें।

## 4. Update code later

जब code में बदलाव करें:

```bash
git add .
git commit -m "Updated Deonex Deals features"
git push origin main
```

Render repository से connected होने पर deployment automatically trigger हो सकता है।

## 5. Before push checklist

- `.env` excluded है
- API keys removed हैं
- Supabase service role key visible नहीं है
- Demo affiliate links clearly marked हैं
- `requirements.txt` updated है
- Python code local environment में tested है