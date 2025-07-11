from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Superhero
from .serializers import SuperheroSerializer
from .utils import fetch_superhero_data


class SuperheroCreateView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response(
                {"error": "Name parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if hero already exists
        if Superhero.objects.filter(name__iexact=name).exists():
            return Response(
                {"error": "Superhero with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch hero data from external API
        hero_data = fetch_superhero_data(name)
        if not hero_data:
            return Response(
                {"error": "Superhero not found in external API"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create new hero
        serializer = SuperheroSerializer(data=hero_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperheroListView(APIView):
    def get(self, request):
        params = request.query_params
        queryset = Superhero.objects.all()

        # Exact name match
        name = params.get('name')
        if name:
            queryset = queryset.filter(name__iexact=name)

        # Numeric filters (exact, gte, lte)
        numeric_fields = ['intelligence', 'strength', 'speed', 'power']
        for field in numeric_fields:
            value = params.get(field)
            if value:
                if value.startswith('gte:'):
                    try:
                        num = int(value[4:])
                        queryset = queryset.filter(**{f"{field}__gte": num})
                    except ValueError:
                        pass
                elif value.startswith('lte:'):
                    try:
                        num = int(value[4:])
                        queryset = queryset.filter(**{f"{field}__lte": num})
                    except ValueError:
                        pass
                else:
                    try:
                        num = int(value)
                        queryset = queryset.filter(**{field: num})
                    except ValueError:
                        pass

        if not queryset.exists():
            return Response(
                {"error": "No superheroes found with these filters"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SuperheroSerializer(queryset, many=True)
        return Response(serializer.data)