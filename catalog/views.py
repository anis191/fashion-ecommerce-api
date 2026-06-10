from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .filters import AdminOnlyFilterBackend

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    lookup_field = "slug"
    pagination_class = None

    @action(detail=False, methods=["get"])
    def tree(self, request):
        roots = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(roots, many=True)
        return Response(serializer.data)

class BrandViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    pagination_class = None
    filter_backends = [AdminOnlyFilterBackend, SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Brand.objects.all()
        return Brand.objects.filter(is_active=True)

class AttributeViewSet(ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

class AttributeValueViewSet(ModelViewSet):
    serializer_class = AttributeValueSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(attribute_id = self.kwargs.get("attribute_pk"))

    def get_queryset(self):
        return AttributeValue.objects.filter(
            attribute_id = self.kwargs.get("attribute_pk")
        )
    
    def get_serializer_context(self):
        return {"attribute_id" : self.kwargs.get("attribute_pk")}
