class Admin:

    def __init__(self, id_admin=None, nome="", login="", senha=None):
        self.id_admin = id_admin
        self.nome = nome
        self.login = login
        self.senha = senha

    def validar_dados(self):
        return bool(self.nome and self.nome.strip() and self.login and self.login.strip() and self.senha)

    def exibir_dados(self):
        print(f"Admin: {self.nome} ({self.login})")
