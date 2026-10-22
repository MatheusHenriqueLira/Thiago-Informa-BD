class Projeto:

    def __init__(
        self,
        id_projeto=None,
        titulo="",
        conteudo="",
        data_criacao="",
        id_admin=None,
        caminho_imagem="",
        nome_admin=None,
    ):
        self.id_projeto = id_projeto
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_criacao = data_criacao
        self.id_admin = id_admin
        self.caminho_imagem = caminho_imagem
        self.nome_admin = nome_admin

    def validar_dados(self):
        return bool(self.titulo and self.titulo.strip() and self.id_admin is not None)
