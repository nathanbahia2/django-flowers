from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.models import Captura
from core import utils


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            foto = request.FILES.get('foto')
            planta = utils.identify_plant(foto)
            captura = Captura.objects.create(json=planta, usuario=request.user)
            return redirect('detalhes', captura.pk)
    return render(request, 'core/index.html')


@login_required
def detail(request, pk):
    if request.user.is_anonymous:
        return redirect('google_login')

    captura = Captura.objects.get(pk=pk)
    informacoes, url_imagem = utils.get_detalhe_captura(captura)
    context = {'url_imagem': url_imagem, 'info': informacoes, 'captura': captura}
    return render(request, 'core/detail.html', context)


@login_required
def capturas_usuario(request):
    if request.user.is_anonymous:
        return redirect('google_login')
    capturas = utils.get_lista_capturas_usuario(request.user)
    context = {'capturas': capturas}
    return render(request, 'core/capturas.html', context)


@login_required
def logout(request):
    if request.user.is_anonymous:
        return redirect('google_login')
    return render(request, 'core/logout.html')
