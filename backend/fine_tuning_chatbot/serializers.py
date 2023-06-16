from rest_framework import serializers
from .models import FineTunedModel, TrainingData

class FineTunedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FineTunedModel
        fields = ['id', 'model_name', 'base_model']


class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = ['id', 'fine_tuned_model', 'metadata', 'prompt', 'completion', 'is_fine_tuned', 'will_be_fine_tuned']
