import os
import questionary
from modelos.admin import Admin
from modelos.responsavel import Responsavel
from controladoras import (
    ControladoraAutenticacao,
    ControladoraInformativo,
    ControladoraProjetos,
    ControladoraTurma,
    ControladoraResponsavel,
)


def login():
    auth = ControladoraAutenticacao.obter_instancia()
    return auth.executar_login()


def exibir_menu_admin(usuario):
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


def exibir_menu_responsavel(usuario):
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
    else:
        print(f"Opcao selecionada: {opcao}")


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
