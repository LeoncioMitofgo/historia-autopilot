"""Cliente Supabase compartido por todos los scripts del pipeline.

No instanciar el cliente en otro sitio: importar `get_client()` desde aquí.
"""
import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


@lru_cache(maxsize=1)
def get_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Faltan SUPABASE_URL / SUPABASE_KEY en el entorno. "
            "Revisa .env (local) o los Secrets del repo (Actions)."
        )
    return create_client(url, key)


def log_event(episode_id: str | None, step: str, message: str,
              level: str = "info", estimated_cost_usd: float | None = None) -> None:
    """Escribe un evento en pipeline_log. Llamar desde cada script,
    tanto en éxito como en error, según las instrucciones del repo."""
    get_client().table("pipeline_log").insert({
        "episode_id": episode_id,
        "step": step,
        "level": level,
        "message": message,
        "estimated_cost_usd": estimated_cost_usd,
    }).execute()
