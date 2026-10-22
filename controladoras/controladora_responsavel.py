from banco import (
    inserir_responsavel,
    listar_responsaveis,
    buscar_responsavel_por_id,
    editar_responsavel,
    excluir_responsavel,
    vincular_responsavel_turma,
    desvincular_responsavel_turma,
)
from modelos.responsavel import Responsavel
from modelos.responsavel_turma import ResponsavelTurma
from serializadores.serializador_responsavel import SerializadorResponsavel
from serializadores.serializador_responsavel_turma import SerializadorResponsavelTurma


class ControladoraResponsavel:
    @classmethod
    def cadastrar_responsavel(cls, nome, login=None, senha="1234"):
        nome = (nome or "").strip()
        login = (login or "").strip() or nome
        senha = (senha or "").strip() or "1234"

        novo_resp = Responsavel(nome=nome, login=login, senha=senha)
        if not novo_resp.validar_dados():
            print("Dados inválidos: nome, login e senha são obrigatórios.")
            return None

        dados = SerializadorResponsavel.serializar(novo_resp)
        id_resp = inserir_responsavel(nome=dados["Nome"], login=dados["Login"], senha=dados["Senha"])
        if id_resp is None:
            print("Erro ao cadastrar: já existe um responsável com este login.")
            return None

        print("Responsável cadastrado com sucesso!")
        return SerializadorResponsavel.desserializar(buscar_responsavel_por_id(id_resp))

    @staticmethod
    def listar_responsaveis():
        linhas = listar_responsaveis()
        responsaveis = [SerializadorResponsavel.desserializar(linha) for linha in linhas]

        print("\n--- LISTA DE RESPONSÁVEIS ---")
        if not responsaveis:
            print("Nenhum responsável cadastrado.")
        for r in responsaveis:
            print(f"[{r.id_resp}] {r.nome} (Login: {r.login})")

        return responsaveis

    @classmethod
    def editar_responsavel(
        cls,
        id_resp,
        novo_nome=None,
        novo_login=None,
        nova_senha=None,
    ):
        atualizado = editar_responsavel(
            id_resp=id_resp,
            novo_nome=novo_nome if novo_nome else None,
            novo_login=novo_login if novo_login else None,
            nova_senha=nova_senha if nova_senha else None,
        )
        if atualizado:
            print("Responsável atualizado com sucesso!")
        else:
            print("Não foi possível atualizar (nenhuma alteração, ID não encontrado ou login já em uso).")

        return SerializadorResponsavel.desserializar(buscar_responsavel_por_id(id_resp))

    @staticmethod
    def excluir_responsavel(id_resp):
        excluido = excluir_responsavel(id_resp)
        if excluido:
            print(f"Responsável {id_resp} excluído.")
        else:
            print("Responsável não encontrado.")
        return excluido

    @staticmethod
    def vincular_turma(id_resp, id_turma):
        vinculo = SerializadorResponsavelTurma.serializar(
            ResponsavelTurma(id_responsavel=id_resp, id_turma=id_turma)
        )
        return vincular_responsavel_turma(vinculo["idResponsavel"], vinculo["idTurma"])

    @staticmethod
    def desvincular_turma(id_resp, id_turma):
        return desvincular_responsavel_turma(id_resp, id_turma)
