class ImgProjeto:
    id_imagem: int
    id_projeto: int

    def __init__(self, id_imagem: int, id_projeto: int):
        self.id_imagem = id_imagem
        self.id_projeto = id_projeto

    def serializar(self) -> dict:
        """Serializa o vínculo ImgProjeto para dicionário."""
        return {
            "idImagem": self.id_imagem,
            "idProjeto": self.id_projeto,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto ImgProjeto."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_imagem=d.get("idImagem"),
            id_projeto=d.get("idProjeto"),
        )
