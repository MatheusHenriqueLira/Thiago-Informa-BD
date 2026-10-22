import os
import questionary
from banco import CAMINHO_BANCO, criar_banco
from controladoras import (
    ControladoraAutenticacao,
    ControladoraInformativo,
    ControladoraProjetos,
    ControladoraTurma,
    ControladoraResponsavel,
    ControladoraImagem,
)

CABECALHO = """
+-------------------------------------------------------------------------------------------+
|                                     THIAGO INFORMA                                        |
+-------------------------------------------------------------------------------------------+
"""


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione Enter para continuar...")


def ler_id(mensagem):
    valor = input(mensagem).strip()
    if not valor.isdigit():
        print("ID inválido! Digite apenas números.")
        return None
    return int(valor)


def login():
    auth = ControladoraAutenticacao.obter_instancia()
    return auth.executar_login()


# ==============================================================================
# Submenus do Administrador
# ==============================================================================

def menu_informativos_admin(usuario):
    while True:
        limpar_tela()
        print(CABECALHO)
        print("--- GERENCIAR INFORMATIVOS ---")
        opcao = questionary.select(
            "Escolha uma ação:",
            choices=[
                "Listar informativos",
                "Visualizar detalhes de um informativo",
                "Cadastrar informativo",
                "Editar informativo",
                "Fixar / Desafixar informativo",
                "Excluir informativo",
                "Voltar",
            ],
        ).ask()

        if opcao is None or opcao == "Voltar":
            break

        if opcao == "Listar informativos":
            ControladoraInformativo.listar_informativos()
            pausar()

        elif opcao == "Visualizar detalhes de um informativo":
            lista = ControladoraInformativo.listar_informativos()
            if lista:
                id_info = ler_id("\nDigite o ID do informativo para ver os detalhes: ")
                if id_info is not None:
                    escolhido = next((i for i in lista if i.id_info == id_info), None)
                    if escolhido:
                        status = "FIXADO" if escolhido.esta_fixado else "Normal"
                        print(f"\nTítulo: {escolhido.titulo}")
                        print(f"Status: {status}")
                        print(f"Autor: {escolhido.nome_admin or escolhido.id_admin}")
                        print(f"Data: {escolhido.data_criacao}")
                        print(f"Imagem: {escolhido.caminho_imagem or 'Sem imagem'}")
                        print(f"Conteúdo:\n{escolhido.conteudo}")
                    else:
                        print("Informativo não encontrado.")
            pausar()

        elif opcao == "Cadastrar informativo":
            ControladoraInformativo.cadastrar_informativo(usuario.id_admin)
            pausar()

        elif opcao == "Editar informativo":
            lista = ControladoraInformativo.listar_informativos()
            if lista:
                id_info = ler_id("\nDigite o ID do informativo que deseja editar: ")
                if id_info is not None:
                    ControladoraInformativo.editar_informativo(id_info)
            pausar()

        elif opcao == "Fixar / Desafixar informativo":
            lista = ControladoraInformativo.listar_informativos()
            if lista:
                id_info = ler_id("\nDigite o ID do informativo para fixar/desafixar: ")
                if id_info is not None:
                    ControladoraInformativo.alterar_fixado(id_info)
            pausar()

        elif opcao == "Excluir informativo":
            lista = ControladoraInformativo.listar_informativos()
            if lista:
                id_info = ler_id("\nDigite o ID do informativo que deseja excluir: ")
                if id_info is not None:
                    ControladoraInformativo.del_informativo(id_info)
            pausar()


