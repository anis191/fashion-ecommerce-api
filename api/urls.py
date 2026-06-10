from django.urls import path,include
from rest_framework_nested import routers
from users.views import *
from catalog.views import *
from products.views import *

router = routers.DefaultRouter()
router.register('addresses', AddressViewSet, basename="address")
router.register('categories', CategoryViewSet, basename="category")
router.register('brands', BrandViewSet, basename="brand")
router.register('attributes', AttributeViewSet, basename="attribute")
router.register('tags', TagViewSet, basename="tag")

attribute_router = routers.NestedDefaultRouter(
    router,
    'attributes',
    lookup = 'attribute'
)
attribute_router.register('values', AttributeValueViewSet, basename="value")

urlpatterns = [
    path('',include(router.urls)),
    path('',include(attribute_router.urls)),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]