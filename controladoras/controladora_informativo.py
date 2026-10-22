from banco import (
    inserir_informativo,
    listar_informativos,
    buscar_informativo_por_id,
    alterar_fixado_informativo,
    editar_informativo,
    excluir_informativo,
)
from modelos.informativo import Informativo
from controladoras.controladora_imagem import ControladoraImagem


class ControladoraInformativo:
    def __init__(self, conta_logada: bool = True):
        self.conta_logada = conta_logada

    @staticmethod
    def obter_input(mensagem: str = "Digite o valor: ") -> str:
        return input(mensagem).strip()

    @classmethod
    def cadastrar_informativo(
        cls,
        id_admin: int,
        titulo: str = None,
        conteudo: str = None,
        usar_dialogo_imagem: bool = True,
    ) -> Informativo | None:
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

        dados = novo_info.serializar()
        id_gerado = inserir_informativo(
            titulo=dados["Titulo"],
            conteudo=dados["Conteudo"],
            id_admin=dados["idAdmin"],
            esta_fixado=dados["estafixado"],
            id_imagem=dados["idImagem"],
        )
        print("Informativo cadastrado com sucesso!")
        return Informativo.desserializar(buscar_informativo_por_id(id_gerado))

    @staticmethod
    def listar_informativos() -> list[Informativo]:
        linhas = listar_informativos()
        lista_objetos = [Informativo.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE INFORMATIVOS ---")
        if not lista_objetos:
            print("Nenhum informativo cadastrado.")
        for obj in lista_objetos:
            status = "FIXADO" if obj.esta_fixado else "Normal"
            autor = obj.nome_admin or obj.id_admin
            print(f"[{obj.id_info}] {obj.titulo} | {status} | Autor: {autor} | Data: {obj.data_criacao}")

        return lista_objetos

    @classmethod
    def editar_informativo(cls, id_info: int, novo_titulo: str = None, novo_conteudo: str = None) -> Informativo | None:
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

        return Informativo.desserializar(buscar_informativo_por_id(id_info))

    @staticmethod
    def alterar_fixado(id_info: int) -> bool | None:
        novo_status = alterar_fixado_informativo(id_info)
        if novo_status is None:
            print("Informativo não encontrado.")
            return None
        acao = "fixado" if novo_status else "desafixado"
        print(f"Informativo {id_info} foi {acao}.")
        return novo_status

    @staticmethod
    def del_informativo(id_info: int) -> bool:
        dados = buscar_informativo_por_id(id_info)
        if not dados:
            print("Informativo não encontrado.")
            return False

        info_obj = Informativo.desserializar(dados)
        excluido = excluir_informativo(id_info)

        if excluido and info_obj.id_imagem is not None:
            ControladoraImagem.excluir(info_obj.id_imagem)

        if excluido:
            print(f"Informativo {id_info} excluído.")
        return excluido
