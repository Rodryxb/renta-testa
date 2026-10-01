import os
import re

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"
dash_path = os.path.join(PROJECT_DIR, 'templates', 'dashboard.html')

with open(dash_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace saveMaquinaria
old_save_maq = """    async function saveMaquinaria(e) {
        e.preventDefault();
        const id = document.getElementById('maq-id').value;
        const tipo = document.getElementById('maq-tipo').value;
        const payload = {
            tipo: tipo,
            nombre: document.getElementById('maq-nombre').value,
            categoria: document.getElementById('maq-categoria').value,
            tarifa_diaria: document.getElementById('maq-tarifa').value,
            garantia: tipo === 'MATERIAL' ? 0 : document.getElementById('maq-garantia').value,
            stock_disponible: document.getElementById('maq-stock').value,
            imagen_url: document.getElementById('maq-img-url').value || null
        };
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/maquinarias/${id}/` : '/api/maquinarias/';
        await fetch(url, { method: method, headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }, body: JSON.stringify(payload) });
        closeModalMaq(); loadData();
    }"""

new_save_maq = """    async function saveMaquinaria(e) {
        e.preventDefault();
        const id = document.getElementById('maq-id').value;
        const tipo = document.getElementById('maq-tipo').value;
        
        const formData = new FormData();
        formData.append('tipo', tipo);
        formData.append('nombre', document.getElementById('maq-nombre').value);
        formData.append('categoria', document.getElementById('maq-categoria').value);
        formData.append('tarifa_diaria', document.getElementById('maq-tarifa').value);
        formData.append('garantia', tipo === 'MATERIAL' ? 0 : document.getElementById('maq-garantia').value);
        formData.append('stock_disponible', document.getElementById('maq-stock').value);
        
        const fileInput = document.getElementById('maq-img-upload');
        if(fileInput && fileInput.files[0]) {
            formData.append('imagen_upload', fileInput.files[0]);
        }
        
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/maquinarias/${id}/` : '/api/maquinarias/';
        await fetch(url, { method: method, headers: { 'Authorization': `Bearer ${token}` }, body: formData });
        closeModalMaq(); loadData();
    }"""
content = content.replace(old_save_maq, new_save_maq)

# Fix editMaquinaria to NOT try to set value on file input
old_edit_maq = "document.getElementById('maq-img-url').value = (m.imagen_final || m.imagen_url) || '';"
new_edit_maq = "if(document.getElementById('maq-img-upload')) document.getElementById('maq-img-upload').value = '';"
content = content.replace(old_edit_maq, new_edit_maq)

# Replace saveServicio
old_save_serv = """    async function saveServicio(e) {
        e.preventDefault();
        const id = document.getElementById('serv-id').value;
        const payload = {
            titulo: document.getElementById('serv-titulo').value,
            descripcion: document.getElementById('serv-desc').value,
            nombre_encargado: document.getElementById('serv-encargado').value,
            titulo_universitario: document.getElementById('serv-titulou').value,
            telefono: document.getElementById('serv-tel').value,
            horario: document.getElementById('serv-horario').value,
            foto_url: document.getElementById('serv-img-url').value || null
        };
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/servicios/${id}/` : '/api/servicios/';
        await fetch(url, { method: method, headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }, body: JSON.stringify(payload) });
        closeModalServ(); loadData();
    }"""

new_save_serv = """    async function saveServicio(e) {
        e.preventDefault();
        const id = document.getElementById('serv-id').value;
        
        const formData = new FormData();
        formData.append('titulo', document.getElementById('serv-titulo').value);
        formData.append('descripcion', document.getElementById('serv-desc').value);
        formData.append('nombre_encargado', document.getElementById('serv-encargado').value);
        formData.append('titulo_universitario', document.getElementById('serv-titulou').value);
        formData.append('telefono', document.getElementById('serv-tel').value);
        formData.append('horario', document.getElementById('serv-horario').value);
        
        const fileInput = document.getElementById('serv-img-upload');
        if(fileInput && fileInput.files[0]) {
            formData.append('foto_upload', fileInput.files[0]);
        }
        
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/servicios/${id}/` : '/api/servicios/';
        await fetch(url, { method: method, headers: { 'Authorization': `Bearer ${token}` }, body: formData });
        closeModalServ(); loadData();
    }"""
content = content.replace(old_save_serv, new_save_serv)

# Fix editServicio
old_edit_serv = "document.getElementById('serv-img-url').value = (s.foto_final || s.foto_url) || '';"
new_edit_serv = "if(document.getElementById('serv-img-upload')) document.getElementById('serv-img-upload').value = '';"
content = content.replace(old_edit_serv, new_edit_serv)


with open(dash_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("JS del Dashboard completamente reparado.")
