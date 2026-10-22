from banco import listar_imagens_do_projeto
from modelos.projeto import Projeto
from serializadores.serializador_imagem import SerializadorImagem

#esse código funciona como um tradutor de dados entre o mundo externo e o interior da aplicação
class SerializadorProjeto:  #faz ponte entre o banco de dados e os abjetos python.
    @staticmethod
    def serializar(projeto):
        """Serializa o objeto Projeto para dicionário."""
        imagens = [
            SerializadorImagem.serializar(img) if hasattr(img, "caminho") else img
            for img in getattr(projeto, "imagens", [])
        ]
        return {
            "idProjeto": projeto.id_projeto,
            "Titulo": projeto.titulo,
            "Conteudo": projeto.conteudo,
            "datacriacao": projeto.data_criacao,
            "idAdmin": projeto.id_admin,
            "CaminhoImagem": projeto.caminho_imagem,
            "Imagens": imagens,
            "NomeAdmin": projeto.nome_admin,
        }

    @staticmethod
    def desserializar(dados):    #faz o caminho inverso da serialização. 
        """Desserializa um dicionário/linha do banco em um objeto Projeto."""
        if not dados:
            return None
        d = dict(dados)
        id_projeto = d.get("idProjeto")

        imagens_brutas = d.get("Imagens")
        if imagens_brutas is None and id_projeto is not None:
            imagens_brutas = listar_imagens_do_projeto(id_projeto)

        imagens = [
            SerializadorImagem.desserializar(img) if isinstance(img, dict) else img
            for img in (imagens_brutas or [])
        ]
        caminhos = ", ".join(img.caminho for img in imagens if getattr(img, "caminho", None))
        caminho_imagem = caminhos or d.get("CaminhoImagem") or ""

        return Projeto(
            id_projeto=id_projeto,
            titulo=d.get("Titulo", ""),
            conteudo=d.get("Conteudo", ""),
            data_criacao=d.get("datacriacao", ""),
            id_admin=d.get("idAdmin"),
            caminho_imagem=caminho_imagem,
            nome_admin=d.get("NomeAdmin"),
            imagens=imagens,
        )
