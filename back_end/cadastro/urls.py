from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('professor/', views.cadastro_professor, name='cadastro_professor'),
    path('turma/', views.cadastrar_turma, name='cadastrar_turma'),
    path('excluir_usuario/', views.excluir_usuario, name='excluir_usuario'),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario'),
]