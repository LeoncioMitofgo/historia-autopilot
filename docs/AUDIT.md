# Auditoría del proyecto — quién hace qué

Estado a fecha de creación del repo. Copilot debe mantener esta tabla
actualizada: marca `[x]` cuando una tarea de código está hecha, y añade
filas nuevas si aparece una dependencia nueva.

## Cuentas y consolas externas — SOLO TÚ puedes hacer esto (Copilot no tiene acceso)

- [ ] Crear proyecto en supabase.com (plan gratuito) → copiar `SUPABASE_URL`
      y `SUPABASE_KEY` a los Secrets del repo de GitHub.
- [ ] Ejecutar `db/schema.sql` en el SQL editor de Supabase.
- [ ] Crear el repositorio en GitHub y subir este scaffold.
- [ ] En Settings → Secrets and variables → Actions del repo, cargar todas
      las variables listadas en `.env.example`.
- [ ] Crear cuenta de Google Cloud Console → habilitar YouTube Data API v3 →
      generar credenciales OAuth → copiar a Secrets (`YOUTUBE_CLIENT_ID`,
      `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`).
- [ ] Convertir la cuenta de Instagram a perfil Business o Creator.
- [ ] Crear una app en developers.facebook.com, añadir el producto Instagram
      Graph API, y darte a ti mismo el rol de "Instagram Tester" (esto
      evita el proceso completo de revisión de Meta, que solo hace falta si
      gestionas cuentas de terceros). Copiar el token a Secrets.
- [ ] Decidir si se paga la API de X o se publica ahí manualmente (ver
      `docs/DECISIONS.md`, punto 4) — no es tarea de código hasta que se
      decida.
- [ ] Elegir y contratar (o no) una API de LLM de pago para
      `generate_script.py` (Claude, GPT...) y cargar la key en Secrets.

## Código — esto lo construye Copilot en este repo

- [ ] `scripts/_supabase_client.py` — cliente compartido de Supabase.
- [ ] `scripts/generate_script.py` — completar la llamada real al LLM
      (el stub ya define el contrato de entrada/salida).
- [ ] `scripts/generate_voice.py` — integrar Edge-TTS (y ElevenLabs opcional).
- [ ] `scripts/fetch_assets.py` — integrar APIs de Pexels/Pixabay/Wikimedia.
- [ ] `scripts/assemble_video.py` — lógica de ensamblado con ffmpeg/MoviePy.
- [ ] `scripts/publish.py` — integrar YouTube Data API y Meta Graph API.
- [ ] `.github/workflows/generate.yml` — completar el cron y los pasos
      (esqueleto ya creado).
- [ ] `.github/workflows/publish.yml` — completar el cron y los pasos
      (esqueleto ya creado).
- [ ] `.github/workflows/keepalive.yml` — ya funcional, no requiere cambios.
- [ ] Tests mínimos en `scripts/tests/` para cada script.

## Notas de auditoría de coste (actualizar según uso real)

| Servicio | Coste esperado | Notas |
|---|---|---|
| GitHub Actions | $0 | dentro de minutos gratis para repo público/privado pequeño |
| Supabase | $0 | plan gratuito, proyecto se pausa tras 1 semana inactivo — `keepalive.yml` lo evita |
| Edge-TTS | $0 | API no oficial, puede romperse sin aviso — tener plan B |
| Pexels/Pixabay/Wikimedia | $0 | gratis con atribución según fuente |
| YouTube Data API | $0 | dentro de cuota diaria gratuita |
| Instagram/Facebook Graph API | $0 | gratis para publicar en tu propia cuenta |
| LLM (guiones) | variable, bajo | depende del proveedor elegido |
| X API | variable | sin tier gratis desde 2026, ~$0.015/post — opcional |
