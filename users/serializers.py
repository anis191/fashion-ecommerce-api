from rest_framework import serializers
from core.serializers import BaseModelSerializer
from .models import Address

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
    
