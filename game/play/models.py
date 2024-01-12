from django.db import models


class Users(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255)


class Session(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(null=True)
    winner_country = models.IntegerField()
    user_country = models.IntegerField()


class CountryScheme(models.Model):
    name = models.CharField(max_length=50)
    king = models.CharField(max_length=100)


class Country(models.Model):
    scheme = models.ForeignKey(CountryScheme, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    gold = models.IntegerField()
    active = models.BooleanField()


class Army(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    size = models.IntegerField()
    level = models.IntegerField()


class War(models.Model):
    loser = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='wars_lost')
    winner = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='wars_won')


class TradingHub(models.Model):
    location = models.CharField(max_length=100, unique=True)


class TradeRelation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hub = models.ForeignKey(TradingHub, on_delete=models.CASCADE)


class MaterialType(models.Model):
    name = models.CharField(max_length=50, unique=True)


class MaterialCost(models.Model):
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    hub = models.ForeignKey(TradingHub, on_delete=models.CASCADE)
    cost = models.IntegerField()


class ConstructionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)


class Construction(models.Model):
    level = models.IntegerField()
    construction_type = models.ForeignKey(ConstructionType, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Material(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    amount = models.IntegerField()
