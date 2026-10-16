"""Páginas de datos: Productos, Facturas, Comercios y Compras.

Cada una muestra un buscador, la tabla de registros y un panel para crear uno nuevo o editar el seleccionado.
La lógica común está en PaginaDatos; cada subclase solo dice qué columnas y campos tiene y qué controlador usa.
"""
from datetime import date
from customtkinter import CTkFrame, CTkLabel
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigPaginas as conPag
from views import componentes as comp
from views.paginas.inicio import avisarDatosCambiados
from views.messagebox import mensajesEmergentes as mss
from controller import productosController, comerciosController, facturasController, comprasController
from controller.validaciones import formatearMoneda, formatearNumero


class PaginaDatos(CTkFrame):
    titulo = ''             #'Productos'
    singular = ''           #'producto'
    nuevo = 'Nuevo'         #'Nueva' para palabras femeninas
    columnas = ()           #((clave, título, ancho, alineación, crece), ...)
    campos = ()             #((clave, etiqueta, tipo), ...) con tipo 'texto' o 'fecha'

    # --- Lo que define cada subclase ---

    def listar(self):
        #(filas, mensaje) con todos los registros
        raise NotImplementedError

    def buscar(self, texto):
        #(filas, mensaje) con los registros que coinciden con el texto
        raise NotImplementedError

    def filaTabla(self, fila):
        #(id, valores que se muestran en la tabla)
        raise NotImplementedError

    def datosFila(self, fila):
        #{clave del campo: texto} para llenar el panel al editar
        raise NotImplementedError

    def crear(self, datos):
        raise NotImplementedError

    def editar(self, idRegistro, datos):
        raise NotImplementedError

    def valoresIniciales(self):
        #Valores de los campos al empezar un registro nuevo
        return {}

    # --- Construcción ---

    def __init__(self, master):
        super().__init__(master, fg_color=tema["fondo"], corner_radius=0)
        self.idEditando = None
        self.filasPorId = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.lbSubtitulo = comp.encabezadoPagina(self, self.titulo)
        self.crearBuscador()
        self.crearTablaRegistros()
        self.crearPanel()
        self.modoNuevo()

    def crearBuscador(self):
        self.etBuscar = comp.campo(self, width=conPag["anchoBuscador"], placeholder_text=f'Buscar {self.singular}...')
        self.etBuscar.grid(row=1, column=0, sticky='w', padx=conPag["padX"] * 2, pady=(0, conPag["padY"]))
        self.etBuscar.bind('<KeyRelease>', lambda evento: self.refrescar())

    def crearTablaRegistros(self):
        marco = comp.tarjeta(self)
        marco.grid(row=2, column=0, sticky='nsew', padx=(conPag["padX"] * 2, conPag["padY"]), pady=(0, conPag["padX"] * 2))
        self.tabla = comp.crearTabla(marco, self.columnas)
        self.tabla.bind('<<TreeviewSelect>>', lambda evento: self.alSeleccionar())

    def crearPanel(self):
        panel = comp.tarjeta(self)
        panel.configure(width=conPag["anchoPanel"])
        panel.grid(row=2, column=1, sticky='ns', padx=(conPag["padY"], conPag["padX"] * 2), pady=(0, conPag["padX"] * 2))
        panel.grid_propagate(False)
        panel.grid_columnconfigure(0, weight=1)
        relleno = conPag["padTarjeta"]

        self.lbTituloPanel = comp.tituloPanel(panel, '')
        self.lbTituloPanel.grid(row=0, column=0, sticky='ew', padx=relleno, pady=(relleno, conPag["padY"]))

        self.widgets = {}
        fila = 1
        for clave, nombre, tipo in self.campos:
            comp.etiqueta(panel, nombre).grid(row=fila, column=0, sticky='ew', padx=relleno, pady=(conPag["padY"] // 2, 2))
            widget = comp.SelectorFecha(panel) if tipo == 'fecha' else comp.campo(panel)
            widget.grid(row=fila + 1, column=0, sticky='ew', padx=relleno)
            self.widgets[clave] = widget
            fila += 2

        #Enter pasa al siguiente campo; en el último guarda. Esc vuelve a "Nuevo"
        entradas = [self.entradaDe(w) for w in self.widgets.values()]
        for indice, entrada in enumerate(entradas):
            siguiente = entradas[indice + 1] if indice + 1 < len(entradas) else None
            entrada.bind('<Return>', lambda evento, s=siguiente: self.guardar() if s is None else s.focus())
            entrada.bind('<Escape>', lambda evento: self.modoNuevo())

        self.lbEstado = CTkLabel(panel, text='', font=comp.fuente(conPag["tamanoEtiqueta"]), text_color=tema["exito"]
                                 ,anchor='w', justify='left', wraplength=conPag["anchoPanel"] - 2 * relleno)
        self.lbEstado.grid(row=fila, column=0, sticky='ew', padx=relleno, pady=(conPag["padY"], 0))
        panel.grid_rowconfigure(fila + 1, weight=1)

        botones = CTkFrame(panel, fg_color='transparent')
        botones.grid(row=fila + 2, column=0, sticky='ew', padx=relleno, pady=relleno)
        botones.grid_columnconfigure((0, 1), weight=1)
        comp.boton(botones, 'Nuevo', self.modoNuevo, 'secundario').grid(row=0, column=0, sticky='ew', padx=(0, conPag["padY"] // 2))
        self.btnGuardar = comp.boton(botones, 'Guardar', self.guardar)
        self.btnGuardar.grid(row=0, column=1, sticky='ew', padx=(conPag["padY"] // 2, 0))

    def entradaDe(self, widget):
        return widget.entry if isinstance(widget, comp.SelectorFecha) else widget

    # --- Comportamiento ---

    def refrescar(self):
        #Vuelve a leer los registros (filtrados por el buscador) y los muestra en la tabla
        texto = self.etBuscar.get().strip()
        filas, mensaje = self.buscar(texto) if texto else self.listar()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        self.filasPorId = {}
        filasTabla = []
        for fila in filas:
            idRegistro, valores = self.filaTabla(fila)
            self.filasPorId[str(idRegistro)] = fila
            filasTabla.append((idRegistro, valores))
        comp.llenarTabla(self.tabla, filasTabla)
        self.lbSubtitulo.configure(text=f'{len(filas)} encontrados' if texto else f'{len(filas)} registrados')
        if self.idEditando is not None and self.tabla.exists(str(self.idEditando)):
            self.tabla.selection_set(str(self.idEditando))
            self.tabla.see(str(self.idEditando))

    def modoNuevo(self):
        self.idEditando = None
        if self.tabla.selection():
            self.tabla.selection_remove(*self.tabla.selection())
        self.lbTituloPanel.configure(text=f'{self.nuevo} {self.singular}')
        self.btnGuardar.configure(text='Guardar')
        iniciales = self.valoresIniciales()
        for clave, widget in self.widgets.items():
            self.ponerTexto(widget, iniciales.get(clave, ''))
        self.entradaDe(next(iter(self.widgets.values()))).focus()

    def alSeleccionar(self):
        seleccion = self.tabla.selection()
        if not seleccion or seleccion[0] not in self.filasPorId:
            return
        fila = self.filasPorId[seleccion[0]]
        self.idEditando = self.filaTabla(fila)[0]
        self.lbTituloPanel.configure(text=f'Editar {self.singular}')
        self.btnGuardar.configure(text='Guardar cambio')
        self.lbEstado.configure(text='')
        for clave, valor in self.datosFila(fila).items():
            self.ponerTexto(self.widgets[clave], valor)

    def ponerTexto(self, widget, texto):
        if isinstance(widget, comp.SelectorFecha):
            widget.poner(texto)
        else:
            widget.delete(0, 'end')
            widget.insert(0, texto)

    def guardar(self):
        datos = {clave: widget.get() for clave, widget in self.widgets.items()}
        creando = self.idEditando is None
        mensaje = self.crear(datos) if creando else self.editar(self.idEditando, datos)
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return
        avisarDatosCambiados(self)
        if creando:
            self.modoNuevo()
        self.refrescar()
        self.lbEstado.configure(text=mensaje[1])
        self.after(4000, lambda: self.lbEstado.configure(text='') if self.lbEstado.winfo_exists() else None)


class PaginaProductos(PaginaDatos):
    titulo = 'Productos'
    singular = 'producto'
    columnas = (('nombre', 'Nombre', 360, 'w', True),)
    campos = (('nombre', 'Nombre', 'texto'),)

    def listar(self):
        return productosController.consultarListaProductos()

    def buscar(self, texto):
        return productosController.consultarProductos(texto)

    def filaTabla(self, fila):
        productoId, nombre = fila
        return productoId, (nombre,)

    def datosFila(self, fila):
        return {'nombre': fila[1]}

    def crear(self, datos):
        return productosController.insertarProducto(datos['nombre'])

    def editar(self, idRegistro, datos):
        return productosController.editarProducto(idRegistro, datos['nombre'])


class PaginaComercios(PaginaDatos):
    titulo = 'Comercios'
    singular = 'comercio'
    columnas = (('nombre', 'Nombre', 240, 'w', True), ('direccion', 'Dirección', 260, 'w', True))
    campos = (('nombre', 'Nombre', 'texto'), ('direccion', 'Dirección', 'texto'))

    def listar(self):
        return comerciosController.consultarListaComercios()

    def buscar(self, texto):
        return comerciosController.consultarComercios(texto)

    def filaTabla(self, fila):
        comercioId, nombre, direccion = fila
        return comercioId, (nombre, direccion)

    def datosFila(self, fila):
        return {'nombre': fila[1], 'direccion': fila[2]}

    def crear(self, datos):
        return comerciosController.insertarComercio(datos['nombre'], datos['direccion'])

    def editar(self, idRegistro, datos):
        return comerciosController.modificarComercio(idRegistro, datos['nombre'], datos['direccion'])


class PaginaFacturas(PaginaDatos):
    titulo = 'Facturas'
    singular = 'factura'
    nuevo = 'Nueva'
    columnas = (('numero', 'Número', 200, 'w', True), ('total', 'Total', 150, 'e', False), ('fecha', 'Fecha', 130, 'center', False))
    campos = (('numero', 'Número', 'texto'), ('total', 'Total', 'texto'), ('fecha', 'Fecha', 'fecha'))

    def listar(self):
        return facturasController.consultarListaFacturas()

    def buscar(self, texto):
        return facturasController.consultarFacturas(texto)

    def filaTabla(self, fila):
        facturaId, numero, total, fecha = fila
        return facturaId, (numero, formatearMoneda(total), fecha)

    def datosFila(self, fila):
        return {'numero': fila[1], 'total': formatearNumero(fila[2]), 'fecha': fila[3]}

    def valoresIniciales(self):
        return {'fecha': date.today().isoformat()}

    def crear(self, datos):
        return facturasController.insertarFactura(datos['numero'], datos['total'], datos['fecha'])

    def editar(self, idRegistro, datos):
        return facturasController.modificarFactura(idRegistro, datos['numero'], datos['total'], datos['fecha'])


class PaginaCompras(PaginaDatos):
    titulo = 'Compras'
    singular = 'compra'
    nuevo = 'Nueva'
    columnas = (('descripcion', 'Descripción', 340, 'w', True), ('fecha', 'Creada', 130, 'center', False))
    campos = (('descripcion', 'Descripción', 'texto'),)

    def listar(self):
        filas, mensaje = comprasController.consultarListaCompras()
        return sorted(filas, reverse=True), mensaje   #las más recientes primero

    def buscar(self, texto):
        filas, mensaje = comprasController.consultarCompras(texto)
        return sorted(filas, reverse=True), mensaje

    def filaTabla(self, fila):
        idCompra, descripcion, fecha = fila
        return idCompra, (descripcion, fecha)

    def datosFila(self, fila):
        return {'descripcion': fila[1]}

    def crear(self, datos):
        #La fecha de creación es la de hoy, como en el registro anterior
        return comprasController.insertarCompra(datos['descripcion'], date.today().isoformat())

    def editar(self, idRegistro, datos):
        return comprasController.modificarCompra(idRegistro, datos['descripcion'])
