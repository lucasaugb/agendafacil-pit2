import sqlite3

from app.database import get_db
from app.models import ValidacaoError


class Servico:
    @staticmethod
    def validar(dados):
        erros = []
        nome = (dados.get("nome") or "").strip()
        if len(nome) < 2:
            erros.append("Informe o nome do serviço.")
        try:
            preco = float(str(dados.get("preco", "")).replace(",", "."))
            if preco < 0:
                erros.append("O preço não pode ser negativo.")
        except ValueError:
            preco = None
            erros.append("Preço inválido.")
        try:
            duracao = int(dados.get("duracao_min", ""))
            if not 5 <= duracao <= 480:
                erros.append("A duração deve ficar entre 5 e 480 minutos.")
        except (ValueError, TypeError):
            duracao = None
            erros.append("Duração inválida.")
        if erros:
            raise ValidacaoError(erros)
        return {
            "nome": nome,
            "descricao": (dados.get("descricao") or "").strip() or None,
            "preco": round(preco, 2),
            "duracao_min": duracao,
        }

    @staticmethod
    def listar(somente_ativos=False):
        sql = "SELECT * FROM servico"
        if somente_ativos:
            sql += " WHERE ativo = 1"
        return get_db().execute(sql + " ORDER BY nome").fetchall()

    @staticmethod
    def buscar_por_id(servico_id):
        return get_db().execute(
            "SELECT * FROM servico WHERE id = ?", (servico_id,)
        ).fetchone()

    @staticmethod
    def criar(dados):
        d = Servico.validar(dados)
        db = get_db()
        try:
            cur = db.execute(
                "INSERT INTO servico (nome, descricao, preco, duracao_min) VALUES (?, ?, ?, ?)",
                (d["nome"], d["descricao"], d["preco"], d["duracao_min"]),
            )
        except sqlite3.IntegrityError:
            raise ValidacaoError("Já existe um serviço com esse nome.")
        db.commit()
        return cur.lastrowid

    @staticmethod
    def atualizar(servico_id, dados):
        d = Servico.validar(dados)
        db = get_db()
        try:
            db.execute(
                "UPDATE servico SET nome = ?, descricao = ?, preco = ?, duracao_min = ? WHERE id = ?",
                (d["nome"], d["descricao"], d["preco"], d["duracao_min"], servico_id),
            )
        except sqlite3.IntegrityError:
            raise ValidacaoError("Já existe um serviço com esse nome.")
        db.commit()

    @staticmethod
    def alternar_ativo(servico_id):
        """Desativa/reativa (em vez de apagar, para manter o histórico)."""
        db = get_db()
        db.execute("UPDATE servico SET ativo = 1 - ativo WHERE id = ?", (servico_id,))
        db.commit()
