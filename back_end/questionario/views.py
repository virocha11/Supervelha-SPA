from django.shortcuts import render, redirect
from django.http import HttpRequest
from cadastro.models import Turma
from .models import Questionario, Pergunta, Resposta, RespondidoPor
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth.models import User
from .padrao_projeto.strategies import professor_verificacao_strategy, nao_autorizado_verificacao_strategy, verificacao_context

def visualizar_questionarios(request: HttpRequest, codigo_turma): # listagem com todos os questionarios
    if request.method == 'GET':
        turma = Turma.objects.get(codigo=codigo_turma)
        if request.user.groups.get().name == 'Professor':
            questionarios = Questionario.objects.filter(turma=turma)
            return render(request, 'paginas/questionarios.html', {'turma': turma, 'questionarios': questionarios})
        elif request.user.groups.get().name == 'Aluno':
            questionarios = Questionario.objects.filter(turma=turma, publico=True)
            return render(request, 'paginas/questionarios_aluno.html', {'turma': turma, 'questionarios': questionarios})
        
def visualizar_questionario(request: HttpRequest, questionario_id): # depois de selecionar um em específico
    if request.method == 'GET':
        questionario = Questionario.objects.get(id=questionario_id)
        questoes = Pergunta.objects.filter(questionario=questionario)
        if request.user.groups.get().name == 'Professor':
            return render(request, 'paginas/questionario.html', {'questionario': questionario, 'questoes': questoes})
        elif request.user.groups.get().name == 'Aluno':
            if questionario.publico:
                try:
                    avaliacao = RespondidoPor.objects.get(questionario=questionario, aluno=request.user)
                    return render(request, 'paginas/questionario_aluno.html', {'questionario': questionario, 'questoes': questoes, 'avaliacao': avaliacao})
                except:
                    return render(request, 'paginas/questionario_aluno.html', {'questionario': questionario, 'questoes': questoes})
            else:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
        
def criar_questionario(request: HttpRequest, codigo_turma):
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            turma = Turma.objects.get(codigo=codigo_turma)
            if request.user != turma.professor:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
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

