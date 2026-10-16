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
```

There is no test suite, linter, or formatter configured.

### Packaging

1. PyInstaller via auto-py-to-exe, using `config_setup/auto-py-to-exe.json` (one-folder, windowed, bundles `img/` and the `customtkinter` package as data; the database is intentionally not bundled). Output goes to `output/main/`.
2. Inno Setup script `config_setup/config_setup.iss` wraps `output/main/main.exe` + `_internal/` into `BillMate_windowns_setup.exe`. Bump `MyAppVersion` there when releasing.

Both configs contain absolute `D:/BillMate/...` paths.

## Architecture

MVC layout with three packages; the flow is always **view → controller → model → SQLite**.

- `main.py` — calls `crearBdController.existeBase()` (creates the DB schema if `Database\BillMate.db` is missing), then builds `VentanaPrincipal` with `FrameMenu` (left menu) and `TreviewUltimoMercado` (main table of the latest purchase).
- `model/` — one class per table, plus `conexionDb.ConexionDb`. Every model method opens a fresh `ConexionDb()`, runs raw SQL built with f-strings, and calls `desconectar()` (which commits and closes). Schema lives in `model/crearTablasBd.py`; `UML/Modelo relacional.png` shows the relational model.
- `controller/` — one controller per entity. Controllers take all the entity's fields in the constructor, validate input, instantiate the model, and return a result list `mensaje = [status, text]` where `1` = success and `0` = error (query methods return `(rows, mensaje)`). Views check `mensaje[0]` and show `mensajesEmergentes.mensajeInformativo` / `mensajeError`.
- `views/` — `ventanaPrincipal`, `frameMenu`, `frameListasTreview`, `frameTotal` (running total widget). Each register/query screen is a `CTkToplevel` in `views/ventanasSecundarias/`. Layout uses absolute `place()` coordinates.

### Styling and layout config

Colors, fonts, and widget sizes/positions are not hard-coded in widgets; they come from dictionaries in `views/configuracionesGenerales.py` (main window) and `views/ventanasSecundarias/configuracionVentanasSecundarias.py` (secondary windows). Icon paths are mapped by name in `views/vwImgConfig.py` (`leerImagen("Guardar")`, etc.). Add new values to these dicts rather than inlining them.

### Purchase workflow (mercadosTemp → mercados)

Line items being entered in `agregarMercados.py` are first written to the staging table `mercadosTemp` (add/edit/delete freely). "Cargar compra" (`fnCargarCompraController` → `cargarCompraModel`) copies all rows into `mercados`, deletes the staging rows, and resets the `mercadosTemp` autoincrement sequence. A `mercados` row links `compras` (a purchase batch), `facturas`, `productos`, and `comercios`.

### Resource paths

- **Database:** always obtained from `model/rutas.ruta_base_datos()`. Frozen (PyInstaller): `%APPDATA%\BillMate\BillMate.db`, so it is writable without admin rights and survives reinstall/uninstall; on first run it copies a v1.6 DB from `_MEIPASS\Database` if one exists. From source: `database/BillMate.db` in the repo (gitignored, so a fresh checkout creates an empty DB). The "Carpeta de datos" menu button opens that folder.
- **Images:** `views/vwImgConfig.resource_path()` uses `sys._MEIPASS` when bundled, else `os.path.abspath(".")`.
