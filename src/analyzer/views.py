from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views import View
from .forms import NewProjectForm, EditProjectForm, SubscriptionForm
from .models import Project, Result, Subscription
from .utils import run_analysis


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

    @staticmethod
    def get_context(project_instance, form, subscription_form):
        results = Result.objects.filter(project=project_instance)
        subscriptions = Subscription.objects.filter(project=project_instance)

        context = {'project': project_instance,
                   'form': form,
                   'results': results,
                   'subscriptions': subscriptions,
                   'subscription_form': subscription_form}
        return context

    def get(self, request, slug):
        project_instance = self.get_instance(slug)
        form = self.form_class(instance=project_instance)
        context = self.get_context(project_instance, form,SubscriptionForm())
        return render(request, self.template_name, context=context)

    def post(self, request, slug, *args, **kwargs):
        project_instance = self.get_instance(slug)
        data = request.POST
        form = self.form_class(instance=project_instance)
        if 'url' in data:
            form = self.form_class(data, instance=project_instance)
            if form.is_valid():
                form.save()
                return redirect('detail', slug=slug)
            else:
                context = self.get_context(project_instance, form, SubscriptionForm())
                return render(request, self.template_name, context=context, status=400)
        else:
            subscription_form = SubscriptionForm(data)
            # subscription_form.data['project'] = project_instance
            if subscription_form.is_valid():
                email = data['email']
                Subscription.objects.get_or_create(email=email, project=project_instance)
                return redirect('detail', slug=slug)
            else:
                context = self.get_context(project_instance, form, subscription_form)
                return render(request, self.template_name, context=context, status=400)


class RunAnalysisView(View):

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=int(project_id))
        project.running = True
        project.last_analyzed = timezone.now()
        project.save()
        run_analysis(int(project_id), request.get_host(), schedule=timezone.now())
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteSubscriptionView(View):

    def get(self, request, subscription_id, *args, **kwargs):
        Subscription.objects.get(id=int(subscription_id)).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
