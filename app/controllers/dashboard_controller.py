from datetime import datetime

from flask import Blueprint, render_template

from app.controllers.auth_controller import login_obrigatorio
from app.models.agendamento import Agendamento

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_obrigatorio
def index():
    hoje = datetime.now().strftime("%Y-%m-%d")
    return render_template(
        "dashboard.html",
        resumo=Agendamento.resumo(hoje),
        agenda=Agendamento.listar(data=hoje),
        hoje=hoje,
    )
