from django.contrib import admin
from .models import FineTunedModel, TrainingData, TrainingDataMetadata

# Register your models here.
@admin.register(FineTunedModel)
class FineTunedModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'base_model')
    search_fields = ('model_name', 'base_model')


@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'completion', 'fine_tuned_model', 'is_fine_tuned', 'will_be_fine_tuned', 'metadata')
    search_fields = ('prompt', 'completion', 'fine_tuned_model__model_name', 'metadata__name')
    list_filter = ('fine_tuned_model', 'is_fine_tuned', 'will_be_fine_tuned', 'metadata')


@admin.register(TrainingDataMetadata)
class TrainingDataMetadataAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'training_date', 'model_architecture', 'loss_function', 'optimizer')
    search_fields = ('name', 'version', 'model_architecture', 'loss_function', 'optimizer')
    list_filter = ('training_date',)
