from modelos.responsavel import Responsavel


class SerializadorResponsavel:
    @staticmethod
    def serializar(responsavel):
        """Serializa o objeto Responsavel para dicionário."""
        return {
            "idresp": responsavel.id_resp,
            "Nome": responsavel.nome,
            "Login": responsavel.login,
            "Senha": responsavel.senha,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto Responsavel."""
        if not dados:
            return None
        d = dict(dados)
        return Responsavel(
            id_resp=d.get("idresp"),
            nome=d.get("Nome", ""),
            login=d.get("Login", ""),
            senha=d.get("Senha"),
        )
