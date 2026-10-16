"""Página Agregar Mercados: registrar los ítems de una compra.

Encabezado (compra, factura, comercio) que se llena una vez, línea de ingreso que se maneja con Enter
y tabla de los ítems de la compra en curso (tabla mercadosTemp), con el cuadre contra la factura.
"""
from datetime import date
from customtkinter import CTkFrame, CTkLabel, CTkInputDialog
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigPaginas as conPag
from views import componentes as comp
from views.campoAutocompletar import CampoAutocompletar
from views.paginas.inicio import avisarDatosCambiados
from views.messagebox import mensajesEmergentes as mss
from controller import productosController, comerciosController, facturasController, comprasController, mercadoTempController
from controller.validaciones import convertirNumero, formatearNumero, formatearMoneda, cantidadNumerica

TECLAS_SIN_TEXTO = ('Return', 'KP_Enter', 'Tab', 'ISO_Left_Tab', 'Escape', 'Shift_L', 'Shift_R')


class PaginaCompra(CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=tema["fondo"], corner_radius=0)
        self.facturas = {}          #facturaId -> (numero, total, fecha), para llenar Total y Fecha
        self.itemEditando = None    #mercadoIdTemp del ítem que se está editando, None si se agrega uno nuevo
        self.totalManual = False    #True si el usuario escribió el total del ítem a mano
        self.listaItems = []

        #La tabla (fila 3) es la que crece con la ventana
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        subtitulo = comp.encabezadoPagina(self, 'Agregar Mercados')
        subtitulo.configure(text='Enter: siguiente campo  ·  Doble clic: editar ítem  ·  Supr: borrar  ·  Ctrl+Enter: cargar')
        self.crearEncabezado()
        self.crearLineaIngreso()
        self.crearTabla()
        self.crearPie()

        #Ctrl+Enter carga la compra desde cualquier campo o desde la tabla de esta página
        for widget in (self.campoCompra.entry, self.campoFactura.entry, self.etTotalFactura, self.selectorFecha.entry
                       ,self.campoComercio.entry, self.campoProducto.entry, self.etCantidad, self.etPrecio, self.etTotalItem
                       ,self.tabla):
            widget.bind('<Control-Return>', lambda evento: self.cargarCompra())
            widget.bind('<Control-KP_Enter>', lambda evento: self.cargarCompra())

    def refrescar(self):
        #Al mostrar la página: opciones al día (pudieron cambiar en otras páginas), ítems y encabezado
        for campo in (self.campoCompra, self.campoFactura, self.campoComercio, self.campoProducto):
            campo.recargar()
            if campo.valorId is not None and campo.textoDe(campo.valorId) is None:
                campo.limpiar()     #el registro elegido ya no existe
        self.refrescarTabla()
        if self.campoCompra.valorId is None and self.campoFactura.valorId is None and self.campoComercio.valorId is None:
            self.encabezadoDesdeItems()
        self.after(150, self.enfocarInicio)

    def marco(self, fila, **opciones):
        #Tarjeta de una sección de la página
        tarjeta = comp.tarjeta(self)
        tarjeta.grid(row=fila, column=0, sticky='nsew', padx=conPag["padX"] * 2, **opciones)
        return tarjeta

    def ubicar(self, master, etiqueta, widget, columna, filaEtiqueta, columnas=1):
        #Etiqueta encima del campo, dentro de una tarjeta
        relleno = conPag["padTarjeta"]
        izquierda = relleno if columna == 0 else conPag["padY"] // 2
        comp.etiqueta(master, etiqueta).grid(row=filaEtiqueta, column=columna, columnspan=columnas, sticky='ew'
                                              ,padx=(izquierda, 0), pady=(conPag["padY"] // 2, 2))
        widget.grid(row=filaEtiqueta + 1, column=columna, columnspan=columnas, sticky='ew', padx=(izquierda, 0))

    # --- Encabezado: compra, factura y comercio ---

    def crearEncabezado(self):
        #Una sola fila, en el orden en que se llena: compra, factura, total, fecha y comercio
        tarjeta = self.marco(1, pady=(0, conPag["padY"]))
        relleno = conPag["padTarjeta"]
        for columna, peso in ((0, 2), (1, 1), (2, 1), (3, 0), (4, 2)):
            tarjeta.grid_columnconfigure(columna, weight=peso)
        estilo = comp.estiloCampo()

        self.campoCompra = CampoAutocompletar(tarjeta, opciones=self.opcionesCompras, crear=self.crearCompra
                                              ,alElegir=lambda i, t: self.campoFactura.entry.focus()
                                              ,width=conPag["merAnchoCampo"], **estilo)
        self.ubicar(tarjeta, 'Compra', self.campoCompra, 0, 0)
        self.campoFactura = CampoAutocompletar(tarjeta, opciones=self.opcionesFacturas, crear=self.crearFactura
                                               ,alElegir=self.facturaElegida, alEscribir=self.facturaSinElegir
                                               ,width=conPag["merAnchoCampo"], **estilo)
        self.ubicar(tarjeta, 'Factura', self.campoFactura, 1, 0)
        self.etTotalFactura = comp.campo(tarjeta, width=conPag["merAnchoCampo"], justify='right')
        self.ubicar(tarjeta, 'Total factura', self.etTotalFactura, 2, 0)
        self.etTotalFactura.bind('<Return>', self.enterTotalFactura)
        self.selectorFecha = comp.SelectorFecha(tarjeta)
        self.ubicar(tarjeta, 'Fecha factura', self.selectorFecha, 3, 0)
        self.campoComercio = CampoAutocompletar(tarjeta, opciones=self.opcionesComercios, crear=self.crearComercio
                                                ,alElegir=lambda i, t: self.campoProducto.entry.focus()
                                                ,width=conPag["merAnchoCampo"], **estilo)
        self.ubicar(tarjeta, 'Comercio', self.campoComercio, 4, 0)
        self.campoComercio.grid_configure(padx=(conPag["padY"] // 2, relleno))
        for widget in tarjeta.grid_slaves(row=1):
            widget.grid_configure(pady=(0, relleno))
        self.facturaSinElegir()

    def opcionesCompras(self):
        lista, mensaje = comprasController.consultarListaCompras()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        #Las más recientes primero
        return [(idCompra, descripcion) for idCompra, descripcion, fecha in sorted(lista, reverse=True)]

    def crearCompra(self, descripcion):
        mensaje = comprasController.insertarCompra(descripcion, date.today().isoformat())
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return None
        return mensaje[2]

    def opcionesFacturas(self):
        lista, mensaje = facturasController.consultarListaFacturas()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        self.facturas = {facturaId: (numero, total, fecha) for facturaId, numero, total, fecha in lista}
        return [(facturaId, numero) for facturaId, numero, total, fecha in sorted(lista, reverse=True)]

    def crearFactura(self, numero):
        #La factura nueva toma el total y la fecha escritos en el encabezado
        if self.etTotalFactura.get().strip() == '':
            mss.mensajeError('Escriba el total de la factura y presione Enter para crearla')
            self.etTotalFactura.focus()
            return None
        mensaje = facturasController.insertarFactura(numero, self.etTotalFactura.get(), self.selectorFecha.get())
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return None
        return mensaje[2]

    def facturaElegida(self, facturaId, numero):
        #Factura existente: Total y Fecha se muestran y no se editan aquí (se cambian en la página Facturas)
        numero, total, fecha = self.facturas[facturaId]
        self.etTotalFactura.configure(state='normal')
        self.etTotalFactura.delete(0, 'end')
        self.etTotalFactura.insert(0, formatearNumero(total))
        self.etTotalFactura.configure(state='disabled', fg_color=tema["campoDeshabilitado"])
        self.selectorFecha.poner(fecha)
        self.selectorFecha.habilitar(False)
        self.actualizarPie()
        self.campoComercio.entry.focus()

    def facturaSinElegir(self):
        #Número de factura nuevo: Total y Fecha se escriben para crearla (la fecha viene con la de hoy)
        if self.etTotalFactura.cget('state') == 'disabled':
            self.etTotalFactura.configure(state='normal')
            self.etTotalFactura.delete(0, 'end')
            self.selectorFecha.habilitar(True)
            self.selectorFecha.poner('')
        self.etTotalFactura.configure(state='normal', fg_color=tema["campo"])
        self.selectorFecha.habilitar(True)
        if self.selectorFecha.get() == '':
            self.selectorFecha.hoy()
        if hasattr(self, 'lbCuadre'):
            self.actualizarPie()

    def enterTotalFactura(self, evento):
        #Enter en Total crea la factura con el número escrito, si todavía no existe
        if evento.state & 0x4:
            return None
        if self.campoFactura.resolverExacto() is None and self.campoFactura.texto():
            self.campoFactura.crearDesdeTexto()
        else:
            self.campoComercio.entry.focus()
        return 'break'

    def opcionesComercios(self):
        lista, mensaje = comerciosController.consultarListaComercios()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        #Con la dirección, para distinguir sucursales con el mismo nombre
        return [(comercioId, f'{nombre} - {direccion}') for comercioId, nombre, direccion in lista]

    def crearComercio(self, nombre):
        dialogo = CTkInputDialog(title='Nuevo comercio', text=f'Dirección de "{nombre}":'
                                 ,fg_color=tema["tarjeta"], button_fg_color=tema["acento"], button_hover_color=tema["acentoHover"]
                                 ,entry_fg_color=tema["campo"], entry_border_color=tema["borde"], entry_text_color=tema["texto"]
                                 ,text_color=tema["texto"])
        direccion = dialogo.get_input()
        if direccion is None:
            return None
        mensaje = comerciosController.insertarComercio(nombre, direccion)
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return None
        return mensaje[2]

    def encabezadoDesdeItems(self):
        #Si hay ítems sin cargar, el encabezado toma la compra, factura y comercio del último agregado
        if not self.listaItems:
            return
        llaves, mensaje = mercadoTempController.consultarLlavesMercadoTemp(self.listaItems[0][0])
        if mensaje[0] == 0 or not llaves:
            return
        compraId, facturaId, productoId, comercioId = llaves[0]
        self.campoCompra.fijar(compraId)
        if self.campoFactura.fijar(facturaId):
            self.facturaElegida(facturaId, None)
        self.campoComercio.fijar(comercioId)

    def enfocarInicio(self):
        #Empieza en el primer dato que falte
        if not self.winfo_ismapped():
            return
        for campo in (self.campoCompra, self.campoFactura, self.campoComercio):
            if campo.valorId is None:
                campo.entry.focus()
                return
        self.campoProducto.entry.focus()

    # --- Línea de ingreso: producto, cantidad, precio y total ---

    def crearLineaIngreso(self):
        tarjeta = self.marco(2, pady=(0, conPag["padY"]))
        relleno = conPag["padTarjeta"]
        #Producto ocupa el doble que cada número; los botones no crecen
        for columna, peso in ((0, 3), (1, 1), (2, 1), (3, 1)):
            tarjeta.grid_columnconfigure(columna, weight=peso)
        estilo = comp.estiloCampo()

        self.campoProducto = CampoAutocompletar(tarjeta, opciones=self.opcionesProductos, crear=self.crearProducto
                                                ,alElegir=lambda i, t: self.enfocar(self.etCantidad)
                                                ,width=conPag["merAnchoCampo"], **estilo)
        self.ubicar(tarjeta, 'Producto', self.campoProducto, 0, 0)
        self.etCantidad = comp.campo(tarjeta, width=conPag["merAnchoCampo"], justify='center')
        self.ubicar(tarjeta, 'Cant', self.etCantidad, 1, 0)
        self.etPrecio = comp.campo(tarjeta, width=conPag["merAnchoCampo"], justify='right')
        self.ubicar(tarjeta, 'Precio unidad', self.etPrecio, 2, 0)
        self.etTotalItem = comp.campo(tarjeta, width=conPag["merAnchoCampo"], justify='right')
        self.ubicar(tarjeta, 'Total', self.etTotalItem, 3, 0)

        self.btnAgregar = comp.boton(tarjeta, 'Agregar', self.guardarItem, ancho=conPag["comAnchoBoton"])
        self.btnAgregar.grid(row=1, column=4, padx=(conPag["padY"], relleno))
        self.btnCancelarEdicion = comp.boton(tarjeta, 'Cancelar', self.limpiarLinea, 'secundario', conPag["comAnchoBoton"])
        for widget in tarjeta.grid_slaves(row=1):
            widget.grid_configure(pady=(0, relleno))

        #Enter pasa al siguiente campo; en Total agrega el ítem
        self.etCantidad.bind('<Return>', lambda evento: self.enterEn(evento, self.etPrecio))
        self.etPrecio.bind('<Return>', lambda evento: self.enterEn(evento, self.etTotalItem))
        self.etTotalItem.bind('<Return>', lambda evento: self.enterEn(evento, None))
        for entry in (self.etCantidad, self.etPrecio):
            entry.bind('<KeyRelease>', self.recalcularTotal)
        self.etTotalItem.bind('<KeyRelease>', self.totalEscrito)
        for entry in (self.campoProducto.entry, self.etCantidad, self.etPrecio, self.etTotalItem):
            entry.bind('<Escape>', lambda evento: self.limpiarLinea() if self.itemEditando is not None else None)

        self.etCantidad.insert(0, '1')

    def opcionesProductos(self):
        lista, mensaje = productosController.consultarListaProductos()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        return [(productoId, nombre) for productoId, nombre in lista]

    def crearProducto(self, nombre):
        mensaje = productosController.insertarProducto(nombre)
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return None
        return mensaje[2]

    def enfocar(self, entry):
        entry.focus()
        entry.select_range(0, 'end')

    def enterEn(self, evento, siguiente):
        if evento.state & 0x4:   #Ctrl+Enter carga la compra
            return None
        if siguiente is None:
            self.guardarItem()
        else:
            self.enfocar(siguiente)
        return 'break'

    def recalcularTotal(self, evento=None):
        #Total sugerido = número con que empieza la cantidad x precio, salvo que el total se haya escrito a mano
        if evento is not None and evento.keysym in TECLAS_SIN_TEXTO:
            return
        if self.totalManual:
            return
        cantidad = cantidadNumerica(self.etCantidad.get())
        precio = convertirNumero(self.etPrecio.get())
        if cantidad is None or precio is None:
            return
        self.etTotalItem.delete(0, 'end')
        self.etTotalItem.insert(0, formatearNumero(round(cantidad * precio, 2)))

    def totalEscrito(self, evento):
        if evento.keysym not in TECLAS_SIN_TEXTO:
            self.totalManual = True

    def guardarItem(self):
        #Agrega el ítem a la compra en curso o guarda el cambio del ítem que se está editando
        if self.campoProducto.resolverExacto() is None:
            mss.mensajeError('Elija un producto de la lista o créelo con "+ Crear"')
            self.campoProducto.entry.focus()
            return

        if self.itemEditando is not None:
            llaves, mensaje = mercadoTempController.consultarLlavesMercadoTemp(self.itemEditando)
            if mensaje[0] == 0 or not llaves:
                mss.mensajeError(mensaje[1] if mensaje[0] == 0 else 'El ítem ya no existe')
                self.limpiarLinea()
                self.refrescarTabla()
                return
            compraId, facturaId, productoId, comercioId = llaves[0]
            mensaje = mercadoTempController.actualizarMercadoTemp(self.itemEditando, compraId, facturaId
                                                                  ,self.campoProducto.valorId, comercioId
                                                                  ,self.etCantidad.get(), self.etPrecio.get()
                                                                  ,self.etTotalItem.get())
        else:
            for campo, nombre in ((self.campoCompra, 'la compra'), (self.campoFactura, 'la factura')
                                  ,(self.campoComercio, 'el comercio')):
                if campo.resolverExacto() is None:
                    mss.mensajeError(f'Elija o cree {nombre} en el encabezado')
                    campo.entry.focus()
                    return
            mensaje = mercadoTempController.insertarMercadoTemp(self.campoCompra.valorId, self.campoFactura.valorId
                                                                ,self.campoProducto.valorId, self.campoComercio.valorId
                                                                ,self.etCantidad.get(), self.etPrecio.get()
                                                                ,self.etTotalItem.get())
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return
        self.limpiarLinea()
        self.refrescarTabla()

    def limpiarLinea(self):
        self.itemEditando = None
        self.totalManual = False
        self.campoProducto.limpiar()
        for entry in (self.etCantidad, self.etPrecio, self.etTotalItem):
            entry.delete(0, 'end')
        self.etCantidad.insert(0, '1')
        self.btnAgregar.configure(text='Agregar')
        self.btnCancelarEdicion.grid_forget()
        self.campoProducto.entry.focus()

    # --- Tabla de ítems ---

    def crearTabla(self):
        tarjeta = self.marco(3, pady=(0, conPag["padY"]))
        columnas = (('producto', 'Producto', conPag["comColProducto"], 'w', True)
                    ,('cantidad', 'Cant', conPag["comColCantidad"], 'center', False)
                    ,('precio', 'Precio unidad', conPag["comColPrecio"], 'e', False)
                    ,('total', 'Total', conPag["comColTotal"], 'e', False))
        self.tabla = comp.crearTabla(tarjeta, columnas)
        self.tabla.bind('<Double-1>', lambda evento: self.editarItem())
        self.tabla.bind('<Return>', lambda evento: self.editarItem())
        self.tabla.bind('<Delete>', lambda evento: self.borrarItem())

    def refrescarTabla(self):
        self.listaItems, mensaje = mercadoTempController.consultarMercadoTemp()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        #consultarMercadoTemp devuelve el más reciente primero; en la tabla van en el orden en que se agregaron
        comp.llenarTabla(self.tabla, [(mercadoIdTemp, (producto, cantidad, formatearMoneda(precioUnidad), formatearMoneda(precioTotal)))
                                      for mercadoIdTemp, producto, cantidad, precioUnidad, precioTotal, *resto in reversed(self.listaItems)])
        hijos = self.tabla.get_children()
        if hijos:
            self.tabla.see(hijos[-1])
        self.actualizarPie()

    def itemSeleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        mercadoIdTemp = int(seleccion[0])
        for fila in self.listaItems:
            if fila[0] == mercadoIdTemp:
                return fila
        return None

    def editarItem(self):
        #Pasa el ítem seleccionado a la línea de ingreso; el botón queda en "Guardar cambio"
        fila = self.itemSeleccionado()
        if fila is None:
            return
        llaves, mensaje = mercadoTempController.consultarLlavesMercadoTemp(fila[0])
        if mensaje[0] == 0 or not llaves:
            mss.mensajeError(mensaje[1] if mensaje[0] == 0 else 'El ítem ya no existe')
            return
        self.limpiarLinea()
        self.itemEditando = fila[0]
        self.campoProducto.fijar(llaves[0][2])
        self.etCantidad.delete(0, 'end')
        self.etCantidad.insert(0, fila[2])
        self.etPrecio.insert(0, formatearNumero(fila[3]))
        self.etTotalItem.insert(0, formatearNumero(fila[4]))
        self.btnAgregar.configure(text='Guardar cambio')
        self.btnCancelarEdicion.grid(row=1, column=5, padx=(0, conPag["padTarjeta"]), pady=(0, conPag["padTarjeta"]))
        self.enfocar(self.etCantidad)

    def borrarItem(self):
        fila = self.itemSeleccionado()
        if fila is None:
            return
        if not mss.preguntar(f'¿Borrar "{fila[1]}" de la compra?'):
            return
        mensaje = mercadoTempController.eliminarMercadoTemp(fila[0])
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        if self.itemEditando == fila[0]:
            self.limpiarLinea()
        self.refrescarTabla()

    # --- Pie: totales, cuadre y carga ---

    def crearPie(self):
        marco = CTkFrame(self, fg_color='transparent')
        marco.grid(row=4, column=0, sticky='ew', padx=conPag["padX"] * 2, pady=(0, conPag["padX"]))
        marco.grid_columnconfigure(2, weight=1)
        self.lbCuadre = CTkLabel(marco, text='', font=comp.fuente(conPag["tamanoCampo"]), text_color=tema["textoSuave"], anchor='w')
        self.lbCuadre.grid(row=0, column=0, sticky='w')
        self.lbDiferencia = CTkLabel(marco, text='', font=comp.fuente(conPag["tamanoCampo"], 'bold'), anchor='w')
        self.lbDiferencia.grid(row=0, column=1, sticky='w', padx=(conPag["padY"] // 2, 0))
        comp.boton(marco, 'Cargar compra', self.cargarCompra, ancho=conPag["comAnchoBotonCargar"]).grid(row=0, column=3, sticky='e')

    def actualizarPie(self):
        #Ítems y suma de toda la compra en curso; cuadre solo con los ítems de la factura del encabezado
        suma = sum(fila[4] for fila in self.listaItems)
        texto = f'Ítems: {len(self.listaItems)}    Suma: {formatearMoneda(suma)}'
        diferencia = None

        facturaId = self.campoFactura.valorId if hasattr(self, 'campoFactura') else None
        if facturaId in self.facturas:
            numero, totalFactura, fecha = self.facturas[facturaId]
            filas, mensaje = mercadoTempController.cuadreFacturas()
            sumaFactura = next((fila[2] for fila in filas if fila[0] == facturaId), 0)
            diferencia = round(totalFactura - sumaFactura, 2)
            texto += f'    Factura {numero}: {formatearMoneda(totalFactura)}    Diferencia:'

        self.lbCuadre.configure(text=texto)
        if diferencia is None:
            self.lbDiferencia.configure(text='')
        else:
            self.lbDiferencia.configure(text=formatearMoneda(diferencia)
                                        ,text_color=tema["exito"] if diferencia == 0 else tema["peligro"])

    def facturasSinCuadrar(self):
        #Texto con las facturas de la compra en curso cuya suma de ítems no coincide con su total
        filas, mensaje = mercadoTempController.cuadreFacturas()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
            return None
        return [f'Factura {numero}: ítems {formatearMoneda(suma)}, total {formatearMoneda(total)}, diferencia {formatearMoneda(diferencia)}'
                for facturaId, numero, suma, total, diferencia in filas if diferencia != 0]

    def cargarCompra(self):
        #Pasa los ítems de la compra en curso a mercados; si alguna factura no cuadra, primero pregunta
        if not self.listaItems:
            mss.mensajeError('No hay ítems para cargar')
            return
        sinCuadrar = self.facturasSinCuadrar()
        if sinCuadrar is None:
            return
        if sinCuadrar and not mss.preguntar('Estas facturas no cuadran:\n\n' + '\n'.join(sinCuadrar)
                                            + '\n\n¿Cargar la compra de todas formas?'):
            return
        mensaje = mercadoTempController.cargarCompra()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
            return
        mss.mensajeInformativo(mensaje[1])
        self.limpiarLinea()
        self.refrescarTabla()
        #La pantalla de inicio vuelve a leer la última compra
        avisarDatosCambiados(self)
