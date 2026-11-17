from werkzeug.security import check_password_hash

from app.database import get_db


class Usuario:
    @staticmethod
    def buscar_por_id(usuario_id):
        return get_db().execute(
            "SELECT id, nome, email FROM usuario WHERE id = ?", (usuario_id,)
        ).fetchone()

    @staticmethod
    def autenticar(email, senha):
        """Retorna o usuário se e-mail e senha estiverem corretos, senão None."""
        email = (email or "").strip().lower()
        if not email or not senha:
            return None
        usuario = get_db().execute(
            "SELECT * FROM usuario WHERE email = ?", (email,)
        ).fetchone()
        if usuario and check_password_hash(usuario["senha_hash"], senha):
            return usuario
        return None
