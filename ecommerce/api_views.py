from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ecommerce.serializers import *
from ecommerce.models import *

@api_view(['GET'])
def marketplace_api(request):
    try:
        marketplaces = MarketPlaces.objects.all()
        serializer = MarketPlaceSerializer(marketplaces, many=True)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        data = str(e)
        return Response({'data': data}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def supported_type_api(request):
    try:
        supported_type = SupportedTypes.objects.all()
        serializer = SupportedTypesSerializer(supported_type, many=True)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        data = str(e)
        return Response({'data': data}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def supported_type_note_api(request):
    try:
        notes = SupportedTypesNotes.objects.all().last()
        serializer = SupportedTypeNotesSerializer(notes, many=False)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        data = str(e)
        return Response({'data': data}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def adjusted_price_note_api(request):
    try:
        notes = AdjustedPriceNotes.objects.all().last()
        serializer = AdjustedPriceNotesSerializer(notes, many=False)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        data = str(e)
        return Response({'data': data}, status=status.HTTP_400_BAD_REQUEST)

