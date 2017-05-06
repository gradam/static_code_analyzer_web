from flake8.api import legacy as flake8
import os
from glob import glob


class Analyzers:
    ALL = ('flake8',)
    CHOICES = (('flake8', 'flake8'),)

    @staticmethod
    def use_flake8(files, ignore):
        style_guide = flake8.get_style_guide(ignore=ignore)
        report = style_guide.check_files(files)
        rep = {
            'Errors': report.get_statistics('E'),
            'Warnings': report.get_statistics('W') + report.get_statistics('F'),
        }
        return rep


def analyze_code(root_dir, analyzers, ignore=None):
    if ignore is None:
        ignore = []
    reports = dict()
    files = [y for x in os.walk(root_dir) for y in glob(os.path.join(x[0], '*.py'))]
    for analyzer in analyzers:
        reports[analyzer] = getattr(Analyzers, f'use_{analyzer}')(files, ignore)