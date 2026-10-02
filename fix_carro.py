import os
import re

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
carro_path = os.path.join(PROJECT_DIR, 'templates', 'carro.html')
with open(carro_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("IR ó PóGóR", "IR A PAGAR")
content = content.replace("BOLETó", "BOLETA")
content = content.replace("FóCTURó", "FACTURA")
content = content.replace("CLóVE", "CLAVE")
content = content.replace("REóL", "REAL")
content = content.replace("ósumiendo", "Asumiendo")
content = content.replace("Transacción", "Transacción")

with open(carro_path, 'w', encoding='utf-8') as f:
    f.write(content)
