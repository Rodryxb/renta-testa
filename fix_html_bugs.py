import os
import re

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"

auth_path = os.path.join(PROJECT_DIR, 'templates', 'auth.html')
with open(auth_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("/[ó-Z]/", "/[A-Z]/")
content = content.replace("ógrega", "Agrega")

with open(auth_path, 'w', encoding='utf-8') as f:
    f.write(content)

cat_path = os.path.join(PROJECT_DIR, 'templates', 'catalogo.html')
with open(cat_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("MóQUINóRIó", "MAQUINARIA")
content = content.replace("MóTERIóL", "MATERIAL")
content = content.replace("BóJó", "BAJA")
content = content.replace("MEDIó", "MEDIA")
content = content.replace("óLTó", "ALTA")
content = content.replace("OTRóS", "OTRAS")
content = content.replace("órriendo", "Arriendo")
content = content.replace("óhorro", "Ahorro")
content = content.replace("COMPRóR", "COMPRAR")
content = content.replace("AGREGAR óL CóRRO", "AGREGAR AL CARRO")
content = content.replace("Móquinas", "Máquinas")

with open(cat_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Plantillas HTML reparadas críticamente.")
