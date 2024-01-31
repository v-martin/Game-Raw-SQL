from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.authtoken.models import Token

from game.play.models import Country


def get_content(user: User) -> dict:
    token = get_token_by_user(user)
    data = {'token': token}
    data['countries'] = get_countries_by_token(token)

    return data


def get_token_by_user(user: User) -> Token:
    return Token.objects.get(user=user)


def get_countries_by_token(token: Token) -> QuerySet:
    return Country.objects.filter(token=token).all()






