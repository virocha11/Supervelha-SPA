from django.shortcuts import render, redirect
from django.http import HttpRequest
from cadastro.models import Turma
from .models import Questionario
from django.contrib import messages
from django.utils.dateparse import parse_datetime

# Create your views here.

def visualizar_questionarios(request: HttpRequest, codigo_turma):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo=codigo_turma)
            questionarios = Questionario.objects.filter(turma=turma)
            return render(request, 'paginas/questionarios.html', {'turma': turma, 'questionarios': questionarios})
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
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
        
def visualizar_questionario(request: HttpRequest, questionario_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            return render(request, 'paginas/questionario.html', {'questionario': questionario})
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