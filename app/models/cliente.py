import re

from app.database import get_db
from app.models import ValidacaoError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Cliente:
    @staticmethod
    def validar(dados):
        erros = []
        nome = (dados.get("nome") or "").strip()
        telefone = (dados.get("telefone") or "").strip()
        email = (dados.get("email") or "").strip()

        if len(nome) < 3:
            erros.append("O nome precisa ter pelo menos 3 letras.")
        digitos = re.sub(r"\D", "", telefone)
        if len(digitos) not in (10, 11):
            erros.append("Telefone inválido. Use DDD + número, ex.: (11) 98888-1111.")
        if email and not EMAIL_RE.match(email):
            erros.append("E-mail inválido.")
        if erros:
            raise ValidacaoError(erros)
        return {
            "nome": nome,
            "telefone": telefone,
            "email": email or None,
            "observacoes": (dados.get("observacoes") or "").strip() or None,
        }

    @staticmethod
    def listar(busca=""):
        busca = (busca or "").strip()
        sql = "SELECT * FROM cliente"
        params = ()
        if busca:
            sql += " WHERE nome LIKE ? OR telefone LIKE ?"
            params = (f"%{busca}%", f"%{busca}%")
        return get_db().execute(sql + " ORDER BY nome", params).fetchall()

    @staticmethod
    def buscar_por_id(cliente_id):
        return get_db().execute(
            "SELECT * FROM cliente WHERE id = ?", (cliente_id,)
        ).fetchone()

    @staticmethod
    def criar(dados):
        d = Cliente.validar(dados)
        db = get_db()
        cur = db.execute(
            "INSERT INTO cliente (nome, telefone, email, observacoes) VALUES (?, ?, ?, ?)",
            (d["nome"], d["telefone"], d["email"], d["observacoes"]),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def atualizar(cliente_id, dados):
        d = Cliente.validar(dados)
        db = get_db()
        db.execute(
            "UPDATE cliente SET nome = ?, telefone = ?, email = ?, observacoes = ? WHERE id = ?",
            (d["nome"], d["telefone"], d["email"], d["observacoes"], cliente_id),
        )
        db.commit()

    @staticmethod
    def excluir(cliente_id):
        db = get_db()
        qtd = db.execute(
            "SELECT COUNT(*) FROM agendamento WHERE cliente_id = ?", (cliente_id,)
        ).fetchone()[0]
        if qtd:
            raise ValidacaoError(
                "Este cliente possui agendamentos e não pode ser excluído. "
                "Cancele ou mantenha o histórico."
            )
        db.execute("DELETE FROM cliente WHERE id = ?", (cliente_id,))
        db.commit()
