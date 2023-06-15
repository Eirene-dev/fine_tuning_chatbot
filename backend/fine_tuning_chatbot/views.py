from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response('Hello, World!')


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FineTunedModel, TrainingData, TrainingDataMetadata
from .serializers import FineTunedModelSerializer, TrainingDataSerializer, TrainingDataMetadataSerializer

class FineTunedModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = FineTunedModel.objects.all()
    serializer_class = FineTunedModelSerializer

class TrainingDataViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer

class TrainingDataMetadataViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TrainingDataMetadata.objects.all()
    serializer_class = TrainingDataMetadataSerializer