def menu_projetos_admin(usuario):
    while True:
        limpar_tela()
        print(CABECALHO)
        print("--- GERENCIAR PROJETOS ---")
        opcao = questionary.select(
            "Escolha uma ação:",
            choices=[
                "Listar todos os projetos",
                "Listar projetos por turma",
                "Visualizar detalhes de um projeto",
                "Cadastrar projeto",
                "Editar projeto",
                "Vincular projeto a uma turma",
                "Desvincular projeto de uma turma",
                "Excluir projeto",
                "Voltar",
            ],
        ).ask()

        if opcao is None or opcao == "Voltar":
            break

        if opcao == "Listar todos os projetos":
            ControladoraProjetos.listar_projetos()
            pausar()

        elif opcao == "Listar projetos por turma":
            turmas = ControladoraTurma.listar_turmas()
            if turmas:
                id_turma = ler_id("\nDigite o ID da turma: ")
                if id_turma is not None:
                    ControladoraProjetos.listar_projetos(id_turma=id_turma)
            pausar()

        elif opcao == "Visualizar detalhes de um projeto":
            lista = ControladoraProjetos.listar_projetos()
            if lista:
                id_proj = ler_id("\nDigite o ID do projeto para ver os detalhes: ")
                if id_proj is not None:
                    escolhido = next((p for p in lista if p.id_projeto == id_proj), None)
                    if escolhido:
                        print(f"\nTítulo: {escolhido.titulo}")
                        print(f"Autor: {escolhido.nome_admin or escolhido.id_admin}")
                        print(f"Data: {escolhido.data_criacao}")
                        print(f"Imagem: {escolhido.caminho_imagem or 'Sem imagem'}")
                        print(f"Conteúdo:\n{escolhido.conteudo}")
                    else:
                        print("Projeto não encontrado.")
            pausar()

        elif opcao == "Cadastrar projeto":
            titulo = ControladoraProjetos.obter_input("Título do projeto: ")
            conteudo = ControladoraProjetos.obter_input("Conteúdo/descrição do projeto: ")

            id_turma = None
            vincular = ControladoraProjetos.obter_input("Deseja vincular a uma turma agora? (s/N): ").lower()
            if vincular == "s":
                turmas = ControladoraTurma.listar_turmas()
                if turmas:
                    id_turma = ler_id("Digite o ID da turma: ")

            ControladoraProjetos.criar_projeto(
                id_admin=usuario.id_admin,
                titulo=titulo,
                conteudo=conteudo,
                id_turma=id_turma,
                usar_dialogo_imagem=True,
            )
            pausar()

        elif opcao == "Editar projeto":
            lista = ControladoraProjetos.listar_projetos()
            if lista:
                id_proj = ler_id("\nDigite o ID do projeto que deseja editar: ")
                if id_proj is not None:
                    ControladoraProjetos.editar_projeto(id_proj)
            pausar()

        elif opcao == "Vincular projeto a uma turma":
            projetos = ControladoraProjetos.listar_projetos()
            turmas = ControladoraTurma.listar_turmas()
            if projetos and turmas:
                id_proj = ler_id("\nDigite o ID do projeto: ")
                id_turma = ler_id("Digite o ID da turma: ")
                if id_proj is not None and id_turma is not None:
                    if ControladoraProjetos.vincular_turma(id_proj, id_turma):
                        print("Projeto vinculado à turma com sucesso!")
                    else:
                        print("Não foi possível vincular (verifique os IDs ou se já está vinculado).")
            pausar()

        elif opcao == "Desvincular projeto de uma turma":
            projetos = ControladoraProjetos.listar_projetos()
            turmas = ControladoraTurma.listar_turmas()
            if projetos and turmas:
                id_proj = ler_id("\nDigite o ID do projeto: ")
                id_turma = ler_id("Digite o ID da turma: ")
                if id_proj is not None and id_turma is not None:
                    if ControladoraProjetos.desvincular_turma(id_proj, id_turma):
                        print("Vínculo removido com sucesso!")
                    else:
                        print("Vínculo não encontrado.")
            pausar()

        elif opcao == "Excluir projeto":
            lista = ControladoraProjetos.listar_projetos()
            if lista:
                id_proj = ler_id("\nDigite o ID do projeto que deseja excluir: ")
                if id_proj is not None:
                    ControladoraProjetos.del_projeto(id_proj)
            pausar()


