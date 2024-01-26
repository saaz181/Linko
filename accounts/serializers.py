from djoser.serializers import UserSerializer, UserCreateSerializer
from .models import User, Address
from rest_framework import serializers


class UserCreate(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['email', 'username', 'password', 're_password', 'phone_number', ]


class CurrentUser(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user_addr', ]


