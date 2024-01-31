from django.urls import path
from .views import *

urlpatterns = [
    path('start', CreateGameView.as_view(), name='start'),
    path('country', CountryDetailsByTokenView.as_view(), name='details'),
    path('country/war', CountryWarView.as_view(), name='country_war'),
    path('country/sell-material', CountrySellMaterialView.as_view(), name='country_sell_material'),
    path('country/construction/upgrade/<int:construction_id>', ConstructionUpgradeView.as_view(),
         name='construction_upgrade'),
    path('country/construction/buy', ConstructionBuyView.as_view(), name='construction_buy'),
    path('country/army/buy', ArmyBuyView.as_view(), name='army_buy'),
    path('county/army/upgrade/<int:army_id>', ArmyUpgradeView.as_view(), name='army_upgrade'),

]
