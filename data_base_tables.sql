create table Instituição(
	nome varchar(40) NOT NULL,
	endereço varchar(40) NOT NULL,
	id_faculdade int,
	primary key(id_faculdade)
);
create table Cursos(
	area varchar(20) NOT NULL,
	nome varchar(25) NOT NULL,
	id_curso int,
	id_faculdade int NOT NULL,
	primary key(id_curso),
    foreign key(id_faculdade) references Instituição
);
create table Alunos(
	nome varchar(50) NOT NULL,
	matricula int,
    email varchar(50) not null,
    telefone int NOT NULL,
	id_cursos int NOT NULL,
	id_instituição int NOT NULL,
	primary key(matricula),
    foreign key(id_instituição) references Instituição,
    foreign key(id_cursos) references Cursos,
);
create table Eventos(
	nome varchar(50) NOT NULL,
	id_evento int,
    id_instituição int,
    data_evento date,
    hora_inicio time NOT NULL,
    hora_final time NOT NULL,
	primary key(id_evento),
    foreign key(id_instituição) references Instituição
);

create table "Nome Evento"(
    id_aluno int,
    nome_aluno varchar(50) NOT null,
    checkin bit,
    checkout bit,
    foreign key(id_aluno) references Alunos
);
#SOMENTE SE NECESSARIO APLICAR CHAVES NA MÃO
alter table alunos add foreign key(id_cursos) references Cursos;
alter table alunos add foreign key(id_instituição) references Instituição;

alter table Cursos add foreign key(id_faculdade) references Instituição;