from django.db import models
from multiselectfield import MultiSelectField
from utils.analyzer import Analyzers


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    last_analyzed = models.DateTimeField(default=None, blank=True, null=True)
    # List of analyzers to use for this project
    analyzers = MultiSelectField(choices=Analyzers.CHOICES, min_choices=1)

    def __str__(self):
        return self.name
