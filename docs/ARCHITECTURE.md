# Arquitectura del pipeline

```
 ┌─────────────────┐     cron mensual      ┌───────────────────────┐
 │ generate.yml     │ ───────────────────▶ │ generate_script.py     │
 │ (GitHub Actions) │                       │ genera guiones (LLM)   │
 └─────────────────┘                       └───────────┬────────────┘
                                                          │ status=pending_review
                                                          ▼
                                             ┌───────────────────────┐
                                             │ tabla `episodes`       │
                                             │ (Supabase)             │
                                             └───────────┬────────────┘
                                                          │ el usuario aprueba
                                                          │ manualmente en el
                                                          │ editor de Supabase
                                                          ▼ status=approved
 ┌─────────────────┐     cron semanal      ┌───────────────────────┐
 │ publish.yml      │ ───────────────────▶ │ generate_voice.py      │
 │ (GitHub Actions) │                       │ fetch_assets.py        │
 └─────────────────┘                       │ assemble_video.py      │
                                             └───────────┬────────────┘
                                                          │ status=rendering → publicado
                                                          ▼
                                             ┌───────────────────────┐
                                             │ publish.py              │
                                             │ YouTube + Instagram/FB  │
                                             └───────────────────────┘
```

## Etapas

1. **generate_script.py** — a partir de una cola de temas (tabla `topics`),
   pide al LLM un guion con gancho + dato verificable + pregunta de cierre,
   y lo guarda en `episodes` con `status = pending_review`.
2. **Revisión humana** — el usuario abre la tabla `episodes` en Supabase,
   lee el resumen (ver prompt `weekly-review-batch`) y cambia `status` a
   `approved` o `rejected`.
3. **generate_voice.py** — convierte el guion aprobado a audio (Edge-TTS por
   defecto).
4. **fetch_assets.py** — busca metraje/imágenes reales de archivo
   (Pexels/Pixabay/Wikimedia/archive.org) que encajen con el guion.
5. **assemble_video.py** — ensambla audio + assets + subtítulos con
   ffmpeg/MoviePy, sube el archivo final a Supabase Storage.
6. **publish.py** — publica en YouTube (API oficial) y, si está configurado,
   en Instagram/Facebook (Graph API). Actualiza `status = published`.

## Tablas de Supabase

- `topics` — cola de ideas pendientes de convertir en episodio.
- `episodes` — el corazón del pipeline (ver `db/schema.sql`).
- `pipeline_log` — todo evento, éxito o error, de cualquier script.
