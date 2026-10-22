from modelos.responsavel_turma import ResponsavelTurma


class SerializadorResponsavelTurma:
    @staticmethod
    def serializar(vinculo):
        """Serializa o objeto ResponsavelTurma para dicionário."""
        return {
            "idResponsavel": vinculo.id_responsavel,
            "idTurma": vinculo.id_turma,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto ResponsavelTurma."""
        if not dados:
            return None
        d = dict(dados)
        return ResponsavelTurma(
            id_responsavel=d.get("idResponsavel"),
            id_turma=d.get("idTurma"),
        )
