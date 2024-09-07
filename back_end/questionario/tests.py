from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpRequest
from .models import Questionario, Pergunta, Resposta, RespondidoPor, Turma

# Create your tests here.

class TesteDeRespostaQuestionario(TestCase):
    def setUp(self): # aparentemente esse nome é padrão
        # cria um professor e um aluno
        self.aluno = User.objects.create_user(username='Testenildo', email='testenildo@gmail.com', password='root')
        self.professor = User.objects.create_user(username='Lula da Silva', email='lulag@gmail.com', password='root')

        # criando os grupos
        try:
            grupo = Group.objects.get(name='Aluno')
        except:
            grupo = Group.objects.create(name='Aluno')
        self.aluno.groups.add(grupo)

        try:
            grupo = Group.objects.get(name='Professor')
        except:
            grupo = Group.objects.create(name='Professor')
        self.professor.groups.add(grupo)

        # criando a turma
        self.turma = Turma.objects.create(
            professor=self.professor,
            nome='ENGsoft',
            capacidade=30
        )

        # criando o questionario e as perguntas
        self.questionario = Questionario.objects.create(
            enunciado = 'Questionario de Teste Agora Vai',
            turma=self.turma,
            abertura=timezone.now() - timezone.timedelta(days=1), # abriu ontem
            fechamento=timezone.now() + timezone.timedelta(days=1), # fecha amanhã
            quantidade_perguntas = 2
        )

        self.pergunta1 = Pergunta.objects.create(
            enunciado='quantos corpos tem na tela',
            questionario=self.questionario
        )
        self.pergunta1 = Pergunta.objects.create(
            enunciado='quer comprar um notebook',
            questionario=self.questionario
        )

        self.client = Client()