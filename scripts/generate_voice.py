"""Convierte el script de un episodio 'approved' en audio.

CONTRATO:
  Entrada:  episodios con status='approved' y audio_path is null.
  Salida:   archivo de audio subido a Supabase Storage (bucket 'audio'),
            episodes.audio_path actualizado, status sigue en 'approved'
            (assemble_video.py decide el siguiente paso).

TODO (Copilot): implementar Edge-TTS como motor por defecto (gratis). Si
existe ELEVENLABS_API_KEY en el entorno, usar ElevenLabs como alternativa
de mayor calidad. Ver .github/instructions/python-scripts.instructions.md
para las convenciones de logging y manejo de errores.
"""
import logging

from dotenv import load_dotenv

from _supabase_client import get_client, log_event

load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def fetch_approved_without_audio() -> list[dict]:
    resp = (
        get_client()
        .table("episodes")
        .select("*")
        .eq("status", "approved")
        .is_("audio_path", "null")
        .execute()
    )
    return resp.data


def synthesize_voice(script: str, episode_id: str) -> str:
    """TODO: generar el audio y subirlo a Supabase Storage.
    Devuelve la ruta/URL final del archivo."""
    raise NotImplementedError("Completar con Edge-TTS / ElevenLabs.")


def main() -> None:
    client = get_client()
    for episode in fetch_approved_without_audio():
        try:
            audio_path = synthesize_voice(episode["script"], episode["id"])
            client.table("episodes").update({"audio_path": audio_path}).eq(
                "id", episode["id"]
            ).execute()
            log_event(episode["id"], "generate_voice", "Audio generado")
        except Exception as exc:  # noqa: BLE001
            log.exception("Fallo generando audio para %s", episode["id"])
            log_event(episode["id"], "generate_voice", str(exc), level="error")


if __name__ == "__main__":
    main()
