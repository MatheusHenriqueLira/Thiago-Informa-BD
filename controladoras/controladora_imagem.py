import shutil
from pathlib import Path
from uuid import uuid4
from tkinter import Tk, filedialog
from banco import (
    PASTA,
    inserir_imagem,
    buscar_imagem_por_id,
    listar_imagens,
    excluir_imagem,
)
from modelos.imagem import Imagem
from serializadores.serializador_imagem import SerializadorImagem

PASTA_IMAGENS = PASTA / "imagens"


class ControladoraImagem:
    @staticmethod
    def salvar_imagem(caminho_origem):
        """
        Copia a imagem selecionada para a pasta 'imagens/' do projeto,
        registra o caminho relativo no banco e retorna o objeto Imagem desserializado.
        """
        PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)
        origem = Path(caminho_origem)

        if not origem.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_origem}")

        nome_unico = f"{uuid4().hex[:8]}_{origem.name}"
        destino = PASTA_IMAGENS / nome_unico
        shutil.copy(origem, destino)

        nova_img = Imagem(caminho=f"imagens/{nome_unico}")
        dados = SerializadorImagem.serializar(nova_img)
        id_imagem = inserir_imagem(dados["caminho"])
        return SerializadorImagem.desserializar(buscar_imagem_por_id(id_imagem))

    @classmethod
    def selecionar_imagem(cls, caminho_img=None):
        """Abre a janela de seleção de arquivo e salva a imagem."""
        if not caminho_img:
            janela = Tk()
            janela.withdraw()
            caminho_img = filedialog.askopenfilename(
                title="Selecione uma imagem",
                filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp")],
            )
            janela.destroy()

        if not caminho_img:
            return None

        return cls.salvar_imagem(caminho_img)

    @staticmethod
    def buscar_por_id(id_imagem):
        return SerializadorImagem.desserializar(buscar_imagem_por_id(id_imagem))

    @staticmethod
    def listar_todas():
        return [SerializadorImagem.desserializar(linha) for linha in listar_imagens()]

    @classmethod
    def excluir(cls, id_imagem):
        img = cls.buscar_por_id(id_imagem)
        if not img:
            return False

        excluido = excluir_imagem(id_imagem)
        if excluido:
            caminho_fisico = PASTA / img.caminho
            if caminho_fisico.exists():
                caminho_fisico.unlink()

        return excluido
