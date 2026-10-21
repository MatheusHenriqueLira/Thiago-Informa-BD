PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Turma (
    idturma INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Admin (
    idAdmin INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Login TEXT NOT NULL UNIQUE,
    Senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Responsavel (
    idresp INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Login TEXT NOT NULL UNIQUE,
    Senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Imagem (
    idImagem INTEGER PRIMARY KEY AUTOINCREMENT,
    Caminho TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Projeto (
    idProjeto INTEGER PRIMARY KEY AUTOINCREMENT,
    datacriacao TEXT DEFAULT CURRENT_TIMESTAMP,
    Titulo TEXT NOT NULL,
    Conteudo TEXT,
    idAdmin INTEGER NOT NULL,

    FOREIGN KEY (idAdmin)
        REFERENCES Admin(idAdmin) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Informativos (
    Idinfo INTEGER PRIMARY KEY AUTOINCREMENT,
    datacriacao TEXT DEFAULT CURRENT_TIMESTAMP,
    Titulo TEXT NOT NULL,
    Conteudo TEXT,
    idAdmin INTEGER NOT NULL,
    estafixado INTEGER NOT NULL DEFAULT 0
        CHECK (estafixado IN (0, 1)),
    idImagem INTEGER,

    FOREIGN KEY (idAdmin)
        REFERENCES Admin(idAdmin) ON DELETE CASCADE,
    FOREIGN KEY (idImagem)
        REFERENCES Imagem(idImagem) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ResponsavelTurma (
    idResponsavel INTEGER,
    idTurma INTEGER,

    PRIMARY KEY (idResponsavel, idTurma),
    FOREIGN KEY (idResponsavel)
        REFERENCES Responsavel(idresp) ON DELETE CASCADE,
    FOREIGN KEY (idTurma)
        REFERENCES Turma(idturma) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ImgProjeto (
    idImagem INTEGER,
    idProjeto INTEGER,

    PRIMARY KEY (idImagem, idProjeto),
    FOREIGN KEY (idImagem)
        REFERENCES Imagem(idImagem) ON DELETE CASCADE,
    FOREIGN KEY (idProjeto)
        REFERENCES Projeto(idProjeto) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ProjetoTurma (
    idProjeto INTEGER,
    idTurma INTEGER,

    PRIMARY KEY (idProjeto, idTurma),
    FOREIGN KEY (idProjeto)
        REFERENCES Projeto(idProjeto) ON DELETE CASCADE,
    FOREIGN KEY (idTurma)
        REFERENCES Turma(idturma) ON DELETE CASCADE
);

INSERT INTO Admin (Nome, Login, Senha)
SELECT 'Catia', 'Catia', '1234'
WHERE NOT EXISTS (
    SELECT 1 FROM Admin WHERE Login = 'Catia'
);

INSERT INTO Responsavel (Nome, Login, Senha)
SELECT 'Responsavel Teste', 'pais', '1234'
WHERE NOT EXISTS (
    SELECT 1 FROM Responsavel WHERE Login = 'pais'
);
