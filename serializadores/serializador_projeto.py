from modelos.projeto import Projeto


class SerializadorProjeto:
    @staticmethod
    def serializar(projeto):
        """Serializa o objeto Projeto para dicionário."""
        return {
            "idProjeto": projeto.id_projeto,
            "Titulo": projeto.titulo,
            "Conteudo": projeto.conteudo,
            "datacriacao": projeto.data_criacao,
            "idAdmin": projeto.id_admin,
            "CaminhoImagem": projeto.caminho_imagem,
            "NomeAdmin": projeto.nome_admin,
        }

    @staticmethod
    def desserializar(dados):
        """Desserializa um dicionário/linha do banco em um objeto Projeto."""
        if not dados:
            return None
        d = dict(dados)
        return Projeto(
            id_projeto=d.get("idProjeto"),
            titulo=d.get("Titulo", ""),
            conteudo=d.get("Conteudo", ""),
            data_criacao=d.get("datacriacao", ""),
            id_admin=d.get("idAdmin"),
            caminho_imagem=d.get("CaminhoImagem", ""),
            nome_admin=d.get("NomeAdmin"),
        )
