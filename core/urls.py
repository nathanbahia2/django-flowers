from django.urls import path

from core.views import index, detail, capturas_usuario


urlpatterns = [
    path('', index, name='index'),
    path('detalhes/<int:pk>', detail, name='detalhes'),
    path('capturas_usuario', capturas_usuario, name='capturas_usuario'),
]
