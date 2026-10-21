import sqlite3
import shutil
import os
from tkinter import Tk, filedialog
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"
PASTA_IMAGENS = Path(__file__).resolve().parent / "imagens"

def cadastrar_informativo(id_admin):
    janela = Tk()
    janela.withdraw()
    caminho_img = filedialog.askopenfilename(filetypes = [("Imagens", "*.png *.jpg *.jpeg *.webp")])
    janela.destroy()

    if not caminho_img: 
        print("Cadastro cancelado")
        return

    os.markedirs(PASTA_IMAGENS, exist_ok=True)
    destino = PASTA_IMAGENS /Path(caminho_img).name
    shutil.copy(caminho_img, destino)

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Imagem (x64) VALUES (?)", (str(destino),))
        id_imagem = cursor.lastrowid

        titulo = input("Título: ")
        conteudo = input("Conteúdo: ")
        cursor.execute("""
            INSERT INTO Informativos (Titulo, Conteudo, idAdmin, id Imagem)
            VALUES (?, ?, ?, ?)
            """, (titulo, conteudo, id_admin, id_imagem))
        conexao.commit()
        print("Informativo cadastrado!!")
