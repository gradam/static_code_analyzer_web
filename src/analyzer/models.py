from django.db import models
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from utils.analyzer import Analyzers


# Create your models here.
class Project(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    url = models.CharField(_('Url'), max_length=200, unique=True)
    last_analyzed = models.DateTimeField(_('Last analyzed'), default=None, blank=True, null=True)
    running = models.BooleanField(_('Running'), default=False)
    # List of analyzers to use for this project
    analyzers = MultiSelectField(_('analyzers'), choices=Analyzers.CHOICES, min_choices=1)

    def __str__(self):
        return self.name
