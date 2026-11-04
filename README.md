# Atlas electoral de Uruguay

Atlas interactivo de resultados por departamento, estilo mapa de Wikipedia.
HTML autocontenido: pestañas (ganador, % por fuerza, participación), ficha al
pasar el mouse y descarga en PNG/SVG. Usa el mapa `uruguay.geo.json` de ECharts
(19 departamentos).

> **Importante**: viene con datos de **EJEMPLO** (sello "DEMO"). No son
> oficiales. Reemplazá el dataset con datos de la Corte Electoral antes de
> publicar nada público (ver abajo).

## Archivos

| Archivo | Qué es |
|---|---|
| `atlas_uruguay.html` | El atlas. Abrilo servido por HTTP (no con doble clic). |
| `uruguay.geo.json` | Mapa base de los 19 departamentos (ECharts). |
| `datos_uruguay.json` | Datos de la elección (hoy, DEMO). Es lo único que se reemplaza. |
| `build_desde_csv.py` | Genera `datos_uruguay.json` desde un CSV de la Corte Electoral. |
| `gen_demo.py` | Regenera el dataset de ejemplo (solo para probar). |

## Ver / probar en local

El atlas carga los `.json` por `fetch`, así que necesita un servidor HTTP
(con doble clic en el `.html` el navegador bloquea la carga):

```
cd carpeta-del-atlas
python -m http.server 8080
# abrir http://localhost:8080/atlas_uruguay.html
```

## Cargar datos oficiales

1. Bajá de la Corte Electoral los resultados por departamento y armá un CSV:
   ```
   departamento,partido,votos,habilitados
   Montevideo,Frente Amplio,472500,1050000
   Montevideo,Partido Nacional,189000,1050000
   ...
   ```
   (los nombres de `departamento` deben coincidir con los del mapa).
2. Generá el dataset:
   ```
   python build_desde_csv.py resultados.csv "Presidencial 2024 · 1ª vuelta" pres2024v1
   ```
3. Recargá el atlas. El sello DEMO desaparece solo (queda `demo: false`).

Colores y nombres de cada fuerza se editan en `COLORES` dentro de
`build_desde_csv.py`.

## Subir a GitHub Pages (recomendado, gratis)

1. Repo nuevo (ej. `atlas-uruguay`), público.
2. Subí los 4 archivos a la raíz: `atlas_uruguay.html`, `uruguay.geo.json`,
   `datos_uruguay.json` y (opcional) los `.py`.
3. **Settings → Pages → Source: Deploy from a branch → `main` / `root`**.
4. En 1–2 min queda en `https://<usuario>.github.io/atlas-uruguay/atlas_uruguay.html`.
   (Si lo renombrás `index.html`, queda en la raíz del sitio.)

Alternativa sin repo: Cloudflare Pages (ver abajo).

## ¿Conviene automatizar con Cloudflare?

Depende de si los datos van a **cambiar solos** (noche de elección, actualización
periódica) o son **históricos fijos**:

- **Atlas histórico / estático** (una elección ya cerrada): **no hace falta
  Cloudflare ni nada**. GitHub Pages alcanza. Cada elección nueva es subir un
  `datos_uruguay.json` y listo.

- **Si querés que se actualice solo** (datos en vivo o refresco periódico), ahí
  sí conviene la arquitectura que ya usás en los monitores:
  `GitHub Actions (scrapea/arma el JSON) → Worker /update-url → KV → el atlas lee el JSON del Worker`.
  Es el mismo patrón de BROU/Temas PY. El atlas cambiaría una línea: en vez de
  `DATA_URL = "./datos_uruguay.json"` apuntaría a la URL del Worker
  (`https://<worker>.workers.dev/api/datos`). Ventaja: no tocás el repo en cada
  actualización y servís con caché de Cloudflare.

- **Hosting**: si ya vivís en Cloudflare, **Cloudflare Pages** (conectado al repo
  de GitHub) es equivalente a GitHub Pages y te deja sumar un Worker para los
  datos en el mismo dominio, sin CORS.

**Recomendación**: empezá estático en GitHub Pages (MVP, cero infraestructura).
Pasalo a Worker + KV **solo** si aparece la necesidad de actualización
automática; el atlas ya está preparado para ese cambio (una sola URL).

## Créditos y licencia del mapa

Mapa base `uruguay.geo.json`: proyecto ECharts (Apache 2.0). Verificá la
atribución del contorno si lo publicás. Datos: Corte Electoral de Uruguay.
