import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent

CAMINHO_BANCO = PASTA / "database" / "banco.db"
CAMINHO_SQL = PASTA / "criar_banco.sql"


def conectar():
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
# Operações SQL - Admin
# ==============================================================================

def buscar_admin(login, senha):
    """Busca um administrador pelo login e senha para autenticação."""
    with conectar() as conn:
        registro = conn.execute(
            """
            SELECT idAdmin, Nome, Login, Senha
            FROM Admin
            WHERE Login = ? AND Senha = ?
            """,
            (login, senha),
        ).fetchone()
        return dict(registro) if registro else None

# ==============================================================================
# Operações SQL - Responsavel
# ==============================================================================

def buscar_responsavel(login, senha):
    """Busca um responsável pelo login e senha para autenticação."""
    with conectar() as conn:
        registro = conn.execute(
            """
            SELECT idresp, Nome, Login, Senha
            FROM Responsavel
            WHERE Login = ? AND Senha = ?
            """,
            (login, senha),
        ).fetchone()
        return dict(registro) if registro else None


def inserir_responsavel(nome, login=None, senha="1234"):
    """Insere um novo responsável e retorna o idresp gerado."""
    nome_limpo = nome.strip()
    login_final = login.strip() if login else nome_limpo
    try:
        with conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO Responsavel (Nome, Login, Senha) VALUES (?, ?, ?)",
                (nome_limpo, login_final, senha),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar_responsaveis():
    """Retorna todos os responsáveis cadastrados em ordem alfabética."""
    with conectar() as conn:
        cursor = conn.execute("SELECT idresp, Nome, Login, Senha FROM Responsavel ORDER BY Nome")
        return [dict(linha) for linha in cursor.fetchall()]


def buscar_responsavel_por_id(id_resp):
    """Busca um responsável pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT idresp, Nome, Login, Senha FROM Responsavel WHERE idresp = ?",
            (id_resp,),
        )
        linha = cursor.fetchone()
        return dict(linha) if linha else None


def editar_responsavel(id_resp, novo_nome=None, novo_login=None, nova_senha=None):
    """Atualiza os dados de um responsável."""
    atualizacoes = []
    parametros = []

    if novo_nome:
        atualizacoes.append("Nome = ?")
        parametros.append(novo_nome.strip())
    if novo_login:
        atualizacoes.append("Login = ?")
        parametros.append(novo_login.strip())
    if nova_senha:
        atualizacoes.append("Senha = ?")
        parametros.append(nova_senha)

    if not atualizacoes:
        return False

    parametros.append(id_resp)
    sql = f"UPDATE Responsavel SET {', '.join(atualizacoes)} WHERE idresp = ?"

    try:
        with conectar() as conn:
            cursor = conn.execute(sql, tuple(parametros))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False


def excluir_responsavel(id_resp):
    """Remove um responsável pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM Responsavel WHERE idresp = ?",
            (id_resp,),
        )
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - Turma
# ==============================================================================

def inserir_turma(nome):
    """Insere uma nova turma e retorna o idturma gerado."""
    try:
        with conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO Turma (Nome) VALUES (?)",
                (nome.strip(),),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar_turmas():
    """Retorna todas as turmas cadastradas em ordem alfabética."""
    with conectar() as conn:
        cursor = conn.execute("SELECT idturma, Nome FROM Turma ORDER BY Nome")
        return [dict(linha) for linha in cursor.fetchall()]


def buscar_turma_por_id(id_turma):
    """Busca uma turma pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT idturma, Nome FROM Turma WHERE idturma = ?",
            (id_turma,),
        )
        linha = cursor.fetchone()
        return dict(linha) if linha else None


def editar_turma(id_turma, novo_nome):
    """Atualiza o nome de uma turma."""
    try:
        with conectar() as conn:
            cursor = conn.execute(
                "UPDATE Turma SET Nome = ? WHERE idturma = ?",
                (novo_nome.strip(), id_turma),
            )
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False


def excluir_turma(id_turma):
    """Remove uma turma pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM Turma WHERE idturma = ?",
            (id_turma,),
        )
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - ResponsavelTurma
# ==============================================================================

