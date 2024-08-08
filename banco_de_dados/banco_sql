USE supervelha;

DROP TABLE IF EXISTS resposta;
DROP TABLE IF EXISTS perguntas;
DROP TABLE IF EXISTS questionario;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS aluno;
DROP TABLE IF EXISTS professor;

CREATE TABLE professor (
	ra_professor INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);

ALTER TABLE professor AUTO_INCREMENT = 100000;

CREATE TABLE aluno (
	ra_aluno INT NOT NULL NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);

ALTER TABLE aluno AUTO_INCREMENT = 200000;

CREATE TABLE turma (
	codigo INT NOT NULL PRIMARY KEY,
    nome TEXT NOT NULL,
    capacidade INT NOT NULL,
    quantidade_alunos INT
);

CREATE TABLE questionario (
	id_questionario INT NOT NULL PRIMARY KEY,
    codigo_turma INT NOT NULL,
    FOREIGN KEY (codigo_turma) REFERENCES turma(codigo) ON DELETE CASCADE ON UPDATE CASCADE 
);

CREATE TABLE perguntas (
	id_pergunta INT NOT NULL PRIMARY KEY,
    enunciado TEXT NOT NULL,
    id_questionario INT NOT NULL,
    FOREIGN KEY (id_questionario) REFERENCES questionario(id_questionario) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE resposta (
	id_resposta INT NOT NULL PRIMARY KEY, 
    id_pergunta INT NOT NULL,
    ra_aluno INT NOT NULL,
    nota INT, 
    FOREIGN KEY (id_pergunta) REFERENCES perguntas(id_pergunta) ON DELETE CASCADE ON UPDATE CASCADE ,
    FOREIGN KEY (ra_aluno) REFERENCES aluno(ra_aluno) ON DELETE CASCADE ON UPDATE CASCADE 
);
