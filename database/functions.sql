create or replace function public.update_updated_at_column()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists products_set_updated_at on public.products;

create trigger products_set_updated_at
before update on public.products
for each row
execute function public.update_updated_at_column();

create or replace function public.increment_product_click(product_uuid uuid)
returns void
language sql
security definer
set search_path = public
as $$
  update public.products
  set clicks = clicks + 1
  where id = product_uuid
    and is_active = true;
$$;