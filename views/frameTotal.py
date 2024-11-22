"""Módulo para calcular el total y contabilizar la cantidad de productos agregados en la tabla tempral e incluir la información en entrys  mostrarlo """
from customtkinter import CTkLabel,CTkEntry,CTkFrame
from views.configuracionesGenerales import dicConfiguracionGeneralColores as conColor
from views.configuracionesGenerales import dicConfiguracionGeneralFuentes as conFuente
from views.ventanasSecundarias.configuracionVentanasSecundarias import dicConfigFrameTotal as tot


class WidgetsDatos():
        #Función para mostrar datos referentes a los productos que se están ingresando
        def __init__ (self
                      ,master
                      ,posX
                      ,posY
                      ,listadoProductos):
                #Constructor
                self.master = master
                self.posX = posX
                self.posY = posY
                self.listadoProductos = listadoProductos
                self.crearFrameTotal()
               
        def crearFrameTotal(self):
                """dibuja los widgets"""

                #Se crea el frame
                self.fmDatos = CTkFrame(self.master
                                        ,fg_color=conColor["fg_color"]
                                        )
                self.fmDatos.place(x=self.posX
                                ,y=self.posY
                                )
    
                #Label total productos cargados
                lbTotalCompra = CTkLabel(self.fmDatos
                                                ,text='Total'
                                                ,fg_color=conColor["bgLabels"]
                                                ,font=(conFuente["Fuente"],conFuente["tamano"])
                                                ,text_color=conColor["colorLetrasLabel"]
                                                ,width=tot["lbTotaCompraWidth"]
                                                ,height=tot["lbTotalCompraHeight"]
                                                ,corner_radius=8)
                lbTotalCompra.grid(column=1
                                   ,row=0
                                   ,pady=5
                                   ,padx=5
                                   )
                
                #Entry total productos cargados
                etTotalCompra = CTkEntry(self.fmDatos
                                         ,fg_color=conColor["bgEntrys"]
                                         ,font=(conFuente["Fuente"],conFuente["tamano"])
                                         ,text_color=conColor["colorLetrasEntry"]
                                         ,justify='center'
                                         ,width=tot["etTotalCompraWidht"]
                                         ,height=tot["etTotalCompraHeight"]
                                         ,corner_radius=8
                                         )
                etTotalCompra.grid(column=1
                                   ,row=1
                                   ,pady=5
                                   ,padx=5
                                   )
                
                #Label Total productos ingresados
                lbTotalProductos = CTkLabel(self.fmDatos
                                            ,text='Productos Ingresados'
                                            ,fg_color=conColor["bgLabels"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
                                            ,text_color=conColor["colorLetrasLabel"]
                                            ,width=tot["lbTotaCompraWidth"]
                                            ,height=tot["lbTotalCompraHeight"]
                                            ,corner_radius=8)
                lbTotalProductos.grid(column=0
                                      ,row=0
                                      ,pady=5
                                      ,padx=5
                                      )
                #Entry Total productos ingresados
                etTotalProductos = CTkEntry(self.fmDatos
                                            ,fg_color=conColor["bgEntrys"]
                                            ,font=(conFuente["Fuente"],conFuente["tamano"])
                                            ,text_color=conColor["colorLetrasEntry"]
                                            ,justify='center'
                                            ,width=tot["etTotalCompraWidht"]
                                            ,height=tot["etTotalCompraHeight"]
                                            ,corner_radius=8)
                etTotalProductos.grid(column=0
                                      ,row=1
                                      ,pady=5
                                      ,padx=5
                                      )
                
                valorTotal, cantidadProductos = self.TotalTemp(self.listadoProductos) 

                etTotalCompra.delete(0,"end")
                etTotalCompra.insert(0,valorTotal)

                etTotalProductos.delete(0,"end")
                etTotalProductos.insert(0,cantidadProductos)

        

        def TotalTemp(self,listado):
        #Calcula el total y la cantidad de productos agregados en la tabla temporal
                total=0
                contador=0
                for i in listado:
                        total+=i[4]
                        contador+=1
                
                return total,contador
    
                
        