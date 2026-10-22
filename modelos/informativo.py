class Informativo:
    id_info: int
    titulo: str
    conteudo: str
    data_criacao: str
    id_admin: int
    esta_fixado: bool
    id_imagem: int
    nome_admin: str
    caminho_imagem: str

    def __init__(
        self,
        id_info: int = None,
        titulo: str = "",
        conteudo: str = "",
        data_criacao: str = "",
        id_admin: int = None,
        esta_fixado: bool = False,
        id_imagem: int = None,
        nome_admin: str = None,
        caminho_imagem: str = None,
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

    def validar_dados(self) -> bool:
        return bool(self.titulo and self.titulo.strip() and self.id_admin is not None)

    def serializar(self) -> dict:
        """Serializa o objeto Informativo para dicionário."""
        return {
            "Idinfo": self.id_info,
            "Titulo": self.titulo,
            "Conteudo": self.conteudo,
            "datacriacao": self.data_criacao,
            "idAdmin": self.id_admin,
            "estafixado": int(bool(self.esta_fixado)),
            "idImagem": self.id_imagem,
            "NomeAdmin": self.nome_admin,
            "CaminhoImagem": self.caminho_imagem,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto Informativo."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_info=d.get("Idinfo"),
            titulo=d.get("Titulo", ""),
            conteudo=d.get("Conteudo", ""),
            data_criacao=d.get("datacriacao", ""),
            id_admin=d.get("idAdmin"),
            esta_fixado=bool(d.get("estafixado", False)),
            id_imagem=d.get("idImagem"),
            nome_admin=d.get("NomeAdmin"),
            caminho_imagem=d.get("CaminhoImagem"),
        )
