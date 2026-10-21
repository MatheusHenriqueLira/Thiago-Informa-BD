from pathlib import Path
import os
import sqlite3
import questionary
from modelos.admin import Admin
from modelos.responsavel import Responsavel

CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"

def login():
    usuario = input("Login: ")
    senha = input("Senha: ")

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        # Verifica se é um administrador
        linha_admin = conexao.execute(
            """
            SELECT idAdmin, Nome, Login, Senha
            FROM Admin
            WHERE Login = ? AND Senha = ?
            """,
            (usuario, senha),
        ).fetchone()

        if linha_admin is not None:
            admin = Admin(
                id_admin=linha_admin["idAdmin"],
                nome=linha_admin["Nome"],
                login=linha_admin["Login"],
                senha=linha_admin["Senha"],
            )
            return "admin", admin

        # Se não for admin, verifica se é um responsável
        linha_resp = conexao.execute(
            """
            SELECT idresp, Nome, Login, Senha
            FROM Responsavel
            WHERE Login = ? AND Senha = ?
            """,
            (usuario, senha),
        ).fetchone()

        if linha_resp is not None:
            responsavel = Responsavel(
                id_resp=linha_resp["idresp"],
                nome=linha_resp["Nome"],
                login=linha_resp["Login"],
                senha=linha_resp["Senha"],
            )
            return "responsavel", responsavel

        print("Login ou senha incorretos.")
        return None

    finally:
        conexao.close()


def exibir_menu_admin(admin: Admin):
    os.system("cls" if os.name == "nt" else "clear")
    print(
        """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""
    )
    print(f"Bem-vindo(a) ao sistema administrativo, {admin.nome}!")
    opcao = questionary.select(
        "Use as setas para escolher:",
        choices=[
            "Informativos",
            "Projetos",
            "Turmas",
            "Responsaveis",
            "Sair",
        ],
    ).ask()

    if opcao is None or opcao == "Sair":
        print("Ate logo!")
    else:
        print(f"Opcao selecionada: {opcao}")

def exibir_menu_responsavel(responsavel: Responsavel):
    os.system("cls" if os.name == "nt" else "clear")
    print(
        """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""
    )
    print(f"Bem-vindo(a) ao sistema, {responsavel.nome}!")
    opcao = questionary.select(
        "Use as setas para escolher:",
        choices=[
            "Informativos",
            "Projetos",
            "Sair",
        ],
    ).ask()

    if opcao is None or opcao == "Sair":
        print("Ate logo!")

def main():
    resultado = login()

    if resultado is None:
        return

    tipo, usuario_logado = resultado

    if tipo == "admin":
        print("Entrando no menu administrativo...")
        exibir_menu_admin(usuario_logado)
    else:
        print("Entrando no menu do responsável...")
        exibir_menu_responsavel(usuario_logado)


if __name__ == "__main__":
    main()