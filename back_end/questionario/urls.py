from django.urls import path
from . import views

urlpatterns = [
    path('turma_id=<codigo_turma>', views.visualizar_questionarios, name='questionarios'),
    path('adicionar/turma_id=<codigo_turma>', views.criar_questionario, name='criar_questionario'),
    path('visualizar/questionario_id=<questionario_id>', views.visualizar_questionario, name='visualizar_questionario'),
    path('editar/questionario_id=<questionario_id>', views.editar_questionario, name='editar_questionario'),
]