def vincular_responsavel_turma(id_responsavel, id_turma):
    """Vincula um responsável a uma turma."""
    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO ResponsavelTurma (idResponsavel, idTurma) VALUES (?, ?)",
                (id_responsavel, id_turma),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def desvincular_responsavel_turma(id_responsavel, id_turma):
    """Remove o vínculo entre responsável e turma."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM ResponsavelTurma WHERE idResponsavel = ? AND idTurma = ?",
            (id_responsavel, id_turma),
        )
        conn.commit()
        return cursor.rowcount > 0


def listar_turmas_do_responsavel(id_responsavel):
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
            (id_responsavel,),
        )
        return [dict(linha) for linha in cursor.fetchall()]


def listar_responsaveis_da_turma(id_turma):
    """Retorna todos os responsáveis vinculados a uma turma."""
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT r.idresp, r.Nome, r.Login
            FROM Responsavel r
            INNER JOIN ResponsavelTurma rt ON r.idresp = rt.idResponsavel
            WHERE rt.idTurma = ?
            ORDER BY r.Nome
            """,
            (id_turma,),
        )
        return [dict(linha) for linha in cursor.fetchall()]


# ==============================================================================
# Operações SQL - Imagem
# ==============================================================================

def inserir_imagem(caminho_relativo):
    """Insere o caminho de uma imagem no banco e retorna o idImagem gerado."""
    try:
        with conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO Imagem (Caminho) VALUES (?)",
                (caminho_relativo,),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def buscar_imagem_por_id(id_imagem):
    """Busca uma imagem pelo ID."""
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT idImagem, Caminho AS caminho FROM Imagem WHERE idImagem = ?",
            (id_imagem,),
        )
        linha = cursor.fetchone()
        return dict(linha) if linha else None


def listar_imagens():
    """Lista todas as imagens cadastradas no banco."""
    with conectar() as conn:
        cursor = conn.execute("SELECT idImagem, Caminho AS caminho FROM Imagem ORDER BY idImagem DESC")
        return [dict(linha) for linha in cursor.fetchall()]


def excluir_imagem(id_imagem):
    """Remove o registro da imagem no banco de dados."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM Imagem WHERE idImagem = ?",
            (id_imagem,),
        )
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - Informativos
# ==============================================================================

def inserir_informativo(titulo, conteudo, id_admin, esta_fixado=0, id_imagem=None):
    """Insere um novo informativo no banco e retorna o Idinfo gerado."""
    try:
        with conectar() as conn:
            cursor = conn.execute(
                """
                INSERT INTO Informativos (Titulo, Conteudo, idAdmin, estafixado, idImagem)
                VALUES (?, ?, ?, ?, ?)
                """,
                (titulo.strip(), conteudo, id_admin, 1 if esta_fixado else 0, id_imagem),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar_informativos():
    """Lista todos os informativos ordenados por fixado e data de criação."""
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT i.Idinfo, i.Titulo, i.Conteudo, i.datacriacao, i.idAdmin,
                   i.estafixado, i.idImagem, a.Nome AS NomeAdmin, img.Caminho AS CaminhoImagem
            FROM Informativos i
            LEFT JOIN Admin a ON i.idAdmin = a.idAdmin
            LEFT JOIN Imagem img ON i.idImagem = img.idImagem
            ORDER BY i.estafixado DESC, i.datacriacao DESC
            """
        )
        return [dict(linha) for linha in cursor.fetchall()]


def buscar_informativo_por_id(id_info):
    """Busca um informativo específico pelo ID."""
    with conectar() as conn:
        linha = conn.execute(
            """
            SELECT i.Idinfo, i.Titulo, i.Conteudo, i.datacriacao, i.idAdmin,
                   i.estafixado, i.idImagem, a.Nome AS NomeAdmin, img.Caminho AS CaminhoImagem
            FROM Informativos i
            LEFT JOIN Admin a ON i.idAdmin = a.idAdmin
            LEFT JOIN Imagem img ON i.idImagem = img.idImagem
            WHERE i.Idinfo = ?
            """,
            (id_info,),
        ).fetchone()
        return dict(linha) if linha else None


