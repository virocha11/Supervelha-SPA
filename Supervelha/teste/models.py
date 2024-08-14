from django.db import models

# Create your models here.

class Professor(models.Model):
    nome = models.TextField(null=False)
    email = models.EmailField(null=False)

class Aluno(models.Model):
    nome = models.TextField(null=False)
    email = models.EmailField(null=False)

class Turma(models.Model):
    nome = models.TextField(null=False)
    capacidade = models.IntegerField(null=False)
    quantidade_alunos = models.IntegerField(default=0, null=False)

class Questionario(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=False)

class Pergunta(models.Model):
    enunciado = models.TextField(null=False)
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE, null=False)

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, null=False)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=False)
    nota = models.IntegerField()