from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Project, Subscription


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'url', 'analyzers')


class NewProjectForm(ProjectForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Add new')))
        super().__init__(*args, **kwargs)


class EditProjectForm(ProjectForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Save changes')))
        super().__init__(*args, **kwargs)


class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.form_method = 'post'
        self.helper.add_input(Submit('Submit', _('Subscribe')))
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subscription
        fields = ('email',)
