class Responsavel:

    def __init__(self, nome="", id_resp=None, login="", senha=None):
        self.id_resp = id_resp
        self.nome = nome
        self.login = login
        self.senha = senha

    def validar_dados(self):
        return bool(self.nome and self.nome.strip() and self.login and self.login.strip() and self.senha)

    def exibir_dados(self):
        print(f"Responsavel: {self.nome} ({self.login})")
