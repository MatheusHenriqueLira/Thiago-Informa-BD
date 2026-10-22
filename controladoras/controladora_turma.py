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
from serializadores.serializador_turma import SerializadorTurma
from serializadores.serializador_responsavel_turma import SerializadorResponsavelTurma


class ControladoraTurma:
    @classmethod
    def cadastrar_turma(cls, nome):
        nova_turma = Turma(nome=nome)
        if not nova_turma.validar_dados():
            print("O nome da turma é obrigatório.")
            return None

        dados = SerializadorTurma.serializar(nova_turma)
        id_turma = inserir_turma(dados["Nome"])
        if id_turma is None:
            print("Erro ao cadastrar: já existe uma turma com este nome.")
            return None

        print("Turma cadastrada com sucesso!")
        return SerializadorTurma.desserializar(buscar_turma_por_id(id_turma))

    @staticmethod
    def listar_turmas():
        linhas = listar_turmas()
        turmas = [SerializadorTurma.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE TURMAS ---")
        if not turmas:
            print("Nenhuma turma cadastrada.")
        for t in turmas:
            print(f"[{t.id_turma}] {t.nome}")

        return turmas

    @classmethod
    def editar_turma(cls, id_turma, novo_nome):
        if not novo_nome or not novo_nome.strip():
            print("Nome inválido.")
            return None

        if editar_turma(id_turma, novo_nome):
            print("Turma atualizada com sucesso!")
        else:
            print("Não foi possível atualizar a turma (ID não encontrado ou nome já existente).")

        return SerializadorTurma.desserializar(buscar_turma_por_id(id_turma))

    @staticmethod
    def excluir_turma(id_turma):
        excluida = excluir_turma(id_turma)
        if excluida:
            print(f"Turma {id_turma} excluída.")
        else:
            print("Turma não encontrada.")
        return excluida

    @staticmethod
    def vincular_responsavel(id_responsavel, id_turma):
        vinculo = SerializadorResponsavelTurma.serializar(
            ResponsavelTurma(id_responsavel=id_responsavel, id_turma=id_turma)
        )
        return vincular_responsavel_turma(vinculo["idResponsavel"], vinculo["idTurma"])

    @staticmethod
    def desvincular_responsavel(id_responsavel, id_turma):
        return desvincular_responsavel_turma(id_responsavel, id_turma)

    @staticmethod
    def listar_turmas_do_responsavel(id_responsavel):
        linhas = listar_turmas_do_responsavel(id_responsavel)
        return [SerializadorTurma.desserializar(linha) for linha in linhas]
