from background_task import background
from .models import Project, Result
from utils.analyzer import analyze_code
from utils.code_getters import get_from_git


@background(shedule=0)
def run_analysis(project_id: int):
    project = Project.objects.get(id=project_id)
    project.running = True
    project.save()

    with get_from_git(project.url) as code_dir:
        results = analyze_code(code_dir, project.analyzers)
    Result.objects.create(results=results, project=project)

    project.running = False
    project.save()


