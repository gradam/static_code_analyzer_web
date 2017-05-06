from django.shortcuts import render, redirect
from django.views import View
from .forms import NewProjectForm, EditProjectForm
from .models import Project


class HomeView(View):
    form_class = NewProjectForm
    template_name = 'home.html'
    queryset = Project.objects.all

    def get(self, request):
        projects = self.queryset()
        context = {'project_form': self.form_class,
                   'projects': projects}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            projects = self.queryset()
            context = {'project_form': form,
                       'projects': projects}
            return render(request, self.template_name, context=context)


class DetailView(View):
    template_name = 'details.html'
    form_class = EditProjectForm

    @staticmethod
    def get_instance(slug):
        return Project.objects.get(slug=slug)

    def get(self, request, slug):
        project_instance = self.get_instance(slug)
        form = self.form_class(instance=project_instance)
        context = {'project': project_instance,
                   'form': form}

        return render(request, self.template_name, context=context)

    def post(self, request, slug, *args, **kwargs):
        project_instance = self.get_instance(slug)
        form = self.form_class(request.POST, instance=project_instance)
        if form.is_valid():
            form.save()
            return redirect('detail', slug=slug)
        else:
            context = {'project': project_instance,
                       'form': form}
            return render(request, self.template_name, context=context)
