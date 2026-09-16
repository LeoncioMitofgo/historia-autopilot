"""Genera guiones a partir de la cola de `topics` y los deja en `episodes`
con status='pending_review'.

CONTRATO (no romper esto al implementar):
  Entrada:  filas de `topics` con used = false.
  Salida:   una fila nueva en `episodes` por cada topic procesado, con
            title, hook, script, citations y status='pending_review'.
            Marcar el topic como used=true al terminar.

TODO (Copilot): implementar la llamada real al proveedor de LLM elegido
(ver .env.example para el nombre de la variable de entorno de la API key).
El guion debe seguir la estructura: gancho -> dato histórico verificable
con su fuente -> pregunta de cierre. Ver docs/DECISIONS.md punto 1: son
hechos reales documentados, no escenarios ficticios.
"""
import logging
import os

from dotenv import load_dotenv

from _supabase_client import get_client, log_event

load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BATCH_SIZE = int(os.environ.get("SCRIPT_BATCH_SIZE", "10"))


def fetch_pending_topics(limit: int = BATCH_SIZE) -> list[dict]:
    resp = (
        get_client()
        .table("topics")
        .select("*")
        .eq("used", False)
        .limit(limit)
        .execute()
    )
    return resp.data


def generate_script_for_topic(topic: dict) -> dict:
    """TODO: llamar al LLM real. Devuelve un dict con
    title, hook, script, citations (todos str)."""
    raise NotImplementedError(
        "Completar con la llamada al proveedor de LLM elegido. "
        "Ver docs/AUDIT.md para decidir el proveedor antes de implementar."
    )


def main() -> None:
    client = get_client()
    topics = fetch_pending_topics()
    log.info("Topics pendientes: %d", len(topics))

    for topic in topics:
        try:
            result = generate_script_for_topic(topic)
            client.table("episodes").insert({
                "topic_id": topic["id"],
                "title": result["title"],
                "hook": result["hook"],
                "script": result["script"],
                "citations": result["citations"],
                "status": "pending_review",
            }).execute()
            client.table("topics").update({"used": True}).eq("id", topic["id"]).execute()
            log_event(None, "generate_script", f"Guion generado para topic {topic['id']}")
        except Exception as exc:  # noqa: BLE001 - se registra y se continúa con el resto
            log.exception("Fallo generando guion para topic %s", topic["id"])
            log_event(None, "generate_script", str(exc), level="error")


if __name__ == "__main__":
    main()
