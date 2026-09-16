# Decisiones estratégicas — memoria del proyecto

Este documento existe para que ni tú ni Copilot tengáis que re-discutir
desde cero decisiones ya tomadas. Si una decisión cambia, edítala aquí con
fecha, para que quede rastro.

## 1. Nicho: historia real poco conocida, no "historia alternativa" ficticia

Se descartó el concepto original de escenas ficticias tipo "Nueva York si
Roma no hubiera caído" como eje visual principal. Motivo: las imágenes
fotorrealistas de IA de escenas inventadas son exactamente el tipo de
contenido que Meta y X están penalizando con reducción de alcance en 2026
(etiquetado obligatorio de contenido "Imagined with AI", fatiga de
audiencia hacia el "AI slop"). Se mantiene el gancho narrativo ("dato
sorprendente + pregunta de cierre") pero aplicado a hechos históricos reales
y documentados, ilustrados con metraje/imágenes de archivo reales.

## 2. Plataforma principal: YouTube, no Instagram/Facebook/X

YouTube tiene la infraestructura de monetización más madura para este
modelo (AdSense, fondo de Shorts) y es más tolerante con el ciclo de
publicación en lote. Instagram y Facebook son distribución secundaria del
mismo activo. X queda fuera del autopiloto por defecto (ver punto 4).

## 3. Intervención humana mínima, no cero

La automatización 100% sin ningún toque humano no es viable de forma
sostenida: el contenido sin ninguna revisión falla las políticas de
"contenido reciclado sin valor añadido" de las plataformas y arriesga
publicar errores históricos. Se mantiene un único punto de revisión
humana: aprobar el `status` de cada episodio en la tabla `episodes` de
Supabase, ~30-60 min por lote mensual. Nada se publica sin pasar por
`approved`.

## 4. X/Twitter: fuera del pipeline automático por defecto

Desde 2026 la API de X ya no tiene tier gratis para publicar (pago por uso,
~$0.015/post). Mientras no se decida explícitamente pagar por ello, `publish.py`
no debe incluir un cliente de X. Si en el futuro se decide activarlo, la
decisión y el presupuesto aprobado deben anotarse aquí con fecha.

## 5. Base de datos: Supabase, no SQLite local

Se eligió Supabase sobre una base de datos local porque su editor de tablas
en el navegador funciona como panel de aprobación gratuito, sin necesidad de
construir una interfaz propia.

## 6. LLM para guiones: Gemini API (gratis) por defecto, con entrada manual como alternativa

Google Gemini API (modelos Flash) es el proveedor por defecto: gratis, sin
tarjeta, con margen de sobra para el volumen mensual de este proyecto (tier
gratuito hasta 1.500 peticiones/día). Groq y OpenRouter quedan como
alternativas gratuitas de respaldo si Gemini cambia sus límites. Cohere
queda descartado pese a tener tier gratis: prohíbe uso comercial en sus
términos, y este proyecto busca monetizar.

`generate_script.py` es un paso opcional, no obligatorio: como la tabla
`episodes` se puede editar a mano desde el panel de Supabase, cualquier mes
se puede sustituir por escribir guiones manualmente (o generarlos en un chat
gratuito como Claude.ai/Gemini/Le Chat) e insertarlos directamente con
`status = pending_review` o `approved`. El resto del pipeline no distingue
el origen del guion.
