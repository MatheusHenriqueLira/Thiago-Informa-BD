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
from serializadores.serializador_projeto import SerializadorProjeto
from serializadores.serializador_img_projeto import SerializadorImgProjeto
from serializadores.serializador_projeto_turma import SerializadorProjetoTurma
from controladoras.controladora_imagem import ControladoraImagem


class ControladoraProjetos:
    def __init__(self, conta_logada=True):
        self.conta_logada = conta_logada

    @classmethod
    def criar_projeto(
        cls,
        id_admin,
        titulo,
        conteudo="",
        id_turma=None,
        caminho_imagem=None,
        id_imagem=None,
    ):
        novo_projeto = Projeto(titulo=titulo, conteudo=conteudo, id_admin=id_admin)
        if not novo_projeto.validar_dados():
            print("Dados inválidos: o título do projeto e o administrador são obrigatórios.")
            return None

        dados = SerializadorProjeto.serializar(novo_projeto)
        id_projeto = inserir_projeto(
            titulo=dados["Titulo"],
            conteudo=dados["Conteudo"],
            id_admin=dados["idAdmin"],
        )
        if id_projeto is None:
            print("Erro ao cadastrar projeto (verifique os dados informados).")
            return None

        if id_turma is not None:
            cls.vincular_turma(id_projeto, id_turma)

        if id_imagem is not None:
            cls.vincular_imagem(id_projeto, id_imagem)

        if caminho_imagem:
            img = ControladoraImagem.salvar_imagem(caminho_imagem)
            if img:
                cls.vincular_imagem(id_projeto, img.id_imagem)

        print("Projeto cadastrado com sucesso!")
        return SerializadorProjeto.desserializar(buscar_projeto_por_id(id_projeto))

    @staticmethod
    def listar_projetos(id_turma=None):
        if id_turma is not None:
            linhas = listar_projetos_da_turma(id_turma)
        else:
            linhas = listar_projetos()

        objetos = [SerializadorProjeto.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE PROJETOS ---")
        if not objetos:
            print("Nenhum projeto encontrado.")
        for proj in objetos:
            autor = proj.nome_admin or proj.id_admin
            img = proj.caminho_imagem or "Sem imagem"
            print(f"[{proj.id_projeto}] {proj.titulo} | Autor: {autor} | Data: {proj.data_criacao} | Imagem: {img}")

        return objetos

    @classmethod
    def editar_projeto(cls, id_projeto, novo_titulo=None, novo_conteudo=None):
        atualizado = editar_projeto(
            id_projeto=id_projeto,
            novo_titulo=novo_titulo if novo_titulo else None,
            novo_conteudo=novo_conteudo if novo_conteudo else None,
        )
        if atualizado:
            print("Projeto atualizado com sucesso!")
        else:
            print("Nenhuma alteração realizada ou projeto não encontrado.")

        return SerializadorProjeto.desserializar(buscar_projeto_por_id(id_projeto))

    @staticmethod
    def del_projeto(id_projeto):
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
    def vincular_imagem(id_projeto, id_imagem):
        vinculo = SerializadorImgProjeto.serializar(
            ImgProjeto(id_imagem=id_imagem, id_projeto=id_projeto)
        )
        return vincular_imagem_projeto(vinculo["idImagem"], vinculo["idProjeto"])

    @staticmethod
    def vincular_turma(id_projeto, id_turma):
        vinculo = SerializadorProjetoTurma.serializar(ProjetoTurma(id_projeto=id_projeto, id_turma=id_turma))
        return vincular_projeto_turma(vinculo["idProjeto"], vinculo["idTurma"])

    @staticmethod
    def desvincular_turma(id_projeto, id_turma):
        return desvincular_projeto_turma(id_projeto, id_turma)