def menu_turmas_admin():
    while True:
        limpar_tela()
        print(CABECALHO)
        print("--- GERENCIAR TURMAS ---")
        opcao = questionary.select(
            "Escolha uma ação:",
            choices=[
                "Listar turmas",
                "Cadastrar turma",
                "Editar turma",
                "Excluir turma",
                "Vincular responsável a uma turma",
                "Desvincular responsável de uma turma",
                "Voltar",
            ],
        ).ask()

        if opcao is None or opcao == "Voltar":
            break

        if opcao == "Listar turmas":
            ControladoraTurma.listar_turmas()
            pausar()

        elif opcao == "Cadastrar turma":
            ControladoraTurma.cadastrar_turma()
            pausar()

        elif opcao == "Editar turma":
            turmas = ControladoraTurma.listar_turmas()
            if turmas:
                id_turma = ler_id("\nDigite o ID da turma que deseja editar: ")
                if id_turma is not None:
                    ControladoraTurma.editar_turma(id_turma)
            pausar()

        elif opcao == "Excluir turma":
            turmas = ControladoraTurma.listar_turmas()
            if turmas:
                id_turma = ler_id("\nDigite o ID da turma que deseja excluir: ")
                if id_turma is not None:
                    ControladoraTurma.excluir_turma(id_turma)
            pausar()

        elif opcao == "Vincular responsável a uma turma":
            responsaveis = ControladoraResponsavel.listar_responsaveis()
            turmas = ControladoraTurma.listar_turmas()
            if responsaveis and turmas:
                id_resp = ler_id("\nDigite o ID do responsável: ")
                id_turma = ler_id("Digite o ID da turma: ")
                if id_resp is not None and id_turma is not None:
                    if ControladoraTurma.vincular_responsavel(id_resp, id_turma):
                        print("Responsável vinculado à turma com sucesso!")
                    else:
                        print("Não foi possível vincular (verifique os IDs ou se já está vinculado).")
            pausar()

        elif opcao == "Desvincular responsável de uma turma":
            responsaveis = ControladoraResponsavel.listar_responsaveis()
            turmas = ControladoraTurma.listar_turmas()
            if responsaveis and turmas:
                id_resp = ler_id("\nDigite o ID do responsável: ")
                id_turma = ler_id("Digite o ID da turma: ")
                if id_resp is not None and id_turma is not None:
                    if ControladoraTurma.desvincular_responsavel(id_resp, id_turma):
                        print("Vínculo removido com sucesso!")
                    else:
                        print("Vínculo não encontrado.")
            pausar()


def menu_responsaveis_admin():
    while True:
        limpar_tela()
        print(CABECALHO)
        print("--- GERENCIAR RESPONSÁVEIS ---")
        opcao = questionary.select(
            "Escolha uma ação:",
            choices=[
                "Listar responsáveis",
                "Cadastrar responsável",
                "Editar responsável",
                "Excluir responsável",
                "Ver turmas de um responsável",
                "Vincular responsável a uma turma",
                "Desvincular responsável de uma turma",
                "Voltar",
            ],
        ).ask()

        if opcao is None or opcao == "Voltar":
            break

        if opcao == "Listar responsáveis":
            ControladoraResponsavel.listar_responsaveis()
            pausar()

        elif opcao == "Cadastrar responsável":
            ControladoraResponsavel.cadastrar_responsavel()
            pausar()

        elif opcao == "Editar responsável":
            lista = ControladoraResponsavel.listar_responsaveis()
            if lista:
                id_resp = ler_id("\nDigite o ID do responsável que deseja editar: ")
                if id_resp is not None:
                    ControladoraResponsavel.editar_responsavel(id_resp)
            pausar()

        elif opcao == "Excluir responsável":
            lista = ControladoraResponsavel.listar_responsaveis()
            if lista:
                id_resp = ler_id("\nDigite o ID do responsável que deseja excluir: ")
                if id_resp is not None:
                    ControladoraResponsavel.excluir_responsavel(id_resp)
            pausar()

        elif opcao == "Ver turmas de um responsável":
            lista = ControladoraResponsavel.listar_responsaveis()
            if lista:
                id_resp = ler_id("\nDigite o ID do responsável: ")
                if id_resp is not None:
                    turmas = ControladoraTurma.listar_turmas_do_responsavel(id_resp)
                    print("\n--- TURMAS DO RESPONSÁVEL ---")
                    if not turmas:
                        print("Nenhuma turma vinculada a este responsável.")
                    for t in turmas:
                        print(f"[{t.id_turma}] {t.nome}")
            pausar()

        elif opcao == "Vincular responsável a uma turma":
            responsaveis = ControladoraResponsavel.listar_responsaveis()
            turmas = ControladoraTurma.listar_turmas()
            if responsaveis and turmas:
                id_resp = ler_id("\nDigite o ID do responsável: ")
                id_turma = ler_id("Digite o ID da turma: ")
                if id_resp is not None and id_turma is not None:
                    if ControladoraResponsavel.vincular_turma(id_resp, id_turma):
                        print("Responsável vinculado à turma com sucesso!")
                    else:
                        print("Não foi possível vincular (verifique os IDs ou se já está vinculado).")
            pausar()

        elif opcao == "Desvincular responsável de uma turma":
            responsaveis = ControladoraResponsavel.listar_responsaveis()
            turmas = ControladoraTurma.listar_turmas()
            if responsaveis and turmas:
                id_resp = ler_id("\nDigite o ID do responsável: ")
                id_turma = ler_id("Digite o ID da turma: ")
                if id_resp is not None and id_turma is not None:
                    if ControladoraResponsavel.desvincular_turma(id_resp, id_turma):
                        print("Vínculo removido com sucesso!")
                    else:
                        print("Vínculo não encontrado.")
            pausar()


