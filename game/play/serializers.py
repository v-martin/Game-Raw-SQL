from rest_framework import serializers
from models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class CountrySchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryScheme
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ArmySerializer(serializers.ModelSerializer):
    class Meta:
        model = Army
        fields = '__all__'


class WarSerializer(serializers.ModelSerializer):
    class Meta:
        model = War
        fields = '__all__'


class TradingHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingHub
        fields = '__all__'


class TradeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeRelation
        fields = '__all__'


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = '__all__'


class MaterialCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCost
        fields = '__all__'


class ConstructionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionType
        fields = '__all__'


class ConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Construction
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
