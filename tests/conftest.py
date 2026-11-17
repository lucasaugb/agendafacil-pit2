import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.database import init_db  # noqa: E402
from app.seed import ADMIN_EMAIL, ADMIN_SENHA  # noqa: E402


@pytest.fixture
def app(tmp_path):
    """Cria uma aplicação com um banco novo e vazio para cada teste."""
    app = create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "teste.db"),
        "SECRET_KEY": "teste",
    })
    with app.app_context():
        init_db(seed=True)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logado(client):
    """Cliente HTTP já autenticado como administrador."""
    client.post("/login", data={"email": ADMIN_EMAIL, "senha": ADMIN_SENHA})
    return client
