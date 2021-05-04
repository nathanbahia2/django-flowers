from django.shortcuts import render, redirect

from core.models import Captura
from core import utils


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            foto = request.FILES.get('foto')
            planta = utils.identify_plant(foto)
            captura = Captura.objects.create(json=planta)
            return redirect('detail', captura.pk)
    return render(request, 'core/index.html')


def detail(request, pk):
    if request.user.is_anonymous:
        return redirect('google_login')

    captura = Captura.objects.get(pk=pk)
    data = eval(captura.json)
    url_imagem = data.get('images')[0].get('url')
    sugestoes = data.get('suggestions')
    info = list()

    for sugestao in sugestoes:
        probabilidade = float(sugestao.get('probability', 0)) * 100
        nomes_comuns = sugestao.get('plant_details').get('common_names')
        if nomes_comuns:
            nomes_comuns = ', '.join(nomes_comuns)

        if probabilidade >= 30:
            d = {
                'nome': sugestao.get('plant_name', 'Não identificado'),
                'probabilidade': probabilidade,
                'nomes_comuns': nomes_comuns,
                'wiki': sugestao.get('plant_details').get('url'),
                'imagens': []     
            }
            for imagem in sugestao.get('similar_images'):
                d['imagens'].append(imagem.get('url'))
            info.append(d)
    context = {
        'url_imagem': url_imagem,
        'info': info,
    }
    return render(request, 'core/detail.html', context)


def capturas_usuario(request):
    if request.user.is_anonymous:
        return redirect('google_login')

    usuario = request.user
    capturas = list()
    query = Captura.objects.filter(usuario=usuario)
    for q in query:
        capturas.append({
            'pk': q.pk,
            'url':  eval(q.json).get('images')[0].get('url')
        })
    context = {'capturas': capturas}
    return render(request, 'core/capturas.html', context)
