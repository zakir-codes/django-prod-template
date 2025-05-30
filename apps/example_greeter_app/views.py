# views.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema

class GreetingViewSet(ViewSet):

    @extend_schema(
        summary="Say Hello",
        description="Returns a simple hello world message.",
        responses={200: str}
    )
    @action(detail=False, methods=['get'], url_path='hello')
    def hello(self, request):
        return Response("Hello, world!")

    @extend_schema(
        summary="Say Goodbye",
        description="Returns a simple goodbye message.",
        responses={200: str}
    )
    @action(detail=False, methods=['get'], url_path='bye')
    def bye(self, request):
        return Response("Goodbye for now!")