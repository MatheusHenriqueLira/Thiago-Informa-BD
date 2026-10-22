class ProjetoTurma:
    id_projeto: int
    id_turma: int

    def __init__(self, id_projeto: int, id_turma: int):
        self.id_projeto = id_projeto
        self.id_turma = id_turma

    def serializar(self) -> dict:
        """Serializa o vínculo ProjetoTurma para dicionário."""
        return {
            "idProjeto": self.id_projeto,
            "idTurma": self.id_turma,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto ProjetoTurma."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_projeto=d.get("idProjeto"),
            id_turma=d.get("idTurma"),
        )
