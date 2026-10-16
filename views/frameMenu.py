"""Modul para crear los frame que contienen el menú"""
from customtkinter import CTkFrame,CTkButton,CTkImage
from PIL import Image
from views import configuracionesGenerales as conGen
from views.vwImgConfig import leerImagen
from views.ventanasSecundarias import registrarFactura as rf
from views.ventanasSecundarias import registrarComercio as rc
from views.ventanasSecundarias import registrarProductos as rp
from views.ventanasSecundarias import agregarMercados as am
from views.ventanasSecundarias import consultarProductos as cp
from views.ventanasSecundarias import consultarMercados as cm
from views.ventanasSecundarias import consultarFacturas as cf
from views.ventanasSecundarias import consultarComercios as cc
from views.ventanasSecundarias import registrarCompras as rcp
from views.ventanasSecundarias import consultarCompras as conCom

class FrameMenu(CTkFrame):
    
    #Este frame contrendrá el menú de nuestra aplicación
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        #Apariencia general
        self._fg_color =fg_color=conGen.dicConfiguracionGeneralColores['bgGeneral']
        self.place(y=conGen.dicConfig["fmYPrincipal"])#Empaquetamieno frame
        #Importación de imagenes
        self.imagenRegistrar=CTkImage(dark_image=Image.open(leerImagen("Registrar")),size=(35,35))
        self.imagenConsultar=CTkImage(dark_image=Image.open(leerImagen("Consultar")),size=(35,35))
        self.crearWidgets()

    def mostrarVentanaRegistrarFactura(self):
        #muestra la ventana secundaria para registrar factura
        ventanaRegistrarFactura=rf.RegistrarFactura(self.master)

    def mostrarVentanaRegistrarComercio(self):
        #muestra la ventana secundaria para registrar comercio
        ventanaRegistrarComercio=rc.RegistrarComercio(self.master)

    def mostrarVentanaRegistrarProducto(self):
        #ventana secundaria registrar producto
        ventanaRegistrarProducto=rp.RegistrarProductos(self.master)

    def mostrarVentanaAgregarMercado(self):
        #ventana secundaria registrar mercado
        ventanaAgregarMercado=am.AgregarMercados(self.master)

    def mostrarVentanaconsultarProductos(self):
        #ventana secundaria consultar productos
        ventanaConsultarProducto=cp.ConsultarProductos(self.master)
        #ventanaConsultarProducto=cpv2.ConsultarFacturas(self)

    def mostrarVentanaConsultarFacturas(self):
        ventanaConsultarFacturas= cf.ConsultarFacturas(self.master)

    def mostrarVentanaConsultarMercados(self):
        #ventana secundaria consultar mercados
        ventanaConsultarMercados=cm.ConsultarMercados(self.master)

    def mostrarVentanaConsultarComercios(self):
        #ventana secundaria consultar comercios
        ventanaConsultarComercios=cc.ConsultarComercios(self.master)

    def mostrarVentanaRegistrarCompras(self):
        #Ventana secundaria registrar compra
        ventanaRegistrarCompras = rcp.RegistrarCompras(self.master)
    
    def mostrarVentanaConsultarCompras(self):
        #Ventana secundaria registrar compra
        ventanaConsultarCompras = conCom.ConsultarCompras(self.master)
        

    def crearWidgets(self):
        #Lectura de imagenes

        self.fmVentanaPrincipal= CTkFrame(self
                                          ,fg_color=conGen.dicConfiguracionGeneralColores['fg_color']
                                          )
        self.fmVentanaPrincipal.pack()
        
#========Creacion Frame de Registros
        fmRegistro=CTkFrame(self.fmVentanaPrincipal
                            ,fg_color= conGen.dicConfiguracionGeneralColores["fg_color"]
                            ,width=conGen.dicConfig["anchoFrameRegistrar"]
                            ,height=conGen.dicConfig["altoFrameRegistrar"]
                            )
        fmRegistro.pack(padx=conGen.dicConfig["fmpadx"]
                        ,pady=conGen.dicConfig["fmpady"]
                        ,anchor=conGen.dicConfig["anchorFmRegistro"])

        #Boton Registrar factura 
        self.btRegistrarFactura=CTkButton(fmRegistro
                                       ,fg_color=conGen.dicConfiguracionGeneralColores["bgBotones"]
                                       #,bg_color='red'
                                       ,image=self.imagenRegistrar
                                       ,cursor=conGen.dicConfig["cursor"]
                                       ,text=' Registrar Facturas    '
                                       ,compound=conGen.dicConfig["compound"]
                                       ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                       #,text_color=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                       ,command=self.mostrarVentanaRegistrarFactura
                                       ,width=conGen.dicConfig["btwidthGeneral"]
                                       )
        self.btRegistrarFactura.place(x=conGen.dicConfig["xbtGeneralRegistro"]
                                      ,y=conGen.dicConfig["ybtRegistrarFactura"]
                                      )
        
        
        #boton Registrar Comercio
        self.btRegistrarComercio=CTkButton(fmRegistro
                                        ,fg_color=conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenRegistrar
                                        ,cursor=conGen.dicConfig["cursor"]
                                        ,text=' Registrar Comercios '
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                        #,fg_color=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,command=self.mostrarVentanaRegistrarComercio
                                        ,width=conGen.dicConfig["btwidthGeneral"]
                                        )
        self.btRegistrarComercio.place(x=conGen.dicConfig["xbtGeneralRegistro"]
                                       ,y=conGen.dicConfig["ybtRegistrarComercio"]
                                       )

        #Boton Registrar producto
        self.btRegistrarProducto=CTkButton(fmRegistro
                                        ,fg_color=conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenRegistrar
                                        ,text=' Registrar Productos  '
                                        ,cursor=conGen.dicConfig["cursor"]
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                        #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,command=self.mostrarVentanaRegistrarProducto
                                        ,width=conGen.dicConfig["btwidthGeneral"]
                                        )
        self.btRegistrarProducto.place(x=conGen.dicConfig["xbtGeneralRegistro"]
                                       ,y=conGen.dicConfig["ybtRegistrarProducto"]
                                       )
        
        #Boton Registrar Meracdo
        self.btRegistrarMercado=CTkButton(fmRegistro
                                          ,fg_color= conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenRegistrar
                                        ,text=' Agregar Mercados '
                                        ,cursor=conGen.dicConfig["cursor"]
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],15)
                                        #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,command=self.mostrarVentanaAgregarMercado
                                        ,width=conGen.dicConfig["btRegistrarMercadoWidth"]
                                        )
        self.btRegistrarMercado.place(x=conGen.dicConfig["xbtGeneralRegistro"]
                                       ,y=conGen.dicConfig["ybtRegistrarMercado"]
                                       )
        
        #Boton registrar compras
        self.btRegistraCompra=CTkButton(fmRegistro
                                          ,fg_color= conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenRegistrar
                                        ,text=' Registrar Compras '
                                        ,cursor=conGen.dicConfig["cursor"]
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],15)
                                        #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,command=self.mostrarVentanaRegistrarCompras
                                        ,width=conGen.dicConfig["btRegistrarCompraWidth"]
                                        )
        self.btRegistraCompra.place(x=conGen.dicConfig["xbtGeneralRegistro"]
                                    ,y=conGen.dicConfig["ybtRegistrarCompra"]
                                    )
        

