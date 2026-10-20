import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "database" / "banco.db"

conexao = sqlite3.connect(CAMINHO_BANCO)
conexao.execute("PRAGMA foreign_keys = ON")

cursor = conexao.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""")

tabelas = cursor.fetchall()

print("Tabelas do banco:")

for tabela in tabelas:
    print("-", tabela[0])

conexao.close()
