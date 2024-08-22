from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('professor/', views.cadastro_professor, name='cadastro_professor'),
    path('turma/', views.cadastrar_turma, name='cadastrar_turma'),
]