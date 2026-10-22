from modelos.admin import Admin


class SerializadorAdmin:
    @staticmethod
    def serializar(admin):
        """Serializa o objeto Admin para dicionário."""
        return {
            "idAdmin": admin.id_admin,
            "Nome": admin.nome,
            "Login": admin.login,
            "Senha": admin.senha,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto Admin."""
        if not dados:
            return None
        d = dict(dados)
        return Admin(
            id_admin=d.get("idAdmin"),
            nome=d.get("Nome", ""),
            login=d.get("Login", ""),
            senha=d.get("Senha"),
        )
