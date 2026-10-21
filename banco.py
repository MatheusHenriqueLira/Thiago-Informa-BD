import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent

CAMINHO_BANCO = PASTA / "database" / "banco.db"
CAMINHO_SQL = PASTA / "criar_banco.sql"


def conectar() -> sqlite3.Connection:
    """Abre conexão com o banco SQLite garantindo que as Foreign Keys estejam ativas."""
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def criar_banco():
    """Cria as tabelas do banco a partir do arquivo criar_banco.sql."""
    conexao = conectar()
    try:
        script_sql = CAMINHO_SQL.read_text(encoding="utf-8")
        conexao.executescript(script_sql)
        conexao.commit()
        print("Banco de dados criado com sucesso!")
    finally:
        conexao.close()


# ==============================================================================
# Operações SQL - Autenticação (Admin e Responsavel)
# ==============================================================================

def buscar_admin(login, senha):
    conexao = conectar()
    try:
        registro = conexao.execute(
            """
            SELECT idAdmin, Nome, Login, Senha
            FROM Admin
            WHERE Login = ? AND Senha = ?
            """,
            (login, senha),
        ).fetchone()

        if registro:
            return dict(registro)
        return None
    finally:
        conexao.close()


def buscar_responsavel(login, senha):
    conexao = conectar()
    try:
        registro = conexao.execute(
            """
            SELECT idresp, Nome, Login, Senha
            FROM Responsavel
            WHERE Login = ? AND Senha = ?
            """,
            (login, senha),
        ).fetchone()

        if registro:
            return dict(registro)
        return None
    finally:
        conexao.close()


# ==============================================================================
# Operações SQL - Turma
# ==============================================================================

def inserir_turma(nome: str) -> int:
    """Insere uma nova turma e retorna o idturma gerado."""
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO Turma (Nome) VALUES (?)",
            (nome.strip(),)
        )
        conn.commit()
        return cursor.lastrowid


def listar_turmas() -> list[dict]:
    """Retorna todas as turmas cadastradas em ordem alfabética."""
    with conectar() as conn:
        cursor = conn.execute("SELECT idturma, Nome FROM Turma ORDER BY Nome")
        return [dict(linha) for linha in cursor.fetchall()]


def buscar_turma_por_id(id_turma: int) -> dict | None:
    """Busca uma turma pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT idturma, Nome FROM Turma WHERE idturma = ?",
            (id_turma,)
        )
        linha = cursor.fetchone()
        return dict(linha) if linha else None


def editar_turma(id_turma: int, novo_nome: str) -> bool:
    """Atualiza o nome de uma turma."""
    with conectar() as conn:
        cursor = conn.execute(
            "UPDATE Turma SET Nome = ? WHERE idturma = ?",
            (novo_nome.strip(), id_turma)
        )
        conn.commit()
        return cursor.rowcount > 0


def excluir_turma(id_turma: int) -> bool:
    """Remove uma turma pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM Turma WHERE idturma = ?",
            (id_turma,)
        )
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - Responsavel
# ==============================================================================

def inserir_responsavel(nome: str, login: str = None, senha: str = "1234") -> int:
    """Insere um novo responsável e retorna o idresp gerado."""
    nome_limpo = nome.strip()
    login_final = login.strip() if login else nome_limpo
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO Responsavel (Nome, Login, Senha) VALUES (?, ?, ?)",
            (nome_limpo, login_final, senha)
        )
        conn.commit()
        return cursor.lastrowid


def listar_responsaveis() -> list[dict]:
    """Retorna todos os responsáveis cadastrados em ordem alfabética."""
    with conectar() as conn:
        cursor = conn.execute("SELECT idresp, Nome, Login, Senha FROM Responsavel ORDER BY Nome")
        return [dict(linha) for linha in cursor.fetchall()]


def buscar_responsavel_por_id(id_resp: int) -> dict | None:
    """Busca um responsável pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT idresp, Nome, Login, Senha FROM Responsavel WHERE idresp = ?",
            (id_resp,)
        )
        linha = cursor.fetchone()
        return dict(linha) if linha else None


def editar_responsavel(id_resp: int, novo_nome: str) -> bool:
    """Atualiza o nome de um responsável."""
    with conectar() as conn:
        cursor = conn.execute(
            "UPDATE Responsavel SET Nome = ? WHERE idresp = ?",
            (novo_nome.strip(), id_resp)
        )
        conn.commit()
        return cursor.rowcount > 0


def excluir_responsavel(id_resp: int) -> bool:
    """Remove um responsável pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM Responsavel WHERE idresp = ?",
            (id_resp,)
        )
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - ResponsavelTurma (Vínculo)
# ==============================================================================

def vincular_responsavel_turma(id_responsavel: int, id_turma: int) -> bool:
    """Vincula um responsável a uma turma."""
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


def desvincular_responsavel_turma(id_responsavel: int, id_turma: int) -> bool:
    """Remove o vínculo entre responsável e turma."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM ResponsavelTurma WHERE idResponsavel = ? AND idTurma = ?",
            (id_responsavel, id_turma)
        )
        conn.commit()
        return cursor.rowcount > 0


def listar_turmas_do_responsavel(id_responsavel: int) -> list[dict]:
    """Retorna todas as turmas vinculadas ao responsável informado."""
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


# ==============================================================================
# Operações SQL - Imagem
# ==============================================================================

def inserir_imagem(caminho_relativo: str) -> int:
    """Insere o caminho de uma imagem no banco e retorna o idImagem gerado."""
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO Imagem (Caminho) VALUES (?)",
            (caminho_relativo,)
        )
        conn.commit()
        return cursor.lastrowid


def buscar_imagem_por_id(id_imagem: int) -> dict | None:
    """Busca uma imagem pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT idImagem, Caminho AS caminho FROM Imagem WHERE idImagem = ?",
            (id_imagem,)
        )
        linha = cursor.fetchone()
        return dict(linha) if linha else None


def excluir_imagem(id_imagem: int) -> bool:
    """Remove o registro da imagem no banco de dados."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM Imagem WHERE idImagem = ?",
            (id_imagem,)
        )
        conn.commit()
        return cursor.rowcount > 0


if __name__ == "__main__":
    criar_banco()
