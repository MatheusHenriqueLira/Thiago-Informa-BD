class Responsavel:
    def __init__(self, id_resp, nome, login, senha=None):
        self.id_resp = id_resp
        self.nome = nome
        self.login = login
        self.senha = senha

    def exibir_dados(self):
        print(f"Responsavel: {self.nome} ({self.login})")