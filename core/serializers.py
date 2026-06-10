from rest_framework import serializers

class EmptySerializer(serializers.Serializer):
    pass

class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
