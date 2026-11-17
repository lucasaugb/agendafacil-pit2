"""Testes de integração: front-end (telas) + back-end (controllers) + banco."""
from datetime import datetime, timedelta

from app.seed import ADMIN_EMAIL


def _html(resp):
    return resp.get_data(as_text=True)


def test_redireciona_para_login_sem_autenticacao(client):
    resp = client.get("/")
    assert resp.status_code == 302 and "/login" in resp.headers["Location"]


def test_login_invalido_mostra_erro(client):
    resp = client.post("/login", data={"email": ADMIN_EMAIL, "senha": "x"})
    assert "E-mail ou senha incorretos" in _html(resp)


def test_login_valido_abre_painel(logado):
    resp = logado.get("/")
    assert resp.status_code == 200 and "Atendimentos hoje" in _html(resp)


def test_logout(logado):
    logado.get("/logout")
    assert logado.get("/").status_code == 302


def test_pagina_inexistente_404(logado):
    resp = logado.get("/nao-existe")
    assert resp.status_code == 404 and "Página não encontrada" in _html(resp)


def test_listar_clientes(logado):
    assert "Ana Souza" in _html(logado.get("/clientes/"))


def test_cadastrar_cliente_pela_tela(logado):
    resp = logado.post("/clientes/novo", data={"nome": "Maria Teste", "telefone": "(11) 95555-4444"},
                       follow_redirects=True)
    html = _html(resp)
    assert "Cliente cadastrado com sucesso" in html and "Maria Teste" in html


def test_cadastrar_cliente_invalido_mostra_mensagem(logado):
    resp = logado.post("/clientes/novo", data={"nome": "Ma", "telefone": "1"})
    html = _html(resp)
    assert "pelo menos 3 letras" in html and "Telefone inválido" in html


def test_editar_cliente(logado):
    resp = logado.post("/clientes/2/editar",
                       data={"nome": "Bruno Lima Jr", "telefone": "(11) 97777-2222"},
                       follow_redirects=True)
    assert "Bruno Lima Jr" in _html(resp)


def test_excluir_cliente_com_agendamento_bloqueado(logado):
    resp = logado.post("/clientes/1/excluir", follow_redirects=True)
    assert "não pode ser excluído" in _html(resp)


def test_editar_cliente_inexistente_404(logado):
    assert logado.get("/clientes/999/editar").status_code == 404


def test_cadastrar_servico(logado):
    resp = logado.post("/servicos/novo",
                       data={"nome": "Sobrancelha", "preco": "20", "duracao_min": "15"},
                       follow_redirects=True)
    assert "Sobrancelha" in _html(resp)


def test_criar_agendamento_pela_tela(logado):
    depois = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    resp = logado.post("/agendamentos/novo",
                       data={"cliente_id": "2", "servico_id": "2", "data": depois, "hora": "17:00"},
                       follow_redirects=True)
    assert "Agendamento criado com sucesso" in _html(resp)


def test_agendamento_conflito_pela_tela(logado):
    amanha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    # seed já tem agendamento amanhã às 09:00 (Escova, 40 min)
    resp = logado.post("/agendamentos/novo",
                       data={"cliente_id": "2", "servico_id": "1", "data": amanha, "hora": "09:20"})
    assert "Já existe um agendamento nesse horário" in _html(resp)


def test_cancelar_agendamento(logado):
    resp = logado.post("/agendamentos/1/status/cancelado", follow_redirects=True)
    assert "Agendamento cancelado" in _html(resp)


def test_filtrar_agenda_por_status(logado):
    logado.post("/agendamentos/1/status/cancelado")
    html = _html(logado.get("/agendamentos/?status=cancelado"))
    assert "Ana Souza" in html and "Bruno Lima" not in html
