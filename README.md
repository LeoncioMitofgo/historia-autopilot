# Historia Autopilot

Pipeline de contenido (historia real, narrado, evergreen) casi
completamente automatizado: guiones en lote, voz IA, montaje y publicación
en YouTube / Instagram / Facebook, con un único punto de revisión humana.

## Empieza aquí

1. Abre este repo en VS Code con GitHub Copilot activado.
2. Lee **`docs/AUDIT.md`** — la primera mitad son cuentas/consolas que solo
   tú puedes crear (Supabase, Google Cloud, Meta for Developers). Hazlas
   antes de pedirle nada a Copilot.
3. Copia `.env.example` a `.env` y rellénalo a medida que vayas creando esas
   cuentas.
4. Pide a Copilot Chat, por ejemplo: *"usa el prompt build-pipeline-step
   para completar generate_script.py"* — ya tiene todo el contexto del
   proyecto vía `.github/copilot-instructions.md`.

## Memoria del proyecto (para ti y para Copilot)

- `docs/DECISIONS.md` — por qué el proyecto es como es (nicho, plataformas,
  qué se descartó y por qué).
- `docs/ARCHITECTURE.md` — cómo encajan las piezas.
- `docs/AUDIT.md` — checklist vivo de tareas, tuyas y de Copilot.

## Estructura

```
.github/
  copilot-instructions.md      # memoria principal para Copilot
  instructions/                # reglas específicas por tipo de archivo
  prompts/                     # prompts reutilizables
  workflows/                   # generate.yml, publish.yml, keepalive.yml
scripts/                       # el pipeline en Python (stubs para Copilot)
db/schema.sql                  # esquema de Supabase, listo para ejecutar
docs/                          # memoria del proyecto
```
