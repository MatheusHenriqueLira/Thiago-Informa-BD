from modelos.informativo import Informativo


class SerializadorInformativo:
    @staticmethod
    def serializar(informativo):
        """Serializa o objeto Informativo para dicionário."""
        return {
            "Idinfo": informativo.id_info,
            "Titulo": informativo.titulo,
            "Conteudo": informativo.conteudo,
            "datacriacao": informativo.data_criacao,
            "idAdmin": informativo.id_admin,
            "estafixado": int(bool(informativo.esta_fixado)),
            "idImagem": informativo.id_imagem,
            "NomeAdmin": informativo.nome_admin,
            "CaminhoImagem": informativo.caminho_imagem,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto Informativo."""
        if not dados:
            return None
        d = dict(dados)
        return Informativo(
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
