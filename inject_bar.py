import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
index_path = os.path.join(PROJECT_DIR, 'templates', 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

info_bar_html = """
<!-- Barra de Información -->
<div class="bg-brandBlack text-white border-b-4 border-brandYellow shadow-lg relative z-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-wrap justify-center md:justify-around items-center py-5 gap-6 text-sm">
            <button onclick="openInfoModal('origen')" class="hover:text-brandYellow transition font-bold flex items-center gap-2 transform hover:scale-105">
                <i class="fa-solid fa-code text-lg"></i> Origen
            </button>
            <button onclick="openInfoModal('trabaja')" class="hover:text-brandYellow transition font-bold flex items-center gap-2 transform hover:scale-105">
                <i class="fa-solid fa-briefcase text-lg"></i> Trabaja con nosotros
            </button>
            <button onclick="openInfoModal('ubicacion')" class="hover:text-brandYellow transition font-bold flex items-center gap-2 transform hover:scale-105">
                <i class="fa-solid fa-location-dot text-lg"></i> Ubicación
            </button>
            <button onclick="openInfoModal('soporte')" class="hover:text-brandYellow transition font-bold flex items-center gap-2 transform hover:scale-105">
                <i class="fa-solid fa-headset text-lg"></i> Área de soporte
            </button>
        </div>
    </div>
</div>
"""

# Insert before <!-- Modal Edición Inline -->
if "<!-- Barra de Información -->" not in content:
    content = content.replace("<!-- Modal Edici", info_bar_html + "\n<!-- Modal Edici")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Barra inyectada con exito.")
else:
    print("La barra ya existe en el archivo.")
