from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSets

router_user = DefaultRouter()
router_user.register("users", CustomUserViewSets)

urlpatterns = [
    path('', include(router_user.urls)),
    path(r'auth/', include('djoser.urls.authtoken'))
]
