from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_turma, name='cadastrar_turma'),
]