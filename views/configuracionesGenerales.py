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

#Configuración común de los botones de todas las ventanas
dicConfig={
           #Cursor en botones
            "cursor":"hand2"#plus

           #ubicación de la imagen dentro del botón
            ,"compound":'left'

            ,"corner_radius":8
        }

#Colores de la pantalla de inicio (barra lateral, tarjetas y tabla de la última compra)
dicTemaInicio={
            "fondo":'#141322'            #área de contenido
            ,"lateral":'#1B1A2E'         #barra lateral
            ,"tarjeta":'#232238'
            ,"borde":'#2F2D4A'
            ,"acento":'#576CBC'          #botón principal y fila seleccionada
            ,"acentoHover":'#6B80D4'
            ,"botonHover":'#2A2944'      #botones de la barra lateral al pasar el mouse
            ,"texto":'#ECECF4'
            ,"textoSuave":'#9A98B5'
            ,"filaPar":'#1C1B30'
            ,"filaImpar":'#232238'
            ,"encabezadoTabla":'#2A2944'
}

#Tamaños y fuentes de la pantalla de inicio
dicConfigInicio={
            #Ventana: tamaño inicial = pantalla menos estos márgenes; tamaño mínimo
            "margenAncho":190
            ,"margenAlto":160
            ,"vnX":100
            ,"vnY":30
            ,"vnMinWidth":1000
            ,"vnMinHeight":560

            #Barra lateral
            ,"anchoLateral":230
            ,"logoTamano":40
            ,"iconoTamano":18
            ,"altoBoton":32
            ,"altoBotonPrincipal":40
            ,"radioBoton":8
            ,"altoSeccion":20

            #Espaciado
            ,"padX":16
            ,"padY":10
            ,"padTarjeta":14

            #Fuentes
            ,"fuente":'Helvetica'
            ,"tamanoNombreApp":20
            ,"tamanoTitulo":24
            ,"tamanoSubtitulo":13
            ,"tamanoSeccion":11
            ,"tamanoBoton":14
            ,"tamanoTarjetaTitulo":12
            ,"tamanoTarjetaValor":22
            ,"tamanoTarjetaDetalle":12
            ,"tamanoTabla":12

            #Tarjetas y tabla
            ,"radioTarjeta":12
            ,"largoTextoTarjeta":18      #caracteres antes de recortar con "…"
            ,"largoDetalleTarjeta":30
            ,"altoFilaTabla":30
            ,"colProductoWidth":260
            ,"colCantidadWidth":70
            ,"colPrecioWidth":110
            ,"colTotalWidth":110
            ,"colFacturaWidth":110
            ,"colFechaWidth":100
            ,"colComercioWidth":170
}
