# Deonex Deals API Setup

यह document अलग-अलग affiliate/product APIs को Deonex Deals project में जोड़ने के लिए है।

## Supported importers

- Amazon: `services/import_amazon.py`
- Flipkart: `services/import_flipkart.py`
- Cuelinks: `services/import_cuelinks.py`
- Admitad: `services/import_admitad.py`
- Manual JSON: `services/import_manual_products.py`

## Important security rule

API keys को कभी भी:

- GitHub repository में commit न करें
- HTML या JavaScript में न रखें
- Frontend browser code में न डालें
- Screenshot या public chat में share न करें

Keys केवल `.env` file और Render Environment Variables में रखें।

## Environment variables

```env
AMAZON_API_URL=
AMAZON_API_KEY=

FLIPKART_API_URL=
FLIPKART_API_KEY=

CUELINKS_API_URL=
CUELINKS_API_KEY=

ADMITAD_API_URL=
ADMITAD_API_KEY=
```

## API response mapping

हर API का response format अलग हो सकता है। Importer में इन fields को API response के अनुसार map करें:

```python
title
external_id
affiliate_url
source_product_url
image_url
current_price
original_price
rating
category_name
store_name
```

## Required standard product format

हर importer अंत में इस standard format का product बनाता है:

```python
{
    "source": "admitad",
    "external_id": "provider-product-id",
    "title": "Product Name",
    "slug": "product-name-provider-id",
    "description": "Product description",
    "image_url": "[https://image-url.jpg](https://image-url.jpg)",
    "affiliate_url": "[https://approved-affiliate-link.com](https://approved-affiliate-link.com)",
    "source_product_url": "[https://original-product-url.com](https://original-product-url.com)",
    "current_price": 999,
    "original_price": 1999,
    "discount_percent": 50,
    "rating": 4.4,
    "store_name": "Partner Store",
    "category_name": "Electronics",
    "is_featured": false
}
```

## Local importer test

पहले virtual environment activate करें:

```bash
pip install -r requirements.txt
```

फिर specific importer run करें:

```bash
python -m services.import_amazon
python -m services.import_flipkart
python -m services.import_cuelinks
python -m services.import_admitad
```

Manual JSON products import करने के लिए:

```bash
python -m services.import_manual_products
```

## Recommended intervals

| Platform type | Suggested interval |
|---|---|
| Flash offers | 1–2 hours |
| Frequently changing prices | 3–6 hours |
| Amazon / catalog products | 6–12 hours |
| Affiliate feed | 12–24 hours |
| Cleanup job | Daily |

## Compliance checklist

- केवल approved affiliate API या approved product feed use करें
- Platform terms and conditions follow करें
- Valid tracking/affiliate URLs use करें
- Price and availability may change notice website पर रखें
- Affiliate disclosure website footer और product page पर रखें
- Unauthorized scraping न करें