#========Creación de frames de Consultas
        fmConsulta=CTkFrame(self.fmVentanaPrincipal
                            ,fg_color=conGen.dicConfiguracionGeneralColores["fg_color"]
                            ,width=conGen.dicConfig["anchoFrameConsultar"]
                            ,height=conGen.dicConfig["altoFrameConsultar"]
                        )
        fmConsulta.pack(padx=conGen.dicConfig["fmpadx"]
                        ,pady=conGen.dicConfig["fmpady"]
                        ,anchor=conGen.dicConfig["anchorFmConsultar"])
#------------------------------------
        #Boton consultar producto
        self.btConsultarProducto=CTkButton(fmConsulta
                                           ,fg_color= conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenConsultar
                                        ,cursor=conGen.dicConfig["cursor"]
                                        ,text=' Consultar Productos'
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                        #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,command= self.mostrarVentanaconsultarProductos
                                        ,width=conGen.dicConfig["btConsultarWidthGeneral"]
                                       )
        self.btConsultarProducto.place(x=conGen.dicConfig["xbtGeneralConsulta"]
                                     ,y=conGen.dicConfig["ybtConsultarProducto"]
                                     )
 #------------------------------------      
        #Boton consultar factura
        self.btConsultarFactura=CTkButton(fmConsulta
                                       ,fg_color=conGen.dicConfiguracionGeneralColores["bgBotones"]
                                       ,image=self.imagenConsultar
                                       ,cursor=conGen.dicConfig["cursor"]
                                       ,text=' Consultar Facturas  '
                                       ,compound=conGen.dicConfig["compound"]
                                       ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                       #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                       ,width=conGen.dicConfig["btConsultarWidthGeneral"]
                                       ,command=self.mostrarVentanaConsultarFacturas
                                       )
        self.btConsultarFactura.place(x=conGen.dicConfig["xbtGeneralConsulta"]
                                     ,y=conGen.dicConfig["ybtConsultarFactura"]
                                     )

 #------------------------------------      
        #Boton consultar comercio
        self.btConsultarComercio=CTkButton(fmConsulta
                                           ,fg_color= conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenConsultar,cursor=conGen.dicConfig["cursor"]
                                        ,text=' Consultar Comercios'
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                        #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,width=conGen.dicConfig["btConsultarWidthGeneral"]
                                        ,command=self.mostrarVentanaConsultarComercios
                                        )
        self.btConsultarComercio.place(x=conGen.dicConfig["xbtGeneralConsulta"]
                                       ,y=conGen.dicConfig["ybtConsultarComercio"]
                                       )
        ##Boton consultar Mercado
        self.btConsultarMercado=CTkButton(fmConsulta
                                          ,fg_color= conGen.dicConfiguracionGeneralColores["bgBotones"]
                                        ,image=self.imagenConsultar
                                        ,text=' Consultar Mercados'
                                        ,compound=conGen.dicConfig["compound"]
                                        ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                        #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                        ,width=conGen.dicConfig["btConsultarWidthGeneral"]
                                        ,command=self.mostrarVentanaConsultarMercados
                                        )
        self.btConsultarMercado.place(x=conGen.dicConfig["xbtGeneralConsulta"]
                                       ,y=conGen.dicConfig["ybtConsultarMercado"]
                                       )
        
        ##Boton consultar Compras
        self.btConsultarCompras=CTkButton(fmConsulta
                                          ,fg_color= conGen.dicConfiguracionGeneralColores["bgBotones"]
                                          ,image=self.imagenConsultar
                                          ,text=' Consultar Compras'
                                          ,compound=conGen.dicConfig["compound"]
                                          ,font=(conGen.dicConfiguracionGeneralFuentes["Fuente"],14)
                                          #,fg=conGen.dicConfiguracionGeneralColores["ColorLetras"]
                                          ,width=conGen.dicConfig["btConsultarWidthGeneral"]
                                          ,command=self.mostrarVentanaConsultarCompras
                                          )
        self.btConsultarCompras.place(x=conGen.dicConfig["xbtGeneralConsulta"]
                                       ,y=conGen.dicConfig["ybtConsultarCompras"]
                                       )
        


       
        
                
