---
description: "Implementar o completar un script del pipeline siguiendo el contrato acordado"
---

Vamos a implementar (o completar) uno de los scripts de `scripts/`.

Antes de escribir código:
1. Relee `docs/ARCHITECTURE.md` para confirmar en qué punto del pipeline
   encaja este script — qué recibe como entrada y qué debe dejar escrito en
   Supabase al terminar.
2. Relee el docstring/TODO existente en el archivo: define el contrato
   (inputs, outputs, tabla que actualiza) y no debe romperse.
3. Revisa `.github/instructions/python-scripts.instructions.md` para las
   convenciones obligatorias (logging, manejo de errores, variables de
   entorno).

Al terminar:
- Actualiza `docs/AUDIT.md` marcando la tarea correspondiente como hecha.
- Si el script necesita una API key nueva, añádela a `.env.example` con un
  comentario y crea la tarea manual correspondiente en `docs/AUDIT.md`.
- Escribe (o actualiza) un test mínimo en `scripts/tests/` que se pueda
  correr en local con datos de ejemplo, sin gastar cuota de ninguna API de
  pago.
