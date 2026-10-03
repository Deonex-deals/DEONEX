create extension if not exists "uuid-ossp";

create table if not exists public.categories (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  slug text unique not null,
  description text,
  image_url text,
  created_at timestamptz not null default now()
);

create table if not exists public.products (
  id uuid primary key default uuid_generate_v4(),
  category_id uuid references public.categories(id) on delete set null,

  source text not null default 'manual',
  external_id text not null,

  title text not null,
  slug text unique not null,
  description text,

  image_url text,
  affiliate_url text not null,
  source_product_url text,

  current_price numeric(12, 2) not null default 0,
  original_price numeric(12, 2) not null default 0,
  discount_percent integer not null default 0,
  rating numeric(2, 1) not null default 0,

  store_name text not null default 'Partner Store',
  clicks integer not null default 0,

  is_active boolean not null default true,
  is_featured boolean not null default false,

  last_synced_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint products_discount_range
    check (discount_percent >= 0 and discount_percent <= 100),

  constraint products_rating_range
    check (rating >= 0 and rating <= 5)
);

create unique index if not exists products_source_external_id_unique
on public.products (source, external_id);

create index if not exists products_category_id_index
on public.products (category_id);

create index if not exists products_slug_index
on public.products (slug);

create index if not exists products_active_featured_index
on public.products (is_active, is_featured);

create index if not exists products_last_synced_at_index
on public.products (last_synced_at);

create table if not exists public.contacts (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  email text not null,
  subject text not null,
  message text not null,
  status text not null default 'new',
  created_at timestamptz not null default now()
);

create table if not exists public.feedback (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  email text not null,
  rating integer not null check (rating between 1 and 5),
  message text not null,
  is_visible boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.product_sync_logs (
  id uuid primary key default uuid_generate_v4(),
  source text not null,
  status text not null default 'started',
  received_count integer not null default 0,
  inserted_count integer not null default 0,
  updated_count integer not null default 0,
  skipped_count integer not null default 0,
  error_message text,
  started_at timestamptz not null default now(),
  completed_at timestamptz
);
