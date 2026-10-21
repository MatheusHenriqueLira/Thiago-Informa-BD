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
    login: str
    senha: str

    def __init__(self, nome: str = None, id_resp: int = None, login: str = None, senha: str = None):
        self.id_resp = id_resp
        self.nome = nome
        self.login = login
        self.senha = senha

    def exibir_dados(self):
        print(f"Responsavel: {self.nome} ({self.login})")

    @staticmethod
    def cadastrar(nome: str, login: str = None, senha: str = "1234") -> int:
        return inserir_responsavel(nome, login, senha)

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
