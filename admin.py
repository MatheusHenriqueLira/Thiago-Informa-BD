class admin:
    def __init__(self, IdAdmin, Nome, Senha):
        self.IdAdmin = IdAdmin
        self.Nome = Nome
        self.Senha = Senha

    def exibir_dados(self):
        print(f"admin:{self.Nome}")