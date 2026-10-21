class Informativo:
    def __init__(self, id_info, titulo, conteudo, data_criacao, id_admin, esta_fixado, id_imagem):
        self.id_info = id_info
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_criacao = data_criacao
        self.id_admin = id_admin
        self.esta_fixado = bool(esta_fixado)
        self.id_imagem = id_imagem
