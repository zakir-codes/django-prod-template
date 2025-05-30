from rest_framework import serializers

class NumberInputSerializer(serializers.Serializer):
    num1 = serializers.FloatField(help_text="The first number")
    num2 = serializers.FloatField(help_text="The second number")

class ResultOutputSerializer(serializers.Serializer):
    result = serializers.FloatField(help_text="The calculated result")