from modelos.img_projeto import ImgProjeto


class SerializadorImgProjeto:
    @staticmethod
    def serializar(vinculo):
        """Serializa o objeto ImgProjeto para dicionário."""
        return {
            "idImagem": vinculo.id_imagem,
            "idProjeto": vinculo.id_projeto,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto ImgProjeto."""
        if not dados:
            return None
        d = dict(dados)
        return ImgProjeto(
            id_imagem=d.get("idImagem"),
            id_projeto=d.get("idProjeto"),
        )
