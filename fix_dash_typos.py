import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
dash_path = os.path.join(PROJECT_DIR, 'templates', 'dashboard.html')

with open(dash_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("óvanzado", "Avanzado")
content = content.replace("TóBS", "TABS")
content = content.replace("BóNNER", "BANNER")
content = content.replace("óltarnativo", "Alternativo")
content = content.replace("MaQUINóS", "MAQUINAS")
content = content.replace("SEPóRóDOS", "SEPARADOS")
content = content.replace("CóRGóR", "CARGAR")
content = content.replace("DóTOS", "DATOS")
content = content.replace("óltarnativo", "Alternativo")

with open(dash_path, 'w', encoding='utf-8') as f:
    f.write(content)
