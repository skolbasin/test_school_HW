import requests
from django.conf import settings


def fetch_superhero_data(name):
    api_token = settings.SUPERHERO_API_TOKEN
    base_url = f"https://superheroapi.com/api/{api_token}"

    # First search by name to get the ID
    search_url = f"{base_url}/search/{name}"
    response = requests.get(search_url)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get('response') == 'error' or not data.get('results'):
        return None

    # Get the first matching hero
    hero_id = data['results'][0]['id']

    # Get powerstats
    powerstats_url = f"{base_url}/{hero_id}/powerstats"
    powerstats_response = requests.get(powerstats_url)

    if powerstats_response.status_code != 200:
        return None

    powerstats = powerstats_response.json()

    if powerstats.get('response') == 'error':
        return None

    return {
        'name': name,
        'intelligence': int(powerstats.get('intelligence', 0)),
        'strength': int(powerstats.get('strength', 0)),
        'speed': int(powerstats.get('speed', 0)),
        'power': int(powerstats.get('power', 0))
    }