from datetime import datetime, timedelta

from app.database import get_db
from app.models import ValidacaoError

HORA_ABERTURA = 8    # 08:00
HORA_FECHAMENTO = 20  # 20:00
FORMATO = "%Y-%m-%d %H:%M"
STATUS_VALIDOS = ("agendado", "concluido", "cancelado")


class Agendamento:
    @staticmethod
    def validar(dados, ignorar_id=None, agora=None):
        """Valida as regras de negócio do agendamento.

        RN01 - cliente e serviço precisam existir (serviço ativo)
        RN02 - não pode agendar no passado
        RN03 - precisa estar dentro do horário de funcionamento (08h-20h)
        RN04 - não pode haver dois agendamentos no mesmo horário (conflito)
        """
        agora = agora or datetime.now()
        db = get_db()
        erros = []

        cliente = db.execute(
            "SELECT id FROM cliente WHERE id = ?", (dados.get("cliente_id"),)
        ).fetchone()
        if not cliente:
            erros.append("Selecione um cliente válido.")

        servico = db.execute(
            "SELECT * FROM servico WHERE id = ? AND ativo = 1", (dados.get("servico_id"),)
        ).fetchone()
        if not servico:
            erros.append("Selecione um serviço válido.")

        data = (dados.get("data") or "").strip()
        hora = (dados.get("hora") or "").strip()
        inicio = None
        try:
            inicio = datetime.strptime(f"{data} {hora}", FORMATO)
        except ValueError:
            erros.append("Informe uma data e hora válidas.")

        if inicio and servico:
            fim = inicio + timedelta(minutes=servico["duracao_min"])
            if inicio < agora:
                erros.append("Não é possível agendar em uma data/hora que já passou.")
            limite = inicio.replace(hour=HORA_FECHAMENTO, minute=0)
            if inicio.hour < HORA_ABERTURA or fim > limite:
                erros.append(
                    f"Fora do horário de funcionamento ({HORA_ABERTURA:02d}h às "
                    f"{HORA_FECHAMENTO:02d}h)."
                )
            if Agendamento.tem_conflito(inicio, fim, ignorar_id):
                erros.append("Já existe um agendamento nesse horário. Escolha outro horário.")

        if erros:
            raise ValidacaoError(erros)
        return {
            "cliente_id": int(dados["cliente_id"]),
            "servico_id": int(dados["servico_id"]),
            "data_hora": inicio.strftime(FORMATO),
            "observacoes": (dados.get("observacoes") or "").strip() or None,
        }

    @staticmethod
    def tem_conflito(inicio, fim, ignorar_id=None):
        """Verifica se [inicio, fim) se sobrepõe a outro agendamento ativo do dia."""
        linhas = get_db().execute(
            """SELECT a.id, a.data_hora, s.duracao_min
                 FROM agendamento a JOIN servico s ON s.id = a.servico_id
                WHERE a.status = 'agendado' AND date(a.data_hora) = ?""",
            (inicio.strftime("%Y-%m-%d"),),
        ).fetchall()
        for linha in linhas:
            if ignorar_id and linha["id"] == int(ignorar_id):
                continue
            outro_inicio = datetime.strptime(linha["data_hora"], FORMATO)
            outro_fim = outro_inicio + timedelta(minutes=linha["duracao_min"])
            if inicio < outro_fim and outro_inicio < fim:
                return True
        return False

    @staticmethod
    def listar(data=None, status=None):
        sql = """SELECT a.*, c.nome AS cliente_nome, c.telefone AS cliente_telefone,
                        s.nome AS servico_nome, s.preco, s.duracao_min
                   FROM agendamento a
                   JOIN cliente c ON c.id = a.cliente_id
                   JOIN servico s ON s.id = a.servico_id
                  WHERE 1 = 1"""
        params = []
        if data:
            sql += " AND date(a.data_hora) = ?"
            params.append(data)
        if status in STATUS_VALIDOS:
            sql += " AND a.status = ?"
            params.append(status)
        return get_db().execute(sql + " ORDER BY a.data_hora", params).fetchall()

    @staticmethod
    def buscar_por_id(agendamento_id):
        return get_db().execute(
            "SELECT * FROM agendamento WHERE id = ?", (agendamento_id,)
        ).fetchone()

    @staticmethod
    def criar(dados, agora=None):
        d = Agendamento.validar(dados, agora=agora)
        db = get_db()
        cur = db.execute(
            "INSERT INTO agendamento (cliente_id, servico_id, data_hora, observacoes) "
            "VALUES (?, ?, ?, ?)",
            (d["cliente_id"], d["servico_id"], d["data_hora"], d["observacoes"]),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def atualizar(agendamento_id, dados, agora=None):
        atual = Agendamento.buscar_por_id(agendamento_id)
        if not atual:
            raise ValidacaoError("Agendamento não encontrado.")
        if atual["status"] != "agendado":
            raise ValidacaoError("Só é possível editar agendamentos em aberto.")
        d = Agendamento.validar(dados, ignorar_id=agendamento_id, agora=agora)
        db = get_db()
        db.execute(
            "UPDATE agendamento SET cliente_id = ?, servico_id = ?, data_hora = ?, "
            "observacoes = ? WHERE id = ?",
            (d["cliente_id"], d["servico_id"], d["data_hora"], d["observacoes"], agendamento_id),
        )
        db.commit()

    @staticmethod
    def alterar_status(agendamento_id, novo_status):
        if novo_status not in STATUS_VALIDOS:
            raise ValidacaoError("Status inválido.")
        atual = Agendamento.buscar_por_id(agendamento_id)
        if not atual:
            raise ValidacaoError("Agendamento não encontrado.")
        if atual["status"] != "agendado" and novo_status != "agendado":
            raise ValidacaoError("Este agendamento já foi finalizado.")
        if novo_status == "agendado" and atual["status"] == "cancelado":
            # Reabrir um cancelado: precisa checar conflito de novo
            inicio = datetime.strptime(atual["data_hora"], FORMATO)
            servico = get_db().execute(
                "SELECT duracao_min FROM servico WHERE id = ?", (atual["servico_id"],)
            ).fetchone()
            fim = inicio + timedelta(minutes=servico["duracao_min"])
            if Agendamento.tem_conflito(inicio, fim, ignorar_id=agendamento_id):
                raise ValidacaoError("Não é possível reabrir: o horário já foi ocupado.")
        db = get_db()
        db.execute("UPDATE agendamento SET status = ? WHERE id = ?", (novo_status, agendamento_id))
        db.commit()

    @staticmethod
    def resumo(hoje=None):
        """Números para o painel inicial."""
        hoje = hoje or datetime.now().strftime("%Y-%m-%d")
        db = get_db()
        r = db.execute(
            """SELECT
                 SUM(CASE WHEN date(a.data_hora) = ? AND a.status = 'agendado' THEN 1 ELSE 0 END) AS hoje,
                 SUM(CASE WHEN date(a.data_hora) > ? AND a.status = 'agendado' THEN 1 ELSE 0 END) AS proximos,
                 SUM(CASE WHEN a.status = 'concluido' AND strftime('%Y-%m', a.data_hora) = strftime('%Y-%m', ?)
                          THEN s.preco ELSE 0 END) AS faturamento_mes
               FROM agendamento a JOIN servico s ON s.id = a.servico_id""",
            (hoje, hoje, hoje),
        ).fetchone()
        total_clientes = db.execute("SELECT COUNT(*) FROM cliente").fetchone()[0]
        return {
            "hoje": r["hoje"] or 0,
            "proximos": r["proximos"] or 0,
            "faturamento_mes": r["faturamento_mes"] or 0,
            "clientes": total_clientes,
        }
