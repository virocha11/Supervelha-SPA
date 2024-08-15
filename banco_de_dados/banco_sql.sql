USE supervelha;

DROP TABLE IF EXISTS resposta;
DROP TABLE IF EXISTS pergunta;
DROP TABLE IF EXISTS questionario;
DROP TABLE IF EXISTS matricula;
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
    ra_professor INT,
    nome TEXT NOT NULL,
    capacidade INT NOT NULL,
    quantidade_alunos INT,
    FOREIGN KEY (ra_professor) REFERENCES professor(ra_professor) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE matricula (
    ra_aluno INT NOT NULL,
    codigo_turma INT NOT NULL,
    ra_professor INT NOT NULL,
    FOREIGN KEY (ra_aluno) REFERENCES aluno(ra_aluno) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (codigo_turma) REFERENCES turma(codigo) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ra_professor) REFERENCES professor(ra_professor) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (ra_aluno, codigo_turma) # um aluno só é matriculado em uma turma uma vez
);


CREATE TABLE questionario (
    id_questionario INT NOT NULL PRIMARY KEY,
    codigo_turma INT NOT NULL,
    FOREIGN KEY (codigo_turma) REFERENCES turma(codigo) ON DELETE CASCADE ON UPDATE CASCADE 
);

CREATE TABLE pergunta (
    id_pergunta INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    enunciado TEXT NOT NULL,
    id_questionario INT NOT NULL,
    FOREIGN KEY (id_questionario) REFERENCES questionario(id_questionario) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE resposta (
    id_resposta INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pergunta INT NOT NULL,
    ra_aluno INT NOT NULL,
    nota INT,
    FOREIGN KEY (id_pergunta) REFERENCES pergunta(id_pergunta) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ra_aluno) REFERENCES aluno(ra_aluno) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (id_pergunta, ra_aluno) # cada aluno só pode responder à uma pergunta uma vez
);
