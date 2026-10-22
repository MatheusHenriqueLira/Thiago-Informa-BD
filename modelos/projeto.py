class Projeto:
    id_projeto: int
    titulo: str
    conteudo: str
    data_criacao: str
    id_admin: int
    caminho_imagem: str
    nome_admin: str

    def __init__(
        self,
        id_projeto: int = None,
        titulo: str = "",
        conteudo: str = "",
        data_criacao: str = "",
        id_admin: int = None,
        caminho_imagem: str = "",
        nome_admin: str = None,
    ):
        self.id_projeto = id_projeto
        self.titulo = titulo
        self.conteudo = conteudo
        self.data_criacao = data_criacao
        self.id_admin = id_admin
        self.caminho_imagem = caminho_imagem
        self.nome_admin = nome_admin

    def validar_dados(self) -> bool:
        return bool(self.titulo and self.titulo.strip() and self.id_admin is not None)

    def serializar(self) -> dict:
        """Serializa o objeto Projeto para dicionário."""
        return {
            "idProjeto": self.id_projeto,
            "Titulo": self.titulo,
            "Conteudo": self.conteudo,
            "datacriacao": self.data_criacao,
            "idAdmin": self.id_admin,
            "CaminhoImagem": self.caminho_imagem,
            "NomeAdmin": self.nome_admin,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto Projeto."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_projeto=d.get("idProjeto"),
            titulo=d.get("Titulo", ""),
            conteudo=d.get("Conteudo", ""),
            data_criacao=d.get("datacriacao", ""),
            id_admin=d.get("idAdmin"),
            caminho_imagem=d.get("CaminhoImagem", ""),
            nome_admin=d.get("NomeAdmin"),
        )
