from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer 

# Create your views here.
class GreetingViewSet(ViewSet):
    
    @extend_schema(
        summary="Say Hello",
        description="Returns a simple hello world message.",
        responses={200:str}
    )
    @action(detail=False, methods=['get'], url_path='hello')
    def hello(self,  request):
        return Response("Hello, world!")