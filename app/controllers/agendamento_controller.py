from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.controllers.auth_controller import login_obrigatorio
from app.models import ValidacaoError
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.servico import Servico

bp = Blueprint("agendamentos", __name__, url_prefix="/agendamentos")


def _opcoes():
    return {"clientes": Cliente.listar(), "servicos": Servico.listar(somente_ativos=True)}


@bp.route("/")
@login_obrigatorio
def listar():
    data = request.args.get("data", "")
    status = request.args.get("status", "")
    return render_template(
        "agendamentos/lista.html",
        agendamentos=Agendamento.listar(data or None, status or None),
        data=data,
        status=status,
    )


@bp.route("/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo():
    if request.method == "POST":
        try:
            Agendamento.criar(request.form)
            flash("Agendamento criado com sucesso!", "sucesso")
            return redirect(url_for("agendamentos.listar"))
        except ValidacaoError as e:
            for erro in e.erros:
                flash(erro, "erro")
    return render_template(
        "agendamentos/form.html", ag=request.form, titulo="Novo agendamento", **_opcoes()
    )


@bp.route("/<int:ag_id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar(ag_id):
    atual = Agendamento.buscar_por_id(ag_id) or abort(404)
    ag = dict(atual)
    ag["data"], _, ag["hora"] = atual["data_hora"].partition(" ")
    if request.method == "POST":
        try:
            Agendamento.atualizar(ag_id, request.form)
            flash("Agendamento atualizado!", "sucesso")
            return redirect(url_for("agendamentos.listar"))
        except ValidacaoError as e:
            for erro in e.erros:
                flash(erro, "erro")
            ag = request.form
    return render_template(
        "agendamentos/form.html", ag=ag, titulo="Editar agendamento", **_opcoes()
    )


@bp.route("/<int:ag_id>/status/<novo_status>", methods=["POST"])
@login_obrigatorio
def status(ag_id, novo_status):
    Agendamento.buscar_por_id(ag_id) or abort(404)
    mensagens = {
        "concluido": "Atendimento marcado como concluído.",
        "cancelado": "Agendamento cancelado.",
        "agendado": "Agendamento reaberto.",
    }
    try:
        Agendamento.alterar_status(ag_id, novo_status)
        flash(mensagens.get(novo_status, "Status alterado."), "sucesso")
    except ValidacaoError as e:
        flash(str(e), "erro")
    return redirect(request.referrer or url_for("agendamentos.listar"))
