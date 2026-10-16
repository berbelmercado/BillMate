"""Genera el logo de BillMate: cuadrado redondeado con degradado y una bolsa de compras con una "B".

Se dibuja a 1024 px y se reduce con LANCZOS a cada tamaño, así queda nítido de 16 a 256 px.
Uso: python config_setup/generar_logo.py img   (escribe img/imgLogo.png e img/Logo.ico)
     python config_setup/generar_logo.py <otra carpeta> --previa   (además, logo_1024.png y previa_tamanos.png)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LADO = 1024
CIAN = (92, 225, 230)        #color del logo anterior
AZUL = (87, 108, 188)        #acento del tema (#576CBC)
VIOLETA = (74, 52, 160)
BLANCO = (255, 255, 255)


def degradado(lado):
    #Diagonal de cian (arriba a la izquierda) a azul y violeta (abajo a la derecha)
    imagen = Image.new('RGB', (lado, lado))
    pixeles = imagen.load()
    for y in range(lado):
        for x in range(lado):
            t = (x + y) / (2 * (lado - 1))
            if t < 0.55:
                a, b, u = CIAN, AZUL, t / 0.55
            else:
                a, b, u = AZUL, VIOLETA, (t - 0.55) / 0.45
            pixeles[x, y] = tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
    return imagen


def fuenteNegrita(tamano):
    for nombre in ('segoeuib.ttf', 'arialbd.ttf'):
        try:
            return ImageFont.truetype(str(Path('C:/Windows/Fonts') / nombre), tamano)
        except OSError:
            continue
    return ImageFont.load_default()


def dibujarLogo(conLetra=True):
    lado = LADO
    #Fondo: cuadrado redondeado con degradado
    mascara = Image.new('L', (lado, lado), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, lado - 1, lado - 1), radius=int(lado * 0.23), fill=255)
    logo = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    logo.paste(degradado(lado), (0, 0), mascara)

    #Bolsa de compras: cuerpo en trapecio (más ancho abajo), asa delgada y abierta, y la boca de la bolsa
    capa = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    dibujo = ImageDraw.Draw(capa)
    arriba, abajo = int(lado * 0.36), int(lado * 0.83)
    izqArriba, derArriba = int(lado * 0.25), int(lado * 0.75)
    izqAbajo, derAbajo = int(lado * 0.19), int(lado * 0.81)
    radio = int(lado * 0.05)

    def trapecio(dib, desplazamiento, color):
        #Trapecio con esquinas redondeadas: polígono más círculos en las esquinas
        d = desplazamiento
        puntos = [(izqArriba + radio, arriba + d), (derArriba - radio, arriba + d), (derArriba, arriba + radio + d)
                  ,(derAbajo, abajo - radio + d), (derAbajo - radio, abajo + d), (izqAbajo + radio, abajo + d)
                  ,(izqAbajo, abajo - radio + d), (izqArriba, arriba + radio + d)]
        dib.polygon(puntos, fill=color)
        for cx, cy in ((izqArriba + radio, arriba + radio + d), (derArriba - radio, arriba + radio + d)
                       ,(izqAbajo + radio, abajo - radio + d), (derAbajo - radio, abajo - radio + d)):
            dib.ellipse((cx - radio, cy - radio, cx + radio, cy + radio), fill=color)

    sombra = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    trapecio(ImageDraw.Draw(sombra), int(lado * 0.025), (20, 16, 60, 110))
    logo = Image.alpha_composite(logo, sombra.filter(ImageFilter.GaussianBlur(lado * 0.02)))

    #Asa: arco delgado y ancho que nace dentro de la boca de la bolsa
    grosor = int(lado * 0.035)
    asa = (int(lado * 0.35), int(lado * 0.19), int(lado * 0.65), int(lado * 0.53))
    dibujo.arc(asa, start=180, end=360, fill=BLANCO, width=grosor)
    medio = (asa[1] + asa[3]) // 2
    for x in (asa[0] + grosor // 2, asa[2] - grosor // 2):
        dibujo.line((x, medio, x, arriba + grosor), fill=BLANCO, width=grosor)
    trapecio(dibujo, 0, BLANCO)
    #Boca de la bolsa: franja más clara en el borde superior
    dibujo.rounded_rectangle((izqArriba + radio // 2, arriba + int(lado * 0.035), derArriba - radio // 2, arriba + int(lado * 0.055))
                             ,radius=int(lado * 0.01), fill=(225, 228, 245, 255))
    #Agujeros del asa
    for x in (asa[0] + grosor // 2, asa[2] - grosor // 2):
        r = int(lado * 0.018)
        dibujo.ellipse((x - r, arriba + int(lado * 0.075) - r, x + r, arriba + int(lado * 0.075) + r), fill=AZUL + (255,))
    cuerpo = (izqAbajo, arriba + int(lado * 0.06), derAbajo, abajo)

    if conLetra:
        #"B" en el color del acento, centrada en la bolsa
        fuente = fuenteNegrita(int(lado * 0.36))
        centroX = (cuerpo[0] + cuerpo[2]) / 2
        centroY = (cuerpo[1] + cuerpo[3]) / 2 + lado * 0.01
        dibujo.text((centroX, centroY), 'B', font=fuente, fill=AZUL + (255,), anchor='mm')

    return Image.alpha_composite(logo, capa)


def reducir(imagen, tamano):
    return imagen.resize((tamano, tamano), Image.LANCZOS)


def main(salida):
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    completo = dibujarLogo(True)
    #En 16 y 24 px la letra no se distingue: solo la bolsa, que se lee mejor
    simple = dibujarLogo(False)

    reducir(completo, 256).save(salida / 'imgLogo.png', optimize=True)
    tamanos = [16, 24, 32, 48, 64, 128, 256]
    imagenes = [reducir(simple if t <= 24 else completo, t) for t in tamanos]
    imagenes[-1].save(salida / 'Logo.ico', format='ICO', sizes=[(t, t) for t in tamanos], append_images=imagenes[:-1])

    if '--previa' not in sys.argv:
        print('listo:', salida / 'imgLogo.png', salida / 'Logo.ico')
        return
    #Vista previa: cada tamaño ampliado sin suavizar, sobre el fondo oscuro de la app
    previa =Image.new('RGBA', (sum(max(t * 4, 64) + 20 for t in tamanos) + 20, 1064), (20, 19, 34, 255))
    x = 20
    for t, imagen in zip(tamanos, imagenes):
        ampliada = imagen.resize((max(t * 4, 64),) * 2, Image.NEAREST)
        previa.alpha_composite(ampliada, (x, 20))
        x += ampliada.width + 20
    previa.save(salida / 'previa_tamanos.png')
    completo.save(salida / 'logo_1024.png')
    print('listo:', [p.name for p in salida.iterdir()])


if __name__ == '__main__':
    main(sys.argv[1])
