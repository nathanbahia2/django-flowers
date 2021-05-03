import base64
import requests


def encode_file(file):
    file_encoded = base64.b64encode(file.read()).decode("ascii")
    return file_encoded


def identify_plant(file):
    image = [encode_file(file)]

    # see the docs for more optional attributes
    params = {
        "api_key": "ElF0gb6R7Nhxa743aLRk7ySapitGYed4RJEaWTmnfKwAtC8z90",
        "images": image,
        "modifiers": ["crops_fast", "similar_images"],
        "plant_language": "pt",
        "plant_details": ["common_names", "taxonomy", "url"]
        }

    headers = { "Content-Type": "application/json" }

    response = requests.post("https://api.plant.id/v2/identify", json=params,  headers=headers)

    return response.json()