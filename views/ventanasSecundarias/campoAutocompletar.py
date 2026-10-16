"""Campo de texto con lista desplegable de coincidencias y opción de crear lo que no existe."""
import tkinter as tk
from customtkinter import CTkFrame, CTkEntry
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigNuevaCompra as conNC

#Teclas que no cambian el texto: no deben volver a filtrar la lista
TECLAS_SIN_TEXTO = {'Up', 'Down', 'Return', 'KP_Enter', 'Escape', 'Tab', 'ISO_Left_Tab', 'Shift_L', 'Shift_R'
                    ,'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Home', 'End'}


class CampoAutocompletar(CTkFrame):
    """Entry que muestra las opciones que contienen lo escrito (sin distinguir mayúsculas).

    opciones:  función sin argumentos que devuelve [(id, texto)]; se llama al crear el campo y en recargar()
    crear:     función(texto) que crea el registro y devuelve su id, o None si no se pudo (ella avisa el error).
               Si es None, la lista no ofrece "+ Crear"
    alElegir:  función(id, texto) que se llama al elegir o crear una opción
    alEscribir: función() que se llama cuando el texto cambia y el campo queda sin opción elegida
    """

    def __init__(self, master, opciones, crear=None, alElegir=None, alEscribir=None, width=200, **estiloEntry):
        super().__init__(master, fg_color='transparent')
        self.opciones = opciones
        self.crear = crear
        self.alElegir = alElegir
        self.alEscribir = alEscribir
        self.valorId = None   #id de la opción elegida; None mientras no haya una
        self.datos = []       #[(id, texto)] de todas las opciones
        self.visibles = []    #opciones que se muestran en la lista: (id, texto) o ('crear', texto escrito)
        self.ventanaLista = None

        self.entry = CTkEntry(self, width=width, **estiloEntry)
        self.entry.pack(fill='x', expand=True)

        self.entry.bind('<KeyRelease>', self._alTeclear)
        self.entry.bind('<Down>', self._bajar)
        self.entry.bind('<Up>', self._subir)
        self.entry.bind('<Return>', self._enter)
        self.entry.bind('<Escape>', lambda evento: self.cerrarLista())
        self.entry.bind('<FocusOut>', lambda evento: self.after(200, self._quizasCerrar))

        self.recargar()

    # --- Datos ---

    def recargar(self):
        #Vuelve a leer las opciones (por ejemplo, después de crear una)
        self.datos = list(self.opciones())

    def texto(self):
        return self.entry.get().strip()

    def textoDe(self, valorId):
        for idOpcion, textoOpcion in self.datos:
            if idOpcion == valorId:
                return textoOpcion
        return None

    def fijar(self, valorId):
        #Muestra la opción con ese id como elegida, sin llamar a alElegir
        textoOpcion = self.textoDe(valorId)
        if textoOpcion is None:
            return False
        self.valorId = valorId
        self.entry.delete(0, 'end')
        self.entry.insert(0, textoOpcion)
        return True

    def limpiar(self):
        self.valorId = None
        self.entry.delete(0, 'end')
        self.cerrarLista()

    def resolverExacto(self):
        #Si lo escrito coincide exactamente con una opción, la toma como elegida (sin llamar a alElegir)
        if self.valorId is None:
            escrito = self.texto().lower()
            for idOpcion, textoOpcion in self.datos:
                if escrito and textoOpcion.lower() == escrito:
                    self.valorId = idOpcion
                    break
        return self.valorId

    def crearDesdeTexto(self):
        #Crea un registro con lo escrito, como si se eligiera "+ Crear"
        if self.crear is not None and self.texto():
            self._elegir(('crear', self.texto()))

    # --- Lista desplegable ---

    def _filtrar(self):
        escrito = self.texto().lower()
        coincidencias = [opcion for opcion in self.datos if escrito in opcion[1].lower()]
        #Primero las que empiezan con lo escrito
        coincidencias.sort(key=lambda opcion: not opcion[1].lower().startswith(escrito))
        self.visibles = coincidencias[:conNC['listaMaxOpciones']]
        existeExacto = any(opcion[1].lower() == escrito for opcion in self.datos)
        if self.crear is not None and escrito and not existeExacto:
            self.visibles.append(('crear', self.texto()))

    def _abrirLista(self):
        self._filtrar()
        if not self.visibles:
            self.cerrarLista()
            return

        if self.ventanaLista is None:
            self.ventanaLista = tk.Toplevel(self)
            self.ventanaLista.overrideredirect(True)
            self.ventanaLista.transient(self.winfo_toplevel())
            self.lista = tk.Listbox(self.ventanaLista
                                    ,font=(conNC['fuente'], conNC['listaTamanoFuente'])
                                    ,bg=conNC['listaFondo']
                                    ,fg=conNC['listaLetra']
                                    ,selectbackground=conNC['listaSeleccion']
                                    ,activestyle='none'
                                    ,exportselection=False
                                    ,borderwidth=1
                                    ,highlightthickness=0)
            self.lista.pack(fill='both', expand=True)
            self.lista.bind('<ButtonRelease-1>', self._clicLista)

        self.lista.delete(0, 'end')
        for idOpcion, textoOpcion in self.visibles:
            self.lista.insert('end', f'+ Crear "{textoOpcion}"' if idOpcion == 'crear' else textoOpcion)
        self.lista.configure(height=min(len(self.visibles), conNC['listaMaxVisibles']))
        self.lista.selection_clear(0, 'end')
        self.lista.selection_set(0)
        self.lista.see(0)

        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        self.ventanaLista.geometry(f'+{x}+{y}')
        self.lista.configure(width=0)
        self.ventanaLista.update_idletasks()
        ancho = max(self.entry.winfo_width(), self.lista.winfo_reqwidth())
        self.ventanaLista.geometry(f'{ancho}x{self.lista.winfo_reqheight()}+{x}+{y}')
        self.ventanaLista.deiconify()
        self.ventanaLista.lift()

    def cerrarLista(self):
        if self.ventanaLista is not None:
            self.ventanaLista.destroy()
            self.ventanaLista = None

    def listaAbierta(self):
        return self.ventanaLista is not None

    def _quizasCerrar(self):
        #Al perder el foco se cierra la lista, salvo que el foco haya pasado a la propia lista
        try:
            if self.listaAbierta() and self.focus_get() is self.lista:
                return
        except KeyError:
            pass
        self.cerrarLista()
        self.resolverExacto()

    def _seleccionActual(self):
        seleccion = self.lista.curselection()
        return seleccion[0] if seleccion else 0

    def _mover(self, paso):
        if not self.listaAbierta():
            self._abrirLista()
            return 'break'
        nuevo = max(0, min(len(self.visibles) - 1, self._seleccionActual() + paso))
        self.lista.selection_clear(0, 'end')
        self.lista.selection_set(nuevo)
        self.lista.see(nuevo)
        return 'break'

    # --- Eventos ---

    def _alTeclear(self, evento):
        if evento.keysym in TECLAS_SIN_TEXTO:
            return
        self.valorId = None
        if self.alEscribir is not None:
            self.alEscribir()
        if self.texto():
            self._abrirLista()
        else:
            self.cerrarLista()

    def _bajar(self, evento):
        return self._mover(1)

    def _subir(self, evento):
        return self._mover(-1)

    def _enter(self, evento):
        if evento.state & 0x4:   #Ctrl+Enter es un atajo de la ventana, no del campo
            return None
        if self.listaAbierta():
            self._elegir(self.visibles[self._seleccionActual()])
        elif self.resolverExacto() is not None:
            if self.alElegir is not None:
                self.alElegir(self.valorId, self.textoDe(self.valorId))
        elif self.texto():
            self._abrirLista()
        return 'break'

    def _clicLista(self, evento):
        if self.visibles:
            self._elegir(self.visibles[self._seleccionActual()])

    def _elegir(self, opcion):
        idOpcion, textoOpcion = opcion
        self.cerrarLista()
        if idOpcion == 'crear':
            nuevoId = self.crear(textoOpcion)
            if nuevoId is None:
                self.entry.focus()
                return
            self.recargar()
            idOpcion = nuevoId
        self.fijar(idOpcion)
        if self.alElegir is not None:
            self.alElegir(self.valorId, self.textoDe(self.valorId))
