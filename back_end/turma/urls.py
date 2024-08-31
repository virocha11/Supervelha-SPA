from django.urls import path
from . import views

urlpatterns = [
    path('', views.minhas_turmas, name='minhas_turmas'),
    path('editar/<codigo_turma>', views.editar_turma , name='editar_turma'),
    path('editar/detalhes/<codigo_turma>', views.editar_detalhes_turma , name='editar_detalhes_turma'),
    path('adicionar_aluno/<codigo_turma>', views.adicionar_aluno, name='adicionar_aluno'),
    path('remover_aluno/<codigo_turma>/<user_aluno>', views.remover_aluno, name='remover_aluno'),
]