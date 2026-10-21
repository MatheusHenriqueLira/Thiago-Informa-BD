import shutil
from pathlib import Path 
from uuid import uuid4
from banco import (
    PASTA,
    inserir_imagem,
    buscar_imagem_por_id,
    excluir_imagem,
)

PASTA_IMAGENS = PASTA / "imagens"

class Imagem:
    id_imagem: int
    caminho: str

    @staticmethod  
    def salvar_imagem(caminho_origem: str) -> int:
        """
        Copia a imagem selecionada para a pasta 'imagens/' do projeto, 
        registra o caminho relativo no banco e retorna o idImagem gerado.
        """
        PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)
        origem = Path(caminho_origem)

        if not origem.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_origem}")

        nome_unico = f"{uuid4().hex[:8]}_{origem.name}"
        destino = PASTA_IMAGENS / nome_unico
        shutil.copy(origem, destino)

        caminho_relativo = f"imagens/{nome_unico}"
        return inserir_imagem(caminho_relativo)

    # Alias de compatibilidade
    salvar_imagen = salvar_imagem

    @staticmethod
    def buscar_por_id(id_imagem: int) -> dict | None:
        return buscar_imagem_por_id(id_imagem)

    @staticmethod
    def excluir(id_imagem: int) -> bool:
        img = buscar_imagem_por_id(id_imagem)

        if not img:
            return False

        excluido = excluir_imagem(id_imagem)

        if excluido:
            caminho_fisico = PASTA / img["caminho"]
            if caminho_fisico.exists():
                caminho_fisico.unlink()

        return excluido
