from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import Turma
import re

def cadastro(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('redirect')
        else:
            return render(request, 'paginas/cadastro.html')

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
        if usuario.email == request.POST.get('email') and usuario.id != request.user.id: # adiçao caso seja da mesma pessoa
            messages.add_message(request, messages.ERROR, 'E-mail já está em uso.')
            error = 1
        if usuario.username == request.POST.get('username') and usuario.id != request.user.id: # adiçao caso seja da mesma pessoa
            messages.add_message(request, messages.ERROR, 'Nome de usuário já está em uso.')
            error = 1
    if error == 1:
        return False
    else:
        return True
        
def cadastro_aluno(request: HttpRequest):
    return cadastrar_aluno(request)

def cadastro_professor(request: HttpRequest):
    return cadastrar_professor(request)

def cadastrar_aluno(request: HttpRequest):
    if request.method == 'POST':
        if (validar_cadastro(request) == True):
            novo_aluno = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            try:
                grupo = Group.objects.get(name='Aluno')
            except:
                grupo = Group.objects.create(name='Aluno')
            novo_aluno.groups.add(grupo)
            login(request, novo_aluno)
            messages.add_message(request, messages.SUCCESS, f'Cadastrado com sucesso! Seu ID é: {novo_aluno.id}')
            return redirect('redirect')
        else:
            return redirect('cadastro')
    else:
        return redirect('cadastro')

def cadastrar_professor(request: HttpRequest):
    if request.method == 'POST':
        if (validar_cadastro(request) == True):
            novo_professor = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            try:
                grupo = Group.objects.get(name='Professor')
            except:
                grupo = Group.objects.create(name='Professor')
            novo_professor.groups.add(grupo)
            login(request, novo_professor)
            messages.add_message(request, messages.SUCCESS, f'Cadastrado com sucesso! Seu ID é: {novo_professor.id}')
            return redirect('redirect')
        else:
            return redirect('cadastro')
    else:
        return redirect('cadastro')
    
def cadastrar_turma(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.groups.get().name == 'Professor':
                return render(request, 'paginas/cadastro_turma.html')
            else:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário não autenticado.')
            redirect('index')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        capacidade = request.POST.get('capacidade')
        quantidade_alunos = 0
        professor_responsavel = User.objects.get(id=request.user.id)
        nova_turma = Turma.objects.create(nome=nome, capacidade=capacidade, professor=professor_responsavel, quantidade_alunos=quantidade_alunos)
        messages.add_message(request, messages.SUCCESS, f'Turma "{nova_turma.nome}" cadastrada com sucesso. O código dela é "{nova_turma.codigo}"!')
        return redirect('cadastrar_turma')

def excluir_usuario(request: HttpRequest):
    if request.method == 'GET':
        request.user.delete()
        messages.add_message(request, messages.SUCCESS, 'Seu usuário foi excluído com sucesso.')
        return redirect('index')

def editar_usuario(request: HttpRequest):
    if request.method == 'POST':
        if not validar_cadastro(request):
            return redirect('perfil')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')
        nova_senha = request.POST.get('nova_senha')
        if senha:
            if not confirma_senha or not nova_senha:
                messages.add_message(request, messages.ERROR, 'Credencias novas incorretas.')
                return redirect('perfil')
            user = authenticate(request, username=request.user.username, password=senha)
            if user is not None:
                if nova_senha == senha:
                    messages.add_message(request, messages.ERROR, 'Nova senha é igual a senha atual.')
                    return redirect('perfil')
                if confirma_senha == nova_senha:
                    request.user.set_password(nova_senha)
                    login(request, request.user)
                else:
                    messages.add_message(request, messages.ERROR, 'Senhas digitadas são diferentes.')
                    return redirect('perfil')
            else:
                messages.add_message(request, messages.ERROR, 'Senha atual incorreta.')
                return redirect('perfil')
        elif nova_senha or confirma_senha:
            messages.add_message(request, messages.ERROR, 'Você precisa informar sua senha atual para alterá-la.')
            return redirect('perfil')
        username = request.POST.get('username')
        email = request.POST.get('email')
        nome = request.POST.get('nome')
        if username:
            request.user.username = username
        if nome:
            request.user.first_name = nome
        if email:
            request.user.email = email
        request.user.save() 
        messages.add_message(request, messages.SUCCESS, 'Suas informações foram atualizadas com sucesso.')
        return redirect('perfil')
    
def excluir_turma(request: HttpRequest, codigo_turma):
    if request.method == 'GET':
        turma = Turma.objects.get(codigo=codigo_turma)
        if request.user != turma.professor:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            redirect('redirect')
        turma.delete()
        messages.add_message(request, messages.SUCCESS, 'Turma excluída com sucesso.')
        return redirect('minhas_turmas')