"""Busca metraje/imágenes de archivo REALES que encajen con el guion.

CONTRATO:
  Entrada:  episodios con audio_path is not null y asset_plan is null.
  Salida:   episodes.asset_plan actualizado con una lista jsonb de
            {source, url, license, query_used} por cada clip/imagen elegido.

TODO (Copilot): integrar Pexels, Pixabay, Wikimedia Commons y/o archive.org
(todas gratis). Ver docs/DECISIONS.md punto 1: nunca sustituir esto por
generación de imágenes IA fotorrealistas de escenas inventadas.
"""
import logging

from dotenv import load_dotenv

from _supabase_client import get_client, log_event

load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def fetch_episodes_needing_assets() -> list[dict]:
    resp = (
        get_client()
        .table("episodes")
        .select("*")
        .not_.is_("audio_path", "null")
        .is_("asset_plan", "null")
        .execute()
    )
    return resp.data


def find_assets_for_script(script: str) -> list[dict]:
    """TODO: extraer temas clave del guion y buscar assets reales en las
    APIs de archivo elegidas. Devuelve una lista de dicts serializables."""
    raise NotImplementedError("Completar con Pexels/Pixabay/Wikimedia/archive.org.")


def main() -> None:
    client = get_client()
    for episode in fetch_episodes_needing_assets():
        try:
            assets = find_assets_for_script(episode["script"])
            client.table("episodes").update({"asset_plan": assets}).eq(
                "id", episode["id"]
            ).execute()
            log_event(episode["id"], "fetch_assets", f"{len(assets)} assets encontrados")
        except Exception as exc:  # noqa: BLE001
            log.exception("Fallo buscando assets para %s", episode["id"])
            log_event(episode["id"], "fetch_assets", str(exc), level="error")


if __name__ == "__main__":
    main()