def publicar_questionario(request: HttpRequest, questionario_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            if request.user != questionario.turma.professor:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
            if questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questionário já está público.')
                return redirect('visualizar_questionario', questionario_id)
            questionario.publico = True
            questionario.save()
            messages.add_message(request, messages.SUCCESS, 'Questionário publicado com sucesso!')
            return redirect('visualizar_questionario', questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')

def excluir_questionario(request: HttpRequest, questionario_id, codigo_turma):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            if request.user != Turma.objects.get(codigo=codigo_turma).professor:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')  
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
            if request.user != questionario.turma.professor:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect') 
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
            if request.user != questionario.turma.professor:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
            if questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questão está público.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
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
                if questionario.publico:
                    messages.add_message(request, messages.ERROR, 'Questionário está público.')
                    return redirect('visualizar_questionario', questionario_id=questionario_id)
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
            if request.user != Questionario.objects.get(id=questionario_id).turma.professor:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
            questionario = Questionario.objects.get(id=questionario_id)
            if questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questionário está público.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
            perguntas = Pergunta.objects.filter(questionario=Questionario.objects.get(id=questionario_id))
            enunciado = request.POST.get('enunciado')
            for pergunta in perguntas:
                if pergunta.enunciado == enunciado:
                    messages.add_message(request, messages.ERROR, 'Questão já existe.')
                    return redirect('visualizar_questionario', questionario_id=questionario_id)
            questao = Pergunta.objects.get(id=questao_id)
            questao.enunciado = enunciado
            questao.save()
            messages.add_message(request, messages.SUCCESS, 'Questão alterada com sucesso!')
            return redirect('visualizar_questionario', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
def responder_questionario(request:HttpRequest, questionario_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Aluno':
            questionario = Questionario.objects.get(id=questionario_id)
            if questionario.publico:
                if questionario.abertura <= timezone.now() <= questionario.fechamento:
                    if request.user not in questionario.respondido_por.all():
                        questoes = Pergunta.objects.filter(questionario=questionario)
                        return render(request, 'paginas/responder_aluno.html', {'questionario': questionario, 'questoes': questoes})
                    else:
                        messages.add_message(request, messages.ERROR, 'Você já respondeu esse questionário.')
                        return redirect('visualizar_questionario', questionario_id=questionario_id)
                else:
                    messages.add_message(request, messages.ERROR, 'Questionário fechado.')
                    return redirect('visualizar_questionario', questionario_id=questionario_id)
            else:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
    if request.method == 'POST':
        if request.user.groups.get().name == 'Aluno':
            questionario = Questionario.objects.get(id=questionario_id)
            if not questionario.publico:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
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

def revisar_respostas(request: HttpRequest, questionario_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Aluno':
            questionario = Questionario.objects.get(id=questionario_id)
            if not questionario.publico:
                messages.add_message(request, messages.ERROR, 'Permissão negada.')
                return redirect('redirect')
            if request.user in questionario.respondido_por.all():
                questoes = Pergunta.objects.filter(questionario=questionario)
                respostas = []
                for questao in questoes:
                    respostas.append(Resposta.objects.get(pergunta=questao, aluno=request.user))
                questoes_respostas = zip(questoes, respostas)
                avaliacao = RespondidoPor.objects.get(questionario=questionario, aluno=request.user)
                return render(request, 'paginas/revisao_aluno.html', {'questionario': questionario, 'questoes_respostas': questoes_respostas, 'avaliacao': avaliacao})
            else:
                messages.add_message(request, messages.ERROR, 'Você não respondeu esse questionário.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
# def verificar_respostas(request: HttpRequest, questionario_id):
#     if request.method == 'GET':
#         if request.user.groups.get().name == 'Professor':
#             questionario = Questionario.objects.get(id=questionario_id)
#             alunos = questionario.respondido_por.all()
#             avaliacao = RespondidoPor.objects.filter(questionario=questionario)
#             alunos_avaliacao = zip(alunos, avaliacao)
#             return render(request, 'paginas/respostas.html', {'questionario': questionario, 'alunos': alunos_avaliacao})
#         else:
#             messages.add_message(request, messages.ERROR, 'Permissão negada.')
#             return redirect('redirect')
def verificar_respostas(request: HttpRequest, questionario_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            strategy = professor_verificacao_strategy()
        else:
            strategy = nao_autorizado_verificacao_strategy()
        # context é uma convenção de strategy: descreve a classe que gerencia a interação entre o usuario e as strategies
        context = verificacao_context(strategy)
        return context.executar_verificacao(request, questionario_id)
        
def avaliar_respostas(request: HttpRequest, questionario_id, aluno_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            if not questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questionário não foi publicado.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
            aluno = User.objects.get(id=aluno_id)
            questoes = Pergunta.objects.filter(questionario=questionario)
            avaliacao = RespondidoPor.objects.get(questionario=questionario, aluno=aluno)
            respostas = []
            for questao in questoes:
                respostas.append(Resposta.objects.get(pergunta=questao, aluno=aluno))
            if not respostas[0].avaliado:
                questoes_respostas = zip(questoes, respostas)
                return render(request, 'paginas/avaliar.html', {'questionario': questionario, 'questoes_respostas': questoes_respostas, 'aluno': aluno, 'avaliacao': avaliacao})
            else:
                messages.add_message(request, messages.ERROR, 'Questionário já avaliado.')
                return redirect('verificar_respostas', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            if not questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questionário não foi publicado.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
            aluno = User.objects.get(id=aluno_id)
            questoes = Pergunta.objects.filter(questionario=questionario)
            respostas = []
            for questao in questoes:
                respostas.append(Resposta.objects.get(pergunta=questao, aluno=aluno))
            if respostas[0].avaliado:
                messages.add_message(request, messages.ERROR, 'Questionário já avaliado.')
                return redirect('verificar_respostas', questionario_id=questionario_id)
            else:
                notas = request.POST.getlist('notas')
                aux = 0
                nota = 0
                for resposta in respostas:
                    resposta.nota = notas[aux]
                    resposta.avaliado = 1
                    resposta.save()
                    nota += int(notas[aux])
                    aux += 1
                nota = nota/aux
                nota = round(nota, 1)
                respondido_por = RespondidoPor.objects.get(questionario=questionario, aluno=aluno)
                respondido_por.nota = nota
                respondido_por.avaliado = True
                respondido_por.save()
                messages.add_message(request, messages.SUCCESS, 'Questionário avaliado com sucesso!')
                return redirect('verificar_respostas', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
        
def editar_avalicao(request: HttpRequest, questionario_id, aluno_id):
    if request.method == 'GET':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            if not questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questionário não foi publicado.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
            aluno = User.objects.get(id=aluno_id)
            questoes = Pergunta.objects.filter(questionario=questionario)
            avaliacao = RespondidoPor.objects.get(questionario=questionario, aluno=aluno)
            respostas = []
            for questao in questoes:
                respostas.append(Resposta.objects.get(pergunta=questao, aluno=aluno))
            if respostas[0].avaliado:
                questoes_respostas = zip(questoes, respostas)
                return render(request, 'paginas/editar_avaliacao.html', {'questionario': questionario, 'questoes_respostas': questoes_respostas, 'aluno': aluno, 'avaliacao': avaliacao})
            else:
                messages.add_message(request, messages.ERROR, 'Questionário não foi avaliado.')
                return redirect('verificar_respostas', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')
    if request.method == 'POST':
        if request.user.groups.get().name == 'Professor':
            questionario = Questionario.objects.get(id=questionario_id)
            if not questionario.publico:
                messages.add_message(request, messages.ERROR, 'Questionário não foi publicado.')
                return redirect('visualizar_questionario', questionario_id=questionario_id)
            aluno = User.objects.get(id=aluno_id)
            questoes = Pergunta.objects.filter(questionario=questionario)
            respostas = []
            for questao in questoes:
                respostas.append(Resposta.objects.get(pergunta=questao, aluno=aluno))
            if not respostas[0].avaliado:
                messages.add_message(request, messages.ERROR, 'Questionário não foi avaliado.')
                return redirect('verificar_respostas', questionario_id=questionario_id)
            else:
                notas = request.POST.getlist('notas')
                aux = 0
                nota = 0
                for resposta in respostas:
                    resposta.nota = notas[aux]
                    resposta.save()
                    nota += float(notas[aux])
                    aux += 1
                nota = nota/aux
                nota = round(nota, 1)
                respondido_por = RespondidoPor.objects.get(questionario=questionario, aluno=aluno)
                respondido_por.nota = nota
                respondido_por.save()
                messages.add_message(request, messages.SUCCESS, 'Avaliação atualizada com sucesso!')
                return redirect('verificar_respostas', questionario_id=questionario_id)
        else:
            messages.add_message(request, messages.ERROR, 'Permissão negada.')
            return redirect('redirect')