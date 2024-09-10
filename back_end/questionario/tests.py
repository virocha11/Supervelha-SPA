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
        self.professor = User.objects.create_user(username='LuladaSilva', email='lulag@gmail.com', password='root')
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
        self.pergunta2 = Pergunta.objects.create(
            enunciado='quer comprar um notebook',
            questionario=self.questionario
        )
        self.questionario.publico = 1
        self.questionario.save()
        self.resposta1 = Resposta.objects.create(
            resposta='103',
            aluno = self.aluno,
            pergunta = self.pergunta1
        )
        self.resposta2 = Resposta.objects.create(
            resposta='sim',
            aluno = self.aluno,
            pergunta = self.pergunta2
        )
        self.respondidoPor = RespondidoPor.objects.create(
            data_envio = timezone.now(),
            aluno = self.aluno,
            questionario = self.questionario
        )
        self.client = Client()

    def test_get_avaliar_questionario(self):
        login = self.client.login(username='LuladaSilva', password='root')
        response = self.client.get(reverse('avaliar_respostas', kwargs={'questionario_id': self.questionario.id, 'aluno_id': self.aluno.id}))
        self.assertEqual(str(response.context['user']), 'LuladaSilva')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/avaliar.html')

    def test_post_avaliar_questionario(self):
        login = self.client.login(username='LuladaSilva', password='root')
        data={"notas": [1,2]}
        response = self.client.post(reverse('avaliar_respostas', kwargs={'questionario_id': self.questionario.id, 'aluno_id': self.aluno.id}), data)
        self.assertRedirects(response, f'/questionario/verificar_respostas/questionario_id={self.questionario.id}')
        self.resposta1 = Resposta.objects.get(pk=self.resposta1.id)
        self.assertEqual(self.resposta1.nota, 1)
        self.resposta2 = Resposta.objects.get(pk=self.resposta2.id)
        self.assertEqual(self.resposta2.nota, 2)
        self.respondidoPor = RespondidoPor.objects.get(pk=self.respondidoPor.id)
        self.assertEqual(self.respondidoPor.nota, 1.5)

    def test_get_revisar_respotas(self):
        login = self.client.login(username='Testenildo', password='root')
        response = self.client.get(reverse('revisar_respostas', kwargs={'questionario_id': self.questionario.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/revisao_aluno.html')

    def test_get_revisar_respostas_avaliadas(self):
        login = self.client.login(username='LuladaSilva', password='root')
        data={"notas": [1,2]}
        response = self.client.post(reverse('avaliar_respostas', kwargs={'questionario_id': self.questionario.id, 'aluno_id': self.aluno.id}), data)

        login = self.client.login(username='Testenildo', password='root')
        response = self.client.get(reverse('revisar_respostas', kwargs={'questionario_id': self.questionario.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/revisao_aluno.html')