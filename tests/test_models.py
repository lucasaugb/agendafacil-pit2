"""Testes unitários das regras de negócio (camada Model)."""
from datetime import datetime

import pytest

from app.models import ValidacaoError
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.seed import ADMIN_EMAIL, ADMIN_SENHA

# Data fixa para os testes não dependerem do dia em que forem executados
AGORA = datetime(2030, 1, 10, 7, 0)


def ag(cliente_id=1, servico_id=1, data="2030-01-10", hora="10:00"):
    return {"cliente_id": cliente_id, "servico_id": servico_id, "data": data, "hora": hora}


# ---------------- Usuário / login ----------------
class TestUsuario:
    def test_login_correto(self, app):
        with app.app_context():
            assert Usuario.autenticar(ADMIN_EMAIL, ADMIN_SENHA) is not None

    def test_login_senha_errada(self, app):
        with app.app_context():
            assert Usuario.autenticar(ADMIN_EMAIL, "errada") is None

    def test_login_campos_vazios(self, app):
        with app.app_context():
            assert Usuario.autenticar("", "") is None

    def test_email_nao_diferencia_maiusculas(self, app):
        with app.app_context():
            assert Usuario.autenticar(ADMIN_EMAIL.upper(), ADMIN_SENHA) is not None


# ---------------- Cliente ----------------
class TestCliente:
    def test_criar_cliente_valido(self, app):
        with app.app_context():
            novo_id = Cliente.criar({"nome": "João Silva", "telefone": "(11) 91234-5678"})
            assert Cliente.buscar_por_id(novo_id)["nome"] == "João Silva"

    @pytest.mark.parametrize("dados, trecho", [
        ({"nome": "Jo", "telefone": "11912345678"}, "nome"),
        ({"nome": "João", "telefone": "123"}, "Telefone"),
        ({"nome": "João", "telefone": "11912345678", "email": "sem-arroba"}, "E-mail"),
    ])
    def test_criar_cliente_invalido(self, app, dados, trecho):
        with app.app_context():
            with pytest.raises(ValidacaoError) as erro:
                Cliente.criar(dados)
            assert trecho in str(erro.value)

    def test_buscar_cliente_por_nome(self, app):
        with app.app_context():
            resultado = Cliente.listar("ana")
            assert len(resultado) == 1 and resultado[0]["nome"] == "Ana Souza"

    def test_nao_exclui_cliente_com_agendamento(self, app):
        with app.app_context():
            with pytest.raises(ValidacaoError):
                Cliente.excluir(1)  # Ana tem agendamento no seed

    def test_exclui_cliente_sem_agendamento(self, app):
        with app.app_context():
            novo_id = Cliente.criar({"nome": "Sem Agenda", "telefone": "11912345678"})
            Cliente.excluir(novo_id)
            assert Cliente.buscar_por_id(novo_id) is None


# ---------------- Serviço ----------------
class TestServico:
    def test_criar_servico_valido(self, app):
        with app.app_context():
            sid = Servico.criar({"nome": "Hidratação", "preco": "45,50", "duracao_min": "30"})
            assert Servico.buscar_por_id(sid)["preco"] == 45.5

    @pytest.mark.parametrize("dados", [
        {"nome": "X", "preco": "10", "duracao_min": "30"},
        {"nome": "Teste", "preco": "-5", "duracao_min": "30"},
        {"nome": "Teste", "preco": "abc", "duracao_min": "30"},
        {"nome": "Teste", "preco": "10", "duracao_min": "1000"},
    ])
    def test_criar_servico_invalido(self, app, dados):
        with app.app_context():
            with pytest.raises(ValidacaoError):
                Servico.criar(dados)

    def test_nome_de_servico_duplicado(self, app):
        with app.app_context():
            with pytest.raises(ValidacaoError, match="Já existe"):
                Servico.criar({"nome": "Barba", "preco": "10", "duracao_min": "10"})

    def test_desativar_servico(self, app):
        with app.app_context():
            Servico.alternar_ativo(1)
            assert Servico.buscar_por_id(1)["ativo"] == 0
            assert all(s["id"] != 1 for s in Servico.listar(somente_ativos=True))


