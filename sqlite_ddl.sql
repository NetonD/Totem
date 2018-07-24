CREATE TABLE instituicao (
    id             INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT
                           NOT NULL ON CONFLICT REPLACE
                           UNIQUE ON CONFLICT REPLACE,
    endereco       VARCHAR NOT NULL,
    nome_faculdade VARCHAR NOT NULL ON CONFLICT FAIL
);
CREATE TABLE cursos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    area      VARCHAR NOT NULL ON CONFLICT FAIL,
    nome      VARCHAR NOT NULL ON CONFLICT FAIL,
    faculdade INTEGER REFERENCES instituicao (id)
);
CREATE TABLE alunos (
    id        INTEGER PRIMARY KEY ON CONFLICT REPLACE AUTOINCREMENT
                      NOT NULL ON CONFLICT REPLACE,
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
CREATE TABLE eventos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      VARCHAR NOT NULL ON CONFLICT FAIL,
    faculdade INTEGER REFERENCES instituicao (id)
                      NOT NULL ON CONFLICT FAIL,
    data      DATE    NOT NULL,
    inicio    TIME    NOT NULL ON CONFLICT FAIL,
    final     TIME    NOT NULL
);

/*teste*/
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
