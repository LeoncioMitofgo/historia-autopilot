---
description: "Preparar el lote semanal de guiones para que el usuario los revise en Supabase"
---

Genera un resumen legible (no una tabla SQL cruda) de los episodios en
estado `pending_review` de la tabla `episodes`: título provisional, gancho
de apertura, fuente del dato histórico citado, y qué activos visuales de
archivo se usarían. El objetivo es que el usuario pueda aprobar o rechazar
cada uno en menos de un minuto por episodio, sin tener que abrir Supabase
para leer el guion completo salvo que algo le genere dudas.

No apruebes ni cambies el `status` de ningún episodio — eso lo decide
siempre el usuario manualmente en la tabla.
