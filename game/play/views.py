from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connections, transaction

from .models import Country, War, Construction, Army, ConstructionType, Material, BASE_MATERIAL_AMOUNT
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
            cursor.execute(
                f"SELECT createUserCountry('{request.headers.get('Authorization').split()[-1]}', '{request.data.get('countryName')}', '{request.data.get('countryKing')}')")

        return Response({'detail': 'Game started successfully'}, status=status.HTTP_200_OK)


class CountryWarView(APIView):
    def post(self, request, *args, **kwargs):
        client_country_id = request.data.get('clientCountryId')
        enemy_country_id = request.data.get('enemyCountryId')
        winner = 0
        client = Country.objects.get(pk=client_country_id)
        enemy = Country.objects.get(pk=enemy_country_id)

        with connections['default'].cursor() as cursor:
            cursor.execute(f"SELECT chooseWarWinner({client_country_id}, {enemy_country_id})")
            result = cursor.fetchone()[0]
            if result == client_country_id:
                winner = client_country_id
            else:
                winner = enemy_country_id

        return Response({'winner': winner}, status=status.HTTP_201_CREATED)


class CountrySellMaterialView(APIView):
    def post(self, request, *args, **kwargs):
        country_id = request.data.get('countryId')
        hub_id = request.data.get('hubId')
        materials = request.data.get('materials')

        with connections['default'].cursor() as cursor:
            for material in materials:
                if material['amount'] > 0:
                    cursor.execute(
                        f'SELECT sellMaterial({material["id"]}, {material["amount"]}, {country_id}, {hub_id})')

        return Response({'detail': 'Material sold successfully'}, status=status.HTTP_200_OK)


class ConstructionUpgradeView(APIView):
    def post(self, request, construction_id, *args, **kwargs):
        with connections['default'].cursor() as cursor:
            cursor.execute(f'SELECT increaseConstructionLevel({construction_id}, 500)')

        return Response({'detail': 'Construction upgraded successfully'}, status=status.HTTP_200_OK)


class ConstructionBuyView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        country_id = request.data.get('countryId')
        type_id = request.data.get('typeId')

        country = Country.objects.get(pk=country_id)

        Construction.objects.create(level=1, construction_type=ConstructionType.objects.get(pk=type_id),
                                    country=country)

        country.gold -= 500
        country.save()

        return Response({'detail': 'Construction purchased successfully'}, status=status.HTTP_200_OK)


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

        return Response({'detail': 'Army purchased successfully'}, status=status.HTTP_200_OK)


class ArmyUpgradeView(APIView):
    def post(self, request, army_id, *args, **kwargs):
        with connections['default'].cursor() as cursor:
            cursor.execute(f'SELECT increaseArmyLevel({army_id}, 500)')

        return Response({'detail': 'Army purchased successfully'}, status=status.HTTP_200_OK)


class BotArmyBuyView(APIView):
    def post(self, request):
        country_ids = request.data.get('countryIds')

        armies = Army.objects.filter(country_id__in=country_ids)

        for army in armies:
            army.size += 1
            army.save()

        return Response({'detail': 'Armies have been successfully bought'}, status=status.HTTP_200_OK)


class BotArmyUpgradeView(APIView):
    def post(self, request):
        country_ids = request.data.get('countryIds')

        armies = Army.objects.filter(country_id__in=country_ids)

        for army in armies:
            army.level += 1
            army.save()

        return Response({'detail': 'Armies have been successfully upgraded'}, status=status.HTTP_200_OK)


class GetResources(APIView):
    def post(self, request, *args, **kwargs):
        country_id = request.data.get('countryId')
        materials = Material.objects.filter(country=country_id).all()
        constructions = Construction.objects.filter(country=country_id).all()

        for material in materials:
            for construction in constructions:
                if material.material_type == construction.construction_type.material_type:
                    material.amount += BASE_MATERIAL_AMOUNT * construction.level
            material.save()

        return Response({'detail': 'Resources extracted successfully'}, status=status.HTTP_200_OK)
