#Este diccionario guarda los colores que usa el sistema
dicConfiguracionGeneralColores={"bgGeneral":'#202020'   #'#75B3FA'#''#75DCFA #202020,#35155D
                         ,"fg_color":"#17153B"#"#0B2447"
                         ,"bgBotones":'#576CBC'#"#DEFA7F"
                         ,"bgEntrys":"#3A3A3A"
                         ,"bgLabels":"#C8ACD6" #576CBC,#607CEB
                         ,"ColorLetras":"#A9A9A9"
                         ,"colorLetrasLabel":'black'
                         ,"colorLetrasEntry":'black'
}

#En este diccionario se guardan los tipos de fuentes que se usa en todo el sistema
dicConfiguracionGeneralFuentes={"Fuente":'Helvetica' 
                                ,"tamano":14
                                }

"""
Diccionario con los valores de las posiciones de los labels,entrys, frames
x al inicio es para los place 
lb=label
construcción del nombre:
x argumento de posición ya sea x o y para place, lb para indicar label nombre del botrón
"""

#En este diccionario están las configuraciones de posiciones los botones del modulo frameMenu
dicConfig={
           #configuración FrameMenu
             "fmYPrincipal":30
            ,"fmWidthPrincipal":215 
            ,"fmHeightPrincipal":450
            ,"anchorFmPrincipal":'nw'

           #configuracion frame de registro
            ,"anchoFrameRegistrar":195
            ,"altoFrameRegistrar":260
            ,"padyyFmRegistrar":30
            ,"fmpadx":10
            ,"fmpady":5
            ,"anchorFmRegistro":'nw'
         
           #Cursor en botones
            ,"cursor":"hand2"#plus

           #ubicación de la imagen dentro del botón
            ,"compound":'left'
           #configuracion botones registro 
            ,"xbtGeneralRegistro":0  
            ,"btwidthGeneral":185
            ,"btRegistrarMercadoWidth":195
            ,"btRegistrarCompraWidth":195
            ,"ybtRegistrarFactura":0
            ,"ybtRegistrarComercio":55
            ,"ybtRegistrarProducto":109
            ,"ybtRegistrarMercado":161
            ,"ybtRegistrarCompra":215

            #configuración Frame Consultar 
            ,"anchoFrameConsultar":195
            ,"altoFrameConsultar":260
            ,"fmpadx":10
            ,"fmpady":5
            ,"anchorFmConsultar":'nw'

             #configuracion Botones Consultas
            ,"xbtGeneralConsulta":0  
            ,"ybtConsultarProducto":0
            ,"ybtConsultarFactura":55
            ,"ybtConsultarComercio":109
            ,"ybtConsultarMercado":161
            ,"ybtConsultarCompras":215

            ,"btConsultarWidthGeneral":195

            ,"corner_radius":8
        }
#Este diccionario guarda la configuración de posición para los widgets en el modulo frameListasTreview
dicConfigFrameUltimoMercado={
                              #Configuración Frame Principal
                              "fmXFramePrincipal":220
                              ,"fmyFramePrincipal":32
                              ,"fmWidthFramePrincipal":1090
                              ,"fmHeightFramePrincipal":960
                              #Configuración Label titulo de la tabla
                              ,"lbPady":5 
                              ,"fmDatosX":550
                              ,"fmDatosY":310



}