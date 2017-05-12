from flake8.api import legacy as flake8
import os
from glob import glob
import logging

import io
from contextlib import redirect_stdout


class Analyzers:
    ALL = ('flake8',)
    CHOICES = (('flake8', 'flake8'),)

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def _parse_flake8(self, report):
        # get rid of tmp folder path:
        redundant_path_part = self.root_dir+'/'
        errors = [error[len(redundant_path_part):] for error in report[:-1]]
        return errors

    def use_flake8(self, files, ignore):
        logging.info('Running flake8')
        style_guide = flake8.get_style_guide(ignore=ignore)
        output = io.StringIO()
        with redirect_stdout(output):
            style_guide.check_files(files)
        report = output.getvalue().split('\n')
        return self._parse_flake8(report)


def analyze_code(root_dir, analyzers_list, ignore=None):
    if ignore is None:
        ignore = []
    reports = dict()
    # recursively list all .py files in the directory
    files = [y for x in os.walk(root_dir) for y in glob(os.path.join(x[0], '*.py'))]
    analyzers = Analyzers(root_dir)
    for analyzer in analyzers_list:
        reports[analyzer] = getattr(analyzers, f'use_{analyzer}')(files, ignore)
    logging.info(reports)
    return reports
