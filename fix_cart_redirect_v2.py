import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
detalle_path = os.path.join(PROJECT_DIR, 'templates', 'producto_detalle.html')

with open(detalle_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace setTimeout redirect with badge update
old_redirect = "setTimeout(() => window.location.href = '/carro/', 1500);"

new_badge_update = """
            // Actualizar la burbuja del carrito global
            fetch('/api/carro-arriendo/', {
                headers: { 'Authorization': `Bearer ${token}` }
            }).then(r => r.json()).then(data => {
                const badge = document.getElementById('global-cart-badge');
                if(badge && data.items) {
                    badge.innerText = data.items.length;
                    badge.classList.remove('hidden');
                }
            });"""

content = content.replace(old_redirect, new_badge_update)

with open(detalle_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Redirección por setTimeout eliminada.")
