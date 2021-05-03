from django.urls import path

from core.views import index, detail


urlpatterns = [
    path('', index, name='index'),
    path('detalhes/<int:pk>', detail, name='detail'),
]
