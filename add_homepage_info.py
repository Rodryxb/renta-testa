import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"

# 1. Update title in base.html
base_path = os.path.join(PROJECT_DIR, 'templates', 'base.html')
with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

base_content = base_content.replace(
    '<title>Renta Testa | E-Commerce</title>',
    '<title>🚜 Renta Testa</title>'
)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_content)

print("Title updated in base.html")

# 2. Update index.html
index_path = os.path.join(PROJECT_DIR, 'templates', 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

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

# Insert the info bar right after the closing div of the hero section
hero_close_tag = "</div>\n    </div>\n\n    <!-- Secciones Informativas -->"
if "<!-- Barra de Información -->" not in index_content:
    index_content = index_content.replace(hero_close_tag, "</div>\n    </div>\n" + info_bar_html + "\n    <!-- Secciones Informativas -->")

modal_js_html = """
    <!-- Modal Dinámico de Información -->
    <div id="info-modal" class="hidden fixed inset-0 bg-black bg-opacity-70 z-50 flex items-center justify-center p-4 backdrop-blur-sm transition-opacity duration-300 opacity-0" onclick="closeInfoModal(event)">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md transform scale-95 transition-transform duration-300 relative border-t-8 border-brandYellow" onclick="event.stopPropagation()">
            <button onclick="closeInfoModal()" class="absolute top-4 right-4 text-gray-400 hover:text-red-500 transition">
                <i class="fa-solid fa-xmark text-2xl"></i>
            </button>
            <div class="p-8 text-center">
                <div id="info-modal-icon" class="text-6xl text-brandBlack mb-6 drop-shadow-md"></div>
                <h3 id="info-modal-title" class="text-2xl font-black text-brandBlack mb-4"></h3>
                <div id="info-modal-content" class="text-gray-600 leading-relaxed text-sm md:text-base"></div>
            </div>
            <div class="bg-gray-50 px-8 py-4 rounded-b-2xl border-t border-gray-100 flex justify-center">
                <button onclick="closeInfoModal()" class="bg-brandBlack text-brandYellow font-bold px-10 py-3 rounded-lg hover:bg-gray-900 transition shadow-md w-full">Cerrar</button>
            </div>
        </div>
    </div>

    <script>
        const infoData = {
            'origen': {
                title: 'El Origen del Proyecto',
                icon: '<i class="fa-solid fa-graduation-cap text-brandYellow"></i>',
                content: 'Renta Testa nació como un ambicioso proyecto de evaluación práctica para la asignatura de <b>Desarrollo Backend y Frontend</b>.<br><br>Su objetivo principal es demostrar la destreza técnica en la integración de arquitecturas Django, bases de datos complejas y el diseño de interfaces interactivas para E-Commerce.'
            },
            'trabaja': {
                title: 'Trabaja con Nosotros',
                icon: '<i class="fa-solid fa-envelope-open-text text-brandYellow"></i>',
                content: '¿Te apasiona el mundo de la maquinaria pesada y la tecnología?<br><br>Únete a nuestro equipo. Envía tu currículum directamente a nuestro equipo de reclutamiento escribiendo a:<br><br><a href="mailto:rentatesta@postula.cl" class="text-xl font-bold text-brandBlack hover:text-brandYellow transition block mt-2">rentatesta@postula.cl</a>'
            },
            'ubicacion': {
                title: 'Nuestra Ubicación',
                icon: '<i class="fa-solid fa-map-location-dot text-brandYellow"></i>',
                content: 'Nuestra base central de operaciones tecnológicas y estacionamiento de maquinarias se encuentra en:<br><br><span class="font-bold text-brandBlack text-lg block mt-2">Sede INACAP Temuco</span>Av. Luis Durand 02150<br>Temuco, Región de La Araucanía, Chile.'
            },
            'soporte': {
                title: 'Área de Soporte',
                icon: '<i class="fa-solid fa-life-ring text-brandYellow"></i>',
                content: '¿Tienes dudas sobre un contrato de arriendo o necesitas asistencia técnica urgente en faena?<br><br>Nuestro equipo de soporte está disponible para ti escribiendo a:<br><br><a href="mailto:rentatesta@soporte.com" class="text-xl font-bold text-brandBlack hover:text-brandYellow transition block mt-2">rentatesta@soporte.com</a>'
            }
        };

        function openInfoModal(type) {
            const modal = document.getElementById('info-modal');
            const data = infoData[type];
            
            document.getElementById('info-modal-icon').innerHTML = data.icon;
            document.getElementById('info-modal-title').innerText = data.title;
            document.getElementById('info-modal-content').innerHTML = data.content;
            
            modal.classList.remove('hidden');
            // Trigger reflow for animation
            void modal.offsetWidth;
            modal.classList.remove('opacity-0');
            modal.children[0].classList.remove('scale-95');
            modal.children[0].classList.add('scale-100');
        }

        function closeInfoModal(e) {
            if(e && e.target.id !== 'info-modal' && !e.target.closest('button')) return;
            const modal = document.getElementById('info-modal');
            modal.classList.add('opacity-0');
            modal.children[0].classList.remove('scale-100');
            modal.children[0].classList.add('scale-95');
            setTimeout(() => {
                modal.classList.add('hidden');
            }, 300);
        }
    </script>
"""

# Insert at the end of the block content
if "infoData =" not in index_content:
    index_content = index_content.replace("{% endblock %}", modal_js_html + "\n{% endblock %}")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Index updated with info bar and dynamic modals.")
