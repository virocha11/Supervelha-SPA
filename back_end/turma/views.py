from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.models import User
from cadastro.models import Turma
from django.contrib import messages

# Create your views here.

def retornar_turmas(request: HttpRequest, path):
    turmas = Turma.objects.filter(professor=request.user.id)
    return render(request, path, {'turmas': turmas})

def adicionar_aluno(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.groups.get().name == 'Professor':
                return retornar_turmas(request, 'registration/adicionar_aluno.html')
            else:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return render(request, 'registration/home.html')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário não autenticado.')
            return render(request, 'registration/home.html')
    if request.method == 'POST':
        try:
            aluno = User.objects.get(username=request.POST.get('aluno'))
        except:
            messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
            return retornar_turmas(request, 'registration/adicionar_aluno.html')
        turma = Turma.objects.get(codigo=request.POST.get('turma'))
        if turma.quantidade_alunos == turma.capacidade:
            messages.add_message(request, messages.ERROR, 'Turma está cheia.')
            return retornar_turmas(request, 'registration/adicionar_aluno.html')
        for alun in turma.alunos.all():
            if alun == aluno:
                messages.add_message(request, messages.ERROR, 'Aluno já está cadastrado nesta turma.')
                return retornar_turmas(request, 'registration/adicionar_aluno.html')
        turma.quantidade_alunos = turma.quantidade_alunos + 1
        turma.alunos.add(aluno)
        turma.save()
        messages.add_message(request, messages.SUCCESS, f'Aluno: {aluno.username} adicionado com sucesso à turma: {turma.nome}.')
        return retornar_turmas(request, 'registration/adicionar_aluno.html')
    
def remover_aluno(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.groups.get().name == 'Professor':
                return retornar_turmas(request, 'registration/remover_aluno.html')
            else:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return render(request, 'registration/home.html')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário não autenticado.')
            return render(request, 'registration/home.html')
    if request.method == 'POST':
        try:
            aluno = User.objects.get(username=request.POST.get('aluno'))
        except:
            messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
            return retornar_turmas(request, 'registration/remover_aluno.html')
        turma = Turma.objects.get(codigo=request.POST.get('turma'))
        for alun in turma.alunos.all():
            if alun == aluno:
                turma.quantidade_alunos = turma.quantidade_alunos - 1
                turma.alunos.remove(aluno)
                turma.save()
                messages.add_message(request, messages.SUCCESS, f'Aluno: {aluno.username} removido com sucesso à turma: {turma.nome}.')
                return retornar_turmas(request, 'registration/remover_aluno.html')
        messages.add_message(request, messages.ERROR, 'Aluno não está cadastrado nesta turma.')
        return retornar_turmas(request, 'registration/remover_aluno.html')