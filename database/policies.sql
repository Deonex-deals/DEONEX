alter table public.categories enable row level security;
alter table public.products enable row level security;
alter table public.contacts enable row level security;
alter table public.feedback enable row level security;
alter table public.product_sync_logs enable row level security;

drop policy if exists "public_read_categories" on public.categories;
drop policy if exists "public_read_active_products" on public.products;
drop policy if exists "public_insert_contacts" on public.contacts;
drop policy if exists "public_insert_feedback" on public.feedback;

create policy "public_read_categories"
on public.categories
for select
to anon, authenticated
using (true);

create policy "public_read_active_products"
on public.products
for select
to anon, authenticated
using (is_active = true);

create policy "public_insert_contacts"
on public.contacts
for insert
to anon, authenticated
with check (true);

create policy "public_insert_feedback"
on public.feedback
for insert
to anon, authenticated
with check (true);