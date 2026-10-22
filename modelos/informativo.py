class Informativo:

    def __init__(
        self,
        id_info=None,
        titulo="",
        conteudo="",
        data_criacao="",
        id_admin=None,
        esta_fixado=False,
        id_imagem=None,
        nome_admin=None,
        caminho_imagem=None,
    ):
        self.id_info = id_info
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_criacao = data_criacao
        self.id_admin = id_admin
        self.esta_fixado = bool(esta_fixado)
        self.id_imagem = id_imagem
        self.nome_admin = nome_admin
        self.caminho_imagem = caminho_imagem

    def validar_dados(self):
        return bool(self.titulo and self.titulo.strip() and self.id_admin is not None)
