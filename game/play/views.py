from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connections, transaction

from .models import Country, War, Construction, Army, ConstructionType
from .serializers import CountryDetailSerializer


class CountryDetailsByTokenView(ListAPIView):
    serializer_class = CountryDetailSerializer

    def get_queryset(self):
        user_token = self.request.auth
        return Country.objects.filter(token=user_token)


class CreateGameView(APIView):

    @transaction.atomic
    def post(self, request):
        with connections['default'].cursor() as cursor:
            cursor.execute(f"CALL createBotCountries('{request.headers.get('Authorization').split()[-1]}')")
            cursor.execute(f"SELECT createUserCountry('{request.headers.get('Authorization').split()[-1]}', '{request.data.get('countryName')}', '{request.data.get('countryKing')}')")

        return Response({'message': 'Game started successfully'}, status=status.HTTP_200_OK)


class CountryWarView(APIView):
    def post(self, request, *args, **kwargs):
        client_country_id = request.data.get('clientCountryId')
        enemy_country_id = request.data.get('enemyCountryId')

        client = Country.objects.get(pk=client_country_id)
        enemy = Country.objects.get(pk=enemy_country_id)

        with connections['default'].cursor() as cursor:
            cursor.execute(f"SELECT chooseWarWinner({client_country_id}, {enemy_country_id})")
            result = cursor.fetchone()
            if result == client_country_id:
                War.objects.create(loser=enemy, winner=client)
            else:
                War.objects.create(loser=client, winner=enemy)

        return Response({'message': 'War initiated successfully'}, status=status.HTTP_201_CREATED)


class CountrySellMaterialView(APIView):
    def post(self, request, *args, **kwargs):
        country_id = request.data.get('countryId')
        hub_id = request.data.get('hubId')
        material_id = request.data.get('materialId')
        size = request.data.get('size')

        with connections['default'].cursor() as cursor:
            cursor.execute(f'SELECT sellMaterial({material_id}, {size}, {country_id}, {hub_id})')

        return Response({'message': 'Material sold successfully'}, status=status.HTTP_200_OK)


class ConstructionUpgradeView(APIView):
    def post(self, request, construction_id, *args, **kwargs):
        with connections['default'].cursor() as cursor:
            cursor.execute(f'SELECT increaseConstructionLevel({request.data.get(construction_id)}, 500)')

        return Response({'message': 'Construction upgraded successfully'}, status=status.HTTP_200_OK)


class ConstructionBuyView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        country_id = request.data.get('countryId')
        type_id = request.data.get('typeId')

        country = Country.objects.get(pk=country_id)

        Construction.objects.create(level=1, constructions_type=ConstructionType.objects.get(pk=type_id),
                                    country=country)

        country.gold -= 500
        country.save()

        return Response({'message': 'Construction purchased successfully'}, status=status.HTTP_200_OK)


class ArmyBuyView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        country_id = request.data.get('countryId')
        count = request.data.get('count')

        country = Country.objects.get(pk=country_id)
        army = Army.objects.get(country=country)

        army.size += count
        army.save()

        country.gold -= (500 * count)
        country.save()

        return Response({'message': 'Army purchased successfully'}, status=status.HTTP_200_OK)


class ArmyUpgradeView(APIView):
    def post(self, request, army_id, *args, **kwargs):
        army = Army.objects.get(pk=army_id)

        with connections['default'].cursor() as cursor:
            cursor.execute(f'SELECT increaseArmyLevel({army_id}, 500)')

        return Response({'message': 'Army purchased successfully'}, status=status.HTTP_200_OK)
