from django_filters.rest_framework import FilterSet
from .models import *
from django_filters.rest_framework import DjangoFilterBackend

class BrandFilter(FilterSet):
    class Meta:
        model = Brand
        fields = {
            'is_active' : ['exact'],
        }

class AdminOnlyFilterBackend(DjangoFilterBackend):
    def get_filterset_class(self, view, queryset = None):
        request = view.request

        if request.user.is_staff:
            return BrandFilter
        return None