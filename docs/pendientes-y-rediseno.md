# BillMate: estado y próximos pasos

Última actualización: 2026-10-16 (versión 1.8, etiqueta `v1.8`).

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

## Hecho después de la 1.8

| Mejora | Commit |
|---|---|
| Mensaje de campos vacíos en comercios corregido; los listados de comercios, facturas y compras muestran los errores de la base de datos | `4afadc3` |
| Ventanas con `transient()` en lugar de `-topmost` (ya no quedan encima de otros programas); los mensajes salen sobre la ventana activa sin crear un `Tk()` nuevo | `c812960` |
| La ventana principal ya no queda bloqueada tras cargar factura o comercio en "Agregar Mercados" ni tras un error en "Registrar Factura"; "Registrar Compras" tiene título | `322d189` |

Pendiente de la 1.8: generar el instalador (auto-py-to-exe con `config_setup/auto-py-to-exe.json` y luego Inno Setup con `config_setup/config_setup.iss`). Opcional: crear un Release en GitHub desde la etiqueta `v1.8` y adjuntar `BillMate_windowns_setup.exe`.

---

## Siguiente gran paso: rediseño de la pantalla de compra

### Cómo funciona hoy (`views/ventanasSecundarias/agregarMercados.py`)

1. Antes de agregar ítems, la compra, la factura y los comercios o productos nuevos se registran por separado, cada uno en su ventana del menú principal.
2. "Agregar Mercados" es una ventana fija de 1345×590, posicionada con `place()`.
3. Por cada producto:
   - el botón "Agregar Productos" abre una ventana de búsqueda;
   - se busca el producto, se selecciona y se presiona "Cargar Producto";
   - se escriben cantidad y precio, y Enter en el precio calcula el total;
   - se presiona "Agregar".
4. La factura, el comercio y la compra se eligen igual, con ventanas de búsqueda. Existen las casillas "Fijar Factura / Compra / Comercio" para no repetirlos.
5. "Cargar Compra" pasa los ítems de `mercadosTemp` a `mercados`.

Son unos 5 clics y una ventana extra por producto. Si el producto no existe, hay que salir a registrarlo.

### Propuesta

```
┌─ Nueva compra ───────────────────────────────────────────────┐
│ Compra: [Quincena octubre    ]  Fecha: [2026-10-16]          │
│ Comercio: [Éxito Cent▾]  Factura: [FE-1234]  Total: [$ 152.300]│
├──────────────────────────────────────────────────────────────┤
│ Producto: [arr▾        ] Cant: [2 ] Precio: [3.500 ] = $ 7.000 [+]│
│           │ Arroz Diana   │                                  │
│           │ Arroz Roa     │   ← autocompleta mientras escribe  │
│           │ + Crear "arr" │   ← o lo crea ahí mismo            │
├──────────────────────────────────────────────────────────────┤
│ Producto        Cant   Precio unidad   Total                 │
│ Arroz Diana     2      $ 3.500         $ 7.000               │
│ Leche Alquería  6      $ 4.200         $ 25.200              │
├──────────────────────────────────────────────────────────────┤
│ Suma ítems: $ 148.900   Factura: $ 152.300   Faltan: $ 3.400 │
│                                      [Cargar compra (Ctrl+↵)]│
└──────────────────────────────────────────────────────────────┘
```

1. **Encabezado que se llena una vez:** compra, comercio y factura se eligen arriba al empezar. Tienen autocompletado y se pueden crear ahí mismo si no existen. La fecha viene con la de hoy. Reemplaza las casillas "Fijar" y las ventanas de búsqueda.
2. **Línea de ingreso rápida:**
   - el producto se autocompleta, con opción "Crear" si no existe;
   - el total se recalcula solo;
   - Enter pasa de campo en campo y, en el último, agrega el ítem y vuelve a "Producto".

   Así una factura completa se registra sin mouse.
3. **Tabla legible:**
   - precios como `$ 12.500`;
   - doble clic para editar y `Supr` para borrar, con confirmación;
   - sin las columnas de factura, comercio y compra, que ya están en el encabezado.
4. **Cuadre con la factura:** compara la suma de los ítems con `facturas.valorTotalFactura` y muestra la diferencia antes de cargar. Hoy ese total se guarda pero no se usa.
5. **Ventana adaptable:** `grid()` con `weight` en lugar de `place()`, redimensionable. Debe funcionar en 1366×768 (la pantalla del autor) y con el escalado de Windows.

### Cambios internos previstos

- **Vistas:** casi todo el trabajo está aquí. El flujo `mercadosTemp` → `mercados` y sus pruebas no cambian.
- **Modelos y controladores:** los `insertar...` de productos, comercios, facturas y compras deben devolver el id creado (`cursor.lastrowid`), para usarlo de inmediato en la compra.
- **Búsquedas para el autocompletado:** ya existen (`consultarProductos`, `consultarComercioModel`, etc., con `LIKE`).
- **Formato de moneda:** se puede apoyar en `controller/validaciones.py`, que ya tiene `convertirNumero` y `formatearNumero`.

### Decisiones abiertas (definir antes de programar)

- ¿El cuadre con la factura solo avisa o impide cargar la compra?
- ¿Una compra puede tener varias facturas, por ejemplo de distintos comercios? Esto cambia el encabezado.
- ¿"Agregar Mercados" se reemplaza o convive un tiempo con la pantalla nueva?
- ¿Crear productos o comercios desde el autocompletado pide confirmación?
- ¿Cómo se maneja la cantidad con unidades ("2 kg")? Hoy es texto libre y el total solo se calcula si es un número.

### Forma de trabajo sugerida

1. Escribir la especificación con las decisiones anteriores (Spec Kit o modo plan de Claude Code).
2. Implementar en fases, cada una usable por sí sola:
   1. Encabezado y autocompletado.
   2. Teclado, formato de precios y cuadre con la factura.
   3. Distribución adaptable con `grid()`.
3. Después de cada fase: `python -m pytest`, prueba manual, commit y push.

---

## Otros pendientes detectados

| Tema | Detalle |
|---|---|
| Productos duplicados | Hay 5 nombres repetidos en `productos`, por ejemplo "Crema Dental" y "Salsa De Tomate". Se podría unificar con una migración y agregar `UNIQUE`. |
| Fechas en dos formatos | `facturas.fechaFactura` usa `2024/09/07` y `compras.fechaCreacion` usa `2024-09-08`. Conviene unificar a `AAAA-MM-DD` con una migración. |
| Base de datos en el historial de GitHub | Se dejó de versionar, pero los commits de 2024 aún tienen `database/BillMate.db`. Si contiene datos que no deben ser públicos, hay que reescribir el historial. |
| Controladores con estado | Reciben todos los campos en el constructor y se instancian con muchos `None`. Se podrían simplificar a funciones con parámetros. |
| Nombre de variable | La columna ya es `compras.descripcion`, pero en Python sigue `describcionCompra`. |
| Git en esta carpeta | La carpeta pertenece a otro usuario de Windows. Para usar git desde la terminal o VS Code: `git config --global --add safe.directory D:/BillMate`. |
