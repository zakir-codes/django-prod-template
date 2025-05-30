from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer

# Import your serializers
from .serializers import NumberInputSerializer, ResultOutputSerializer

class CalculatorViewSet(ViewSet):
    @extend_schema(
        summary="Add two numbers",
        description="Returns the sum of two numbers.",
        request=NumberInputSerializer,
        responses={200: ResultOutputSerializer},
        examples=[
            OpenApiExample(
                'Addition Example',
                summary='Example for adding two numbers',
                description='Demonstrates adding 5 and 3 to get 8',
                value={'num1': 5, 'num2': 3},
                request_only=True
            )
        ]
    )
    @action(detail=False, methods=['post'], url_path='add')
    def add(self, request):
        serializer = NumberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        num1 = serializer.validated_data['num1']
        num2 = serializer.validated_data['num2']
        result = num1 + num2
        return Response({'result': result}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Subtract two numbers",
        description="Returns the difference of two numbers (num1 - num2).",
        request=NumberInputSerializer,
        responses={200: ResultOutputSerializer},
        examples=[
            OpenApiExample(
                'Subtraction Example',
                summary='Example for subtracting two numbers',
                description='Demonstrates subtracting 3 from 5 to get 2',
                value={'num1': 5, 'num2': 3},
                request_only=True
            )
        ]
    )
    @action(detail=False, methods=['post'], url_path='subtract')
    def subtract(self, request):
        serializer = NumberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        num1 = serializer.validated_data['num1']
        num2 = serializer.validated_data['num2']
        result = num1 - num2
        return Response({'result': result}, status=status.HTTP_200_OK)