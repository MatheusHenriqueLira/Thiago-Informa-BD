import sqlite3
from pathlib import Path
import questionary
import os
CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"
conexao = sqlite3.connect(CAMINHO_BANCO)
conexao.execute("PRAGMA foreign_keys = ON")
cursor = conexao.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""")

tabelas = cursor.fetchall()

conexao.close()


def exibir_menu_admin():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
+-------------------------------------------------------------------------------------------------+
|                                        THIAGO INFORMA                                           |
+-------------------------------------------------------------------------------------------------+
""")
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

if __name__ == "__main__":
    exibir_menu_admin()
