from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from autoslug import AutoSlugField
import jsonfield

from utils.analyzer import Analyzers


# Create your models here.
class Project(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    url = models.CharField(_('Url of the repository'), max_length=200, unique=True)
    last_analyzed = models.DateTimeField(_('Last analyzed'), default=None, blank=True, null=True)
    running = models.BooleanField(_('Running'), default=False)
    # List of analyzers to use for this project
    analyzers = MultiSelectField(_('analyzers'), choices=Analyzers.CHOICES, min_choices=1)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    results = jsonfield.JSONField()
    date = models.DateTimeField(_('Date'), default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Project'))

    def __str__(self):
        return f'{self.project.name}: {self.date}'
