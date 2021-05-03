from django.db import models


class Captura(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    json = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
