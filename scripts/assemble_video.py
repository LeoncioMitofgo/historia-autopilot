"""Ensambla audio + assets + subtítulos en el vídeo final.

CONTRATO:
  Entrada:  episodios con audio_path y asset_plan no nulos, video_path null.
  Salida:   vídeo final subido a Supabase Storage (bucket 'video'),
            episodes.video_path actualizado, status -> 'ready_to_publish'.

TODO (Copilot): implementar el ensamblado con ffmpeg/MoviePy dentro del
runner de GitHub Actions. Generar subtítulos a partir del propio script
(no depender de un servicio externo de transcripción, ya tenemos el texto).
"""
import logging

from dotenv import load_dotenv

from _supabase_client import get_client, log_event

load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def fetch_ready_to_assemble() -> list[dict]:
    resp = (
        get_client()
        .table("episodes")
        .select("*")
        .not_.is_("audio_path", "null")
        .not_.is_("asset_plan", "null")
        .is_("video_path", "null")
        .execute()
    )
    return resp.data


def assemble(episode: dict) -> str:
    """TODO: ensamblar el vídeo final y devolver su ruta/URL en Storage."""
    raise NotImplementedError("Completar con ffmpeg/MoviePy.")


def main() -> None:
    client = get_client()
    for episode in fetch_ready_to_assemble():
        try:
            video_path = assemble(episode)
            client.table("episodes").update({
                "video_path": video_path,
                "status": "ready_to_publish",
            }).eq("id", episode["id"]).execute()
            log_event(episode["id"], "assemble_video", "Vídeo ensamblado")
        except Exception as exc:  # noqa: BLE001
            log.exception("Fallo ensamblando vídeo para %s", episode["id"])
            log_event(episode["id"], "assemble_video", str(exc), level="error")


if __name__ == "__main__":
    main()
