from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.controllers.auth_controller import login_obrigatorio
from app.models import ValidacaoError
from app.models.servico import Servico

bp = Blueprint("servicos", __name__, url_prefix="/servicos")


@bp.route("/")
@login_obrigatorio
def listar():
    return render_template("servicos/lista.html", servicos=Servico.listar())


@bp.route("/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo():
    if request.method == "POST":
        try:
            Servico.criar(request.form)
            flash("Serviço cadastrado com sucesso!", "sucesso")
            return redirect(url_for("servicos.listar"))
        except ValidacaoError as e:
            for erro in e.erros:
                flash(erro, "erro")
    return render_template("servicos/form.html", servico=request.form, titulo="Novo serviço")


@bp.route("/<int:servico_id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar(servico_id):
    servico = Servico.buscar_por_id(servico_id) or abort(404)
    if request.method == "POST":
        try:
            Servico.atualizar(servico_id, request.form)
            flash("Serviço atualizado com sucesso!", "sucesso")
            return redirect(url_for("servicos.listar"))
        except ValidacaoError as e:
            for erro in e.erros:
                flash(erro, "erro")
            servico = request.form
    return render_template("servicos/form.html", servico=servico, titulo="Editar serviço")


@bp.route("/<int:servico_id>/ativar", methods=["POST"])
@login_obrigatorio
def alternar(servico_id):
    Servico.buscar_por_id(servico_id) or abort(404)
    Servico.alternar_ativo(servico_id)
    flash("Situação do serviço alterada.", "sucesso")
    return redirect(url_for("servicos.listar"))
