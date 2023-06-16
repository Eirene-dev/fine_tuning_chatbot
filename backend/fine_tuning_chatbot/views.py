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


import os
import json

from django.http import JsonResponse
from .models import FineTunedModel, TrainingData

def create_jsonl_file(request, finetuned_model_id):
    if request.method == "GET":
        try:
            # Check if the FineTunedModel exists
            FineTunedModel.objects.get(id=finetuned_model_id)

            # Query all training data related to the fine-tuned model
            training_data = TrainingData.objects.filter(fine_tuned_model_id=finetuned_model_id)

            # Convert training data to JSONL format and write it to a file
            file_name = f"fine_tuned_model_{finetuned_model_id}.jsonl"
            with open(file_name, 'w') as f:
                for data in training_data:
                    f.write(json.dumps({'prompt': data.prompt + '\n', 'completion': data.completion + '\n'}))
                    f.write('\n')

            # Compute file information
            file_info = os.stat(file_name)

            # Return file information
            response = {
                'file_name': file_name,
                'lines': len(training_data),
                'file_size': file_info.st_size,
            }
            return JsonResponse(response)

        except FineTunedModel.DoesNotExist:
            return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=400)


import os
from django.http import JsonResponse
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
import openai

from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
def upload_jsonl_file(request, finetuned_model_id):
    try:
        # Check if the FineTunedModel exists
        FineTunedModel.objects.get(id=finetuned_model_id)

        # Query all training data related to the fine-tuned model
        training_data = TrainingData.objects.filter(fine_tuned_model_id=finetuned_model_id)

        # Convert training data to JSONL format and write it to a file
        file_name = f"fine_tuned_model_{finetuned_model_id}.jsonl"
        with open(file_name, 'w') as f:
            for data in training_data:
                f.write(json.dumps({'prompt': data.prompt + '\n', 'completion': data.completion + '\n'}))
                f.write('\n')

        with open(file_name, 'rb') as file:
            openai.api_key = settings.OPENAI_API_KEY
            result = openai.File.create(
                file=file,
                purpose='fine-tune'
            )

        # Delete the file after use
        if default_storage.exists(file_name):
            default_storage.delete(file_name)

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)