from django.contrib.auth.models import User
from django.db import models

# Your models
class FineTunedModel(models.Model):
    MODEL_CHOICES = [
        ('ada', 'Ada'),
        ('babbage', 'Babbage'),
        ('curie', 'Curie'),
        ('davinci', 'Davinci'),
    ]

    model_name = models.CharField(max_length=100)
    base_model = models.CharField(max_length=100, choices=MODEL_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fine_tuned_models', null=True)
    file_id = models.CharField(max_length=200, null=True, blank=True)
    fine_tune_id = models.CharField(max_length=200, null=True, blank=True)
    fine_tuned_model = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.model_name


class TrainingDataMetadata(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    training_date = models.DateField()
    description = models.TextField()
    model_architecture = models.CharField(max_length=255)
    loss_function = models.CharField(max_length=255)
    optimizer = models.CharField(max_length=255)
    performance_metrics = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_data_metadatas', null=True)

    def __str__(self):
        return f'{self.name} v{self.version}'


class TrainingData(models.Model):
    fine_tuned_model = models.ForeignKey(FineTunedModel, on_delete=models.CASCADE, related_name='training_data')
    metadata = models.ForeignKey(TrainingDataMetadata, on_delete=models.SET_NULL, null=True, related_name='training_data')
    prompt = models.TextField()
    completion = models.TextField()
    is_fine_tuned = models.BooleanField(default=False)
    will_be_fine_tuned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_datas', null=True)

    def __str__(self):
        return f"Training Data for {self.fine_tuned_model.model_name}"
