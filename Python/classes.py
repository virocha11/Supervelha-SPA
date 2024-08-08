class Professor:
    def __init__(self, nome, email, ra):
        self.nome = nome
        self.email = email
        self.ra = ra

class Aluno:
    def __init__(self, nome, email, ra):
        self.nome = nome
        self.email = email
        self.ra = ra

class Turma:
    def __init__(self, codigo, nome, capacidade, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.capacidade = capacidade
        self.quantidade = quantidade

class Questionario:
    def __init__(self, id, codigo_turma):
        self.id = id
        self.codigo_turma = codigo_turma

class Pergunta:
    def __init__(self, id, enunciado):
        self.id = id
        self.enunciado = enunciado

class Resposta:
    def __init__(self, id, ra_aluno, id_pergunta, avaliacao):
        self.id = id
        self.ra_aluno = ra_aluno
        self.id_pergunta = id_pergunta
        self.avaliacao = avaliacao