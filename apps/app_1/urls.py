from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import GreetingViewSet

router = DefaultRouter()
router.register(r'', GreetingViewSet, basename='greet')

urlpatterns = [
    path('greet/', include(router.urls)),
]