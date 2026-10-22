from modelos.imagem import Imagem


class SerializadorImagem:
    @staticmethod
    def serializar(imagem):
        """Serializa o objeto Imagem para dicionário."""
        return {
            "idImagem": imagem.id_imagem,
            "caminho": imagem.caminho,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto Imagem."""
        if not dados:
            return None
        d = dict(dados)
        return Imagem(
            id_imagem=d.get("idImagem"),
            caminho=d.get("caminho", d.get("Caminho", "")),
        )
