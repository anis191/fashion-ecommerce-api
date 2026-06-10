from rest_framework import serializers
from .models import *
from core.serializers import BaseModelSerializer

class CategoryMinimalSerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]

class CategorySerializer(BaseModelSerializer):
    parent = CategoryMinimalSerializer(read_only=True)
    children = CategoryMinimalSerializer(many=True,read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source="parent",
        write_only=True,
        allow_null=True,
        required=False,
    )
    class Meta:
        model = Category
        fields = ["id","name","slug","description","image","is_active","sort_order","full_path","parent","parent_id","children","created_at","updated_at"]
        read_only_fields = ["id", "slug", "created_at", "updated_at","full_path"]
    
class BrandSerializer(BaseModelSerializer):
    class Meta:
        model = Brand
        fields = ["id","name","slug","logo","description","website","is_active","created_at","updated_at",]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

class AttributeValueSerializer(BaseModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ["id", "value", "display_value", "sort_order"]
        read_only_fields = ["id"]
    
    # For create and update(put/patch) both time this will be checked:
    def validate_value(self, value):
        attribute_id = self.context.get("attribute_id")

        if AttributeValue.objects.filter(
            attribute_id = attribute_id,
            value = value
        ).exists():
            raise serializers.ValidationError(
                "This value already exists for this attribute."
            )
        return value

class AttributeSerializer(BaseModelSerializer):
    # values = AttributeValueSerializer(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ["id", "name", "display_type"]
        read_only_fields = ["id"]

"""
class AttributeWriteSerializer(BaseModelSerializer):
    values = AttributeValueSerializer(many=True, required=False)
    class Meta:
        model = Attribute
        fields = ["id", "name", "display_type","values"]
        read_only_fields = ["id"]
    
    def create(self, validated_data: dict) -> Attribute:
        values_data = validated_data.pop("values", [])
        attribute = Attribute.objects.create(**validated_data)
        
        attribute_values = [
            AttributeValue(
                attribute = attribute,
                value = values.get("value"),
                display_value = values.get("display_value", ""),
                sort_order = values.get("sort_order", 0),
            )
            for values in values_data
        ]
        AttributeValue.objects.bulk_create(attribute_values)

        return attribute
"""

