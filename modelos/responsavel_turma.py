from banco import (
    vincular_responsavel_turma,
    desvincular_responsavel_turma,
    listar_turmas_do_responsavel,
)

class ResponsavelTurma:
    id_responsavel: int
    id_turma: int

    @staticmethod 
    def vincular(id_responsavel: int, id_turma: int) -> bool:
        """Concede acesso de uma turma a um responsavel/usuário."""
        return vincular_responsavel_turma(id_responsavel, id_turma)

    @staticmethod
    def desvincular(id_responsavel: int, id_turma: int) -> bool:
        """Remove o acesso de um responsavel a uma turma."""
        return desvincular_responsavel_turma(id_responsavel, id_turma)

    @staticmethod
    def listar_turmas_do_responsavel(id_responsavel: int) -> list:
        """Retorna todas as turmas (idturma e Nome) que o usuário tem permissão para visualizar."""
        return listar_turmas_do_responsavel(id_responsavel)
