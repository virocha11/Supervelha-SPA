from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def index(request: HttpRequest):
    return render(request, 'index.html')

def redirect_group(request: HttpRequest):
    if request.user.groups.get().name == 'Professor':
        return redirect('inicio_professor')
    elif request.user.groups.get().name == 'Aluno':
        return redirect('inicio_aluno')

def home_professor(request: HttpRequest):
    return render(request, 'paginas/inicio_professor.html')

def home_aluno(request: HttpRequest):
    return render(request, 'paginas/inicio_aluno.html')

def login_validate(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('redirect')
    else:
        if request.method == 'GET':
            return render(request, 'paginas/login.html')
        elif request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('redirect')
            else:
                messages.add_message(request, messages.ERROR, 'Nome de usuário ou senha incorretos.')
                return render(request, 'paginas/login.html')
        
def logout_validate(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Sessão inválida.')
            return redirect('login')
        
def perfil_professor(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'paginas/perfil_prof.html')