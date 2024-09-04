from django.db import models
from django.contrib.auth.models import User
from cadastro.models import Turma
from django.utils import timezone

# Create your models here.

class Questionario(models.Model):
    enunciado = models.TextField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    abertura = models.DateTimeField(default=timezone.now)
    fechamento = models.DateTimeField(default=timezone.now)
    quantidade_perguntas = models.IntegerField(default=0)
    respondido_por = models.ManyToManyField(User, through='RespondidoPor')
    def __str__(self):
        return self.enunciado

class RespondidoPor(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Aluno'})
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    avaliado = models.BooleanField(default=0)
    nota = models.FloatField(null=True)
    data_envio = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.aluno.username
   
class Pergunta(models.Model):
    enunciado = models.TextField()
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    def __str__(self):
        return self.enunciado

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Aluno'})
    resposta = models.TextField()
    avaliado = models.BooleanField(default=0)
    nota = models.IntegerField(null=True)
    def __str__(self):
        return self.resposta