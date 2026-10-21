from pathlib import Path
from getpass import getpass
import os
import sqlite3
import questionary

CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"


def login():
    usuario = input("Login: ")
    senha = getpass("Senha: ")

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        # Verifica se é um administrador
        admin = conexao.execute(
            """
            SELECT idAdmin, Nome
            FROM Admin
            WHERE Login = ? AND Senha = ?
            """,
            (usuario, senha),
        ).fetchone()

        if admin is not None:
            return "admin", admin["idAdmin"]

        # Se não for admin, verifica se é um responsável
        responsavel = conexao.execute(
            """
            SELECT idresp, Nome
            FROM Responsavel
            WHERE Login = ? AND Senha = ?
            """,
            (usuario, senha),
        ).fetchone()

        if responsavel is not None:
            return "responsavel", responsavel["idresp"]

        print("Login ou senha incorretos.")
        return None

    finally:
        conexao.close()


def exibir_menu_admin():
    os.system("cls" if os.name == "nt" else "clear")
    print(
        """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""
    )
    print("Bem-vindo ao sistema admin")
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

def exibir_menu_responsavel():
    os.system("cls" if os.name == "nt" else "clear")
    print(
        """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""
    )
    print("Bem-vindo ao sistema")
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
    else:
        print(f"Opcao selecionada: {opcao}")


def main():
    resultado = login()

    if resultado is None:
        return

    tipo, id_usuario = resultado

    if tipo == "admin":
        print("Entrando no menu administrativo...")
        exibir_menu_admin()
    else:
        print("Entrando no menu do responsável...")
        exibir_menu_responsavel()


if __name__ == "__main__":
    main()