
import os
import sqlite3
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, abort
)

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "clave-local-de-desarrollo"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "clientes.db")
PER_PAGE = 10


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_cliente(cliente_id):
    with get_db() as conn:
        cliente = conn.execute(
            "SELECT * FROM clientes WHERE id = ?",
            (cliente_id,)
        ).fetchone()

    if cliente is None:
        abort(404)

    return cliente


def validar_formulario(form):
    errores = []

    nombre = form.get("nombre_contacto", "").strip()
    empresa = form.get("empresa", "").strip()
    email = form.get("email", "").strip()
    estado = form.get("estado", "").strip()
    fecha = form.get("fecha_alta", "").strip()
    facturacion = form.get("facturacion_acumulada", "0").strip()

    if not nombre:
        errores.append("El nombre de contacto es obligatorio.")

    if not empresa:
        errores.append("La empresa es obligatoria.")

    if not email or "@" not in email:
        errores.append("Introduce un correo electrónico válido.")

    if estado not in ("Activo", "Inactivo"):
        errores.append("Selecciona un estado válido.")

    if not fecha:
        errores.append("La fecha de alta es obligatoria.")

    try:
        if float(facturacion) < 0:
            errores.append("La facturación no puede ser negativa.")
    except ValueError:
        errores.append("La facturación debe ser un número.")

    return errores


def obtener_valores(form):
    return (
        form.get("nombre_contacto", "").strip(),
        form.get("empresa", "").strip(),
        form.get("email", "").strip(),
        form.get("telefono", "").strip(),
        form.get("estado", "Activo").strip(),
        form.get("direccion", "").strip(),
        form.get("pais", "").strip(),
        form.get("comercial_asignado", "").strip(),
        form.get("fecha_alta", "").strip(),
        float(form.get("facturacion_acumulada", "0") or 0),
    )


@app.route("/")
def index():
    busqueda = request.args.get("q", "").strip()
    estado = request.args.get("estado", "").strip()
    pais = request.args.get("pais", "").strip()
    comercial = request.args.get("comercial", "").strip()

    try:
        pagina = max(1, int(request.args.get("pagina", 1)))
    except ValueError:
        pagina = 1

    condiciones = []
    parametros = []

    if busqueda:
        condiciones.append(
            "(nombre_contacto LIKE ? OR empresa LIKE ? OR email LIKE ?)"
        )
        termino = f"%{busqueda}%"
        parametros.extend([termino, termino, termino])

    if estado in ("Activo", "Inactivo"):
        condiciones.append("estado = ?")
        parametros.append(estado)

    if pais:
        condiciones.append("pais = ?")
        parametros.append(pais)

    if comercial:
        condiciones.append("comercial_asignado = ?")
        parametros.append(comercial)

    where = (
        " WHERE " + " AND ".join(condiciones)
        if condiciones else ""
    )

    with get_db() as conn:
        total = conn.execute(
            f"SELECT COUNT(*) FROM clientes{where}",
            parametros
        ).fetchone()[0]

        total_paginas = max(1, (total + PER_PAGE - 1) // PER_PAGE)
        pagina = min(pagina, total_paginas)
        offset = (pagina - 1) * PER_PAGE

        clientes = conn.execute(
            f"""SELECT * FROM clientes{where}
                ORDER BY id DESC LIMIT ? OFFSET ?""",
            parametros + [PER_PAGE, offset]
        ).fetchall()

        paises = conn.execute(
            """SELECT DISTINCT pais FROM clientes
               WHERE pais IS NOT NULL AND pais != ''
               ORDER BY pais"""
        ).fetchall()

        comerciales = conn.execute(
            """SELECT DISTINCT comercial_asignado FROM clientes
               WHERE comercial_asignado IS NOT NULL
               AND comercial_asignado != ''
               ORDER BY comercial_asignado"""
        ).fetchall()

    return render_template(
        "index.html",
        clientes=clientes,
        busqueda=busqueda,
        estado=estado,
        pais=pais,
        comercial=comercial,
        paises=paises,
        comerciales=comerciales,
        pagina=pagina,
        total_paginas=total_paginas,
        total=total
    )


@app.route("/cliente/<int:cliente_id>")
def detalle(cliente_id):
    cliente = get_cliente(cliente_id)
    return render_template("detail.html", cliente=cliente)


@app.route("/cliente/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        errores = validar_formulario(request.form)

        if errores:
            for error in errores:
                flash(error, "error")

            return render_template(
                "form.html", cliente=request.form, modo="nuevo"
            )

        try:
            with get_db() as conn:
                conn.execute(
                    """INSERT INTO clientes (
                        nombre_contacto, empresa, email, telefono,
                        estado, direccion, pais, comercial_asignado,
                        fecha_alta, facturacion_acumulada
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    obtener_valores(request.form)
                )

            flash("Cliente creado correctamente.", "success")
            return redirect(url_for("index"))

        except sqlite3.IntegrityError:
            flash(
                "No se pudo crear el cliente. "
                "Comprueba si el correo ya existe.",
                "error"
            )

    return render_template("form.html", cliente={}, modo="nuevo")


@app.route("/cliente/<int:cliente_id>/editar",
           methods=["GET", "POST"])
def editar(cliente_id):
    cliente = get_cliente(cliente_id)

    if request.method == "POST":
        errores = validar_formulario(request.form)

        if errores:
            for error in errores:
                flash(error, "error")

            return render_template(
                "form.html", cliente=request.form, modo="editar"
            )

        try:
            with get_db() as conn:
                conn.execute(
                    """UPDATE clientes SET
                        nombre_contacto = ?,
                        empresa = ?,
                        email = ?,
                        telefono = ?,
                        estado = ?,
                        direccion = ?,
                        pais = ?,
                        comercial_asignado = ?,
                        fecha_alta = ?,
                        facturacion_acumulada = ?,
                        fecha_ultima_modificacion = CURRENT_TIMESTAMP
                    WHERE id = ?""",
                    obtener_valores(request.form) + (cliente_id,)
                )

            flash("Cliente actualizado correctamente.", "success")
            return redirect(
                url_for("detalle", cliente_id=cliente_id)
            )

        except sqlite3.IntegrityError:
            flash(
                "No se pudo actualizar. Comprueba si el correo "
                "ya pertenece a otro cliente.",
                "error"
            )

    return render_template(
        "form.html", cliente=dict(cliente), modo="editar"
    )


@app.route("/cliente/<int:cliente_id>/eliminar", methods=["POST"])
def eliminar(cliente_id):
    get_cliente(cliente_id)

    with get_db() as conn:
        conn.execute(
            "DELETE FROM clientes WHERE id = ?",
            (cliente_id,)
        )

    flash("Cliente eliminado correctamente.", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def no_encontrado(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        raise FileNotFoundError(
            "No se encuentra clientes.db. "
            "Copia aquí la base de datos del Requisito A."
        )

    app.run(debug=True)