from django.shortcuts import render, redirect
from django.http import HttpRequest
from cadastro.models import Turma
from .models import Questionario, Pergunta, Resposta
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.utils import timezone

# Create your views here.

def visualizar_questionarios(request: HttpRequest, codigo_turma):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo=codigo_turma)
            questionarios = Questionario.objects.filter(turma=turma)
            return render(request, 'paginas/questionarios.html', {'turma': turma, 'questionarios': questionarios})
        elif request.user.groups.get().name == 'Aluno':
            turma = Turma.objects.get(codigo=codigo_turma)
            questionarios = Questionario.objects.filter(turma=turma)
            return render(request, 'paginas/questionarios_aluno.html', {'turma': turma, 'questionarios': questionarios})
        
def visualizar_questionario(request: HttpRequest, questionario_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            questoes = Pergunta.objects.filter(questionario=questionario)
            return render(request, 'paginas/questionario.html', {'questionario': questionario, 'questoes': questoes})
        elif request.user.groups.get().name == 'Aluno':
            questionario = Questionario.objects.get(id=questionario_id)
            if questionario.abertura <= timezone.now() <= questionario.fechamento:
                questoes = Pergunta.objects.filter(questionario=questionario)
                return render(request, 'paginas/questionario_aluno.html', {'questionario': questionario, 'questoes': questoes})
            else:
                messages.add_message(request, messages.ERROR, 'Questionário fechado.')
                return redirect('questionarios', questionario.turma.codigo)
        
def criar_questionario(request: HttpRequest, codigo_turma):
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo=codigo_turma)
            abertura_str = request.POST.get('abertura')
            abertura = parse_datetime(abertura_str)
            fechamento_str = request.POST.get('fechamento')
            fechamento = parse_datetime(fechamento_str)
            questionario = Questionario.objects.create(enunciado=request.POST.get('enunciado'), turma=turma, abertura=abertura, fechamento=fechamento)
            messages.add_message(request, messages.SUCCESS, f'Questionário criado com sucesso! ID: {questionario.id}')
            return redirect('questionarios', turma.codigo)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')

def excluir_questionario(request: HttpRequest, questionario_id, codigo_turma):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            questionario.delete()
            messages.add_message(request, messages.SUCCESS, 'Questionário excluído com sucesso!')
            return redirect('questionarios', codigo_turma)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
def editar_questionario(request: HttpRequest, questionario_id):
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            enunciado = request.POST.get('enunciado')
            if enunciado:
                questionario.enunciado = enunciado
            abertura_str = request.POST.get('abertura')
            if abertura_str:
                abertura = parse_datetime(abertura_str)
                questionario.abertura = abertura
            fechamento_str = request.POST.get('fechamento')
            if fechamento_str:
                fechamento = parse_datetime(fechamento_str)
                questionario.fechamento = fechamento
            questionario.save()
            messages.add_message(request, messages.SUCCESS, 'Questionario alterado com sucesso!')
            return redirect('visualizar_questionario', questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
def adicionar_pergunta(request: HttpRequest, questionario_id):
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            enunciado = request.POST.get('enunciado')
            if enunciado:
                try: 
                    pergunta = Pergunta.objects.get(enunciado=enunciado, questionario_id=questionario_id)
                    messages.add_message(request, messages.ERROR, 'Questão já existe.')
                except:
                    Pergunta.objects.create(enunciado=enunciado, questionario=questionario)
                    questionario.quantidade_perguntas += 1
                    questionario.save()
                    messages.add_message(request, messages.SUCCESS, 'Questão adicionada com sucesso!')
            return redirect('visualizar_questionario', questionario_id=questionario_id)
        
def remover_pergunta(request: HttpRequest, questionario_id, questao_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            pergunta = Pergunta.objects.get(id=questao_id)
            if pergunta:
                questionario = Questionario.objects.get(id=questionario_id)
                if questionario.turma.professor == request.user:
                    pergunta.delete()
                    questionario.quantidade_perguntas -= 1
                    questionario.save()
                    messages.add_message(request, messages.SUCCESS, 'Questão removida com sucesso!')
                    return redirect('visualizar_questionario', questionario_id=questionario_id)
                else:
                    messages.add_message(request, messages.ERROR, 'Permissão negada.')
                    return redirect('redirect')
            else:
                messages.add_message(request, messages.ERROR, 'Questão não existe.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
def editar_pergunta(request: HttpRequest, questionario_id, questao_id):
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            questao = Pergunta.objects.get(id=questao_id)
            enunciado = request.POST.get('enunciado')
            questao.enunciado = enunciado
            questao.save()
            messages.add_message(request, messages.SUCCESS, 'Questão alterada com sucesso!')
            return redirect('visualizar_questionario', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
def responder_questionario(request:HttpRequest, questionario_id):
    if request.method == 'POST':
        if request.user.groups.get().name == 'Aluno':
            questionario = Questionario.objects.get(id=questionario_id)
            if request.user not in questionario.respondido_por.all():
                perguntas = Pergunta.objects.filter(questionario=questionario)
                respostas = request.POST.getlist('resposta')
                aux = 0
                for pergunta in perguntas:
                    Resposta.objects.create(aluno=request.user, pergunta=pergunta, resposta=respostas[aux])
                    aux += 1
                questionario.respondido_por.add(request.user)
                questionario.save()
                messages.add_message(request, messages.SUCCESS, 'Questionário respondido com sucesso!')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
            else:
                messages.add_message(request, messages.ERROR, 'Você já respondeu esse questionário.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')