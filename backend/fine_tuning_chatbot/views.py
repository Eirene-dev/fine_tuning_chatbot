from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

import os
import json
import openai

from .models import FineTunedModel, TrainingData
from .serializers import FineTunedModelSerializer, TrainingDataSerializer


@api_view(['GET'])
def hello_world(request):
    return Response('Hello, World!')


class FineTunedModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = FineTunedModel.objects.all()
    serializer_class = FineTunedModelSerializer


class TrainingDataViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer


def create_and_save_jsonl(finetuned_model_id):
    training_data = TrainingData.objects.filter(fine_tuned_model_id=finetuned_model_id)

    file_name = f"fine_tuned_model_{finetuned_model_id}.jsonl"
    with open(file_name, 'w') as f:
        for data in training_data:
            f.write(json.dumps({'prompt': data.prompt + '\n', 'completion': data.completion + '\n'}))
            f.write('\n')
    
    return file_name, training_data


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def convert_jsonl_file(request, finetuned_model_id):
    try:
        FineTunedModel.objects.get(id=finetuned_model_id)

        file_name, training_data = create_and_save_jsonl(finetuned_model_id)

        file_info = os.stat(file_name)

        response = {
            'file_name': file_name,
            'lines': len(training_data),
            'file_size': file_info.st_size,
        }
        return JsonResponse(response)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_jsonl_file(request, finetuned_model_id):
    try:
        finetuned_model = FineTunedModel.objects.get(id=finetuned_model_id)

        file_name, _ = create_and_save_jsonl(finetuned_model_id)

        with open(file_name, 'rb') as file:
            openai.api_key = settings.OPENAI_API_KEY
            result = openai.File.create(file=file, purpose='fine-tune')
        
        finetuned_model.file_id = result['id']
        finetuned_model.save()

        if default_storage.exists(file_name):
            default_storage.delete(file_name)

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_finetune(request, finetuned_model_id):
    try:
        finetuned_model = FineTunedModel.objects.get(id=finetuned_model_id)

        openai.api_key = settings.OPENAI_API_KEY
        result = openai.FineTune.create(
            model=finetuned_model.base_model,
            training_file=finetuned_model.file_id,
        )

        finetuned_model.fine_tune_id = result['id']
        finetuned_model.save()

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def retrieve_finetune(request, finetuned_model_id):
    try:
        finetuned_model = FineTunedModel.objects.get(id=finetuned_model_id)

        openai.api_key = settings.OPENAI_API_KEY
        fine_tune_id = finetuned_model.fine_tune_id

        result = openai.FineTune.retrieve(id=fine_tune_id)

        finetuned_model.status = result['status']
        finetuned_model.fine_tuned_model = result['fine_tuned_model']
        finetuned_model.save()

        return JsonResponse(result)

    except FineTunedModel.DoesNotExist:
        return JsonResponse({'error': 'FineTunedModel with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
