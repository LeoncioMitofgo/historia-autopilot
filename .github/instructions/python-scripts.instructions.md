---
description: "Convenciones para los scripts Python del pipeline"
applyTo: "scripts/**/*.py"
---

- Cada script debe poder ejecutarse de forma aislada (`python scripts/x.py`)
  para poder probarlo en local antes de meterlo en un workflow.
- Lee toda configuración vía variables de entorno con `os.environ.get(...)`,
  nunca hardcodeada. Si falta una variable obligatoria, falla rápido con un
  mensaje claro en vez de continuar con un valor por defecto silencioso.
- Usa `from dotenv import load_dotenv` + `load_dotenv()` al inicio de cada
  script para que funcione igual en local (con `.env`) y en Actions (con
  Secrets inyectados como variables de entorno).
- Todas las llamadas a Supabase deben usar el cliente `supabase-py` ya
  configurado en `scripts/_supabase_client.py` (créalo si no existe) — no
  reinstancies el cliente en cada script.
- Cualquier función que genere contenido (guion, voz, vídeo) debe escribir
  su resultado con un `status` explícito en la tabla `episodes`
  (`draft`, `pending_review`, `approved`, `rendering`, `published`,
  `rejected`, `error`). Nunca dejes un registro sin `status`.
- Los scripts que llaman a APIs externas de pago (LLM, ElevenLabs) deben
  registrar el coste estimado de la llamada en `pipeline_log` para que el
  usuario pueda auditar gasto mensual desde Supabase.
