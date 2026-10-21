class Admin:
    def __init__(self, id_admin, nome, login, senha=None):
        self.id_admin = id_admin
        self.nome = nome
        self.login = login
        self.senha = senha

    def exibir_dados(self):
        print(f"Admin: {self.nome} ({self.login})")