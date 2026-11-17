"""AgendaFácil - fábrica da aplicação Flask (padrão MVC)."""
import os

from flask import Flask, render_template

from app import database


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder="views",      # V do MVC: telas HTML (Jinja2)
        static_folder="static",
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
        DATABASE=os.environ.get(
            "DATABASE_PATH", os.path.join(app.instance_path, "agendafacil.db")
        ),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    database.init_app(app)

    # C do MVC: controllers registrados como Blueprints
    from app.controllers import (
        agendamento_controller,
        auth_controller,
        cliente_controller,
        dashboard_controller,
        servico_controller,
    )

    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(dashboard_controller.bp)
    app.register_blueprint(cliente_controller.bp)
    app.register_blueprint(servico_controller.bp)
    app.register_blueprint(agendamento_controller.bp)

    # Cria o banco automaticamente na primeira execução
    if not os.path.exists(app.config["DATABASE"]):
        with app.app_context():
            database.init_db(seed=not app.config.get("TESTING"))

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return render_template("erro.html", codigo=404,
                               mensagem="Página não encontrada."), 404

    @app.errorhandler(500)
    def erro_interno(_e):
        return render_template("erro.html", codigo=500,
                               mensagem="Ocorreu um erro inesperado. Tente novamente."), 500

    @app.template_filter("data_br")
    def data_br(valor):
        """'2026-11-18 09:00' -> '18/11/2026 09:00'"""
        if not valor:
            return ""
        data, _, hora = valor.partition(" ")
        a, m, d = data.split("-")
        return f"{d}/{m}/{a} {hora}".strip()

    @app.template_filter("moeda")
    def moeda(valor):
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return app