# ==============================================================================
# Menus Principais (Admin e Responsável)
# ==============================================================================

def exibir_menu_admin(usuario):
    while True:
        limpar_tela()
        print(CABECALHO)
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
            ControladoraAutenticacao.obter_instancia().logout()
            print("Até logo!")
            break
        elif opcao == "Informativos":
            menu_informativos_admin(usuario)
        elif opcao == "Projetos":
            menu_projetos_admin(usuario)
        elif opcao == "Turmas":
            menu_turmas_admin()
        elif opcao == "Responsaveis":
            menu_responsaveis_admin()


def exibir_menu_responsavel(usuario):
    while True:
        limpar_tela()
        print(CABECALHO)
        print(f"Bem-vindo(a) ao sistema, {usuario.nome}!")
        opcao = questionary.select(
            "Use as setas para escolher:",
            choices=[
                "Informativos",
                "Projetos",
                "Minhas Turmas",
                "Sair",
            ],
        ).ask()

        if opcao is None or opcao == "Sair":
            ControladoraAutenticacao.obter_instancia().logout()
            print("Até logo!")
            break

        elif opcao == "Informativos":
            lista = ControladoraInformativo.listar_informativos()
            if lista:
                ver = input("\nDeseja ler o conteúdo de algum informativo? Digite o ID (ou Enter para voltar): ").strip()
                if ver.isdigit():
                    id_info = int(ver)
                    escolhido = next((i for i in lista if i.id_info == id_info), None)
                    if escolhido:
                        status = "FIXADO" if escolhido.esta_fixado else "Normal"
                        print(f"\nTítulo: {escolhido.titulo} ({status})")
                        print(f"Autor: {escolhido.nome_admin or escolhido.id_admin} | Data: {escolhido.data_criacao}")
                        print(f"Imagem: {escolhido.caminho_imagem or 'Sem imagem'}")
                        print(f"Conteúdo:\n{escolhido.conteudo}")
                    else:
                        print("Informativo não encontrado.")
            pausar()

        elif opcao == "Projetos":
            turmas = ControladoraTurma.listar_turmas_do_responsavel(usuario.id_resp)
            if turmas:
                print("\nSuas turmas vinculadas:")
                for t in turmas:
                    print(f"[{t.id_turma}] {t.nome}")
                escolha_turma = input("\nDigite o ID da turma para filtrar (ou Enter para ver todos os projetos): ").strip()
                if escolha_turma.isdigit():
                    projetos = ControladoraProjetos.listar_projetos(id_turma=int(escolha_turma))
                else:
                    projetos = ControladoraProjetos.listar_projetos()
            else:
                projetos = ControladoraProjetos.listar_projetos()

            if projetos:
                ver = input("\nDeseja ler os detalhes de algum projeto? Digite o ID (ou Enter para voltar): ").strip()
                if ver.isdigit():
                    id_proj = int(ver)
                    escolhido = next((p for p in projetos if p.id_projeto == id_proj), None)
                    if escolhido:
                        print(f"\nTítulo: {escolhido.titulo}")
                        print(f"Autor: {escolhido.nome_admin or escolhido.id_admin} | Data: {escolhido.data_criacao}")
                        print(f"Imagem: {escolhido.caminho_imagem or 'Sem imagem'}")
                        print(f"Conteúdo:\n{escolhido.conteudo}")
                    else:
                        print("Projeto não encontrado.")
            pausar()

        elif opcao == "Minhas Turmas":
            turmas = ControladoraTurma.listar_turmas_do_responsavel(usuario.id_resp)
            print("\n--- MINHAS TURMAS ---")
            if not turmas:
                print("Você ainda não está vinculado a nenhuma turma.")
            for t in turmas:
                print(f"[{t.id_turma}] {t.nome}")
            pausar()


def main():
    if not CAMINHO_BANCO.exists():
        criar_banco()

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
