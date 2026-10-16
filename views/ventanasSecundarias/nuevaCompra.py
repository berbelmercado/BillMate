"""Pantalla para registrar los ítems de una compra en una sola ventana (reemplaza a Agregar Mercados).

Encabezado (compra, factura, comercio) que se llena una vez, línea de ingreso que se maneja con Enter
y tabla de los ítems de la compra en curso (tabla mercadosTemp).
"""
from datetime import date
from tkinter import ttk
from PIL import Image
from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkImage, CTkInputDialog, CTkScrollbar
from tkcalendar import Calendar
from views.ventanasSecundarias.campoAutocompletar import CampoAutocompletar
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigNuevaCompra as conNC
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColor
from views.configuracionesGenerales import dicConfig as conMaus
from controller import productosController, comerciosController, facturasController, comprasController, mercadoTempController
from controller.validaciones import convertirNumero, formatearNumero, formatearMoneda, cantidadNumerica
from views.messagebox import mensajesEmergentes as mss
from views.vwImgConfig import leerImagen
from views.frameListasTreview import TreviewUltimoMercado


class NuevaCompra(CTkToplevel):

    def __init__(self, master):
        super().__init__(master, fg_color=conColor["fg_color"])
        self.master = master
        self.title("Agregar Mercados")
        self.geometry(f'{conNC["vnWidth"]}x{conNC["vnHeight"]}+{conNC["vnX"]}+{conNC["vnY"]}')
        self.minsize(conNC["vnMinWidth"], conNC["vnMinHeight"])
        self.transient(master)
        self.lift()

        self.imagenGuardar = CTkImage(dark_image=Image.open(leerImagen("Guardar")), size=(24, 24))
        self.imagenCancelar = CTkImage(dark_image=Image.open(leerImagen("Cancelar")), size=(24, 24))
        self.imagenAgregar = CTkImage(dark_image=Image.open(leerImagen("Agregar")), size=(24, 24))
        self.imagenCargar = CTkImage(dark_image=Image.open(leerImagen("cargar")), size=(24, 24))

        self.facturas = {}          #facturaId -> (numero, total, fecha), para llenar Total y Fecha
        self.itemEditando = None    #mercadoIdTemp del ítem que se está editando, None si se agrega uno nuevo
        self.totalManual = False    #True si el usuario escribió el total del ítem a mano
        self.listaItems = []

        #La tabla (fila 2) es la que crece al agrandar la ventana
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.crearEncabezado()
        self.crearLineaIngreso()
        self.crearTabla()
        self.crearPie()

        self.bind('<Control-Return>', lambda evento: self.cargarCompra())
        self.bind('<Control-KP_Enter>', lambda evento: self.cargarCompra())

        self.refrescarTabla()
        self.encabezadoDesdeItems()
        self.after(150, self.enfocarInicio)

    # --- Estilo común ---

    def fuente(self):
        return (conNC["fuente"], conNC["tamanoFuente"])

    def estiloEntry(self):
        return dict(height=conNC["altoCampo"]
                    ,font=self.fuente()
                    ,fg_color=conColor["bgEntrys"]
                    ,text_color=conColor["colorLetrasEntry"]
                    ,corner_radius=8)

    def etiqueta(self, master, texto):
        return CTkLabel(master
                        ,text=texto
                        ,font=self.fuente()
                        ,fg_color=conColor["bgLabels"]
                        ,text_color=conColor["colorLetrasLabel"]
                        ,corner_radius=8
                        ,height=conNC["altoCampo"])

    def boton(self, master, texto, comando, ancho, imagen=None):
        return CTkButton(master
                         ,text=texto
                         ,command=comando
                         ,fg_color=conColor["bgBotones"]
                         ,font=self.fuente()
                         ,image=imagen
                         ,compound=conMaus["compound"]
                         ,cursor=conMaus["cursor"]
                         ,width=ancho
                         ,height=conNC["altoCampo"])

    def grid_(self, widget, fila, columna, **opciones):
        widget.grid(row=fila, column=columna, padx=conNC["padX"], pady=conNC["padY"], **opciones)

    # --- Encabezado: compra, factura y comercio ---

    def crearEncabezado(self):
        marco = CTkFrame(self, fg_color=conColor["fg_color"])
        marco.grid(row=0, column=0, sticky='ew', padx=conNC["padX"], pady=conNC["padY"])

        self.grid_(self.etiqueta(marco, ' Compra '), 0, 0, sticky='w')
        self.campoCompra = CampoAutocompletar(marco
                                              ,opciones=self.opcionesCompras
                                              ,crear=self.crearCompra
                                              ,alElegir=lambda i, t: self.campoFactura.entry.focus()
                                              ,width=conNC["campoCompraWidth"]
                                              ,**self.estiloEntry())
        self.grid_(self.campoCompra, 0, 1, columnspan=3, sticky='w')

        self.grid_(self.etiqueta(marco, ' Factura '), 1, 0, sticky='w')
        self.campoFactura = CampoAutocompletar(marco
                                               ,opciones=self.opcionesFacturas
                                               ,crear=self.crearFactura
                                               ,alElegir=self.facturaElegida
                                               ,alEscribir=self.facturaSinElegir
                                               ,width=conNC["campoFacturaWidth"]
                                               ,**self.estiloEntry())
        self.grid_(self.campoFactura, 1, 1, sticky='w')

        self.grid_(self.etiqueta(marco, ' Total '), 1, 2, sticky='w')
        self.etTotalFactura = CTkEntry(marco, width=conNC["etTotalFacturaWidth"], justify='right', **self.estiloEntry())
        self.grid_(self.etTotalFactura, 1, 3, sticky='w')
        self.etTotalFactura.bind('<Return>', self.enterTotalFactura)

        self.grid_(self.etiqueta(marco, ' Fecha '), 1, 4, sticky='w')
        self.etFechaFactura = CTkEntry(marco, width=conNC["etFechaFacturaWidth"], justify='center', **self.estiloEntry())
        self.grid_(self.etFechaFactura, 1, 5, sticky='w')
        self.btnCalendario = self.boton(marco, '...', self.abrirCalendario, conNC["btnCalendarioWidth"])
        self.grid_(self.btnCalendario, 1, 6, sticky='w')
        self.facturaSinElegir()

        self.grid_(self.etiqueta(marco, ' Comercio '), 2, 0, sticky='w')
        self.campoComercio = CampoAutocompletar(marco
                                                ,opciones=self.opcionesComercios
                                                ,crear=self.crearComercio
                                                ,alElegir=lambda i, t: self.campoProducto.entry.focus()
                                                ,width=conNC["campoComercioWidth"]
                                                ,**self.estiloEntry())
        self.grid_(self.campoComercio, 2, 1, columnspan=3, sticky='w')

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
        mensaje = facturasController.insertarFactura(numero, self.etTotalFactura.get(), self.etFechaFactura.get())
        if mensaje[0] != 1:
            mss.mensajeError(mensaje[1])
            return None
        return mensaje[2]

    def facturaElegida(self, facturaId, numero):
        #Factura existente: Total y Fecha se muestran y no se editan aquí
        numero, total, fecha = self.facturas[facturaId]
        for entry, valor in ((self.etTotalFactura, formatearNumero(total)), (self.etFechaFactura, fecha)):
            entry.configure(state='normal')
            entry.delete(0, 'end')
            entry.insert(0, valor)
            entry.configure(state='disabled')
        self.btnCalendario.configure(state='disabled')
        self.actualizarPie()
        self.campoComercio.entry.focus()

    def facturaSinElegir(self):
        #Número de factura nuevo: Total y Fecha se escriben para crearla (la fecha viene con la de hoy)
        if self.etTotalFactura.cget('state') == 'disabled':
            self.etTotalFactura.configure(state='normal')
            self.etTotalFactura.delete(0, 'end')
            self.etFechaFactura.configure(state='normal')
            self.etFechaFactura.delete(0, 'end')
        self.etTotalFactura.configure(state='normal')
        self.etFechaFactura.configure(state='normal')
        if self.etFechaFactura.get().strip() == '':
            self.etFechaFactura.insert(0, date.today().isoformat())
        self.btnCalendario.configure(state='normal')
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

    def abrirCalendario(self):
        self.venCalendario = CTkToplevel(self)
        self.venCalendario.title("Fecha de la factura")
        self.venCalendario.transient(self)
        self.venCalendario.grab_set()
        calendario = Calendar(self.venCalendario, selectmode='day', locale='es_ES', date_pattern="yyyy-MM-dd")
        calendario.pack()

        def seleccionar():
            self.etFechaFactura.delete(0, 'end')
            self.etFechaFactura.insert(0, calendario.get_date())
            self.venCalendario.destroy()

        self.boton(self.venCalendario, 'Seleccionar', seleccionar, 150, self.imagenGuardar).pack(pady=conNC["vcPady"])

    def opcionesComercios(self):
        lista, mensaje = comerciosController.consultarListaComercios()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        #Con la dirección, para distinguir sucursales con el mismo nombre
        return [(comercioId, f'{nombre} - {direccion}') for comercioId, nombre, direccion in lista]

    def crearComercio(self, nombre):
        dialogo = CTkInputDialog(title='Nuevo comercio', text=f'Dirección de "{nombre}":')
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
        for campo in (self.campoCompra, self.campoFactura, self.campoComercio):
            if campo.valorId is None:
                campo.entry.focus()
                return
        self.campoProducto.entry.focus()

    # --- Línea de ingreso: producto, cantidad, precio y total ---

    def crearLineaIngreso(self):
        marco = CTkFrame(self, fg_color=conColor["fg_color"])
        marco.grid(row=1, column=0, sticky='ew', padx=conNC["padX"], pady=conNC["padY"])

        self.grid_(self.etiqueta(marco, ' Producto '), 0, 0)
        self.campoProducto = CampoAutocompletar(marco
                                                ,opciones=self.opcionesProductos
                                                ,crear=self.crearProducto
                                                ,alElegir=lambda i, t: self.enfocar(self.etCantidad)
                                                ,width=conNC["campoProductoWidth"]
                                                ,**self.estiloEntry())
        self.grid_(self.campoProducto, 0, 1)

        self.grid_(self.etiqueta(marco, ' Cant '), 0, 2)
        self.etCantidad = CTkEntry(marco, width=conNC["etCantidadWidth"], justify='center', **self.estiloEntry())
        self.grid_(self.etCantidad, 0, 3)

        self.grid_(self.etiqueta(marco, ' Precio '), 0, 4)
        self.etPrecio = CTkEntry(marco, width=conNC["etPrecioWidth"], justify='right', **self.estiloEntry())
        self.grid_(self.etPrecio, 0, 5)

        self.grid_(self.etiqueta(marco, ' Total '), 0, 6)
        self.etTotalItem = CTkEntry(marco, width=conNC["etTotalItemWidth"], justify='right', **self.estiloEntry())
        self.grid_(self.etTotalItem, 0, 7)

        self.btnAgregar = self.boton(marco, 'Agregar', self.guardarItem, conNC["btnAgregarWidth"], self.imagenAgregar)
        self.grid_(self.btnAgregar, 0, 8)
        self.btnCancelarEdicion = self.boton(marco, 'Cancelar', self.limpiarLinea, conNC["btnCancelarEdicionWidth"], self.imagenCancelar)

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
        if evento is not None and evento.keysym in ('Return', 'KP_Enter', 'Tab', 'ISO_Left_Tab', 'Escape'):
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
        if evento.keysym not in ('Return', 'KP_Enter', 'Tab', 'ISO_Left_Tab', 'Escape', 'Shift_L', 'Shift_R'):
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
        self.btnAgregar.configure(text='Agregar', image=self.imagenAgregar)
        self.btnCancelarEdicion.grid_forget()
        self.campoProducto.entry.focus()

    # --- Tabla de ítems ---

    def crearTabla(self):
        marco = CTkFrame(self, fg_color=conColor["fg_color"])
        marco.grid(row=2, column=0, sticky='nsew', padx=conNC["padX"], pady=conNC["padY"])
        marco.grid_columnconfigure(0, weight=1)
        marco.grid_rowconfigure(0, weight=1)

        estilo = ttk.Style()
        estilo.configure('Compra.Treeview', font=(conNC["fuente"], conNC["tablaTamanoFuente"]), rowheight=conNC["tablaAltoFila"])
        estilo.configure('Compra.Treeview.Heading', font=(conNC["fuente"], conNC["tablaTamanoFuente"], 'bold'))

        columnas = ('producto', 'cantidad', 'precio', 'total')
        self.tabla = ttk.Treeview(marco, columns=columnas, show='headings', style='Compra.Treeview', selectmode='browse')
        for columna, titulo, ancho, alineacion in (('producto', 'Producto', conNC["colProductoWidth"], 'w')
                                                   ,('cantidad', 'Cant', conNC["colCantidadWidth"], 'center')
                                                   ,('precio', 'Precio unidad', conNC["colPrecioWidth"], 'e')
                                                   ,('total', 'Total', conNC["colTotalWidth"], 'e')):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor=alineacion, stretch=(columna == 'producto'))
        self.tabla.grid(row=0, column=0, sticky='nsew')

        barra = CTkScrollbar(marco, command=self.tabla.yview)
        barra.grid(row=0, column=1, sticky='ns')
        self.tabla.configure(yscrollcommand=barra.set)

        self.tabla.bind('<Double-1>', lambda evento: self.editarItem())
        self.tabla.bind('<Return>', lambda evento: self.editarItem())
        self.tabla.bind('<Delete>', lambda evento: self.borrarItem())

        CTkLabel(marco
                 ,text='Doble clic o Enter: editar ítem    Supr: borrar ítem    Ctrl+Enter: cargar compra'
                 ,text_color=conColor["ColorLetras"]
                 ,font=(conNC["fuente"], conNC["tablaTamanoFuente"])).grid(row=1, column=0, sticky='w')

    def refrescarTabla(self):
        self.listaItems, mensaje = mercadoTempController.consultarMercadoTemp()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        self.tabla.delete(*self.tabla.get_children())
        #consultarMercadoTemp devuelve el más reciente primero; en la tabla van en el orden en que se agregaron
        for mercadoIdTemp, producto, cantidad, precioUnidad, precioTotal, *resto in reversed(self.listaItems):
            self.tabla.insert('', 'end', iid=str(mercadoIdTemp)
                              ,values=(producto, cantidad, formatearMoneda(precioUnidad), formatearMoneda(precioTotal)))
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
        self.btnAgregar.configure(text='Guardar cambio', image=self.imagenGuardar)
        self.grid_(self.btnCancelarEdicion, 0, 9)
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

    # --- Pie: totales y botones ---

    def crearPie(self):
        marco = CTkFrame(self, fg_color=conColor["fg_color"])
        marco.grid(row=3, column=0, sticky='ew', padx=conNC["padX"], pady=conNC["padY"])
        marco.grid_columnconfigure(0, weight=1)

        self.lbCuadre = CTkLabel(marco, text='', font=self.fuente(), text_color=conColor["ColorLetras"], anchor='w')
        self.lbCuadre.grid(row=0, column=0, sticky='w', padx=conNC["padX"])

        self.grid_(self.boton(marco, 'Cerrar', self.destroy, conNC["btnPieWidth"], self.imagenCancelar), 0, 1)
        self.grid_(self.boton(marco, 'Cargar compra', self.cargarCompra, conNC["btnPieWidth"], self.imagenCargar), 0, 2)

    def actualizarPie(self):
        suma = sum(fila[4] for fila in self.listaItems)
        self.lbCuadre.configure(text=f'Ítems: {len(self.listaItems)}     Suma: {formatearMoneda(suma)}')

    def cargarCompra(self):
        #Pasa los ítems de la compra en curso a mercados
        if not self.listaItems:
            mss.mensajeError('No hay ítems para cargar')
            return
        mensaje = mercadoTempController.cargarCompra()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
            return
        mss.mensajeInformativo(mensaje[1])
        self.limpiarLinea()
        self.refrescarTabla()
        #Actualizamos la tabla del último mercado en la ventana principal
        TreviewUltimoMercado(self.master)
