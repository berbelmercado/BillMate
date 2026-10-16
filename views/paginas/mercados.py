"""Página Mercados: buscar los ítems ya cargados (por producto, factura o compra), editarlos y eliminarlos."""
from customtkinter import CTkFrame, CTkSegmentedButton
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigPaginas as conPag
from views import componentes as comp
from views.campoAutocompletar import CampoAutocompletar
from views.paginas.inicio import avisarDatosCambiados
from views.messagebox import mensajesEmergentes as mss
from controller import mercadosController, productosController, facturasController, comerciosController, comprasController
from controller.validaciones import convertirNumero, formatearNumero, formatearMoneda, cantidadNumerica

#Texto del selector de búsqueda -> opción de mercadosController.consultarMercados
OPCIONES_BUSQUEDA = {'Producto': mercadosController.OPCION_PRODUCTO
                     ,'Factura': mercadosController.OPCION_FACTURA
                     ,'Compra': mercadosController.OPCION_COMPRA}

TECLAS_SIN_TEXTO = ('Return', 'KP_Enter', 'Tab', 'ISO_Left_Tab', 'Escape', 'Shift_L', 'Shift_R')


class PaginaMercados(CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=tema["fondo"], corner_radius=0)
        self.filasPorId = {}
        self.idEditando = None
        self.totalManual = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.lbSubtitulo = comp.encabezadoPagina(self, 'Mercados')
        self.crearBuscador()
        self.crearTablaItems()
        self.crearPanel()
        self.limpiarPanel()

    # --- Búsqueda y tabla ---

    def crearBuscador(self):
        marco = CTkFrame(self, fg_color='transparent')
        marco.grid(row=1, column=0, sticky='w', padx=conPag["padX"] * 2, pady=(0, conPag["padY"]))
        self.selectorBusqueda = CTkSegmentedButton(marco
                                                   ,values=list(OPCIONES_BUSQUEDA)
                                                   ,command=lambda valor: self.refrescar()
                                                   ,width=conPag["merAnchoSegmentos"]
                                                   ,height=conPag["altoCampo"]
                                                   ,font=comp.fuente(conPag["tamanoEtiqueta"], 'bold')
                                                   ,fg_color=tema["campo"]
                                                   ,selected_color=tema["acento"]
                                                   ,selected_hover_color=tema["acentoHover"]
                                                   ,unselected_color=tema["campo"]
                                                   ,unselected_hover_color=tema["botonHover"]
                                                   ,text_color=tema["texto"])
        self.selectorBusqueda.set('Producto')
        self.selectorBusqueda.grid(row=0, column=0, padx=(0, conPag["padY"]))
        self.etBuscar = comp.campo(marco, width=conPag["anchoBuscador"], placeholder_text='Buscar...')
        self.etBuscar.grid(row=0, column=1)
        self.etBuscar.bind('<KeyRelease>', lambda evento: self.refrescar())

    def crearTablaItems(self):
        marco = comp.tarjeta(self)
        marco.grid(row=2, column=0, sticky='nsew', padx=conPag["padX"] * 2, pady=(0, conPag["padY"]))
        columnas = (('producto', 'Producto', conPag["merColProducto"], 'w', True)
                    ,('cantidad', 'Cant', conPag["merColCantidad"], 'center', False)
                    ,('precio', 'Precio unidad', conPag["merColPrecio"], 'e', False)
                    ,('total', 'Total', conPag["merColTotal"], 'e', False)
                    ,('factura', 'Factura', conPag["merColFactura"], 'center', False)
                    ,('fecha', 'Fecha', conPag["merColFecha"], 'center', False)
                    ,('comercio', 'Comercio', conPag["merColComercio"], 'w', True)
                    ,('compra', 'Compra', conPag["merColCompra"], 'w', True))
        self.tabla = comp.crearTabla(marco, columnas)
        self.tabla.bind('<<TreeviewSelect>>', lambda evento: self.alSeleccionar())
        self.tabla.bind('<Delete>', lambda evento: self.eliminar())

    def refrescar(self):
        #Vuelve a leer las opciones del autocompletado y los ítems que coinciden con la búsqueda
        for campo in (self.campoProducto, self.campoFactura, self.campoComercio, self.campoCompra):
            campo.recargar()
        opcion = OPCIONES_BUSQUEDA[self.selectorBusqueda.get()]
        filas, mensaje = mercadosController.consultarMercados(opcion, self.etBuscar.get().strip())
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        #Cada fila: id, producto, cantidad, precio unidad, total, número de factura, fecha factura, comercio, compra
        self.filasPorId = {str(fila[0]): fila for fila in filas}
        comp.llenarTabla(self.tabla, [(fila[0], (fila[1], fila[2], formatearMoneda(fila[3]), formatearMoneda(fila[4])
                                                 ,fila[5], fila[6], fila[7], fila[8])) for fila in filas])
        self.lbSubtitulo.configure(text=f'{len(filas)} ítems  ·  {formatearMoneda(sum(fila[4] for fila in filas))}')
        if self.idEditando is not None:
            if self.tabla.exists(str(self.idEditando)):
                self.tabla.selection_set(str(self.idEditando))
                self.tabla.see(str(self.idEditando))
            else:
                self.limpiarPanel()

    # --- Panel de edición ---

    def crearPanel(self):
        panel = comp.tarjeta(self)
        panel.grid(row=3, column=0, sticky='ew', padx=conPag["padX"] * 2, pady=(0, conPag["padX"] * 2))
        relleno = conPag["padTarjeta"]
        for columna in range(5):
            panel.grid_columnconfigure(columna, weight=1, uniform='panel')

        self.lbTituloPanel = comp.tituloPanel(panel, '')
        self.lbTituloPanel.grid(row=0, column=0, columnspan=5, sticky='ew', padx=relleno, pady=(relleno, conPag["padY"] // 2))

        estilo = comp.estiloCampo()
        self.campoProducto = CampoAutocompletar(panel, opciones=self.opcionesProductos, width=conPag["merAnchoCampo"], **estilo)
        self.etCantidad = comp.campo(panel, width=conPag["merAnchoCampo"], justify='center')
        self.etPrecio = comp.campo(panel, width=conPag["merAnchoCampo"], justify='right')
        self.etTotal = comp.campo(panel, width=conPag["merAnchoCampo"], justify='right')
        self.campoFactura = CampoAutocompletar(panel, opciones=self.opcionesFacturas, width=conPag["merAnchoCampo"], **estilo)
        self.campoComercio = CampoAutocompletar(panel, opciones=self.opcionesComercios, width=conPag["merAnchoCampo"], **estilo)
        self.campoCompra = CampoAutocompletar(panel, opciones=self.opcionesCompras, width=conPag["merAnchoCampo"], **estilo)

        #Filas 1-2: producto (dos columnas), cantidad, precio y total. Filas 3-4: factura, comercio, compra y botones
        for fila, widgets in ((1, ((self.campoProducto, 'Producto', 0, 2), (self.etCantidad, 'Cant', 2, 1)
                                   ,(self.etPrecio, 'Precio unidad', 3, 1), (self.etTotal, 'Total', 4, 1)))
                              ,(3, ((self.campoFactura, 'Factura', 0, 1), (self.campoComercio, 'Comercio', 1, 1)
                                    ,(self.campoCompra, 'Compra', 2, 1)))):
            for widget, nombre, columna, ancho in widgets:
                comp.etiqueta(panel, nombre).grid(row=fila, column=columna, columnspan=ancho, sticky='ew'
                                                   ,padx=(relleno if columna == 0 else conPag["padY"] // 2, 0), pady=(0, 2))
                widget.grid(row=fila + 1, column=columna, columnspan=ancho, sticky='ew'
                            ,padx=(relleno if columna == 0 else conPag["padY"] // 2, 0), pady=(0, conPag["padY"] // 2))

        #Los botones comparten la fila de factura, comercio y compra para no quitarle alto a la tabla
        self.btnEliminar = comp.boton(panel, 'Eliminar', self.eliminar, 'peligro')
        self.btnEliminar.grid(row=4, column=3, sticky='ew', padx=(conPag["padY"] // 2, 0), pady=(0, relleno))
        self.btnGuardar = comp.boton(panel, 'Guardar cambio', self.guardar)
        self.btnGuardar.grid(row=4, column=4, sticky='ew', padx=(conPag["padY"] // 2, relleno), pady=(0, relleno))
        self.campoCompra.grid_configure(pady=(0, relleno))
        self.campoFactura.grid_configure(pady=(0, relleno))
        self.campoComercio.grid_configure(pady=(0, relleno))

        #Total sugerido como en Agregar Mercados: número inicial de la cantidad x precio, salvo que se escriba a mano
        for entry in (self.etCantidad, self.etPrecio):
            entry.bind('<KeyRelease>', self.recalcularTotal)
        self.etTotal.bind('<KeyRelease>', self.totalEscrito)
        for entry in (self.etCantidad, self.etPrecio, self.etTotal):
            entry.bind('<Return>', lambda evento: self.guardar())
            entry.bind('<Escape>', lambda evento: self.limpiarPanel())

    def opcionesProductos(self):
        lista, mensaje = productosController.consultarListaProductos()
        return [(productoId, nombre) for productoId, nombre in lista]

    def opcionesFacturas(self):
        lista, mensaje = facturasController.consultarListaFacturas()
        return [(facturaId, numero) for facturaId, numero, total, fecha in sorted(lista, reverse=True)]

    def opcionesComercios(self):
        lista, mensaje = comerciosController.consultarListaComercios()
        return [(comercioId, f'{nombre} - {direccion}') for comercioId, nombre, direccion in lista]

    def opcionesCompras(self):
        lista, mensaje = comprasController.consultarListaCompras()
        return [(idCompra, descripcion) for idCompra, descripcion, fecha in sorted(lista, reverse=True)]

    def limpiarPanel(self):
        self.idEditando = None
        self.totalManual = False
        if self.tabla.selection():
            self.tabla.selection_remove(*self.tabla.selection())
        for campo in (self.campoProducto, self.campoFactura, self.campoComercio, self.campoCompra):
            campo.limpiar()
        for entry in (self.etCantidad, self.etPrecio, self.etTotal):
            entry.delete(0, 'end')
        self.lbTituloPanel.configure(text='Selecciona un ítem de la tabla para editarlo')
        for boton in (self.btnGuardar, self.btnEliminar):
            boton.configure(state='disabled')

    def alSeleccionar(self):
        seleccion = self.tabla.selection()
        if not seleccion or seleccion[0] not in self.filasPorId:
            return
        fila = self.filasPorId[seleccion[0]]
        llaves, mensaje = mercadosController.consultarLlavesMercado(fila[0])
        if mensaje[0] == 0 or not llaves:
            mss.mensajeError(mensaje[1] if mensaje[0] == 0 else 'El ítem ya no existe')
            return
        compraId, facturaId, productoId, comercioId = llaves[0]
        self.idEditando = fila[0]
        self.totalManual = False
        self.campoProducto.fijar(productoId)
        self.campoFactura.fijar(facturaId)
        self.campoComercio.fijar(comercioId)
        self.campoCompra.fijar(compraId)
        for entry, valor in ((self.etCantidad, fila[2]), (self.etPrecio, formatearNumero(fila[3])), (self.etTotal, formatearNumero(fila[4]))):
            entry.delete(0, 'end')
            entry.insert(0, valor)
        self.lbTituloPanel.configure(text=f'Editar ítem: {fila[1]}')
        for boton in (self.btnGuardar, self.btnEliminar):
            boton.configure(state='normal')

    def recalcularTotal(self, evento=None):
        if evento is not None and evento.keysym in TECLAS_SIN_TEXTO:
            return
        if self.totalManual:
            return
        cantidad = cantidadNumerica(self.etCantidad.get())
        precio = convertirNumero(self.etPrecio.get())
        if cantidad is None or precio is None:
            return
        self.etTotal.delete(0, 'end')
        self.etTotal.insert(0, formatearNumero(round(cantidad * precio, 2)))

    def totalEscrito(self, evento):
        if evento.keysym not in TECLAS_SIN_TEXTO:
            self.totalManual = True

    def guardar(self):
        if self.idEditando is None:
            return
        llaves = {}
        for clave, campo, nombre in (('producto', self.campoProducto, 'el producto'), ('factura', self.campoFactura, 'la factura')
                                     ,('comercio', self.campoComercio, 'el comercio'), ('compra', self.campoCompra, 'la compra')):
            if campo.resolverExacto() is None:
                mss.mensajeError(f'Elija {nombre} de la lista')
                campo.entry.focus()
                return
            llaves[clave] = campo.valorId
        mensaje = mercadosController.actualizarMercado(self.idEditando, llaves['compra'], llaves['factura'], llaves['producto']
                                                       ,llaves['comercio'], self.etCantidad.get(), self.etPrecio.get(), self.etTotal.get())
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return
        avisarDatosCambiados(self)
        self.refrescar()

    def eliminar(self):
        if self.idEditando is None:
            return
        fila = self.filasPorId.get(str(self.idEditando))
        nombre = fila[1] if fila else 'el ítem'
        if not mss.preguntar(f'¿Eliminar "{nombre}"? Esta acción no se puede deshacer.'):
            return
        mensaje = mercadosController.eliminarMercado(self.idEditando)
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return
        avisarDatosCambiados(self)
        self.limpiarPanel()
        self.refrescar()
