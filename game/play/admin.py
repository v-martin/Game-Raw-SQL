from django.contrib import admin
from .models import Country, Army, War, TradingHub, TradeRelation, MaterialType, MaterialCost, ConstructionType, Construction, Material, CountrySchema

admin.site.register(Country)
admin.site.register(Army)
admin.site.register(War)
admin.site.register(TradingHub)
admin.site.register(TradeRelation)
admin.site.register(MaterialType)
admin.site.register(MaterialCost)
admin.site.register(ConstructionType)
admin.site.register(Construction)
admin.site.register(Material)
admin.site.register(CountrySchema)
