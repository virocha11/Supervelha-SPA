from django.urls import path
from . import views

urlpatterns = [
    path('adicionar_aluno/', views.adicionar_aluno, name='adicionar_aluno'),
    path('remover_aluno/', views.remover_aluno, name='remover_aluno'),
]