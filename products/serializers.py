from rest_framework import serializers
from core.serializers import BaseModelSerializer
from catalog.serializers import AttributeValueSerializer
from .models import *

class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]

class ProductListSerializer(BaseModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    price_range = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id","name","slug","short_description","base_price","price_range","category","brand","gender","status","is_featured","is_new_arrival","primary_image","tags","created_at",]
    
    def get_primary_image(self, obj: Product) -> str | None:
        request = self.context.get("request")
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return request.build_absolute_uri(primary.image.url)
        return None
    
    def get_price_range(self, obj: Product) -> dict:
        all_prices = []
        all_variants = obj.variants.filter(is_active=True)
        for variant in all_variants:
            all_prices.append(variant.effective_price)
        
        if not all_prices:
            return {"min": obj.base_price, "max": obj.base_price}
        return {"min": min(all_prices), "max": max(all_prices)}

class ProductImageSerializer(BaseModelSerializer):
    variant = serializers.PrimaryKeyRelatedField(
        queryset = ProductVariant.objects.none(),
        write_only=True,
    )

    class Meta:
        model = ProductImage
        fields = ["id","image","alt_text","is_primary","sort_order","variant",]
        read_only_fields = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        product_id = self.context.get("product_id")
        if product_id:
            self.fields["variant"].queryset = ProductVariant.objects.filter(
                product_id = product_id
            )
        
class ProductVariantSerializer(BaseModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    attribute_values = AttributeValueSerializer(many=True,read_only=True)
    attribute_values_ids = serializers.PrimaryKeyRelatedField(
        queryset = AttributeValue.objects.all(),
        source="attribute_values",
        write_only=True,
        many=True,
    )
    low_stock_threshold = serializers.IntegerField(write_only=True)
    class Meta:
        model = ProductVariant
        fields = ["id","name","sku","price","compare_at_price","effective_price","stock","is_in_stock","low_stock_threshold","is_low_stock","weight","attribute_values","attribute_values_ids","images","is_active","created_at","updated_at",]

class ProductDetailSerializer(BaseModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    # variants = ProductVariantReadSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id","name","slug","description","short_description","base_price","category","brand","gender","status","material","care_instructions","is_featured","is_new_arrival","meta_title","meta_description","tags","images","created_at","updated_at",]
        # average_rating,review_count

class ProductWriteSerializer(BaseModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    brand = serializers.CharField(source="brand.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source="category",
        write_only=True,
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset = Brand.objects.all(),
        source="brand",
        write_only=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset = Tag.objects.all(),
        many=True,
        source="tags",
        write_only=True,
        allow_null=True,
        required=False,
    )
    class Meta:
        model = Product
        fields = ["id",
            "name",
            "slug",
            "description",
            "short_description",
            "base_price",
            # write-only
            "category_id",
            "brand_id",
            "tag_ids",
            # read-only
            "category",
            "brand",
            "tags",
            "gender",
            "status",
            "material",
            "care_instructions",
            "is_featured",
            "is_new_arrival",
            "meta_title",
            "meta_description",
            "created_at",
            "updated_at",]
        read_only_fields = ["id", "slug","created_at","updated_at"]
