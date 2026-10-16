#Configuración común de los botones
dicConfig={
           #Cursor en botones
            "cursor":"hand2"#plus

           #ubicación de la imagen dentro del botón
            ,"compound":'left'

            ,"corner_radius":8
        }

#Colores de la aplicación (barra lateral, páginas, tarjetas, campos y tablas)
dicTema={
            "fondo":'#141322'            #área de contenido
            ,"lateral":'#1B1A2E'         #barra lateral
            ,"tarjeta":'#232238'
            ,"borde":'#2F2D4A'
            ,"acento":'#576CBC'          #botón principal y fila seleccionada
            ,"acentoHover":'#6B80D4'
            ,"botonHover":'#2A2944'      #botones planos al pasar el mouse y botón activo de la barra lateral
            ,"texto":'#ECECF4'
            ,"textoSuave":'#9A98B5'
            ,"filaPar":'#1C1B30'
            ,"filaImpar":'#232238'
            ,"encabezadoTabla":'#2A2944'
            ,"campo":'#1C1B30'           #fondo de los campos de texto
            ,"campoDeshabilitado":'#191828'
            ,"exito":'#7FD18B'
            ,"peligro":'#E05A5A'
            ,"peligroHover":'#F07070'
}

#Tamaños y fuentes comunes de las páginas (views/componentes.py y views/paginas/)
dicConfigPaginas={
            "fuente":'Helvetica'
            ,"tamanoTitulo":24
            ,"tamanoSubtitulo":13
            ,"tamanoEtiqueta":12
            ,"tamanoCampo":14
            ,"tamanoBoton":14
            ,"tamanoTabla":12
            ,"tamanoTituloPanel":16

            ,"altoCampo":34
            ,"altoBoton":36
            ,"radio":8
            ,"radioTarjeta":12
            ,"altoFilaTabla":30

            ,"padX":16
            ,"padY":10
            ,"padTarjeta":14

            #Panel de formulario de las pantallas de datos
            ,"anchoPanel":300
            ,"anchoBuscador":420

            #Lista desplegable del autocompletado (views/campoAutocompletar.py)
            ,"listaMaxOpciones":50
            ,"listaMaxVisibles":8
            ,"listaTamanoFuente":12

            #Selector de fecha
            ,"anchoFecha":130
            ,"anchoBotonFecha":40
            ,"padCalendario":10

            #Página Mercados: columnas de la tabla y ancho mínimo de los campos del panel de edición
            ,"merColProducto":200
            ,"merColCantidad":70
            ,"merColPrecio":100
            ,"merColTotal":100
            ,"merColFactura":100
            ,"merColFecha":95
            ,"merColComercio":140
            ,"merColCompra":150
            ,"merAnchoCampo":60
            ,"merAnchoSegmentos":300

            #Página Agregar Mercados: columnas de la tabla de ítems y botones
            ,"comColProducto":320
            ,"comColCantidad":90
            ,"comColPrecio":140
            ,"comColTotal":140
            ,"comAnchoBoton":140
            ,"comAnchoBotonCargar":180
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
