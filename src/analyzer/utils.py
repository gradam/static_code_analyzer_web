import logging

from background_task import background
from django.core.mail import send_mail
from django.urls import reverse

from utils.analyzers import analyze_code
from utils.code_getters import get_from_git
from .models import Project, Result, Subscription


@background(schedule=5)
def run_analysis(project_id: int, host: str):
    logging.info(f'Running analysis for project {project_id}')
    project = Project.objects.get(id=project_id)
    project.running = True
    project.save()
    with get_from_git(project.url) as code_dir:
        results = analyze_code(code_dir, project.analyzers)
    Result.objects.create(results=results, project=project)
    logging.info(f'Done running analysis for project {project_id}')
    project.running = False
    project.save()
    send_notification_email(project, host)


def send_notification_email(project: Project, host: str):
    emails = Subscription.objects.filter(project=project).values_list('email', flat=True)
    url = reverse('detail', kwargs={'slug': project.slug})
    title = f'Finished running analyzers for project `{project.name}`'
    massage = f"""
    Finished running analyzers for project `{project.name}`. 
    See the results at {host}/{url}.
    """
    from_user = 'admin@127.0.0.1'
    send_mail(
        title,
        massage,
        from_user,
        emails
    )
