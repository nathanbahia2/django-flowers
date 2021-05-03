from django.shortcuts import render, redirect

from core.models import Captura
from core import utils


def index(request):
    if request.method == "POST":
        foto = request.FILES.get('foto')
        planta = utils.identify_plant(foto)
        captura = Captura.objects.create(json=planta)                 
        return redirect('detail', captura.pk)
    return render(request, 'core/index.html')


def detail(request, pk):
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

        if probabilidade >= 50:
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

    print(info)

    return render(request, 'core/detail.html', context)
