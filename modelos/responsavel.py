class Responsavel:
    id_resp: int
    nome: str
    login: str
    senha: str

    def __init__(self, nome: str = "", id_resp: int = None, login: str = "", senha: str = None):
        self.id_resp = id_resp
        self.nome = nome
        self.login = login
        self.senha = senha

    def validar_dados(self) -> bool:
        return bool(self.nome and self.nome.strip() and self.login and self.login.strip() and self.senha)

    def exibir_dados(self):
        print(f"Responsavel: {self.nome} ({self.login})")

    def serializar(self) -> dict:
        """Serializa o objeto Responsavel para dicionário."""
        return {
            "idresp": self.id_resp,
            "Nome": self.nome,
            "Login": self.login,
            "Senha": self.senha,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto Responsavel."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_resp=d.get("idresp"),
            nome=d.get("Nome", ""),
            login=d.get("Login", ""),
            senha=d.get("Senha"),
        )
