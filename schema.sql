--
-- File generated with SQLiteStudio v3.1.1 on ter jul 24 13:36:00 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: alunos
CREATE TABLE alunos (
    id        INTEGER PRIMARY KEY ON CONFLICT REPLACE AUTOINCREMENT,
    nome      VARCHAR NOT NULL ON CONFLICT FAIL,
    email     VARCHAR NOT NULL ON CONFLICT FAIL,
    telefone  VARCHAR NOT NULL ON CONFLICT FAIL,
    matricula VARCHAR UNIQUE ON CONFLICT FAIL
                      NOT NULL ON CONFLICT FAIL,
    curso     INTEGER REFERENCES cursos (id) 
                      NOT NULL ON CONFLICT FAIL,
    faculdade INTEGER REFERENCES instituicao (id) 
                      NOT NULL ON CONFLICT FAIL
);


-- Table: cursos
CREATE TABLE cursos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    area      VARCHAR NOT NULL ON CONFLICT FAIL,
    nome      VARCHAR NOT NULL ON CONFLICT FAIL,
    faculdade INTEGER REFERENCES instituicao (id) 
                      NOT NULL ON CONFLICT FAIL
);


-- Table: eventos
CREATE TABLE eventos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      VARCHAR NOT NULL ON CONFLICT FAIL,
    faculdade INTEGER REFERENCES instituicao (id) 
                      NOT NULL ON CONFLICT FAIL,
    data      DATE    NOT NULL,
    inicio    TIME    NOT NULL ON CONFLICT FAIL,
    final     TIME    NOT NULL
);


-- Table: instituicao
CREATE TABLE instituicao (
    id             INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT
                           UNIQUE ON CONFLICT REPLACE,
    endereco       VARCHAR NOT NULL,
    nome_faculdade VARCHAR NOT NULL ON CONFLICT FAIL
);


-- Table: Tecweek
CREATE TABLE Tecweek (
    aluno      INTEGER REFERENCES alunos (id) 
                       NOT NULL ON CONFLICT FAIL
                       UNIQUE ON CONFLICT FAIL,
    nome_aluno VARCHAR NOT NULL ON CONFLICT FAIL,
    checkin    BOOLEAN NOT NULL
                       DEFAULT false,
    checkout   BOOLEAN NOT NULL
                       DEFAULT false
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
