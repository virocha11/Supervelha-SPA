from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from cadastro.models import Turma
from django.contrib import messages

# Create your views here.

def minhas_turmas(request: HttpRequest):
    if request.user.groups.get().name == 'Professor':
        turmas = Turma.objects.filter(professor=request.user.id)
        return render(request, 'paginas/turmas_prof.html', {'turmas': turmas})
    elif request.user.groups.get().name == 'Aluno':
        turmas = Turma.objects.filter(alunos=request.user)
        return render(request, 'paginas/turmas_aluno.html', {'turmas': turmas})

def visualizar_turma(request: HttpRequest, codigo_turma):
    if request.user.groups.get().name == 'Professor':
        turma = Turma.objects.get(codigo=codigo_turma)
        alunos = turma.alunos.all()
        return render(request, 'paginas/turma.html', {'turma': turma, 'alunos': alunos})
    elif request.user.groups.get().name == 'Aluno':
        turma = Turma.objects.get(codigo=codigo_turma)
        return render(request, 'paginas/turma_aluno.html', {'turma': turma})

def editar_turma(request: HttpRequest, codigo_turma):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo = codigo_turma)
            alunos = turma.alunos.all()
            return render(request, 'paginas/editar_turma.html', {'turma': turma, 'alunos': alunos})
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect') 
        
def editar_detalhes_turma(request: HttpRequest, codigo_turma):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo = codigo_turma)
            return render(request, 'paginas/editar_detalhes_turma.html', {'turma': turma})
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo = codigo_turma)
            nome = request.POST.get('nome')
            capacidade = request.POST.get('capacidade')
            if capacidade:
                if int(capacidade) < turma.quantidade_alunos:
                    messages.add_message(request, messages.ERROR, 'Capacidade menor que quantidade de alunos atual.')
                    return redirect('minhas_turmas')
                elif int(capacidade) < 0:
                    messages.add_message(request, messages.ERROR, 'Capacidade não pode ser negativa.')
                    return redirect('minhas_turmas')
                else:
                    turma.capacidade = capacidade
                    turma.save()
            if nome:
                turma.nome = nome
                turma.save()
            messages.add_message(request, messages.SUCCESS, 'Detalhes alterados com sucesso!')
            return redirect('minhas_turmas')

def adicionar_aluno(request: HttpRequest, codigo_turma):
    if request.method == 'POST':
        try:
            aluno = User.objects.get(username=request.POST.get('aluno'))
        except:
            messages.add_message(request, messages.ERROR, 'Aluno não encontrado.')
            return visualizar_turma(request, codigo_turma)
        turma = Turma.objects.get(codigo=codigo_turma)
        if turma.quantidade_alunos == turma.capacidade:
            messages.add_message(request, messages.ERROR, 'Turma está cheia.')
            return visualizar_turma(request, codigo_turma)
        for alun in turma.alunos.all():
            if alun == aluno:
                messages.add_message(request, messages.ERROR, 'Aluno já está cadastrado nesta turma.')
                return visualizar_turma(request, codigo_turma)
        turma.quantidade_alunos = turma.quantidade_alunos + 1
        turma.alunos.add(aluno)
        turma.save()
        messages.add_message(request, messages.SUCCESS, f'Aluno: {aluno.username} adicionado com sucesso à turma: {turma.nome}.')
        return visualizar_turma(request, codigo_turma)
    
def remover_aluno(request: HttpRequest, codigo_turma, user_aluno):
    if request.method == 'GET':
        aluno = User.objects.get(username=user_aluno)
        turma = Turma.objects.get(codigo=codigo_turma)
        turma.quantidade_alunos = turma.quantidade_alunos - 1
        turma.alunos.remove(aluno)
        turma.save()
        messages.add_message(request, messages.SUCCESS, f'Aluno: {aluno.username} removido com sucesso da turma: {turma.nome}.')
        return visualizar_turma(request, codigo_turma)