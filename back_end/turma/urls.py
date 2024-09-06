from django.urls import path
from . import views

urlpatterns = [
    path('', views.minhas_turmas, name='minhas_turmas'),
    path('visualizar/turma_id=<codigo_turma>', views.visualizar_turma, name='visualizar_turma'),
    path('editar/detalhes/turma_id=<codigo_turma>', views.editar_detalhes_turma , name='editar_detalhes_turma'),
    path('adicionar_aluno/turma_id=<codigo_turma>', views.adicionar_aluno, name='adicionar_aluno'),
    path('remover_aluno/turma_id=<codigo_turma>/user_id=<user_aluno>', views.remover_aluno, name='remover_aluno'),
]