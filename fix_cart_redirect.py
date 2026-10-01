import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
detalle_path = os.path.join(PROJECT_DIR, 'templates', 'producto_detalle.html')

with open(detalle_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Snippet to replace the redirect with a Toast + Badge Update
new_success_logic = """if(res.ok) {
            showToast('¡Producto agregado al carro de compras!');
            
            // Actualizar la burbuja del carrito global
            fetch('/api/carro-arriendo/', {
                headers: { 'Authorization': `Bearer ${token}` }
            }).then(r => r.json()).then(data => {
                const badge = document.getElementById('global-cart-badge');
                if(badge && data.items) {
                    badge.innerText = data.items.length;
                    badge.classList.remove('hidden');
                }
            });
        }"""

# Reemplazar en agregarCarroMaquina
content = content.replace(
    "if(res.ok) {\n            window.location.href = '/carro/';\n        }",
    new_success_logic
)

# Reemplazar en agregarCarroMaterial (por si acaso también existe idéntico)
content = content.replace(
    "if(res.ok) {\n            window.location.href = '/carro/';\n        }",
    new_success_logic
)

with open(detalle_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Redirección al carrito eliminada.")
