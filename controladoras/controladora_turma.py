from banco import (
    inserir_turma,
    listar_turmas,
    buscar_turma_por_id,
    editar_turma,
    excluir_turma,
    vincular_responsavel_turma,
    desvincular_responsavel_turma,
    listar_turmas_do_responsavel,
)
from modelos.turma import Turma
from modelos.responsavel_turma import ResponsavelTurma


class ControladoraTurma:
    @staticmethod
    def obter_input(mensagem: str = "Digite o valor: ") -> str:
        return input(mensagem).strip()

    @classmethod
    def cadastrar_turma(cls, nome: str = None) -> Turma | None:
        if nome is None:
            nome = cls.obter_input("Nome da turma: ")

        nova_turma = Turma(nome=nome)
        if not nova_turma.validar_dados():
            print("O nome da turma é obrigatório.")
            return None

        dados = nova_turma.serializar()
        id_turma = inserir_turma(dados["Nome"])
        print("Turma cadastrada com sucesso!")
        return Turma.desserializar(buscar_turma_por_id(id_turma))

    @staticmethod
    def listar_turmas() -> list[Turma]:
        linhas = listar_turmas()
        turmas = [Turma.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE TURMAS ---")
        if not turmas:
            print("Nenhuma turma cadastrada.")
        for t in turmas:
            print(f"[{t.id_turma}] {t.nome}")

        return turmas

    @classmethod
    def editar_turma(cls, id_turma: int, novo_nome: str = None) -> Turma | None:
        if novo_nome is None:
            novo_nome = cls.obter_input("Novo nome da turma: ")
        if not novo_nome:
            print("Nome inválido.")
            return None

        if editar_turma(id_turma, novo_nome):
            print("Turma atualizada com sucesso!")
        else:
            print("Turma não encontrada.")

        return Turma.desserializar(buscar_turma_por_id(id_turma))

    @staticmethod
    def excluir_turma(id_turma: int) -> bool:
        excluida = excluir_turma(id_turma)
        if excluida:
            print(f"Turma {id_turma} excluída.")
        else:
            print("Turma não encontrada.")
        return excluida

    @staticmethod
    def vincular_responsavel(id_responsavel: int, id_turma: int) -> bool:
        vinculo = ResponsavelTurma(id_responsavel=id_responsavel, id_turma=id_turma).serializar()
        return vincular_responsavel_turma(vinculo["idResponsavel"], vinculo["idTurma"])

    @staticmethod
    def desvincular_responsavel(id_responsavel: int, id_turma: int) -> bool:
        return desvincular_responsavel_turma(id_responsavel, id_turma)

    @staticmethod
    def listar_turmas_do_responsavel(id_responsavel: int) -> list[Turma]:
        linhas = listar_turmas_do_responsavel(id_responsavel)
        return [Turma.desserializar(linha) for linha in linhas]
