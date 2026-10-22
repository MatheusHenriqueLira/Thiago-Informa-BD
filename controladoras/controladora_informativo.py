from banco import (
    inserir_informativo,
    listar_informativos,
    buscar_informativo_por_id,
    alterar_fixado_informativo,
    editar_informativo,
    excluir_informativo,
)
from modelos.informativo import Informativo
from serializadores.serializador_informativo import SerializadorInformativo
from controladoras.controladora_imagem import ControladoraImagem


class ControladoraInformativo:
    def __init__(self, conta_logada=True):
        self.conta_logada = conta_logada

    @staticmethod
    def obter_input(mensagem="Digite o valor: "):
        return input(mensagem).strip()

    @classmethod
    def cadastrar_informativo(
        cls,
        id_admin,
        titulo=None,
        conteudo=None,
        usar_dialogo_imagem=True,
    ):
        if titulo is None:
            titulo = cls.obter_input("Título do informativo: ")
        if conteudo is None:
            conteudo = cls.obter_input("Conteúdo do informativo: ")

        id_imagem = None
        if usar_dialogo_imagem:
            resp_img = cls.obter_input("Deseja anexar uma imagem? (s/N): ").lower()
            if resp_img == "s":
                img = ControladoraImagem.selecionar_imagem()
                if img:
                    id_imagem = img.id_imagem

        novo_info = Informativo(
            titulo=titulo,
            conteudo=conteudo,
            id_admin=id_admin,
            esta_fixado=False,
            id_imagem=id_imagem,
        )
        if not novo_info.validar_dados():
            print("Dados inválidos: o título e o administrador são obrigatórios.")
            return None

        dados = SerializadorInformativo.serializar(novo_info)
        id_gerado = inserir_informativo(
            titulo=dados["Titulo"],
            conteudo=dados["Conteudo"],
            id_admin=dados["idAdmin"],
            esta_fixado=dados["estafixado"],
            id_imagem=dados["idImagem"],
        )
        print("Informativo cadastrado com sucesso!")
        return SerializadorInformativo.desserializar(buscar_informativo_por_id(id_gerado))

    @staticmethod
    def listar_informativos():
        linhas = listar_informativos()
        lista_objetos = [SerializadorInformativo.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE INFORMATIVOS ---")
        if not lista_objetos:
            print("Nenhum informativo cadastrado.")
        for obj in lista_objetos:
            status = "FIXADO" if obj.esta_fixado else "Normal"
            autor = obj.nome_admin or obj.id_admin
            img = obj.caminho_imagem or "Sem imagem"
            print(f"[{obj.id_info}] {obj.titulo} | {status} | Autor: {autor} | Data: {obj.data_criacao} | Imagem: {img}")

        return lista_objetos

    @classmethod
    def editar_informativo(cls, id_info, novo_titulo=None, novo_conteudo=None):
        if novo_titulo is None:
            novo_titulo = cls.obter_input("Digite o novo título (deixe em branco para manter): ")
        if novo_conteudo is None:
            novo_conteudo = cls.obter_input("Digite o novo conteúdo (deixe em branco para manter): ")

        atualizado = editar_informativo(
            id_info=id_info,
            novo_titulo=novo_titulo if novo_titulo else None,
            novo_conteudo=novo_conteudo if novo_conteudo else None,
        )
        if atualizado:
            print("Informativo atualizado!")
        else:
            print("Nenhuma alteração realizada ou informativo não encontrado.")

        return SerializadorInformativo.desserializar(buscar_informativo_por_id(id_info))

    @staticmethod
    def alterar_fixado(id_info):
        novo_status = alterar_fixado_informativo(id_info)
        if novo_status is None:
            print("Informativo não encontrado.")
            return None
        acao = "fixado" if novo_status else "desafixado"
        print(f"Informativo {id_info} foi {acao}.")
        return novo_status

    @staticmethod
    def del_informativo(id_info):
        dados = buscar_informativo_por_id(id_info)
        if not dados:
            print("Informativo não encontrado.")
            return False

        info_obj = SerializadorInformativo.desserializar(dados)
        excluido = excluir_informativo(id_info)

        if excluido and info_obj.id_imagem is not None:
            ControladoraImagem.excluir(info_obj.id_imagem)

        if excluido:
            print(f"Informativo {id_info} excluído.")
        return excluido
