# Instrucciones para GitHub Copilot — Proyecto "Historia Autopilot"

Este archivo se carga siempre que Copilot trabaja en este repositorio. Léelo
completo antes de generar o modificar código. El resto de la "memoria" del
proyecto vive en `docs/` — consúltalo cuando necesites contexto adicional:

- `docs/DECISIONS.md` — decisiones estratégicas ya tomadas y su porqué. No las
  re-abras salvo que el usuario lo pida explícitamente.
- `docs/ARCHITECTURE.md` — cómo encajan las piezas del pipeline.
- `docs/AUDIT.md` — checklist de qué falta, quién lo hace (usuario vs Copilot)
  y el estado actual. Actualízalo cada vez que completes una tarea.

## Qué es este proyecto

Un canal de contenido (YouTube primero, Instagram/Facebook como distribución
secundaria) sobre historia real poco conocida, narrado con voz IA sobre
metraje/imágenes de archivo reales (no imágenes fotorrealistas generadas por
IA de escenas ficticias — ver `docs/DECISIONS.md` para el motivo). Producción
en lote mensual, publicación programada, con un único punto de intervención
humana: aprobar guiones en una tabla de Supabase antes de que se generen en
vídeo y se publiquen.

## Restricciones no negociables

1. **Ningún secreto o API key en el código.** Todo va vía variables de
   entorno (`os.environ`) y GitHub Secrets. Si necesitas una key nueva,
   añádela a `.env.example` con un comentario explicando para qué sirve y
   anota en `docs/AUDIT.md` que el usuario debe generarla y cargarla como
   Secret en el repositorio.
2. **Ninguna pieza del pipeline publica nada sin pasar por el estado
   `approved` en la tabla `episodes` de Supabase.** No construyas atajos que
   se salten la revisión humana, aunque parezca "más autopiloto".
3. **Los assets visuales deben venir de fuentes de archivo real con licencia
   libre** (Pexels, Pixabay, Wikimedia Commons, archive.org) — no generes ni
   propongas imágenes IA fotorrealistas de escenas inventadas como
   sustituto. Si el usuario pide explícitamente cambiar esto, es su
   decisión, pero señala que contradice `docs/DECISIONS.md`.
4. **Los scripts deben ser idempotentes.** Un workflow programado puede
   volver a correr por retrasos o reintentos de GitHub Actions; nunca deben
   duplicar publicaciones ni sobrescribir un episodio ya `published`.
5. **X/Twitter no tiene publicación automática por defecto** (la API dejó de
   tener tier gratis en 2026). No asumas que `publish.py` puede publicar en
   X sin que el usuario haya decidido explícitamente pagar por ello o
   confirmado publicación manual — revisa `docs/DECISIONS.md`.

## Stack técnico

- **Lenguaje:** Python 3.11+ para todos los scripts del pipeline.
- **Orquestación:** GitHub Actions (cron), no hay servidor propio.
- **Base de datos:** Supabase (Postgres) vía `supabase-py`. Esquema en
  `db/schema.sql`.
- **Voz:** Edge-TTS por defecto (gratis). Si el usuario configura
  `ELEVENLABS_API_KEY`, úsalo como alternativa de mayor calidad.
- **Vídeo:** ffmpeg / MoviePy, todo dentro del runner de Actions.
- **Publicación:** YouTube Data API v3, Meta Graph API (Instagram/Facebook).

## Convenciones de código

- Usa `logging`, no `print`, para cualquier cosa que corra dentro de un
  workflow — los logs de Actions son la única forma de depurar sin acceso a
  un servidor.
- Cada función que toque la base de datos o una API externa debe capturar
  excepciones y dejar constancia del fallo en la tabla `pipeline_log` de
  Supabase (no solo en el log de Actions, que se pierde a los 90 días).
- Nombres de variables de entorno en `MAYUSCULAS_CON_GUION_BAJO`.
- Comentarios de código en español; nombres de funciones/variables en inglés
  (convención estándar, mejor soporte de herramientas).

## Cómo trabajar en este repo

- Antes de tocar `scripts/publish.py`, relee la sección de restricciones
  arriba — es la parte con más riesgo de romper algo en producción o de
  saltarse la revisión humana.
- Si añades un paso nuevo al pipeline, actualízalo también en
  `docs/ARCHITECTURE.md` y añade la tarea correspondiente en
  `docs/AUDIT.md`.
- Si no sabes si algo requiere una cuenta/consola externa (Google Cloud,
  Meta for Developers, Supabase), asume que sí y añádelo como tarea manual
  en `docs/AUDIT.md` en vez de intentar automatizarlo con credenciales que
  no existen.
