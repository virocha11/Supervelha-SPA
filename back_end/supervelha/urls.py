from django.contrib import admin
from django.urls import path, include
from . import views
import debug_toolbar

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_validate, name='login'),
    path('logout/', views.logout_validate, name='logout'),
    path('redirect/', views.redirect_group, name='redirect'),
    path('inicio/professor/', views.home_professor, name='inicio_professor'),
    path('inicio/aluno/', views.home_aluno, name='inicio_aluno'),
    path('cadastro/', include('cadastro.urls')),
    path('turma/', include('turma.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    # path('conta/', include('django.contrib.auth.urls')),
]