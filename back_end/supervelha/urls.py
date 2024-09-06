from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_validate, name='login'),
    path('logout/', views.logout_validate, name='logout'),
    path('redirect/', views.redirect_group, name='redirect'),
    path('inicio/professor/', views.home_professor, name='inicio_professor'),
    path('inicio/aluno/', views.home_aluno, name='inicio_aluno'),
    path('perfil/', views.perfil, name='perfil'),
    path('cadastro/', include('cadastro.urls')),
    path('turma/', include('turma.urls')),
    path('questionario/', include('questionario.urls')),
    path('admin/', admin.site.urls),
]