
from apps.map.serializers import (MarkerListSerializer, MarkerCreateSerializer)
from apps.map.models import (Marker)
from config.settings.base import MEDIA_URL
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from decimal import Decimal

import numpy as np


class MarkerCreationAPIView(generics.CreateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerCreateSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        company_image = request.FILES.getlist("company_image")
        lon = Decimal(request.data.get("lon"))
        lat = Decimal(request.data.get("lat"))
        company_name = request.data.get("company_name")
        address = request.data.get("address")
        phone_number = request.data.get("phone_number")
        tags = request.data.get("tags")
        opening_hours = request.data.get("opening_hours")
        data = {
            "lon": lon,
            "lat": lat,
            "company_name": company_name,
            "address": address,
            "phone_number": phone_number,
            "tags": tags,
            "opening_hours": opening_hours,
            "created_by": request.user.id,
        }
        if company_image:
            data.update({"company_image": company_image[0]})
        serializer = MarkerCreateSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return Response(serializer.data)
    
class MarkerListAPIView(generics.ListAPIView):

    serializer_class = MarkerListSerializer

    def get_queryset(self):
        return Marker.objects.all()