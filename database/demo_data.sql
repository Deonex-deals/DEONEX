insert into public.categories (name, slug, description, image_url)
values
(
  'Electronics',
  'electronics',
  'Smart gadgets, audio devices, accessories and electronics deals.',
  'https://images.unsplash.com/photo-1498049794561-7780e7231661?auto=format&fit=crop&w=800&q=80'
),
(
  'Fashion',
  'fashion',
  'Trending fashion, shoes, watches and lifestyle deals.',
  'https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=800&q=80'
),
(
  'Home & Kitchen',
  'home-kitchen',
  'Useful home, kitchen and daily essentials deals.',
  'https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=800&q=80'
),
(
  'Beauty',
  'beauty',
  'Beauty, grooming and personal care products.',
  'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=800&q=80'
)
on conflict (slug) do nothing;

insert into public.products (
  category_id,
  source,
  external_id,
  title,
  slug,
  description,
  image_url,
  affiliate_url,
  source_product_url,
  current_price,
  original_price,
  discount_percent,
  rating,
  store_name,
  is_active,
  is_featured
)
values
(
  (select id from public.categories where slug = 'electronics'),
  'manual',
  'demo-headphones-001',
  'Wireless Noise Cancelling Headphones',
  'wireless-noise-cancelling-headphones',
  'Premium wireless headphones with immersive sound, long battery life and a comfortable fit.',
  'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
  'https://example.com/affiliate-headphones',
  'https://example.com/product-headphones',
  2499,
  4999,
  50,
  4.5,
  'Partner Store',
  true,
  true
),
(
  (select id from public.categories where slug = 'fashion'),
  'manual',
  'demo-sneakers-001',
  'Classic Everyday Sneakers',
  'classic-everyday-sneakers',
  'Comfortable sneakers for daily casual wear, walking and travel.',
  'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80',
  'https://example.com/affiliate-sneakers',
  'https://example.com/product-sneakers',
  1799,
  3499,
  49,
  4.3,
  'Partner Store',
  true,
  true
),
(
  (select id from public.categories where slug = 'home-kitchen'),
  'manual',
  'demo-kitchen-001',
  'Stainless Steel Kitchen Set',
  'stainless-steel-kitchen-set',
  'Everyday kitchen essentials with a modern stainless-steel finish.',
  'https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=800&q=80',
  'https://example.com/affiliate-kitchen',
  'https://example.com/product-kitchen',
  1299,
  2399,
  46,
  4.2,
  'Partner Store',
  true,
  true
),
(
  (select id from public.categories where slug = 'beauty'),
  'manual',
  'demo-skincare-001',
  'Daily Skin Care Combo',
  'daily-skin-care-combo',
  'A practical personal-care combo designed for an everyday routine.',
  'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=800&q=80',
  'https://example.com/affiliate-skincare',
  'https://example.com/product-skincare',
  899,
  1599,
  44,
  4.4,
  'Partner Store',
  true,
  false
)
on conflict (source, external_id) do nothing;