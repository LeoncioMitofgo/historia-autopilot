---
description: "Convenciones del esquema de Supabase"
applyTo: "db/**"
---

- Cualquier cambio de esquema se escribe como una migración nueva
  (`db/migrations/NNN_descripcion.sql`), nunca editando `schema.sql`
  directamente una vez que el proyecto ya está en producción — así el
  usuario puede aplicar los cambios en el SQL editor de Supabase sin perder
  histórico.
- Toda tabla lleva `created_at timestamptz default now()` y, si aplica,
  `updated_at` mantenido por un trigger — no lo actualices manualmente
  desde Python.
- El campo `status` de `episodes` es la fuente de verdad para el pipeline.
  No dupliques ese estado en otra tabla ni en un archivo local: cualquier
  script que necesite saber "qué falta publicar" debe consultarlo desde
  Supabase, no desde una caché.
