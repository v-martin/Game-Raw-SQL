from django.db import models


class CountrySchema(models.Model):
    name = models.CharField(max_length=50, unique=True)
    king = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    schema = models.ForeignKey(CountrySchema, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    gold = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return f'{self.schema.name} {str(self.token)[:5]}'


class Army(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    size = models.IntegerField()
    level = models.IntegerField()

    def __str__(self):
        return f'army of {str(self.country)}'


class War(models.Model):
    loser = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='wars_lost')
    winner = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='wars_won')

    def __str__(self):
        return f'{self.loser} lost to {self.winner}'


class TradingHub(models.Model):
    location = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.location


class TradeRelation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hub = models.ForeignKey(TradingHub, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hub.location} hub of {self.country}'


class MaterialType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MaterialCost(models.Model):
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    hub = models.ForeignKey(TradingHub, on_delete=models.CASCADE)
    cost = models.IntegerField()

    def __str__(self):
        return f'{self.material_type} cost in {self.hub}'


class ConstructionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Construction(models.Model):
    level = models.IntegerField()
    construction_type = models.ForeignKey(ConstructionType, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.construction_type} of {self.country}'


class Material(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.material_type} of {self.country}'
