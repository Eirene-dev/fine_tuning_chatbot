from django.urls import path
from . import views


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FineTunedModelViewSet, TrainingDataViewSet, TrainingDataMetadataViewSet

router = DefaultRouter()
router.register(r'fine_tuned_models', FineTunedModelViewSet)
router.register(r'training_data', TrainingDataViewSet)
router.register(r'training_metadata', TrainingDataMetadataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
