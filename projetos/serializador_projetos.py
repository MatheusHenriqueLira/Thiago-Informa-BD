from projetos import Projeto

class Projeto:
    def __init__(self, id_projeto, titulo, conteudo, data_criacao, id_admin, caminho_imagem=""):
        self.id_projeto = id_projeto
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_criacao = data_criacao
        self.id_admin = id_admin
        self.caminho_imagem = caminho_imagem

    #serializador em formato de método da classe
    @classmethod
    def de_dicionario(cls, dados_db):
        if not dados_db:
            return None
        return cls(
            id_projeto=dados_db.get("idProjeto"),
            titulo=dados_db.get("Titulo"),
            conteudo=dados_db.get("Conteudo"),
            data_criacao=dados_db.get("DataCriacao"),
            id_admin=dados_db.get("idAdmin"),
            caminho_imagem=dados_db.get("CaminhoImagem", "")
        )
    
    def para_dicionario(self): #arrumando o commit
        return {
            "id": self.id_projeto,
            "titulo": self.titulo,
            "conteudo": self.conteudo,
            "data_criacao": self.data_criacao,
            "id_admin": self.id_admin,
            "caminho_imagem": self.caminho_imagem
        }



