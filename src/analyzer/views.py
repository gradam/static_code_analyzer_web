from django.shortcuts import render
from .forms import ProjectForm
from .models import Project


def home_view(request):
    projects = Project.objects.all()
    context = {'project_form': ProjectForm,
               'projects': projects}
    return render(request, 'home.html', context=context)
