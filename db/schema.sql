-- Ejecutar en el SQL editor de Supabase (proyecto vacío, plan gratuito).

create extension if not exists "uuid-ossp";

create table if not exists topics (
    id uuid primary key default uuid_generate_v4(),
    title text not null,
    source_notes text,
    used boolean not null default false,
    created_at timestamptz not null default now()
);

create table if not exists episodes (
    id uuid primary key default uuid_generate_v4(),
    topic_id uuid references topics(id),
    title text not null,
    hook text,
    script text not null,
    citations text,               -- fuentes del dato histórico, para auditar
    asset_plan jsonb,              -- qué clips/imágenes de archivo se usarán
    audio_path text,               -- ruta en Supabase Storage
    video_path text,               -- ruta en Supabase Storage
    status text not null default 'draft'
        check (status in (
            'draft', 'pending_review', 'approved', 'rejected',
            'rendering', 'ready_to_publish', 'published', 'error'
        )),
    youtube_url text,
    instagram_url text,
    facebook_url text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists pipeline_log (
    id uuid primary key default uuid_generate_v4(),
    episode_id uuid references episodes(id),
    step text not null,            -- ej: 'generate_script', 'publish'
    level text not null default 'info' check (level in ('info', 'warning', 'error')),
    message text,
    estimated_cost_usd numeric(10, 4),
    created_at timestamptz not null default now()
);

-- Trigger simple para mantener updated_at al día en episodes.
create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_episodes_updated_at on episodes;
create trigger trg_episodes_updated_at
    before update on episodes
    for each row
    execute function set_updated_at();
