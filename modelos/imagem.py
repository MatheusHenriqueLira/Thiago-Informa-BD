import shutil
from pathlib import Path 
from uuid import uuid4
from banco import conectar, PASTA

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

        with conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO Imagem (caminho) VALUES (?)",
                (caminho_relativo,)
            )
            conn.commit()
            return cursor.lastrowid

    # Alias de compatibilidade
    salvar_imagen = salvar_imagem

    @staticmethod
    def buscar_por_id(id_imagem: int) -> dict | None:
        with conectar() as conn:
            cursor = conn.execute(
                "SELECT idImagem, caminho FROM Imagem WHERE idImagem = ?",
                (id_imagem,)
            )
            linha = cursor.fetchone()
            return dict(linha) if linha else None

    @staticmethod
    def excluir(id_imagem: int) -> bool:
        img = Imagem.buscar_por_id(id_imagem)

        if not img:
            return False

        with conectar() as conn:
            conn.execute(
                "DELETE FROM Imagem WHERE idImagem = ?",
                (id_imagem,)
            )
            conn.commit()

        caminho_fisico = PASTA / img["caminho"]
        if caminho_fisico.exists():
            caminho_fisico.unlink()

        return True
