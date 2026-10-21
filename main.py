from pathlib import Path
import os
import questionary
from modelos.admin import Admin
from modelos.responsavel import Responsavel
from banco import buscar_admin, buscar_responsavel

def login():
    usuario = input("Login: ")
    senha = input("Senha: ")

    # 1. Tenta autenticar como administrador
    dados = buscar_admin(usuario, senha)

    if dados:
        usuario_admin = Admin(
            id_admin=dados["idAdmin"],
            nome=dados["Nome"],
            login=dados["Login"],
            senha=dados["Senha"],
        )
        return "admin", usuario_admin

    # 2. Se não for admin, tenta autenticar como responsável
    dados = buscar_responsavel(usuario, senha)

    if dados:
        usuario_resp = Responsavel(
            id_resp=dados["idresp"],
            nome=dados["Nome"],
            login=dados["Login"],
            senha=dados["Senha"],
        )
        return "responsavel", usuario_resp

    print("Login ou senha incorretos.")
    return None


def exibir_menu_admin(usuario: Admin):
    os.system("cls" if os.name == "nt" else "clear")
    print(
        """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""
    )
    print(f"Bem-vindo(a) ao sistema administrativo, {usuario.nome}!")
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

def exibir_menu_responsavel(usuario: Responsavel):
    os.system("cls" if os.name == "nt" else "clear")
    print(
        """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""
    )
    print(f"Bem-vindo(a) ao sistema, {usuario.nome}!")
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
        exibir_menu_admin(usuario_logado)
    else:
        exibir_menu_responsavel(usuario_logado)


if __name__ == "__main__":
    main()