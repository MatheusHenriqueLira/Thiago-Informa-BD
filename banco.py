import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent

CAMINHO_BANCO = PASTA / "database" / "banco.db"
CAMINHO_SQL = PASTA / "criar_banco.sql"


def criar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        conexao.execute("PRAGMA foreign_keys = ON")
        script_sql = CAMINHO_SQL.read_text(encoding="utf-8")
        conexao.executescript(script_sql)
        print("Banco de dados criado com sucesso!")
    finally:
        conexao.close()


def buscar_admin(login, senha):
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

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
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

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


if __name__ == "__main__":
    criar_banco()
