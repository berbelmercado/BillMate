# BillMate: estado y próximos pasos

Última actualización: 2026-10-16 (versión 1.9, etiqueta `v1.9`).

## Hecho en la versión 1.8

| Mejora | Commit |
|---|---|
| Base de datos en `%APPDATA%\BillMate` y botón "Carpeta de datos" | `bcd5e1a` |
| Manejo de errores en controladores (`sqlite3.Error`, mensajes con detalle) | `7588d6f` |
| SQL con parámetros (los nombres con apóstrofe funcionan) | `d0894ae` |
| Pruebas automáticas con pytest (`python -m pytest`) | `5bba4e9` |
| Migraciones del esquema (`PRAGMA user_version`), claves foráneas reales, respaldo automático | `0f1ca3f` |
| Precios con formato colombiano (`12.500` = 12500) | `fa30395` |
| Versión 1.8 en el instalador | `dfb8125` |

## Hecho en la versión 1.9

| Mejora | Commit |
|---|---|
| Mensaje de campos vacíos en comercios corregido; los listados de comercios, facturas y compras muestran los errores de la base de datos | `4afadc3` |
| Ventanas con `transient()` en lugar de `-topmost` (ya no quedan encima de otros programas); los mensajes salen sobre la ventana activa sin crear un `Tk()` nuevo | `c812960` |
| La ventana principal ya no queda bloqueada tras cargar factura o comercio en "Agregar Mercados" ni tras un error en "Registrar Factura"; "Registrar Compras" tiene título | `322d189` |
| Errata `describcion` corregida a `descripcion` en el código y en los textos de pantalla | `d8fd28f` |
| Fechas de factura en `AAAA-MM-DD` como las de compras (migración 2 y calendarios) | `f156889` |
| Una escritura fallida ya no deja la base bloqueada ("database is locked") | `3faa6d1` |
| Productos duplicados unidos (migración 3) y nombre de producto único | `c06dd36` |
| Controladores como funciones con parámetros (productos, comercios, facturas, compras, mercados), con varias correcciones de paso | `3205323`, `82dac4c`, `2daa39b`, `c45e451`, `8157db8` |
| Versión 1.9 en el instalador (probado sobre una base de la 1.8) | `37352d8` |

Opcional: crear un Release en GitHub desde la etiqueta `v1.9` y adjuntar `BillMate_windowns_setup.exe`.

---

## Hecho después de la 1.9 (para la próxima versión)

### Rediseño de la pantalla de compra

"Agregar Mercados" abre ahora una sola ventana (`views/ventanasSecundarias/nuevaCompra.py`).

- Encabezado con compra, factura y comercio. Se eligen una vez con autocompletado y se pueden crear ahí mismo.
- Línea de ingreso que se maneja con Enter, con el total sugerido.
- Tabla con precios `$ 12.500`, edición con doble clic y borrado con Supr.
- Cuadre con la factura en el pie.
- Carga de la compra con Ctrl+Enter.
- Distribución con `grid`; la ventana es redimensionable y cabe en 1366×768.

| Fase | Commit |
|---|---|
| 1. Ids de lo creado, `formatearMoneda`, `cantidadNumerica`, `cuadreFacturas`, `preguntar` | `4044a74` |
| 2. Pantalla nueva con `CampoAutocompletar`, línea de ingreso, tabla y carga | `ba41d05` |
| 3. Cuadre en el pie, confirmación al cargar, retiro de `agregarMercados.py` | `3d70f5b` |

Decisiones tomadas:

- El cuadre con la factura solo avisa: si no cuadra, al cargar pregunta "¿Cargar de todas formas?".
- Se trabaja una factura por vez en el encabezado. Cada ítem conserva su factura, y el cuadre es por factura.
- La pantalla nueva reemplazó a la anterior.
- Crear productos, comercios, facturas o compras desde el autocompletado no pide confirmación. El comercio pide la dirección.
- La cantidad sigue siendo texto libre. Si empieza con un número ("2", "0.8k"), el total sugerido es ese número × el precio. El total siempre se puede escribir a mano.

---

## Otros pendientes detectados

| Tema | Detalle |
|---|---|
| Base de datos en el historial de GitHub | Se dejó de versionar, pero los commits de 2024 aún tienen `database/BillMate.db`. Si contiene datos que no deben ser públicos, hay que reescribir el historial. |
| Git en esta carpeta | La carpeta pertenece a otro usuario de Windows. Para usar git desde la terminal o VS Code: `git config --global --add safe.directory D:/BillMate`. |
