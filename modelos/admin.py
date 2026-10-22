class Admin:
    id_admin: int
    nome: str
    login: str
    senha: str

    def __init__(self, id_admin: int = None, nome: str = "", login: str = "", senha: str = None):
        self.id_admin = id_admin
        self.nome = nome
        self.login = login
        self.senha = senha

    def validar_dados(self) -> bool:
        return bool(self.nome and self.nome.strip() and self.login and self.login.strip() and self.senha)

    def exibir_dados(self):
        print(f"Admin: {self.nome} ({self.login})")

    def serializar(self) -> dict:
        """Serializa o objeto Admin para dicionário."""
        return {
            "idAdmin": self.id_admin,
            "Nome": self.nome,
            "Login": self.login,
            "Senha": self.senha,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto Admin."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_admin=d.get("idAdmin"),
            nome=d.get("Nome", ""),
            login=d.get("Login", ""),
            senha=d.get("Senha"),
        )
