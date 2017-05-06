from django.shortcuts import render
from django.views import View
from .forms import ProjectForm
from .models import Project


class HomeView(View):
    form_class = ProjectForm
    template_name = 'home.html'

    def get(self, request):
        projects = Project.objects.all()
        context = {'project_form': self.form_class,
                   'projects': projects}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return self.get(request)
