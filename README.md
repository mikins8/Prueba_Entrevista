# Prueba_Entrevista

# Prueba técnica — Gestión de clientes

## Descripción

Proyecto desarrollado para una prueba técnica de selección de Desarrollador Junior de Sistemas y Soporte Backend.

El objetivo es implementar una solución de gestión de clientes utilizando SQLite como base de datos y Python para desarrollar una aplicación web.

## Requisitos implementados

### Requisito A — Base de datos SQLite

* Creación de la estructura de la base de datos.
* Tabla de clientes con los campos solicitados.
* Inserción de 50 clientes ficticios.
* Restricciones para garantizar la integridad de los datos.

### Requisito B — Aplicación web en Python

* Framework Flask.
* Listado de clientes con paginación.
* Búsqueda por nombre, empresa y correo electrónico.
* Filtros por estado, país y comercial asignado.
* Consulta individual de clientes.
* Operaciones CRUD: crear, consultar, editar y eliminar.
* Validación de datos y gestión de errores.
* Persistencia de los cambios en SQLite.

### Requisito C

Pendiente de implementar según el enunciado correspondiente.

## Tecnologías utilizadas

* Python 3
* Flask
* SQLite
* SQL
* HTML5 y CSS3
* Jinja2

## Instalación y ejecución

1. Clonar el repositorio.
2. Acceder a la carpeta `requisito-b-web`.
3. Crear y activar un entorno virtual.
4. Instalar las dependencias con `pip install -r requirements.txt`.
5. Ejecutar `python app.py`.
6. Abrir `http://127.0.0.1:5000` en el navegador.

## Datos de prueba

La aplicación utiliza clientes ficticios para facilitar las pruebas de las funcionalidades.

## Decisiones técnicas

Se ha elegido Flask por su sencillez, flexibilidad y adecuación para una aplicación CRUD de tamaño reducido. SQLite permite almacenar los datos de forma persistente sin necesidad de configurar un servidor de base de datos independiente.

La aplicación utiliza consultas SQL parametrizadas para reducir el riesgo de inyección SQL.
