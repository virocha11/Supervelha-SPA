from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, Group
from django.contrib import messages

import re

# Create your views here.

def home(request: HttpRequest):
    return render(request, 'registration/home.html')

def cadastro_aluno(request: HttpRequest):
    return render(request, 'registration/aluno.html')

def cadastro_professor(request: HttpRequest):
    return render(request, 'registration/professor.html')

def validar_cadastro(request: HttpRequest):
    error = 0
    if request.POST.get('password') != request.POST.get('cpassword'):
        messages.add_message(request, messages.ERROR, 'As duas senhas digitadas são diferentes.')
        error = 1
    r = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
    if (not r.match(request.POST.get('email'))):
        messages.add_message(request, messages.ERROR, 'E-mail inválido.')
        error = 1
    usuarios = User.objects.all()
    for usuario in usuarios:
        if usuario.email == request.POST.get('email'):
            messages.add_message(request, messages.ERROR, 'E-mail já está em uso.')
            error = 1
        if usuario.username == request.POST.get('username'):
            messages.add_message(request, messages.ERROR, 'Nome de usuário já está em uso.')
            error = 1
    if error == 1:
        return False
    else:
        return True

def cadastrar_aluno(request: HttpRequest):
    if (validar_cadastro(request) == True):
        novo_aluno = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        try:
            grupo = Group.objects.get(name='Aluno')
        except:
            grupo = Group.objects.create(name='Aluno')
        novo_aluno.groups.add(grupo)
        messages.add_message(request, messages.SUCCESS, f'Cadastrado com sucesso! Seu ID é: {novo_aluno.id}')
        return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/aluno.html')

def cadastrar_professor(request: HttpRequest):
    if (validar_cadastro(request) == True):
        novo_professor = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        try:
            grupo = Group.objects.get(name='Professor')
        except:
            grupo = Group.objects.create(name='Professor')
        novo_professor.groups.add(grupo)
        messages.add_message(request, messages.SUCCESS, f'Cadastrado com sucesso! Seu ID é: {novo_professor.id}')
        return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/professor.html')