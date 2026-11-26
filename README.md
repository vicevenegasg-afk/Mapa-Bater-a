# Mapa de batería

App web para anotar, desde la batería, la estructura de cada canción: dinámica de cada parte (Silencio, Cerrado, Acompañamiento, Build up, Abierto), fills, golpes, cortes, platos y notas. Incluye un modo en vivo con las próximas tres partes y una barra de avance.

## Instalar en el iPhone
1. Abre la página de GitHub Pages de este repositorio en **Safari**.
2. Toca **Compartir** → **Agregar a pantalla de inicio**.
3. Abre la app desde el ícono. Funciona sin internet.

Las canciones se guardan en el teléfono. Usa **⋯ → Exportar respaldo** de vez en cuando.

## Actualizar
`index.html`, `sw.js` y `seed.js` se generan con `python3 build.py` desde `app.html` (fuente de la app).
