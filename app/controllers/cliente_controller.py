from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.controllers.auth_controller import login_obrigatorio
from app.models import ValidacaoError
from app.models.cliente import Cliente

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/")
@login_obrigatorio
def listar():
    busca = request.args.get("busca", "")
    return render_template("clientes/lista.html", clientes=Cliente.listar(busca), busca=busca)


@bp.route("/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo():
    if request.method == "POST":
        try:
            Cliente.criar(request.form)
            flash("Cliente cadastrado com sucesso!", "sucesso")
            return redirect(url_for("clientes.listar"))
        except ValidacaoError as e:
            for erro in e.erros:
                flash(erro, "erro")
    return render_template("clientes/form.html", cliente=request.form, titulo="Novo cliente")


@bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar(cliente_id):
    cliente = Cliente.buscar_por_id(cliente_id) or abort(404)
    if request.method == "POST":
        try:
            Cliente.atualizar(cliente_id, request.form)
            flash("Cliente atualizado com sucesso!", "sucesso")
            return redirect(url_for("clientes.listar"))
        except ValidacaoError as e:
            for erro in e.erros:
                flash(erro, "erro")
            cliente = request.form
    return render_template("clientes/form.html", cliente=cliente, titulo="Editar cliente")


@bp.route("/<int:cliente_id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir(cliente_id):
    Cliente.buscar_por_id(cliente_id) or abort(404)
    try:
        Cliente.excluir(cliente_id)
        flash("Cliente excluído.", "sucesso")
    except ValidacaoError as e:
        flash(str(e), "erro")
    return redirect(url_for("clientes.listar"))
