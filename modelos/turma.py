from banco import conectar

class Turma:
    id_turma: int
    nome: str

    def __init__(self, nome: str, id_turma: int = None):
        self.id_turma = id_turma
        self.nome = nome

    @staticmethod
    def cadastrar(nome: str) -> int:
        with conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO Turma (Nome) VALUES (?)",
                (nome.strip(),)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def listar_todas() -> list:
        with conectar() as conn:
            cursor = conn.execute("SELECT idturma, Nome FROM Turma ORDER BY Nome")
            return [dict(linha) for linha in cursor.fetchall()]

    @staticmethod
    def buscar_por_id(id_turma: int) -> dict | None:
        with conectar() as conn:
            cursor = conn.execute(
                "SELECT idturma, Nome FROM Turma WHERE idturma = ?",
                (id_turma,)
            )
            linha = cursor.fetchone()
            return dict(linha) if linha else None

    @staticmethod
    def editar(id_turma: int, novo_nome: str) -> bool:
        with conectar() as conn:
            cursor = conn.execute(
                "UPDATE Turma SET Nome = ? WHERE idturma = ?",
                (novo_nome.strip(), id_turma)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def excluir(id_turma: int) -> bool:
        with conectar() as conn:
            cursor = conn.execute(
                "DELETE FROM Turma WHERE idturma = ?",
                (id_turma,)
            )
            conn.commit()
            return cursor.rowcount > 0
