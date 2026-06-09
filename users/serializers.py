from rest_framework import serializers
from core.serializers import BaseModelSerializer
from .models import Address
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = BaseUserCreateSerializer.Meta.model
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
        )

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = BaseUserSerializer.Meta.model
        ref_name = 'CustomUser'
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_staff',
        )
        read_only_fields = ('is_staff',)

class AddressSerializer(BaseModelSerializer):
    class Meta:
        model = Address
        fields = ["id","address_type","full_name","phone_number","street_address","apartment","city","state","postal_code","country","is_default","created_at","updated_at",]
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def validate(self, attrs):
        user = self.context.get("user")
        if user and self.instance is None:
            count = Address.objects.filter(user = user).count()
            if count >= 5:
                raise serializers.ValidationError(
                    "You cannot save more than 5 addresses."
                )
        return attrs
    
