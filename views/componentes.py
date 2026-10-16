"""Piezas visuales comunes de las páginas, con el estilo del Inicio (colores en dicTema, tamaños en dicConfigPaginas)"""
from datetime import date
from tkinter import ttk, TclError
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkToplevel, CTkScrollbar
from tkcalendar import Calendar
from views.configuracionesGenerales import dicTema as tema
from views.configuracionesGenerales import dicConfigPaginas as conPag
from views.configuracionesGenerales import dicConfig as conMaus


def fuente(tamano, peso='normal'):
    return (conPag["fuente"], tamano, peso)


def prepararEstiloTablas():
    #Estilo 'App.Treeview' de las tablas de las páginas: sin bordes, filas altas y encabezado oscuro.
    #Se basa en el tema 'clam' de ttk, el único que respeta los colores del encabezado
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure('App.Treeview'
                     ,background=tema["tarjeta"]
                     ,fieldbackground=tema["tarjeta"]
                     ,foreground=tema["texto"]
                     ,font=fuente(conPag["tamanoTabla"])
                     ,rowheight=conPag["altoFilaTabla"]
                     ,borderwidth=0)
    estilo.configure('App.Treeview.Heading'
                     ,background=tema["encabezadoTabla"]
                     ,foreground=tema["textoSuave"]
                     ,font=fuente(conPag["tamanoTabla"], 'bold')
                     ,relief='flat'
                     ,borderwidth=0)
    estilo.map('App.Treeview'
               ,background=[('selected', tema["acento"])]
               ,foreground=[('selected', 'white')])
    estilo.map('App.Treeview.Heading', background=[('active', tema["botonHover"])])
    estilo.layout('App.Treeview', [('App.Treeview.treearea', {'sticky': 'nswe'})])


# --- Textos ---

