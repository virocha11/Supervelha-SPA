from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login
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
    if (validar_cadastro(request) == True):
        novo_aluno = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        try:
            grupo = Group.objects.get(name='Aluno')
        except:
            grupo = Group.objects.create(name='Aluno')
        novo_aluno.groups.add(grupo)
        login(request, novo_aluno)
        messages.add_message(request, messages.SUCCESS, f'Cadastrado com sucesso! Seu ID é: {novo_aluno.id}')
        return render(request, 'paginas/cadastro.html')
    else:
        return render(request, 'paginas/cadastro.html')

def cadastrar_professor(request: HttpRequest):
    if (validar_cadastro(request) == True):
        novo_professor = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        try:
            grupo = Group.objects.get(name='Professor')
        except:
            grupo = Group.objects.create(name='Professor')
        novo_professor.groups.add(grupo)
        login(request, novo_professor)
        messages.add_message(request, messages.SUCCESS, f'Cadastrado com sucesso! Seu ID é: {novo_professor.id}')
        
        return render(request, 'paginas/cadastro.html')
    else:
        return render(request, 'paginas/cadastro.html')
    
def cadastrar_turma(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.groups.get().name == 'Professor':
                return render(request, 'registration/cadastrar_turma.html')
            else:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return render(request, 'registration/home.html')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário não autenticado.')
            return render(request, 'registration/home.html')

    if request.method == 'POST': # se for envio de formulário
        nome = request.POST.get('nome') # pegando os valores passados etc tal
        capacidade = request.POST.get('capacidade')
        quantidade_alunos = 0
        professor_responsavel = User.objects.get(id=request.user.id) # recupera o professor responsável baseado no id do formulario
        # cria nova turma se deus quiser com os valores pegos do get
        nova_turma = Turma.objects.create(nome=nome, capacidade=capacidade, professor=professor_responsavel, quantidade_alunos=quantidade_alunos)
        messages.add_message(request, messages.SUCCESS, f'Turma "{nova_turma.nome}" cadastrada com sucesso. O código dela é "{nova_turma.codigo}"!') # retorna pro ''front''
        return render(request, 'registration/cadastrar_turma.html') # retorna essa listinha
    
    # professores = User.objects.filter(groups__name='Professor')  # filtra apenas professores naquele campinho pra pessoa escolher

def excluir_usuario(request: HttpRequest):
    if request.method == 'GET': # somente exibe o formulario se voce estiver autenticado
        if request.user.is_authenticated:
            return render(request, 'registration/excluir_usuario.html')
        else:
            messages.add_message(request, messages.ERROR, 'Você precisa estar autenticado para excluir seu usuario.')
            return render(request, 'registration/home.html')

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id') # id do formulario
        try:
            usuario = User.objects.get(id=usuario_id) # buscando o id do formulario no banco
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Usuário não encontrado.')
            return render(request, 'registration/excluir_usuario.html')

        # verifica se o id do usuario autenticado é o mesmo de quem ele tá tentando calar
        if request.user.id != usuario.id:
            messages.add_message(request, messages.ERROR, 'Você só pode excluir seu próprio usuário.')
            return render(request, 'registration/excluir_usuario.html')

        # remove o usuário
        usuario.delete()
        messages.add_message(request, messages.SUCCESS, 'Seu usuário foi excluído com sucesso.')
        return render(request, 'registration/excluir_usuario.html')
    
def editar_usuario(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated: # somente exibe o formulario se voce estiver autenticado
            return render(request, 'registration/editar_usuario.html')
        else:
            messages.add_message(request, messages.ERROR, 'Você precisa estar autenticado para editar suas informações.')
            return render(request, 'registration/home.html')

    if request.method == 'POST':
        # validar os dados de entrada com validar cadastro
        if not validar_cadastro(request):
            return render(request, 'registration/editar_usuario.html')

        # se passou seja o que deus quiser
        nome = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')

        request.user.username = nome
        request.user.email = email

        if senha: # se o campo senha não estiver vazio
            request.user.set_password(senha)

        request.user.save() # salva as alterações
        messages.add_message(request, messages.SUCCESS, 'Suas informações foram atualizadas com sucesso.')
        return render(request, 'registration/editar_usuario.html')