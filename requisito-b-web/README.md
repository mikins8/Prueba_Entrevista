
# Requisito B — Aplicación web de gestión de clientes

## Descripción
Aplicación web desarrollada con Python, Flask, SQLite, HTML y CSS para gestionar clientes.

## Funcionalidades
- Listado de clientes con paginación.
- Búsqueda por contacto, empresa y email.
- Filtros por estado, país y comercial.
- Consulta del detalle de cada cliente.
- Creación, edición y eliminación de registros.
- Validación básica de datos.
- Consultas SQL parametrizadas.

## Tecnologías
- Python
- Flask
- SQLite
- HTML5
- CSS3

## Instalación

1. Copiar `clientes.db` a esta carpeta.
2. Crear un entorno virtual:
   `py -m venv .venv`
3. Activarlo en PowerShell:
   `.\.venv\Scripts\Activate.ps1`
4. Instalar las dependencias:
   `pip install -r requirements.txt`
5. Ejecutar la aplicación:
   `python app.py`
6. Abrir http://127.0.0.1:5000 en el navegador.

## Decisión técnica
Se ha elegido Flask por su sencillez y ligereza para desarrollar
una aplicación CRUD pequeña. SQLite permite reutilizar la base
de datos del Requisito A sin configurar un servidor adicional.