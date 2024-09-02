from django.urls import path
from . import views

urlpatterns = [
    path('turma_id=<codigo_turma>', views.visualizar_questionarios, name='questionarios'),
    path('adicionar/turma_id=<codigo_turma>', views.criar_questionario, name='criar_questionario'),
    path('visualizar/questionario_id=<questionario_id>', views.visualizar_questionario, name='visualizar_questionario'),
    path('editar/questionario_id=<questionario_id>', views.editar_questionario, name='editar_questionario'),
    path('excluir/turma_id=<codigo_turma>&questionario_id=<questionario_id>', views.excluir_questionario, name='excluir_questionario'),
    path('adicionar_questao/questionario_id=<questionario_id>', views.adicionar_pergunta, name='adicionar_questao'),
    path('remover_questao/questionario_id=<questionario_id>&questao_id=<questao_id>', views.remover_pergunta, name='remover_questao'),
    path('editar_questao/questionario_id=<questionario_id>&questao_id=<questao_id>', views.editar_pergunta, name='editar_questao'),
    path('responder/questionario_id=<questionario_id>', views.responder_questionario, name='responder_questionario'),
    path('revisar/questionario_id=<questionario_id>', views.revisar_respostas, name='revisar_respostas'),
    path('verificar_respostas/questionario_id=<questionario_id>', views.verificar_respostas, name='verificar_respostas'),
    path('avaliar/questionario_id=<questionario_id>&aluno_id=<aluno_id>', views.avaliar_respostas, name='avaliar_respostas'),
    path('editar_avaliacao/questionario_id=<questionario_id>&aluno_id=<aluno_id>', views.editar_avalicao, name='editar_avaliacao'),
]