def alterar_fixado_informativo(id_info):
    """Inverte o status de fixado (0 -> 1 ou 1 -> 0) de um informativo e retorna o novo status."""
    with conectar() as conn:
        linha = conn.execute(
            "SELECT estafixado FROM Informativos WHERE Idinfo = ?",
            (id_info,),
        ).fetchone()

        if linha is None:
            return None

        novo_status = 1 if linha["estafixado"] == 0 else 0
        conn.execute(
            "UPDATE Informativos SET estafixado = ? WHERE Idinfo = ?",
            (novo_status, id_info),
        )
        conn.commit()
        return bool(novo_status)


def editar_informativo(id_info, novo_titulo=None, novo_conteudo=None, id_imagem=None):
    """Atualiza título, conteúdo e/ou imagem de um informativo."""
    atualizacoes = []
    parametros = []

    if novo_titulo:
        atualizacoes.append("Titulo = ?")
        parametros.append(novo_titulo.strip())
    if novo_conteudo:
        atualizacoes.append("Conteudo = ?")
        parametros.append(novo_conteudo)
    if id_imagem is not None:
        atualizacoes.append("idImagem = ?")
        parametros.append(id_imagem)

    if not atualizacoes:
        return False

    parametros.append(id_info)
    sql = f"UPDATE Informativos SET {', '.join(atualizacoes)} WHERE Idinfo = ?"

    with conectar() as conn:
        cursor = conn.execute(sql, tuple(parametros))
        conn.commit()
        return cursor.rowcount > 0


def excluir_informativo(id_info):
    """Remove um informativo pelo ID."""
    with conectar() as conn:
        cursor = conn.execute("DELETE FROM Informativos WHERE Idinfo = ?", (id_info,))
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - Projeto
# ==============================================================================

def inserir_projeto(titulo, conteudo, id_admin):
    """Insere um novo projeto e retorna o idProjeto gerado."""
    try:
        with conectar() as conn:
            cursor = conn.execute(
                """
                INSERT INTO Projeto (Titulo, Conteudo, idAdmin)
                VALUES (?, ?, ?)
                """,
                (titulo.strip(), conteudo, id_admin),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar_projetos():
    """Lista todos os projetos cadastrados."""
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT p.idProjeto, p.datacriacao, p.Titulo, p.Conteudo, p.idAdmin,
                   a.Nome AS NomeAdmin, GROUP_CONCAT(img.Caminho, ', ') AS CaminhoImagem
            FROM Projeto p
            LEFT JOIN Admin a ON p.idAdmin = a.idAdmin
            LEFT JOIN ImgProjeto ip ON p.idProjeto = ip.idProjeto
            LEFT JOIN Imagem img ON ip.idImagem = img.idImagem
            GROUP BY p.idProjeto
            ORDER BY p.datacriacao DESC
            """
        )
        return [dict(linha) for linha in cursor.fetchall()]


def buscar_projeto_por_id(id_projeto):
    """Busca um projeto pelo ID."""
    with conectar() as conn:
        linha = conn.execute(
            """
            SELECT p.idProjeto, p.datacriacao, p.Titulo, p.Conteudo, p.idAdmin,
                   a.Nome AS NomeAdmin, GROUP_CONCAT(img.Caminho, ', ') AS CaminhoImagem
            FROM Projeto p
            LEFT JOIN Admin a ON p.idAdmin = a.idAdmin
            LEFT JOIN ImgProjeto ip ON p.idProjeto = ip.idProjeto
            LEFT JOIN Imagem img ON ip.idImagem = img.idImagem
            WHERE p.idProjeto = ?
            GROUP BY p.idProjeto
            """,
            (id_projeto,),
        ).fetchone()
        if linha and linha["idProjeto"] is not None:
            return dict(linha)
        return None


def editar_projeto(id_projeto, novo_titulo=None, novo_conteudo=None):
    """Atualiza o título e/ou conteúdo de um projeto."""
    atualizacoes = []
    parametros = []

    if novo_titulo:
        atualizacoes.append("Titulo = ?")
        parametros.append(novo_titulo.strip())
    if novo_conteudo:
        atualizacoes.append("Conteudo = ?")
        parametros.append(novo_conteudo)

    if not atualizacoes:
        return False

    parametros.append(id_projeto)
    sql = f"UPDATE Projeto SET {', '.join(atualizacoes)} WHERE idProjeto = ?"

    with conectar() as conn:
        cursor = conn.execute(sql, tuple(parametros))
        conn.commit()
        return cursor.rowcount > 0


def excluir_projeto(id_projeto):
    """Remove um projeto pelo ID."""
    with conectar() as conn:
        cursor = conn.execute("DELETE FROM Projeto WHERE idProjeto = ?", (id_projeto,))
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# Operações SQL - ImgProjeto 
# ==============================================================================

def vincular_imagem_projeto(id_imagem, id_projeto):
    """Vincula uma imagem a um projeto."""
    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO ImgProjeto (idImagem, idProjeto) VALUES (?, ?)",
                (id_imagem, id_projeto),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def desvincular_imagem_projeto(id_imagem, id_projeto):
    """Remove o vínculo entre uma imagem e um projeto."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM ImgProjeto WHERE idImagem = ? AND idProjeto = ?",
            (id_imagem, id_projeto),
        )
        conn.commit()
        return cursor.rowcount > 0


