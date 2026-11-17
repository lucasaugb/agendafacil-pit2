"""M do MVC: regras de negócio, validação e acesso ao banco."""


class ValidacaoError(Exception):
    """Erro de regra de negócio. A mensagem é mostrada ao usuário."""

    def __init__(self, erros):
        if isinstance(erros, str):
            erros = [erros]
        self.erros = erros
        super().__init__("; ".join(erros))
