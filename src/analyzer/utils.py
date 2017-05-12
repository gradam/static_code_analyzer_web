from background_task import background
from .models import Project, Result
from utils.analyzer import analyze_code


@background(shedule=0)
def run_analysation(project_id: int):
    project = Project.objects.get(id=project_id)


