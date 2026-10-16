# BillMate: estado y próximos pasos

Última actualización: 2026-10-16 (versión 2.0, etiqueta `v2.0`).

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

---

## Hecho en la versión 2.0

### Rediseño de la pantalla de compra

"Agregar Mercados" es ahora una sola pantalla (hoy la página `views/paginas/compra.py`).

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

### Rediseño moderno de toda la aplicación

Toda la aplicación funciona en una sola ventana. Una barra lateral fija muestra las páginas a la derecha:

- **Inicio:** tarjetas de resumen (última compra, total, productos, gasto del mes) y la tabla de la última compra.
- **Productos, Facturas, Comercios y Compras:** una página por dato que une lo que antes eran "Registrar" y "Consultar". Tiene buscador, tabla y un panel que crea un registro nuevo o edita el seleccionado.
- **Mercados:** búsqueda por producto, factura o compra, edición con autocompletado y eliminación con confirmación.
- **Agregar Mercados:** la pantalla de compra como página, con el selector de fecha nuevo; el calendario se abre con el botón o con un clic en el campo.

| Cambio | Commit |
|---|---|
| Autocompletado sin demoras (la lista se cerraba sola y la ventana perdía la activación) y botón "Agregar" visible | `142c8ec` |
| Pantalla de inicio rediseñada | `74c57d0` |
| Resto de pantallas como páginas, componentes comunes y retiro de las ventanas viejas | `a2d42b8` |

Decisiones tomadas:

- Las pantallas se abren dentro de la ventana principal, no en ventanas aparte.
- Registrar y consultar cada dato se hace en la misma página.

### Logo y versión 2.0

| Cambio | Commit |
|---|---|
| Logo nuevo y nítido (bolsa de compras con "B"), generado por `config_setup/generar_logo.py` | `4b5109d` |
| Versión 2.0 en el instalador (probado con una base nueva, con una de la 1.9 y con una de la 1.8) | `0f9d32c` |

Opcional: crear un Release en GitHub desde la etiqueta `v2.0` y adjuntar `BillMate_windowns_setup.exe`.

---

## Otros pendientes detectados

| Tema | Detalle |
|---|---|
| Base de datos en el historial de GitHub | Se dejó de versionar, pero los commits de 2024 aún tienen `database/BillMate.db`. Si contiene datos que no deben ser públicos, hay que reescribir el historial. |
| Git en esta carpeta | La carpeta pertenece a otro usuario de Windows. Para usar git desde la terminal o VS Code: `git config --global --add safe.directory D:/BillMate`. |
