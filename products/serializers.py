from rest_framework import serializers
from core.serializers import BaseModelSerializer
from .models import *

class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]
