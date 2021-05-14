import base64
import requests

from django.conf import settings

from core.models import Captura


def encode_file(file):
    file_encoded = base64.b64encode(file.read()).decode("ascii")
    return file_encoded


def identify_plant(file):
    image = [encode_file(file)]

    params = {
        "api_key": settings.API_KEY,
        "images": image,
        "modifiers": ["crops_fast", "similar_images"],
        "plant_language": "pt",
        "plant_details": ["common_names", "taxonomy", "url"]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post("https://api.plant.id/v2/identify", json=params, headers=headers)

    return response.json()


def get_detalhe_captura(captura):
    data = eval(captura.json)
    url_imagem = data.get('images')[0].get('url')
    sugestoes = data.get('suggestions', {})
    info = list()

    for sugestao in sugestoes:
        probabilidade = float(sugestao.get('probability', 0)) * 100
        nomes_comuns = sugestao.get('plant_details', {}).get('common_names')
        if nomes_comuns:
            nomes_comuns = ', '.join(nomes_comuns)

        if probabilidade >= 30:
            d = {
                'nome': sugestao.get('plant_name', 'Não identificado'),
                'probabilidade': probabilidade,
                'nomes_comuns': nomes_comuns,
                'wiki': sugestao.get('plant_details', {}).get('url'),
                'imagens': []
            }
            for imagem in sugestao.get('similar_images', {}):
                d['imagens'].append(imagem.get('url'))
            info.append(d)
    return info, url_imagem


def get_lista_capturas_usuario(usuario):
    capturas = list()
    query = Captura.objects.filter(usuario=usuario)
    for q in query:
        capturas.append({
            'pk': q.pk,
            'data': q.data.strftime('%d/%m/%Y %H:%M'),
            'nome': eval(q.json).get('suggestions', [{'plant_name', 'Não identificado'}])[0].get('plant_name'),
            'url': eval(q.json).get('images')[0].get('url')
        })
    return capturas
