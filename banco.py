import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent

CAMINHO_BANCO = PASTA / "database" / "banco.db"
CAMINHO_SQL = PASTA / "criar_banco.sql"

def conectar() -> sqlite3.Connection:
    """Abre conexão com o banco SQLite garantindo que as Foreign Keys estejam ativas"""
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def criar_banco():
    """Cria as tabelas do banco a partir do arquivo criar_banco.sql"""
    conexao = conectar()

    try:
        script_sql = CAMINHO_SQL.read_text(encoding="utf-8")
        conexao.executescript(script_sql)
        conexao.commit()
        print("Banco de dados criado com sucesso!")
    finally:
        conexao.close()

if __name__ == "__main__":
    criar_banco()
