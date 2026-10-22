from banco import (
    inserir_projeto,
    listar_projetos,
    buscar_projeto_por_id,
    editar_projeto,
    excluir_projeto,
    vincular_imagem_projeto,
    listar_imagens_do_projeto,
    vincular_projeto_turma,
    desvincular_projeto_turma,
    listar_projetos_da_turma,
)
from modelos.projeto import Projeto
from modelos.img_projeto import ImgProjeto
from modelos.projeto_turma import ProjetoTurma
from controladoras.controladora_imagem import ControladoraImagem


class ControladoraProjetos:
    def __init__(self, conta_logada: bool = True):
        self.conta_logada = conta_logada

    @staticmethod
    def obter_input(mensagem: str = "Digite o valor: ") -> str:
        return input(mensagem).strip()

    @classmethod
    def criar_projeto(
        cls,
        id_admin: int,
        titulo: str = None,
        conteudo: str = None,
        id_turma: int = None,
        caminho_imagem: str = None,
    ) -> Projeto | None:
        if titulo is None:
            titulo = cls.obter_input("Título do projeto: ")
        if conteudo is None:
            conteudo = cls.obter_input("Conteúdo/descrição do projeto: ")

        novo_projeto = Projeto(titulo=titulo, conteudo=conteudo, id_admin=id_admin)
        if not novo_projeto.validar_dados():
            print("Dados inválidos: o título do projeto e o administrador são obrigatórios.")
            return None

        dados = novo_projeto.serializar()
        id_projeto = inserir_projeto(
            titulo=dados["Titulo"],
            conteudo=dados["Conteudo"],
            id_admin=dados["idAdmin"],
        )

        if id_turma is not None:
            vinculo_turma = ProjetoTurma(id_projeto=id_projeto, id_turma=id_turma).serializar()
            vincular_projeto_turma(vinculo_turma["idProjeto"], vinculo_turma["idTurma"])

        if caminho_imagem:
            img = ControladoraImagem.salvar_imagem(caminho_imagem)
            vinculo_img = ImgProjeto(id_imagem=img.id_imagem, id_projeto=id_projeto).serializar()
            vincular_imagem_projeto(vinculo_img["idImagem"], vinculo_img["idProjeto"])

        print("Projeto cadastrado com sucesso!")
        return Projeto.desserializar(buscar_projeto_por_id(id_projeto))

    @staticmethod
    def listar_projetos(id_turma: int = None) -> list[Projeto]:
        if id_turma is not None:
            linhas = listar_projetos_da_turma(id_turma)
        else:
            linhas = listar_projetos()

        objetos = [Projeto.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE PROJETOS ---")
        if not objetos:
            print("Nenhum projeto encontrado.")
        for proj in objetos:
            autor = proj.nome_admin or proj.id_admin
            print(f"[{proj.id_projeto}] {proj.titulo} | Autor: {autor} | Data: {proj.data_criacao}")

        return objetos

    @classmethod
    def editar_projeto(cls, id_projeto: int, novo_titulo: str = None, novo_conteudo: str = None) -> Projeto | None:
        if novo_titulo is None:
            novo_titulo = cls.obter_input("Novo título do projeto (em branco para manter): ")
        if novo_conteudo is None:
            novo_conteudo = cls.obter_input("Novo conteúdo do projeto (em branco para manter): ")

        atualizado = editar_projeto(
            id_projeto=id_projeto,
            novo_titulo=novo_titulo if novo_titulo else None,
            novo_conteudo=novo_conteudo if novo_conteudo else None,
        )
        if atualizado:
            print("Projeto atualizado com sucesso!")
        else:
            print("Nenhuma alteração realizada ou projeto não encontrado.")

        return Projeto.desserializar(buscar_projeto_por_id(id_projeto))

    @staticmethod
    def del_projeto(id_projeto: int) -> bool:
        imagens = listar_imagens_do_projeto(id_projeto)
        excluido = excluir_projeto(id_projeto)

        if excluido:
            for img in imagens:
                ControladoraImagem.excluir(img["idImagem"])
            print(f"Projeto {id_projeto} excluído.")
        else:
            print("Projeto não encontrado.")
        return excluido

    @staticmethod
    def vincular_turma(id_projeto: int, id_turma: int) -> bool:
        vinculo = ProjetoTurma(id_projeto=id_projeto, id_turma=id_turma).serializar()
        return vincular_projeto_turma(vinculo["idProjeto"], vinculo["idTurma"])

    @staticmethod
    def desvincular_turma(id_projeto: int, id_turma: int) -> bool:
        return desvincular_projeto_turma(id_projeto, id_turma)
