from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Turma(models.Model):
    codigo = models.AutoField(primary_key=True)
    ra_professor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Professor'}) # somente
    # professor consegue cadastrar
    nome = models.CharField(max_length=100) # mudei de text pra char pq senao fica mto grande ne
    capacidade = models.IntegerField()
    quantidade_alunos = models.IntegerField(null=True, blank=True) # pode ter 0 alunos no banco, pode ser deixado vazio no formulario

    def __str__(self):
        return self.nome
