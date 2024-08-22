from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('cadastro/', include('cadastro.urls')),
    path('conta/', include('django.contrib.auth.urls')),
    path('turma/', include('turma.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]