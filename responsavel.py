class Responsavel:
    def __init__(self, Idresp, Nome, Senha):
        self.Idresp = Idresp
        self.Nome = Nome
        self.Senha = Senha

    def exibir_dados(self):
        print(f"Responsavel:{self.Nome}")