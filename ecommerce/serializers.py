from rest_framework import serializers
from ecommerce.models import *

class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlaces
        fields = '__all__'

class SupportedTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportedTypes
        fields = '__all__'

class SupportedTypeNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportedTypesNotes
        fields = '__all__'

class AdjustedPriceNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdjustedPriceNotes
        fields = '__all__'