from django.db import models
from django.contrib.auth.models import User


class Captura(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    json = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
