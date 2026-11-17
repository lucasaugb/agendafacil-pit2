"""Dados de exemplo para demonstração e testes."""
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

# Usuário de demonstração (troque a senha se for usar de verdade)
ADMIN_EMAIL = "admin@agendafacil.com"
ADMIN_SENHA = "agenda123"


def popular_banco(db):
    db.execute(
        "INSERT INTO usuario (nome, email, senha_hash) VALUES (?, ?, ?)",
        ("Administrador", ADMIN_EMAIL, generate_password_hash(ADMIN_SENHA)),
    )
    servicos = [
        ("Corte masculino", "Corte na tesoura ou máquina", 40.00, 30),
        ("Barba", "Barba com toalha quente", 30.00, 20),
        ("Corte + Barba", "Combo completo", 60.00, 50),
        ("Escova", "Escova modeladora", 50.00, 40),
        ("Coloração", "Coloração completa", 120.00, 90),
    ]
    db.executemany(
        "INSERT INTO servico (nome, descricao, preco, duracao_min) VALUES (?, ?, ?, ?)",
        servicos,
    )
    clientes = [
        ("Ana Souza", "(11) 98888-1111", "ana@email.com", "Prefere atendimento pela manhã"),
        ("Bruno Lima", "(11) 97777-2222", "bruno@email.com", None),
        ("Carla Mendes", "(11) 96666-3333", None, "Alergia a amônia"),
    ]
    db.executemany(
        "INSERT INTO cliente (nome, telefone, email, observacoes) VALUES (?, ?, ?, ?)",
        clientes,
    )
    amanha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    agendamentos = [
        (1, 4, f"{amanha} 09:00", "agendado"),
        (2, 3, f"{amanha} 10:00", "agendado"),
        (3, 5, f"{amanha} 14:00", "agendado"),
    ]
    db.executemany(
        "INSERT INTO agendamento (cliente_id, servico_id, data_hora, status) VALUES (?, ?, ?, ?)",
        agendamentos,
    )
