from typing import TypeVar

from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)

        token['email'] = user.email

        return token