# ---------------- Agendamento (regras de negócio) ----------------
class TestAgendamento:
    def test_agendamento_valido(self, app):
        with app.app_context():
            aid = Agendamento.criar(ag(), agora=AGORA)
            assert Agendamento.buscar_por_id(aid)["status"] == "agendado"

    def test_rn02_nao_agenda_no_passado(self, app):
        with app.app_context():
            with pytest.raises(ValidacaoError, match="já passou"):
                Agendamento.criar(ag(data="2020-01-01"), agora=AGORA)

    @pytest.mark.parametrize("hora", ["07:30", "19:50"])
    def test_rn03_fora_do_horario(self, app, hora):
        # Serviço 1 (Corte masculino) dura 30 min: 19:50 termina 20:20 -> fora
        with app.app_context():
            with pytest.raises(ValidacaoError, match="horário de funcionamento"):
                Agendamento.criar(ag(hora=hora), agora=AGORA)

    def test_rn04_conflito_de_horario(self, app):
        with app.app_context():
            Agendamento.criar(ag(hora="10:00"), agora=AGORA)          # 10:00-10:30
            with pytest.raises(ValidacaoError, match="Já existe um agendamento"):
                Agendamento.criar(ag(cliente_id=2, hora="10:15"), agora=AGORA)

    def test_horario_colado_nao_e_conflito(self, app):
        with app.app_context():
            Agendamento.criar(ag(hora="10:00"), agora=AGORA)          # 10:00-10:30
            Agendamento.criar(ag(cliente_id=2, hora="10:30"), agora=AGORA)

    def test_cancelado_libera_horario(self, app):
        with app.app_context():
            aid = Agendamento.criar(ag(hora="11:00"), agora=AGORA)
            Agendamento.alterar_status(aid, "cancelado")
            Agendamento.criar(ag(cliente_id=2, hora="11:00"), agora=AGORA)

    def test_rn01_servico_inativo(self, app):
        with app.app_context():
            Servico.alternar_ativo(1)
            with pytest.raises(ValidacaoError, match="serviço válido"):
                Agendamento.criar(ag(), agora=AGORA)

    def test_data_invalida(self, app):
        with app.app_context():
            with pytest.raises(ValidacaoError, match="data e hora válidas"):
                Agendamento.criar(ag(data="31/02/2030"), agora=AGORA)

    def test_concluir_e_nao_cancelar_depois(self, app):
        with app.app_context():
            aid = Agendamento.criar(ag(), agora=AGORA)
            Agendamento.alterar_status(aid, "concluido")
            with pytest.raises(ValidacaoError, match="finalizado"):
                Agendamento.alterar_status(aid, "cancelado")

    def test_editar_mesmo_horario_nao_conflita_consigo(self, app):
        with app.app_context():
            aid = Agendamento.criar(ag(hora="15:00"), agora=AGORA)
            Agendamento.atualizar(aid, {**ag(hora="15:00"), "observacoes": "ok"}, agora=AGORA)
            assert Agendamento.buscar_por_id(aid)["observacoes"] == "ok"

    def test_reabrir_cancelado_com_horario_ocupado(self, app):
        with app.app_context():
            aid = Agendamento.criar(ag(hora="16:00"), agora=AGORA)
            Agendamento.alterar_status(aid, "cancelado")
            Agendamento.criar(ag(cliente_id=2, hora="16:00"), agora=AGORA)
            with pytest.raises(ValidacaoError, match="ocupado"):
                Agendamento.alterar_status(aid, "agendado")

    def test_status_invalido(self, app):
        with app.app_context():
            with pytest.raises(ValidacaoError):
                Agendamento.alterar_status(1, "qualquer")

    def test_faturamento_do_mes(self, app):
        with app.app_context():
            aid = Agendamento.criar(ag(servico_id=3), agora=AGORA)   # Corte + Barba R$ 60
            Agendamento.alterar_status(aid, "concluido")
            assert Agendamento.resumo("2030-01-10")["faturamento_mes"] == 60
