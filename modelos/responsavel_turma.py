class ResponsavelTurma:
    id_responsavel: int
    id_turma: int

    def __init__(self, id_responsavel: int, id_turma: int):
        self.id_responsavel = id_responsavel
        self.id_turma = id_turma

    def serializar(self) -> dict:
        """Serializa o vínculo ResponsavelTurma para dicionário."""
        return {
            "idResponsavel": self.id_responsavel,
            "idTurma": self.id_turma,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto ResponsavelTurma."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_responsavel=d.get("idResponsavel"),
            id_turma=d.get("idTurma"),
        )
