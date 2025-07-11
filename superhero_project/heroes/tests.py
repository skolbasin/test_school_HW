import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from superheroes.models import Superhero


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_hero():
    def _create_hero(name, intelligence=100, strength=100, speed=100, power=100):
        return Superhero.objects.create(
            name=name,
            intelligence=intelligence,
            strength=strength,
            speed=speed,
            power=power
        )

    return _create_hero


@pytest.mark.django_db
def test_create_hero_success(client, mocker):
    # Mock the external API call
    mock_data = {
        'name': 'Batman',
        'intelligence': 100,
        'strength': 26,
        'speed': 27,
        'power': 47
    }
    mocker.patch(
        'superheroes.utils.fetch_superhero_data',
        return_value=mock_data
    )

    url = reverse('hero-create')
    data = {'name': 'Batman'}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Superhero.objects.count() == 1
    assert Superhero.objects.get().name == 'Batman'


@pytest.mark.django_db
def test_create_hero_missing_name(client):
    url = reverse('hero-create')
    response = client.post(url, {}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data
    assert response.data['error'] == 'Name parameter is required'


@pytest.mark.django_db
def test_create_hero_not_found(client, mocker):
    mocker.patch(
        'superheroes.utils.fetch_superhero_data',
        return_value=None
    )

    url = reverse('hero-create')
    data = {'name': 'UnknownHero'}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'error' in response.data
    assert response.data['error'] == 'Superhero not found in external API'


@pytest.mark.django_db
def test_list_heroes_empty(client):
    url = reverse('hero-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'error' in response.data
    assert response.data['error'] == 'No superheroes found with these filters'


@pytest.mark.django_db
def test_list_heroes_name_filter(client, create_hero):
    create_hero(name='Batman')
    create_hero(name='Superman')

    url = reverse('hero-list')
    response = client.get(url, {'name': 'Batman'})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Batman'


@pytest.mark.django_db
def test_list_heroes_numeric_filters(client, create_hero):
    create_hero(name='WeakHero', intelligence=50, strength=50, speed=50, power=50)
    create_hero(name='StrongHero', intelligence=90, strength=90, speed=90, power=90)

    # Test exact match
    url = reverse('hero-list')
    response = client.get(url, {'intelligence': '90'})
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'StrongHero'

    # Test gte
    response = client.get(url, {'strength': 'gte:80'})
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'StrongHero'

    # Test lte
    response = client.get(url, {'speed': 'lte:60'})
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'WeakHero'

    # Combined filters
    response = client.get(url, {
        'power': 'gte:40',
        'power': 'lte:60'
    })
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'WeakHero'