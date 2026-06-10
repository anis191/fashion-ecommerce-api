from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from core.serializers import EmptySerializer
from .serializers import AddressSerializer
from .models import Address
from rest_framework.decorators import action
from rest_framework.response import Response
 
class AddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user = self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def get_serializer_context(self):
        return {'user' : self.request.user}
    
    @action(detail=True, methods=["post"])
    def set_default(self, request, pk=None):
        address = self.get_object()
        address.is_default = True
        address.save()
        return Response(
            AddressSerializer(address, context={"request": request}).data
        )
    
    def get_serializer_class(self):
        if self.action == 'set_default':
            return EmptySerializer
        return AddressSerializer