def listar_imagens_do_projeto(id_projeto):
    """Retorna todas as imagens vinculadas a um projeto."""
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT i.idImagem, i.Caminho AS caminho
            FROM Imagem i
            INNER JOIN ImgProjeto ip ON i.idImagem = ip.idImagem
            WHERE ip.idProjeto = ?
            """,
            (id_projeto,),
        )
        return [dict(linha) for linha in cursor.fetchall()]


# ==============================================================================
# Operações SQL - ProjetoTurma
# ==============================================================================

def vincular_projeto_turma(id_projeto, id_turma):
    """Vincula um projeto a uma turma."""
    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO ProjetoTurma (idProjeto, idTurma) VALUES (?, ?)",
                (id_projeto, id_turma),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def desvincular_projeto_turma(id_projeto, id_turma):
    """Remove o vínculo entre um projeto e uma turma."""
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM ProjetoTurma WHERE idProjeto = ? AND idTurma = ?",
            (id_projeto, id_turma),
        )
        conn.commit()
        return cursor.rowcount > 0


def listar_turmas_do_projeto(id_projeto):
    """Retorna todas as turmas vinculadas a um projeto."""
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT t.idturma, t.Nome
            FROM Turma t
            INNER JOIN ProjetoTurma pt ON t.idturma = pt.idTurma
            WHERE pt.idProjeto = ?
            ORDER BY t.Nome
            """,
            (id_projeto,),
        )
        return [dict(linha) for linha in cursor.fetchall()]


def listar_projetos_da_turma(id_turma):
    """Retorna todos os projetos vinculados a uma turma."""
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT p.idProjeto, p.datacriacao, p.Titulo, p.Conteudo, p.idAdmin,
                   a.Nome AS NomeAdmin, GROUP_CONCAT(img.Caminho, ', ') AS CaminhoImagem
            FROM Projeto p
            INNER JOIN ProjetoTurma pt ON p.idProjeto = pt.idProjeto
            LEFT JOIN Admin a ON p.idAdmin = a.idAdmin
            LEFT JOIN ImgProjeto ip ON p.idProjeto = ip.idProjeto
            LEFT JOIN Imagem img ON ip.idImagem = img.idImagem
            WHERE pt.idTurma = ?
            GROUP BY p.idProjeto
            ORDER BY p.datacriacao DESC
            """,
            (id_turma,),
        )
        return [dict(linha) for linha in cursor.fetchall()]


if __name__ == "__main__":
    criar_banco()
