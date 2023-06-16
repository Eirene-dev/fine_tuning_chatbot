from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FineTunedModelViewSet, 
    TrainingDataViewSet, 
    TrainingDataMetadataViewSet, 
    create_jsonl_file, 
    upload_jsonl_file,
)

router = DefaultRouter()
router.register(r'fine_tuned_models', FineTunedModelViewSet)
router.register(r'training_data', TrainingDataViewSet)
router.register(r'training_metadata', TrainingDataMetadataViewSet)

jsonl_patterns = [
    path('create/<int:finetuned_model_id>/', create_jsonl_file, name='create_jsonl_file'),
    path('upload/<int:finetuned_model_id>/', upload_jsonl_file, name='upload_jsonl_file'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('jsonl/', include(jsonl_patterns)),
]
