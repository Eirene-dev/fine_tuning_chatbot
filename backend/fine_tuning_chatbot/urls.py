from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FineTunedModelViewSet, 
    TrainingDataViewSet, 
    TrainingDataMetadataViewSet, 
    convert_jsonl_file, 
    upload_jsonl_file,
    create_finetune,
    retrieve_finetune,
)

router = DefaultRouter()
router.register(r'fine_tuned_models', FineTunedModelViewSet)
router.register(r'training_data', TrainingDataViewSet)
router.register(r'training_metadata', TrainingDataMetadataViewSet)

jsonl_patterns = [
    path('convert/<int:finetuned_model_id>/', convert_jsonl_file, name='convert_jsonl_file'),
    path('upload/<int:finetuned_model_id>/', upload_jsonl_file, name='upload_jsonl_file'),
    path('create/<int:finetuned_model_id>/', create_finetune, name='create_finetune'),
    path('retrieve/<int:finetuned_model_id>/', retrieve_finetune, name='retrieve_finetune'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('dataset/', include(jsonl_patterns)),
]
