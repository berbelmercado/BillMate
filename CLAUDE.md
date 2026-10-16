# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

BillMate is a Windows desktop app (CustomTkinter + SQLite) for recording grocery purchases ("mercados"): invoices, stores, products, and the line items bought. The codebase, identifiers, comments, and UI text are in Spanish — keep new code consistent with that.

## Commands

Run everything from the repo root: when running from source, DB and image paths are resolved relative to the current working directory (see "Resource paths" below).

```powershell
# Activate the bundled virtualenv (Python 3.13)
.\envBillMate\Scripts\Activate.ps1

# Install dependencies (the `librerias` file is a pip freeze, UTF-16 encoded)
pip install -r librerias

# Run the app
python main.py

# Tests (dev dependency: pip install -r requirements-dev.txt)
python -m pytest                                    # all tests
python -m pytest tests/test_controladores.py -k apostrofes   # one test
```

Tests call controllers/models directly (no GUI). The `bd` fixture in `tests/conftest.py` chdirs into `tmp_path` and builds the schema, so `ruta_base_datos()` resolves to a throwaway `./database/BillMate.db` and the real DB is never touched; `empaquetado` simulates a PyInstaller build (`sys.frozen`, `sys._MEIPASS`, `APPDATA`). No linter or formatter is configured.

Git commands fail with "dubious ownership" unless run as `git -c safe.directory=D:/BillMate ...` (or after adding it to the global config).

Planned work and the purchase-screen redesign are tracked in `docs/pendientes-y-rediseno.md`.

### Packaging

1. PyInstaller via auto-py-to-exe, using `config_setup/auto-py-to-exe.json` (one-folder, windowed, bundles `img/` and the `customtkinter` package as data; the database is intentionally not bundled). Output goes to `output/main/`.
2. Inno Setup script `config_setup/config_setup.iss` wraps `output/main/main.exe` + `_internal/` into `BillMate_windowns_setup.exe`. Bump `MyAppVersion` there when releasing.

Both configs contain absolute `D:/BillMate/...` paths.

## Architecture

MVC layout with three packages; the flow is always **view → controller → model → SQLite**.

- `main.py` — calls `crearBdController.existeBase()` (creates the DB if missing and applies pending schema migrations), then builds `VentanaPrincipal` with `FrameMenu` (left menu) and `TreviewUltimoMercado` (main table of the latest purchase). Startup errors are also shown in a message box, since the packaged exe has no console.
- `model/` — one class per table, plus `conexionDb.ConexionDb`. Every model method opens a fresh `ConexionDb()` (which enables `PRAGMA foreign_keys`), runs parameterized SQL (`?`), and calls `desconectar()` (which commits and closes). `UML/Modelo relacional.png` shows the relational model.
- **Schema and migrations** — `model/crearTablasBd.CreacionBbBillMate` creates the original schema (version 0) and must not be edited. `model/migraciones.MIGRACIONES` holds one function per version; `aplicarMigraciones()` tracks the version in `PRAGMA user_version`, backs up an existing DB to `BillMate.db.respaldo-v<N>` first, and runs each migration in a transaction that is rolled back on failure. To change the schema, append a new function to `MIGRACIONES` (never edit a released one) and add a test in `tests/test_migraciones.py`. Note that the Python attribute is still `describcionCompra` while the column is `compras.descripcion`.
- `controller/` — one controller per entity. Controllers take all the entity's fields in the constructor, validate input, instantiate the model, and return a result list `mensaje = [status, text]` where `1` = success and `0` = error (query methods return `(rows, mensaje)`). Views check `mensaje[0]` and show `mensajesEmergentes.mensajeInformativo` / `mensajeError`.
- Price input is parsed by `controller/validaciones.convertirNumero` (Colombian format: `.` thousands separator, `,` decimal; `1.500` → 1500, `12.5` → 12.5) and written back with `formatearNumero`. Use these instead of `float()` on user input.
- `views/` — `ventanaPrincipal`, `frameMenu`, `frameListasTreview`, `frameTotal` (running total widget). Each register/query screen is a `CTkToplevel` in `views/ventanasSecundarias/`. Layout uses absolute `place()` coordinates.

### Styling and layout config

Colors, fonts, and widget sizes/positions are not hard-coded in widgets; they come from dictionaries in `views/configuracionesGenerales.py` (main window) and `views/ventanasSecundarias/configuracionVentanasSecundarias.py` (secondary windows). Icon paths are mapped by name in `views/vwImgConfig.py` (`leerImagen("Guardar")`, etc.). Add new values to these dicts rather than inlining them.

### Purchase workflow (mercadosTemp → mercados)

Line items being entered in `agregarMercados.py` are first written to the staging table `mercadosTemp` (add/edit/delete freely). "Cargar compra" (`fnCargarCompraController` → `cargarCompraModel`) copies all rows into `mercados`, deletes the staging rows, and resets the `mercadosTemp` autoincrement sequence. A `mercados` row links `compras` (a purchase batch), `facturas`, `productos`, and `comercios`.

### Resource paths

- **Database:** always obtained from `model/rutas.ruta_base_datos()`. Frozen (PyInstaller): `%APPDATA%\BillMate\BillMate.db`, so it is writable without admin rights and survives reinstall/uninstall; on first run it copies a v1.6 DB from `_MEIPASS\Database` if one exists. From source: `database/BillMate.db` in the repo (gitignored, so a fresh checkout creates an empty DB). The "Carpeta de datos" menu button opens that folder.
- **Images:** `views/vwImgConfig.resource_path()` uses `sys._MEIPASS` when bundled, else `os.path.abspath(".")`.
