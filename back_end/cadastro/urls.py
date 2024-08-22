from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/aluno', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor', views.cadastro_professor, name='cadastro_professor'),
    path('cadastro/aluno/successo', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('cadastro/professor/sucesso', views.cadastrar_professor, name='cadastrar_professor'),
]