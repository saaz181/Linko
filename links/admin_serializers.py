from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class CryptoSerializer(ModelSerializer):
    class Meta:
        model = CryptoWalletAddress
        fields = '__all__'