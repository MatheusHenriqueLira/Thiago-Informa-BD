class Imagem:
    id_imagem: int
    caminho: str

    def __init__(self, caminho: str = "", id_imagem: int = None):
        self.id_imagem = id_imagem
        self.caminho = caminho

    def validar_dados(self) -> bool:
        return bool(self.caminho and self.caminho.strip())

    def serializar(self) -> dict:
        """Serializa o objeto Imagem para dicionário."""
        return {
            "idImagem": self.id_imagem,
            "caminho": self.caminho,
        }

    @classmethod
    def desserializar(cls, dados: dict):
        """Desserializa um dicionário/linha do banco em um objeto Imagem."""
        if not dados:
            return None
        d = dict(dados)
        return cls(
            id_imagem=d.get("idImagem"),
            caminho=d.get("caminho", d.get("Caminho", "")),
        )
