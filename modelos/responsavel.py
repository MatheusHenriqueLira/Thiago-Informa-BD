from banco import conectar 

class Responsavel:
    id_resp: int
    nome: str

    def __init__(self, nome: str, id_resp: int = None):
        self.id_resp = id_resp
        self.nome = nome

    @staticmethod
    def cadastrar(nome: str) -> int:
        with conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO Responsavel (Nome) VALUES (?)",
                (nome.strip(),)
            )
            conn.commit()
            return cursor.lastrowid

    # Alias de compatibilidade
    cadastar = cadastrar

    @staticmethod
    def listar_todos() -> list: 
        with conectar() as conn:
            cursor = conn.execute("SELECT idresp, Nome FROM Responsavel ORDER BY Nome")
            return [dict(linha) for linha in cursor.fetchall()]

    @staticmethod
    def buscar_por_id(id_resp: int) -> dict | None:
        with conectar() as conn:
            cursor = conn.execute(
                "SELECT idresp, Nome FROM Responsavel WHERE idresp = ?",
                (id_resp,)
            )
            linha = cursor.fetchone()
            return dict(linha) if linha else None

    @staticmethod
    def editar(id_resp: int, novo_nome: str) -> bool:
        with conectar() as conn:
            cursor = conn.execute(
                "UPDATE Responsavel SET Nome = ? WHERE idresp = ?",
                (novo_nome.strip(), id_resp)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod 
    def excluir(id_resp: int) -> bool:
        with conectar() as conn:
            cursor = conn.execute(
                "DELETE FROM Responsavel WHERE idresp = ?",
                (id_resp,)
            )
            conn.commit()
            return cursor.rowcount > 0
