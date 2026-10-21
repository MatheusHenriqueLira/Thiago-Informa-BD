import sqlite3
from banco import conectar

class ResponsavelTurma:
    id_responsavel: int
    id_turma: int

    @staticmethod 
    def vincular(id_responsavel: int, id_turma: int) -> bool:
        """Concede acesso de uma turma a um responsavel/usuário."""
        try:
            with conectar() as conn:
                conn.execute(
                    "INSERT INTO ResponsavelTurma (idResponsavel, idTurma) VALUES (?, ?)",
                    (id_responsavel, id_turma)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def desvincular(id_responsavel: int, id_turma: int) -> bool:
        """Remove o acesso de um responsavel a uma turma."""
        with conectar() as conn:
            cursor = conn.execute(
                "DELETE FROM ResponsavelTurma WHERE idResponsavel = ? AND idTurma = ?",
                (id_responsavel, id_turma)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def listar_turmas_do_responsavel(id_responsavel: int) -> list:
        """Retorna todas as turmas (idturma e Nome) que o usuário tem permissão para visualizar."""
        with conectar() as conn:
            cursor = conn.execute(
                """
                SELECT t.idturma, t.Nome
                FROM Turma t
                INNER JOIN ResponsavelTurma rt ON t.idturma = rt.idTurma
                WHERE rt.idResponsavel = ? 
                ORDER BY t.Nome
                """,
                (id_responsavel,)
            )
            return [dict(linha) for linha in cursor.fetchall()]
