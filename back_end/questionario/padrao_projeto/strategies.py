from abc import ABC, abstractmethod
from django.shortcuts import render, redirect
from django.contrib import messages
from questionario.models import Questionario, RespondidoPor

class verificar_respostas_strategy(ABC): # ABC = classe base abstrata, ou seja, define métodos para serem implementados por suas subclasses
    @abstractmethod # indica os métodos abstratos
    def verificar(self, request, questionario_id): # deve ser implementado por subclasses
        pass

class professor_verificacao_strategy(verificar_respostas_strategy): # herda de verificar_respostas_strategy e portanto def verificar
    def verificar(self, request, questionario_id): # implementação concreta do método abstrato: instância, requisição HTTP e o questionário a ser verificado
        questionario = Questionario.objects.get(id=questionario_id)
        alunos = questionario.respondido_por.all() # obtém todos os alunos que responderam ao questionário
        avaliacao = RespondidoPor.objects.filter(questionario=questionario) # obtém todas as avaliações associadas ao question[ário
        alunos_avaliacao = zip(alunos, avaliacao) # combina os alunos e suas avaliaçoes
        return render(request, 'paginas/respostas.html', {'questionario': questionario, 'alunos': alunos_avaliacao})

class nao_autorizado_verificacao_strategy(verificar_respostas_strategy): # herda de verificar_respostas_strategy e portanto def verificar
    def verificar(self, request, questionario_id): # implementação concreta do método abstrato
        messages.add_message(request, messages.ERROR, 'Permissão negada.') # não é um professor
        return redirect('redirect')
    
class verificacao_context: # context é uma convenção de strategy: descreve a classe que gerencia a interação entre o usuario e as strategies
    def __init__(self, strategy: verificar_respostas_strategy): # vai receber a instancia de uma classe que implementou verificar_respostas_strategy
        self._strategy = strategy

    def executar_verificacao(self, request, questionario_id):
        return self._strategy.verificar(request, questionario_id) # chama o método verificar da estratégia atual (da classe que foi instanciada e chamada)
