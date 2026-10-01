import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(26, 26, 26) # Dark gray
        self.cell(0, 10, 'Torpedo de Estudio: Proyecto Renta Testa', border=False, align='C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(217, 161, 38) # Brand yellow/gold
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        # multi_cell automatically handles line breaks
        self.multi_cell(0, 8, body)
        self.ln(5)

pdf = PDF()
pdf.add_page()

# Intro
intro_text = (
    "Este documento es tu 'torpedo' oficial para entender como funciona tu E-Commerce por debajo. "
    "Te lo explicare con manzanas, como si fuera un restaurante, para que sepas exactamente donde ubicar "
    "cada cosa si el profesor te pregunta."
)
pdf.chapter_body(intro_text)

# Cap 1
pdf.chapter_title("1. La Arquitectura (El Restaurante)")
c1_text = (
    "Tu proyecto tiene dos grandes mundos que conversan entre si:\n\n"
    "EL CLIENTE (Frontend): Son tus archivos HTML y JavaScript. Viven en la carpeta 'templates/'. "
    "Piensa que son los menus impresos y los botones que el usuario puede tocar en su navegador. "
    "Ellos nunca tocan la base de datos directamente.\n\n"
    "EL SERVIDOR (Backend): Es tu codigo Python (Django) que vive en carpetas como 'core/' y 'renting/'. "
    "Es la 'Cocina' del restaurante. Protege los datos, hace matematicas y guarda informacion en PostgreSQL.\n\n"
    "EL MESERO (API REST): Cuando el cliente presiona 'Agregar al Carro', JavaScript manda un 'mesero' "
    "al servidor. Ese mensaje viaja en un formato de texto llamado JSON."
)
pdf.chapter_body(c1_text)

# Cap 2
pdf.chapter_title("2. Mapa del Tesoro: Donde ubicarme si me piden un cambio")
c2_text = (
    "Si te piden cambiar algo durante la presentacion, esto es lo que debes buscar:\n\n"
    "- SI TE PIDEN CAMBIAR UN BOTON O EL DISEÑO: Ve directo a la carpeta 'templates/'. Ahi estan todos tus "
    "archivos visuales como 'index.html', 'dashboard.html' o 'producto_detalle.html'.\n\n"
    "- SI TE PIDEN AGREGAR UNA NUEVA CARACTERISTICA A LA BASE DE DATOS (Ej: Que las maquinas ahora tengan color): "
    "Ve al archivo 'renting/models.py'. Ahi estan definidas tus tablas como Maquinaria, Usuario y ServicioExterno.\n\n"
    "- SI TE PIDEN CAMBIAR LA MATEMATICA O LOGICA (Ej: Que el delivery ahora cueste el doble): "
    "Ve a 'renting/views.py' o los scripts de tus 'templates'. 'views.py' es el cerebro donde le dices a Django "
    "que hacer cuando alguien pide datos.\n\n"
    "- SI ALGO FALLA EN LA RUTA (Ej: /carro te da error 404): Ve a 'core/urls.py' o 'renting/urls.py'. "
    "Ahi esta el mapa de navegacion."
)
pdf.chapter_body(c2_text)

# Cap 3
pdf.chapter_title("3. Conceptos Dificiles Explicados Facil")
c3_text = (
    "- ¿Que es JWT (Autenticacion)?: Imagina que cuando el usuario inicia sesion, el servidor no se acuerda de el. "
    "En su lugar, le entrega un 'brazalete VIP' encriptado (el Token). El navegador guarda ese brazalete en el 'localStorage'. "
    "Cada vez que el usuario quiere ver su perfil, le muestra el brazalete a Django y Django lo deja pasar. Asi de simple!\n\n"
    "- ¿Que es Tailwind CSS?: Tradicionalmente la gente escribe archivos CSS gigantes y aparte. Nosotros con Tailwind "
    "simplemente le pusimos palabras clave al HTML. Si pusimos 'bg-black', el fondo se hace negro. 'text-white', texto blanco. "
    "Por eso no ves archivos CSS externos en tu proyecto!\n\n"
    "- ¿Que es un Serializador (serializers.py)?: Es un simple TRADUCTOR. Toma tu maquina de la base de datos (que es Python) "
    "y la convierte a JSON (texto entendible por navegadores) para poder mandarla por internet."
)
pdf.chapter_body(c3_text)

# Cap 4
pdf.chapter_title("4. Como subimos archivos pesados (Imagenes)")
c4_text = (
    "Originalmente tu plataforma solo aceptaba links de internet para las imagenes. Para hacer que aceptara "
    "archivos reales de tu pendrive, hicimos que el formulario dejara de mandar JSON (que solo soporta texto) "
    "y pasara a mandar 'FormData' (que empaqueta archivos binarios). Django lo lee, guarda la foto en la "
    "carpeta 'media/' y anota el nombre en la base de datos."
)
pdf.chapter_body(c4_text)

# Output
pdf.output("Torpedo_RentaTesta.pdf")
print("PDF Generado!")
