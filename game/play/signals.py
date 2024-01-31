# import logging
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.db import transaction
# from rest_framework.authtoken.models import Token
#
# from .models import Country, Army, Material, TradeRelation, Construction, War, CountrySchema, MaterialType, \
#     ConstructionType, TradingHub
#
# logger = logging.getLogger(__name__)
#
#
# @receiver(post_save, sender=Token)
# @transaction.atomic
# def create_static(sender, instance, created, **kwargs):
#     """
#     Signal to create static objects when a token in created.
#     """
#     if created:
#         logging.info(f"Creating static objects for token: {instance}")
#
#         mapping = {'Камень': 'Каменоломня', 'Железо': 'Шахта', 'Древесина': 'Лесопилка', 'Зерно': 'Ферма'}
#         for name in ('Камень', 'Железо', 'Древесина', 'Зерно'):
#             material_type = MaterialType.objects.create(name=name)
#             ConstructionType.objects.create(name=mapping[name], material_type=material_type)
#         for name, king in (('bri', 'lou'), ('spi', 'poul'), ('rus', 'oleg'), ('sch', 'pav'), ('cri', 'lev'),
#                            ('fr', 'mri'), ('gre', 'kans'), ('intd', 'fall'), ('otv', 'bam'), ('cleare', 'strong')):
#             CountrySchema.objects.create(name=name, king=king)
#
#
# @receiver(post_save, sender=Token)
# @transaction.atomic
# def create_objects(sender, instance, created, **kwargs):
#     """
#     Signal to create objects associated when a token is created.
#     """
#     if created:
#         logging.info(f"Creating objects for token: {instance}")
#
#         for schema in CountrySchema.objects.all():
#             Country.objects.create(schema=schema, token=instance, gold=1000, active=True)
#
#
# @receiver(post_save, sender=Country)
# @transaction.atomic
# def create_sub_objects(sender, instance, created, **kwargs):
#     """
#     Signal to create associated objects when a new country is created.
#     """
#     if created:
#         logging.info(f"Creating sub-objects for country: {instance}")
#
#         Army.objects.create(country=instance, size=0, level=0)
#         for material_type in MaterialType.objects.all():
#             Material.objects.create(country=instance, material_type=material_type, amount=0)
#
#         for hub in TradingHub.objects.all():
#             TradeRelation.objects.create(country=instance, hub=hub)
#
#
# @receiver(post_delete, sender=War)
# def loser_army_func(sender, instance, **kwargs):
#     """
#     Signal to delete the army of the loser when a war occurs.
#     """
#     logging.info(f"Deleting army of the loser for war: {instance}")
#
#     Army.objects.filter(country_id=instance.country_id).delete()
#
#
# @receiver(post_save, sender=War)
# @transaction.atomic
# def winner_army_func(sender, instance, created, **kwargs):
#     """
#     Signal to update the size of the winner's army after a war.
#     """
#     if not created:
#         logging.info(f"Updating size of the winner's army for war: {instance}")
#
#         loser = Army.objects.filter(country_id=instance.loser).first()
#         if loser:
#             instance.size = (instance.size * instance.level - (loser.size * loser.level * 0.5)) / instance.level
#             instance.save()
#
#
# @receiver(post_save, sender=War)
# def change_construction_ownership(sender, instance, created, **kwargs):
#     """
#     Signal to update the ownership of a construction after a war.
#     """
#     if not created:
#         logging.info(f"Changing construction ownership for war: {instance}")
#
#         Construction.objects.filter(country_id=instance.loser).update(country_id=instance.winner)
#
#
# @receiver(post_save, sender=War)
# def deactivate_country(sender, instance, created, **kwargs):
#     """
#     Signal to deactivate a country after a war.
#     """
#     if not created:
#         logging.info(f"Deactivating country for war: {instance}")
#
#         Country.objects.filter(country_id=instance.loser).update(active=False)
#
#
# @receiver(post_save, sender=War)
# def change_trading_relations(sender, instance, created, **kwargs):
#     """
#     Signal to update trading relations after a war.
#     """
#     if not created:
#         logging.info(f"Changing trading relations for war: {instance}")
#
#         TradeRelation.objects.filter(country_id=instance.loser).update(country_id=instance.winner)
