import requests
from django.conf import settings
from .exceptions import SuperheroNotFoundError

class SuperheroAPIService:
    @staticmethod
    def get_hero_data(name):
        url = f"{settings.SUPERHERO_API_URL}{settings.SUPERHERO_API_TOKEN}/search/{name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise SuperheroNotFoundError("Failed to fetch superhero data")

        data = response.json()

        if data.get('response') == 'error' or not data.get('results'):
            raise SuperheroNotFoundError(f"Superhero {name} not found")

        hero_id = data['results'][0]['id']
        powerstats_url = f"{settings.SUPERHERO_API_URL}{settings.SUPERHERO_API_TOKEN}/{hero_id}/powerstats"
        powerstats_response = requests.get(powerstats_url)

        if powerstats_response.status_code != 200:
            raise SuperheroNotFoundError("Failed to fetch superhero powerstats")

        powerstats = powerstats_response.json()

        if powerstats.get('response') == 'error':
            raise SuperheroNotFoundError("Invalid superhero powerstats data")

        return {
            'name': name,
            'intelligence': int(powerstats.get('intelligence', 0)),
            'strength': int(powerstats.get('strength', 0)),
            'speed': int(powerstats.get('speed', 0)),
            'power': int(powerstats.get('power', 0))
        }