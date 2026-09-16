"""Publica episodios 'ready_to_publish' en YouTube y, si está configurado,
en Instagram/Facebook.

CONTRATO:
  Entrada:  episodios con status='ready_to_publish'.
  Salida:   youtube_url (y instagram_url/facebook_url si aplica) rellenados,
            status -> 'published'. Si falla una plataforma, NO marcar
            'published' hasta que todas las plataformas activas confirmen
            éxito -- mejor reintentar en la siguiente corrida que dar por
            publicado algo a medias.

NOTA IMPORTANTE (ver docs/DECISIONS.md punto 4):
  X/Twitter queda deliberadamente FUERA de este script por defecto. La API
  de X no tiene tier gratis desde 2026. No añadir un cliente de X aquí sin
  que el usuario haya confirmado explícitamente el presupuesto en
  docs/DECISIONS.md.

TODO (Copilot): implementar YouTube Data API v3 (OAuth con refresh token) y
Meta Graph API (Instagram/Facebook, usando el token de la app en modo
Tester -- ver docs/AUDIT.md).
"""
import logging

from dotenv import load_dotenv

from _supabase_client import get_client, log_event

load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def fetch_ready_to_publish() -> list[dict]:
    resp = (
        get_client()
        .table("episodes")
        .select("*")
        .eq("status", "ready_to_publish")
        .execute()
    )
    return resp.data


def publish_to_youtube(episode: dict) -> str:
    """TODO: subir video_path a YouTube, devolver la URL publicada."""
    raise NotImplementedError("Completar con YouTube Data API v3.")


def publish_to_meta(episode: dict) -> dict:
    """TODO: publicar en Instagram y/o Facebook vía Graph API.
    Devuelve {'instagram_url': ..., 'facebook_url': ...} (claves opcionales
    según qué plataformas estén configuradas)."""
    raise NotImplementedError("Completar con Meta Graph API.")


def main() -> None:
    client = get_client()
    for episode in fetch_ready_to_publish():
        try:
            youtube_url = publish_to_youtube(episode)
            meta_urls = publish_to_meta(episode)
            client.table("episodes").update({
                "youtube_url": youtube_url,
                "instagram_url": meta_urls.get("instagram_url"),
                "facebook_url": meta_urls.get("facebook_url"),
                "status": "published",
            }).eq("id", episode["id"]).execute()
            log_event(episode["id"], "publish", "Publicado en todas las plataformas activas")
        except Exception as exc:  # noqa: BLE001
            log.exception("Fallo publicando episodio %s", episode["id"])
            log_event(episode["id"], "publish", str(exc), level="error")


if __name__ == "__main__":
    main()
