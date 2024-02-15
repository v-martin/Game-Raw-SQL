from rest_framework import serializers
from .models import CountrySchema, Country, Army, War, TradingHub, TradeRelation, MaterialType, MaterialCost, \
    ConstructionType, Construction, Material


class CountrySchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountrySchema
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    schema = CountrySchemaSerializer(read_only=True)

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
    hub = TradingHubSerializer(read_only=True)

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
    construction_type = ConstructionTypeSerializer(read_only=True)

    class Meta:
        model = Construction
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    material_type = MaterialTypeSerializer(read_only=True)

    class Meta:
        model = Material
        fields = '__all__'


class CountryDetailSerializer(serializers.ModelSerializer):
    army = ArmySerializer(read_only=True)
    constructions = ConstructionSerializer(many=True, read_only=True)
    trade_relations = TradeRelationSerializer(many=True, read_only=True)
    hubs = TradingHubSerializer(many=True, read_only=True)
    schema = CountrySchemaSerializer(read_only=True)
    materials = MaterialSerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = ['id', 'schema', 'token', 'gold', 'active', 'army', 'constructions', 'trade_relations', 'hubs',
                  'materials']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        trading_relations = TradeRelation.objects.filter(country=instance)
        hub_ids = trading_relations.values_list('hub__id', flat=True)
        hubs = TradingHub.objects.filter(pk__in=hub_ids)
        materials = Material.objects.filter(country=instance)
        constructions = Construction.objects.filter(country=instance)


        data['hubs'] = TradingHubWithCostsSerializer(hubs, many=True).data
        data['materials'] = MaterialSerializer(materials, many=True).data
        data['constructions'] = ConstructionSerializer(constructions, many=True).data
        return data


class TradingHubWithCostsSerializer(serializers.ModelSerializer):
    costs = MaterialCostSerializer(read_only=True, many=True)

    class Meta:
        model = TradingHub
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        costs = MaterialCost.objects.filter(hub=instance)

        data['costs'] = MaterialCostSerializer(costs, many=True).data
        return data
