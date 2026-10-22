class Turma:
    id_turma: int
    nome: str

    def __init__(self, nome: str = "", id_turma: int = None):
        self.id_turma = id_turma
        self.nome = nome

    def validar_dados(self) -> bool:
        return bool(self.nome and self.nome.strip())

    def serializar(self) -> dict:
        """Serializa o objeto Turma para dicionário."""
        return {
            "idturma": self.id_turma,
            "Nome": self.nome,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto Turma."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_turma=d.get("idturma"),
            nome=d.get("Nome", ""),
        )
