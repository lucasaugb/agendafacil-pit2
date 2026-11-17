"""Conexão com o banco de dados SQLite (camada de acesso a dados)."""
import os
import sqlite3

from flask import current_app, g

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")


def get_db():
    """Retorna a conexão da requisição atual (abre se ainda não existir)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(seed=True):
    """Cria as tabelas e, opcionalmente, insere dados de exemplo."""
    db = get_db()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        db.executescript(f.read())
    if seed:
        from app.seed import popular_banco
        popular_banco(db)
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        """flask --app run init-db  -> recria o banco com dados de exemplo."""
        init_db()
        print("Banco de dados criado com sucesso.")
