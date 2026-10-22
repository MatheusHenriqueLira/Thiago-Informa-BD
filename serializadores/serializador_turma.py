from modelos.turma import Turma


class SerializadorTurma:
    @staticmethod
    def serializar(turma):
        """Serializa o objeto Turma para dicionário."""
        return {
            "idturma": turma.id_turma,
            "Nome": turma.nome,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto Turma."""
        if not dados:
            return None
        d = dict(dados)
        return Turma(
            id_turma=d.get("idturma"),
            nome=d.get("Nome", ""),
        )
