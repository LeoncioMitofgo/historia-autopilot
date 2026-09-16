---
description: "Convenciones para los workflows de GitHub Actions"
applyTo: ".github/workflows/**"
---

- Todos los secretos se referencian como `${{ secrets.NOMBRE }}`, nunca en
  texto plano. Si un workflow necesita una key nueva, añádela a
  `.env.example` y a `docs/AUDIT.md` como tarea manual del usuario (crear el
  Secret en Settings → Secrets and variables → Actions).
- Usa `timeout-minutes` explícito en cada job (los runners gratuitos tienen
  límite de 6h, pero un job colgado desperdicia minutos gratis del plan).
- Los workflows programados (`schedule: cron`) deben incluir también
  `workflow_dispatch:` para poder lanzarlos manualmente desde la pestaña
  Actions al probar o depurar.
- GitHub desactiva automáticamente los workflows programados si el
  repositorio lleva 60 días sin ningún commit. El workflow `keepalive.yml`
  existe para evitar esto — no lo borres ni cambies su cron sin avisar en
  `docs/AUDIT.md`.
- Cachea dependencias de Python (`actions/setup-python` con `cache: pip`)
  para no gastar minutos reinstalando en cada corrida.
- Cualquier fallo del pipeline debe dejar constancia en la tabla
  `pipeline_log` de Supabase antes de que el job termine, aunque termine en
  error — así el usuario lo ve desde la tabla sin tener que abrir Actions.
