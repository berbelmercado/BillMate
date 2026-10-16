"""Pantalla de inicio: encabezado, tarjetas de resumen y detalle de la última compra cargada"""
from datetime import date
import tkinter
from customtkinter import CTkFrame,CTkLabel
from views.componentes import crearTabla
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigInicio as conIni
from controller import mercadosController
from controller.validaciones import formatearMoneda
from views.messagebox import mensajesEmergentes as mss

MESES = ('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre'
         ,'noviembre', 'diciembre')
DIAS = ('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo')

#Evento que emiten las ventanas que cambian compras (cargar, editar, borrar) para que el inicio se actualice
EVENTO_DATOS_CAMBIADOS = '<<DatosCambiados>>'


def recortar(texto, largo):
    #Acorta textos largos para que no se salgan de las tarjetas
    texto = str(texto)
    return texto if len(texto) <= largo else texto[:largo - 1] + '…'


def avisarDatosCambiados(widget):
    #Pide a la pantalla de inicio que vuelva a leer los datos (ver PanelInicio)
    widget.event_generate(EVENTO_DATOS_CAMBIADOS)


class PanelInicio(CTkFrame):
    """Página de inicio; VentanaPrincipal.mostrar('inicio') la ubica a la derecha de la barra lateral."""

    def __init__(self, master=None):
        super().__init__(master, fg_color=tema["fondo"], corner_radius=0)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.crearEncabezado()
        self.crearTarjetas()
        self.crearDetalle()
        self.refrescar()

        #Cualquier ventana que cargue, edite o borre compras emite este evento. CustomTkinter bloquea bind_all
        #en sus widgets, así que se usa el de tkinter: la etiqueta 'all' recibe el evento desde cualquier ventana
        tkinter.Misc.bind_all(self, EVENTO_DATOS_CAMBIADOS, lambda evento: self.refrescar(), '+')

    def fuente(self, tamano, peso='normal'):
        return (conIni["fuente"], tamano, peso)

    # --- Encabezado ---

    def crearEncabezado(self):
        marco = CTkFrame(self, fg_color='transparent')
        marco.grid(row=0, column=0, sticky='ew', padx=conIni["padX"] * 2, pady=(conIni["padX"] + conIni["padY"] // 2, conIni["padY"]))
        marco.grid_columnconfigure(0, weight=1)
        CTkLabel(marco, text='Inicio', font=self.fuente(conIni["tamanoTitulo"], 'bold'), text_color=tema["texto"]
                 ,anchor='w').grid(row=0, column=0, sticky='w')
        hoy = date.today()
        CTkLabel(marco, text=f'{DIAS[hoy.weekday()]} {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'
                 ,font=self.fuente(conIni["tamanoSubtitulo"]), text_color=tema["textoSuave"]
                 ,anchor='e').grid(row=0, column=1, sticky='e')

    # --- Tarjetas de resumen ---

    def crearTarjetas(self):
        marco = CTkFrame(self, fg_color='transparent')
        marco.grid(row=1, column=0, sticky='ew', padx=conIni["padX"] * 2 - conIni["padY"] // 2, pady=conIni["padY"])
        self.tarjetas = {}
        for columna, (clave, titulo) in enumerate((('compra', 'ÚLTIMA COMPRA'), ('total', 'TOTAL')
                                                   ,('productos', 'PRODUCTOS'), ('mes', 'ESTE MES'))):
            marco.grid_columnconfigure(columna, weight=1, uniform='tarjetas')
            tarjeta = CTkFrame(marco, fg_color=tema["tarjeta"], corner_radius=conIni["radioTarjeta"]
                               ,border_width=1, border_color=tema["borde"])
            tarjeta.grid(row=0, column=columna, sticky='nsew', padx=conIni["padY"] // 2)
            tarjeta.grid_columnconfigure(0, weight=1)
            CTkLabel(tarjeta, text=titulo, font=self.fuente(conIni["tamanoTarjetaTitulo"], 'bold')
                     ,text_color=tema["textoSuave"], anchor='w').grid(row=0, column=0, sticky='ew'
                                                                       ,padx=conIni["padTarjeta"], pady=(conIni["padTarjeta"], 0))
            valor = CTkLabel(tarjeta, text='—', font=self.fuente(conIni["tamanoTarjetaValor"], 'bold')
                             ,text_color=tema["texto"], anchor='w')
            valor.grid(row=1, column=0, sticky='ew', padx=conIni["padTarjeta"])
            detalle = CTkLabel(tarjeta, text='', font=self.fuente(conIni["tamanoTarjetaDetalle"])
                               ,text_color=tema["textoSuave"], anchor='w')
            detalle.grid(row=2, column=0, sticky='ew', padx=conIni["padTarjeta"], pady=(0, conIni["padTarjeta"]))
            self.tarjetas[clave] = (valor, detalle)

    def ponerTarjeta(self, clave, valor, detalle=''):
        etiquetaValor, etiquetaDetalle = self.tarjetas[clave]
        etiquetaValor.configure(text=valor)
        etiquetaDetalle.configure(text=detalle)

    # --- Tabla de la última compra ---

    def crearDetalle(self):
        self.lbDetalle = CTkLabel(self, text='Detalle de la última compra', font=self.fuente(conIni["tamanoSubtitulo"] + 2, 'bold')
                                  ,text_color=tema["texto"], anchor='w')
        self.lbDetalle.grid(row=2, column=0, sticky='ew', padx=conIni["padX"] * 2, pady=(conIni["padX"], conIni["padY"] // 2))

        marco = CTkFrame(self, fg_color=tema["tarjeta"], corner_radius=conIni["radioTarjeta"]
                         ,border_width=1, border_color=tema["borde"])
        marco.grid(row=3, column=0, sticky='nsew', padx=conIni["padX"] * 2, pady=(0, conIni["padX"] * 2))
        marco.grid_columnconfigure(0, weight=1)
        marco.grid_rowconfigure(0, weight=1)

        columnas = (('producto', 'Producto', conIni["colProductoWidth"], 'w', True)
                    ,('cantidad', 'Cant', conIni["colCantidadWidth"], 'center', False)
                    ,('precio', 'Precio unidad', conIni["colPrecioWidth"], 'e', False)
                    ,('total', 'Total', conIni["colTotalWidth"], 'e', False)
                    ,('factura', 'Factura', conIni["colFacturaWidth"], 'center', False)
                    ,('fecha', 'Fecha', conIni["colFechaWidth"], 'center', False)
                    ,('comercio', 'Comercio', conIni["colComercioWidth"], 'w', True))
        self.tabla = crearTabla(marco, columnas)

        self.lbVacio = CTkLabel(marco, text='Aún no hay compras cargadas.\nUsa "Agregar Mercados" para registrar la primera.'
                                ,font=self.fuente(conIni["tamanoSubtitulo"]), text_color=tema["textoSuave"])

    # --- Datos ---

    def refrescar(self):
        #Vuelve a leer la última compra y el gasto del mes, y actualiza tarjetas y tabla
        filas, mensaje = mercadosController.consultarUltimoMercado()
        if mensaje[0] == 0:
            mss.mensajeError(mensaje[1])
        hoy = date.today()
        gastoMes, mensajeMes = mercadosController.gastoDelMes(hoy.strftime('%Y-%m'))
        if mensajeMes[0] == 0:
            mss.mensajeError(mensajeMes[1])

        self.tabla.delete(*self.tabla.get_children())
        #Cada fila: id, producto, cantidad, precio unidad, total, número de factura, fecha factura, comercio, compra
        for indice, (mercadoId, producto, cantidad, precioUnidad, precioTotal, factura, fecha, comercio, compra) in enumerate(filas):
            self.tabla.insert('', 'end', iid=str(mercadoId), tags=('par' if indice % 2 == 0 else 'impar',)
                              ,values=(producto, cantidad, formatearMoneda(precioUnidad), formatearMoneda(precioTotal)
                                       ,factura, fecha, comercio))

        if filas:
            self.lbVacio.place_forget()
            facturas = {fila[5] for fila in filas}
            comercios = sorted({fila[7] for fila in filas})
            textoFacturas = f'{len(facturas)} factura' + ('s' if len(facturas) != 1 else '')
            self.ponerTarjeta('compra', recortar(filas[0][8], conIni["largoTextoTarjeta"])
                              ,recortar(f'{" · ".join(comercios)} · {textoFacturas}', conIni["largoDetalleTarjeta"]))
            self.ponerTarjeta('total', formatearMoneda(sum(fila[4] for fila in filas)), textoFacturas)
            self.ponerTarjeta('productos', str(len(filas)), 'ítems en la compra')
        else:
            self.lbVacio.place(relx=0.5, rely=0.5, anchor='center')
            self.ponerTarjeta('compra', '—', 'sin compras cargadas')
            self.ponerTarjeta('total', '—')
            self.ponerTarjeta('productos', '—')
        self.ponerTarjeta('mes', formatearMoneda(gastoMes), f'{MESES[hoy.month - 1]} de {hoy.year}')
