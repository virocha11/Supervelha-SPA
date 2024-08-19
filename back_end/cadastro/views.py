from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, Group
import re

# Create your views here.

def home(request: HttpRequest):
    return render(request, 'registration/home.html')

def cadastro_aluno(request: HttpRequest):
    return render(request, 'registration/aluno.html')

def cadastro_professor(request: HttpRequest):
    return render(request, 'registration/professor.html')

def validar_cadastro(request: HttpRequest):
    if request.POST.get('password') != request.POST.get('cpassword'):
        return False, HttpResponse('As duas senhas digitadas são diferentes.')
    r = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
    if (not r.match(request.POST.get('email'))):
        return False, HttpResponse('E-mail inválido.')
    usuarios = User.objects.all()
    for usuario in usuarios:
        if usuario.email == request.POST.get('email'):
            return False, HttpResponse('E-mail já cadastrado.')
        if usuario.username == request.POST.get('username'):
            return False, HttpResponse('Nome de usuário em uso.')
    return True

def cadastrar_aluno(request: HttpRequest):
    if (validar_cadastro(request) == True):
        novo_aluno = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        try:
            grupo = Group.objects.get(name='Aluno')
        except:
            grupo = Group.objects.create(name='Aluno')
        novo_aluno.groups.add(grupo)
        return HttpResponse(f'Cadastrado com sucesso! Seu ID é: {novo_aluno.id}')
    else:
        return(validar_cadastro(request)[1])

def cadastrar_professor(request: HttpRequest):
    if (validar_cadastro(request) == True):
        novo_professor = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        try:
            grupo = Group.objects.get(name='Professor')
        except:
            grupo = Group.objects.create(name='Professor')
        novo_professor.groups.add(grupo)
        return HttpResponse(f'Cadastrado com sucesso! Seu ID é: {novo_professor.id}')
    else:
        return(validar_cadastro(request)[1])