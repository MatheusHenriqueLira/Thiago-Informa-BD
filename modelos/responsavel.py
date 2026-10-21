from banco import (
    inserir_responsavel,
    listar_responsaveis,
    buscar_responsavel_por_id,
    editar_responsavel,
    excluir_responsavel,
)

class Responsavel:
    id_resp: int
    nome: str

    def __init__(self, nome: str, id_resp: int = None):
        self.id_resp = id_resp
        self.nome = nome

    @staticmethod
    def cadastrar(nome: str) -> int:
        return inserir_responsavel(nome)

    # Alias de compatibilidade
    cadastar = cadastrar

    @staticmethod
    def listar_todos() -> list:
        return listar_responsaveis()

    @staticmethod
    def buscar_por_id(id_resp: int) -> dict | None:
        return buscar_responsavel_por_id(id_resp)

    @staticmethod
    def editar(id_resp: int, novo_nome: str) -> bool:
        return editar_responsavel(id_resp, novo_nome)

    @staticmethod 
    def excluir(id_resp: int) -> bool:
        return excluir_responsavel(id_resp)
