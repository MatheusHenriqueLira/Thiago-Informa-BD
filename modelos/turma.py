class Turma:

    def __init__(self, nome="", id_turma=None):
        self.id_turma = id_turma
        self.nome = nome

    def validar_dados(self):
        return bool(self.nome and self.nome.strip())
