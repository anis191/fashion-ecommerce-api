from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, status
from .serializers import *
from core.permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter
from core.serializers import EmptySerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "slug"
    filter_backends = [SearchFilter]
    search_fields = ["name"]

class ProductViewSet(ModelViewSet):
    lookup_field = "slug"
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action in ("create", "update", "partial_update"):
            return ProductWriteSerializer
        if self.action == "images":
            return ProductImageSerializer
        return ProductDetailSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
    
        if self.action == "images":
            context["product_id"] = self.get_object().id
    
        return context

    @action(detail=True, methods=["get", "post"])
    def images(self, request, slug=None):
        product = self.get_object()

        if request.method == "GET":
            qs = product.images.all()
            serializer = ProductImageSerializer(
                qs, many=True
            )
            return Response(serializer.data)
        
        serializer = ProductImageSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductVariantViewSet(ModelViewSet):
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        return ProductVariant.objects.filter(product__slug = self.kwargs.get("product_slug"))
    
    def get_product(self):
        return get_object_or_404(
            Product,
            slug = self.kwargs.get("product_slug")
        )
    
    def perform_create(self, serializer):
        serializer.save(product = self.get_product())