def encabezadoPagina(master, titulo, fila=0):
    #Título grande a la izquierda y un subtítulo a la derecha (se cambia con .configure(text=...))
    marco = CTkFrame(master, fg_color='transparent')
    marco.grid(row=fila, column=0, columnspan=2, sticky='ew', padx=conPag["padX"] * 2, pady=(conPag["padX"] + conPag["padY"] // 2, conPag["padY"]))
    marco.grid_columnconfigure(0, weight=1)
    CTkLabel(marco, text=titulo, font=fuente(conPag["tamanoTitulo"], 'bold'), text_color=tema["texto"]
             ,anchor='w').grid(row=0, column=0, sticky='w')
    subtitulo = CTkLabel(marco, text='', font=fuente(conPag["tamanoSubtitulo"]), text_color=tema["textoSuave"], anchor='e')
    subtitulo.grid(row=0, column=1, sticky='e')
    return subtitulo


def etiqueta(master, texto):
    #Nombre del campo, encima de él
    return CTkLabel(master, text=texto, font=fuente(conPag["tamanoEtiqueta"], 'bold'), text_color=tema["textoSuave"], anchor='w')


def tituloPanel(master, texto):
    return CTkLabel(master, text=texto, font=fuente(conPag["tamanoTituloPanel"], 'bold'), text_color=tema["texto"], anchor='w')


# --- Campos y botones ---

def estiloCampo():
    return dict(height=conPag["altoCampo"]
                ,font=fuente(conPag["tamanoCampo"])
                ,fg_color=tema["campo"]
                ,border_color=tema["borde"]
                ,border_width=1
                ,text_color=tema["texto"]
                ,placeholder_text_color=tema["textoSuave"]
                ,corner_radius=conPag["radio"])


def campo(master, width=200, **opciones):
    return CTkEntry(master, width=width, **estiloCampo(), **opciones)


def boton(master, texto, comando, tipo='principal', ancho=None, imagen=None):
    #tipo: 'principal' (acento), 'secundario' (plano con borde) o 'peligro' (rojo)
    colores = {'principal': dict(fg_color=tema["acento"], hover_color=tema["acentoHover"], text_color='white', border_width=0)
               ,'secundario': dict(fg_color='transparent', hover_color=tema["botonHover"], text_color=tema["texto"]
                                   ,border_width=1, border_color=tema["borde"])
               ,'peligro': dict(fg_color=tema["peligro"], hover_color=tema["peligroHover"], text_color='white', border_width=0)}
    opciones = dict(text=texto, command=comando, image=imagen, compound='left', height=conPag["altoBoton"]
                    ,corner_radius=conPag["radio"], font=fuente(conPag["tamanoBoton"], 'bold'), cursor=conMaus["cursor"]
                    ,**colores[tipo])
    if ancho is not None:
        opciones['width'] = ancho
    return CTkButton(master, **opciones)


def tarjeta(master):
    return CTkFrame(master, fg_color=tema["tarjeta"], corner_radius=conPag["radioTarjeta"], border_width=1, border_color=tema["borde"])


# --- Tabla ---

def crearTabla(master, columnas, fila=0):
    """Tabla con barra de desplazamiento dentro de master (normalmente una tarjeta).

    columnas: [(clave, título, ancho, alineación, crece)]. Devuelve el Treeview.
    """
    master.grid_columnconfigure(0, weight=1)
    master.grid_rowconfigure(fila, weight=1)
    tabla = ttk.Treeview(master, columns=[c[0] for c in columnas], show='headings', style='App.Treeview', selectmode='browse')
    for clave, titulo, ancho, alineacion, crece in columnas:
        tabla.heading(clave, text=titulo, anchor=alineacion)
        tabla.column(clave, width=ancho, minwidth=ancho // 2, anchor=alineacion, stretch=crece)
    tabla.tag_configure('par', background=tema["filaPar"])
    tabla.tag_configure('impar', background=tema["filaImpar"])
    tabla.grid(row=fila, column=0, sticky='nsew', padx=(conPag["padY"], 0), pady=conPag["padY"])

    barra = CTkScrollbar(master, command=tabla.yview, fg_color='transparent'
                         ,button_color=tema["borde"], button_hover_color=tema["textoSuave"])
    barra.grid(row=fila, column=1, sticky='ns', padx=(0, conPag["padY"] // 2), pady=conPag["padY"])
    tabla.configure(yscrollcommand=barra.set)
    return tabla


def llenarTabla(tabla, filas):
    #filas: [(id, (valores...))]; el id queda como iid de la fila y las filas alternan de color
    tabla.delete(*tabla.get_children())
    for indice, (idFila, valores) in enumerate(filas):
        tabla.insert('', 'end', iid=str(idFila), values=valores, tags=('par' if indice % 2 == 0 else 'impar',))


# --- Selector de fecha ---

class SelectorFecha(CTkFrame):
    """Campo de fecha AAAA-MM-DD con botón; el calendario se abre con el botón o con un clic en el campo."""

    def __init__(self, master, **opciones):
        super().__init__(master, fg_color='transparent')
        self.entry = campo(self, width=conPag["anchoFecha"], justify='center')
        self.entry.grid(row=0, column=0, sticky='ew')
        self.btnCalendario = boton(self, '...', self.abrirCalendario, 'secundario', conPag["anchoBotonFecha"])
        self.btnCalendario.grid(row=0, column=1, padx=(conPag["padY"] // 2, 0))
        self.grid_columnconfigure(0, weight=1)
        self.entry.bind('<Button-1>', lambda evento: self.abrirCalendario() if self.activo else None)
        self.venCalendario = None
        self.activo = True

    def get(self):
        return self.entry.get().strip()

    def poner(self, texto):
        estado = self.entry.cget('state')
        self.entry.configure(state='normal')
        self.entry.delete(0, 'end')
        self.entry.insert(0, texto)
        self.entry.configure(state=estado)

    def habilitar(self, activo):
        #Deshabilitado, la fecha solo se muestra (no se escribe ni se abre el calendario)
        self.activo = activo
        self.entry.configure(state='normal' if activo else 'disabled'
                             ,fg_color=tema["campo"] if activo else tema["campoDeshabilitado"])
        self.btnCalendario.configure(state='normal' if activo else 'disabled')

    def hoy(self):
        self.poner(date.today().isoformat())

    def abrirCalendario(self):
        if self.venCalendario is not None and self.venCalendario.winfo_exists():
            self.venCalendario.lift()
            return
        self.venCalendario = CTkToplevel(self)
        self.venCalendario.title('Fecha')
        self.venCalendario.transient(self.winfo_toplevel())
        self.venCalendario.resizable(False, False)
        #Bajo el campo
        self.venCalendario.geometry(f'+{self.entry.winfo_rootx()}+{self.entry.winfo_rooty() + self.entry.winfo_height() + 4}')

        calendario = Calendar(self.venCalendario, selectmode='day', locale='es_ES', date_pattern='yyyy-MM-dd'
                              ,background=tema["acento"], selectbackground=tema["acento"])
        try:
            calendario.selection_set(self.get())
        except (ValueError, TclError):
            pass
        calendario.pack(padx=conPag["padCalendario"], pady=(conPag["padCalendario"], 0))

        def elegir(evento=None):
            self.poner(calendario.get_date())
            self.venCalendario.destroy()
            self.entry.focus()

        calendario.bind('<<CalendarSelected>>', elegir)
        boton(self.venCalendario, 'Elegir', elegir).pack(pady=conPag["padCalendario"])
        #El grab solo es posible cuando la ventana ya se ve (CustomTkinter la muestra un instante después)
        self.venCalendario.after(150, self._bloquearFondo)

    def _bloquearFondo(self):
        try:
            if self.venCalendario is not None and self.venCalendario.winfo_exists():
                self.venCalendario.grab_set()
                self.venCalendario.focus_force()
        except TclError:
            pass
