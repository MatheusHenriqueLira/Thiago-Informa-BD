from modelos.projeto_turma import ProjetoTurma


class SerializadorProjetoTurma:
    @staticmethod
    def serializar(vinculo):
        """Serializa o objeto ProjetoTurma para dicionário."""
        return {
            "idProjeto": vinculo.id_projeto,
            "idTurma": vinculo.id_turma,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto ProjetoTurma."""
        if not dados:
            return None
        d = dict(dados)
        return ProjetoTurma(
            id_projeto=d.get("idProjeto"),
            id_turma=d.get("idTurma"),
        )
