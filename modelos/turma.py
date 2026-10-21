from banco import (
    inserir_turma,
    listar_turmas,
    buscar_turma_por_id,
    editar_turma,
    excluir_turma,
)

class Turma:
    id_turma: int
    nome: str

    def __init__(self, nome: str, id_turma: int = None):
        self.id_turma = id_turma
        self.nome = nome

    @staticmethod
    def cadastrar(nome: str) -> int:
        return inserir_turma(nome)

    @staticmethod
    def listar_todas() -> list:
        return listar_turmas()

    @staticmethod
    def buscar_por_id(id_turma: int) -> dict | None:
        return buscar_turma_por_id(id_turma)

    @staticmethod
    def editar(id_turma: int, novo_nome: str) -> bool:
        return editar_turma(id_turma, novo_nome)

    @staticmethod
    def excluir(id_turma: int) -> bool:
        return excluir_turma(id_turma)
