from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GreetingViewSet

router = DefaultRouter()
router.register(r'', GreetingViewSet, basename='greet') # Your greeter endpoints will be at /greet/hello, /greet/bye etc.

urlpatterns = [
    path('', include(router.urls)), # This means 'greet/' will be appended to the path it's included at.
]