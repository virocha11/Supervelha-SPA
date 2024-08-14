from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(Questionario)
admin.site.register(Pergunta)
admin.site.register(Resposta)