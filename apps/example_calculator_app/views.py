import logging

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer

# Import your serializers
from .serializers import NumberInputSerializer, ResultOutputSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
        logger.info("Received request to add numbers.")
        serializer = NumberInputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            num1 = serializer.validated_data['num1']
            num2 = serializer.validated_data['num2']
            result = num1 + num2
            logger.info(f"Successfully added {num1} and {num2}. Result: {result}")
            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during addition: {e}", exc_info=True) # exc_info=True sends traceback to Sentry
            # Re-raise or return an appropriate error response
            # raise # Sentry will catch this unhandled exception
            return Response({'error': 'An error occurred during addition'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        logger.info("Received request to subtract numbers.")
        serializer = NumberInputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            num1 = serializer.validated_data['num1']
            num2 = serializer.validated_data['num2']
            result = num1 - num2
            logger.info(f"Successfully subtracted {num2} from {num1}. Result: {result}")
            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during subtraction: {e}", exc_info=True)
            # raise # Sentry will catch this unhandled exception
            return Response({'error': 'An error occurred during addition'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
