from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Turma(models.Model):
    codigo = models.AutoField(primary_key=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Professor'})
    nome = models.CharField(max_length=100)
    capacidade = models.IntegerField()
    alunos = models.ManyToManyField(User, limit_choices_to={'groups__name': 'Aluno'}, related_name='alunos_set')
    quantidade_alunos = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.nome