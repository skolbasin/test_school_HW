from django.urls import path
from .views import SuperheroCreateView, SuperheroListView

urlpatterns = [
    path('hero/', SuperheroCreateView.as_view(), name='hero-create'),
    path('hero/list/', SuperheroListView.as_view(), name='hero-list'),
]