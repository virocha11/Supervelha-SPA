from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpRequest
from .models import Turma

# Create your views here.

# def hello(request):
#     return HttpResponse('Hello!')

def cadastrar_turma(request: HttpRequest):
    if request.method == 'POST': # se for envio de formulário
        nome = request.POST.get('nome') # pegando os valores passados etc tal
        capacidade = request.POST.get('capacidade')
        ra_professor = request.POST.get('ra_professor')
        quantidade_alunos = request.POST.get('quantidade_alunos')

        professor_responsavel = User.objects.get(id=ra_professor) # recupera o professor responsável baseado no id do formulario

        # cria nova turma se deus quiser com os valores pegos do get
        nova_turma = Turma.objects.create(nome=nome, capacidade=capacidade, ra_professor=professor_responsavel, quantidade_alunos=quantidade_alunos)

        messages.add_message(request, messages.SUCCESS, f'Turma "{nova_turma.nome}" cadastrada com sucesso. O código dela é "{nova_turma.codigo}"!') # retorna pro ''front''
    
    professores = User.objects.filter(groups__name='Professor')  # filtra apenas professores naquele campinho pra pessoa escolher
    return render(request, 'registration/cadastrar_turma.html', {'professores': professores}) # retorna essa listinha

