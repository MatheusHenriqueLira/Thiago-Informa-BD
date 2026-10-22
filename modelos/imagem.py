class Imagem:

    def __init__(self, caminho="", id_imagem=None):
        self.id_imagem = id_imagem
        self.caminho = caminho

    def validar_dados(self):
        return bool(self.caminho and self.caminho.strip())
