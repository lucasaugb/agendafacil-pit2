import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.models.usuario import Usuario

bp = Blueprint("auth", __name__)


@bp.before_app_request
def carregar_usuario():
    uid = session.get("usuario_id")
    g.usuario = Usuario.buscar_por_id(uid) if uid else None


def login_obrigatorio(view):
    """Decorator: só deixa acessar a tela se estiver logado."""

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if g.usuario is None:
            if request.path != "/":
                flash("Faça login para continuar.", "aviso")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapper


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario:
        return redirect(url_for("dashboard.index"))
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "")
        usuario = Usuario.autenticar(email, request.form.get("senha", ""))
        if usuario:
            session.clear()
            session["usuario_id"] = usuario["id"]
            flash(f"Bem-vindo(a), {usuario['nome']}!", "sucesso")
            return redirect(url_for("dashboard.index"))
        flash("E-mail ou senha incorretos.", "erro")
    return render_template("auth/login.html", email=email)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("auth.login"))
