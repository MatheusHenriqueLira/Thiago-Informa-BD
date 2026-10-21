import sqlite3
from pathlib import Path
import os
from serializador_informativo import desserializar_informativo

CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"

import sqlite3
from pathlib import Path
import os
from serializador_informativo import desserializar_informativo

CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"

def listar_informativos():
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT i.Idinfo, i.Titulo, i.Conteudo, i.datacriacao, i.estafixado, a.Nome as NomeAdmin
            FROM Informativos i
            JOIN Admin a ON i.idAdmin = a.idAdmin
            ORDER BY i.estafixado DESC, i.datacriacao DESC
        """)
        
        informativos_banco = cursor.fetchall()
        
        lista_objetos = [desserializar_informativo(linha) for linha in informativos_banco]
        
        print("\n--- LISTA DE INFORMATIVOS ---")
        
        for obj in lista_objetos:
            status = "FIXADO" if obj.esta_fixado else "Normal"
            print(f"[{obj.id_info}] {obj.titulo} | {status} | Autor: {obj.id_admin} | Data: {obj.data_criacao}")
        
        return lista_objetos


def alterar_fixado(id_info):
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.cursor()

        cursor.execute("SELECT estaficado FROM Informativos WHERE Idinfo = ?", (id_info,))
        resultado = cursor.fetchone()

        if resultado is not None:
            status_atual = resultado[0]
            novo_status = 1 if status_atual == 0 else 0

            cursor.execute("UPDATE Informativos SET estafixado = ? WHERE Idinfo = ?", (novo_status, id_info))
            conexao.commit()
            acao = "fixado" if novo_status == 1 else "desafixado"
            print("Informativo {id_info} foi {acao}.")
        else:
            print("Informativo não encontrato")


def editar_informativo(id_info):
    novo_titulo = input("Digite o novo título: ") #se deixar em branco não altera nada
    novo_conteudo = input("Digite o novo conteudo: ") #mesma coisa, se tiver em branco não muda

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.cursor()

        if novo_titulo:
            cursor.execute("UPDATE Informativos SET Titulo = ? WHERE Idinfo = ?", (novo_titulo, id_info))
        if novo_conteudo:
            cursor.execute("UPDATE Informativos SET Conteudo = ? WHERE Idinfo = ?," (novo_conteudo, id_info))

        conexao.commit()
        print("Informativo atualizado!")


def excluir_informativo(id_info):
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.cursor()

        cursor.execute("SELECT idImagem FROM Informativos WHERE Idinfo = ?", (id_info,))
        resultado = cursor.fetchone()

        cursor.execute("DELETE FROM Informativos WHERE Idinfo = ?", (id_info,))

        if resultado and resultado[0] is not None:
            id_imagem = resultado[0]

            cursor.execute("SELECT x64 FROM Imagem WHERE Idimagem = ?", (id_imagem,))
            caminho_img = cursor.fetchone()
            if caminho_img and os.path.exists(caminho_img[0]):
                os.remove(caminho_img[0])

            cursor.execute("DELETE FROM Imagem WHERE idImagem = ?", (id_imagem,))

        conexao.commit
        print("Informativo {id_info} excluido.")




