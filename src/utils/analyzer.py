import os
from glob import glob
import logging
import io
from contextlib import redirect_stdout
import re

from flake8.api import legacy as flake8
from pylint import epylint as lint


class Analyzers:
    ALL = ('flake8', 'pylint')
    CHOICES = (('flake8', 'flake8'), ('pylint', 'pylint'))

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def _parse_flake8(self, report):
        redundant_path_part = self.root_dir + '/'
        parsed_massages = []
        for massage in report[:-1]:
            massage = massage[len(redundant_path_part):]  # get rid of tmp folder path:
            file, massage = massage.split(' ', 1)
            file, line, character = file.split(':')[:-1]
            position = ':'.join([line, character])
            parsed_massages.append({
                'file': file,
                'position': position,
                'massage': massage
            })

        return parsed_massages

    def _parse_pylint(self, results):
        parsed_massage = []
        pattern = re.compile(r'\d+\.\d{2}')
        counter = 0
        score = 0
        for line in results:
            if line.startswith(self.root_dir):
                line = line[len(self.root_dir):]
                file, error_type, massage = line.split(' ', 2)
                file, position = file.split(':')[:-1]
                parsed_massage.append({
                    'file': file,
                    'position': position,
                    'massage': massage
                })
            elif line.startswith('Your code has been rated'):
                current, *_ = pattern.findall(line)
                score += float(current)
                counter += 1
        final_score = '{:.2f}/10'.format(score/counter)
        return parsed_massage, final_score



    def use_flake8(self, files, ignore):
        logging.info('Running flake8')
        style_guide = flake8.get_style_guide(ignore=ignore)
        output = io.StringIO()
        with redirect_stdout(output):
            style_guide.check_files(files)
        report = output.getvalue().split('\n')
        return self._parse_flake8(report)

    def use_pylint(self, files, *_):
        results = ""
        for file in files:
            pylint_stdout, pylint_stderr = lint.py_run(file, return_std=True)
            text = pylint_stdout.getvalue()
            results += '\n' + text
        results = [line.strip() for line in results.split('\n')]



def analyze_code(root_dir, analyzers_list, ignore=None):
    if ignore is None:
        ignore = []
    reports = dict()
    # recursively list all .py files in the directory
    files = [y for x in os.walk(root_dir) for y in glob(os.path.join(x[0], '*.py'))]
    analyzers = Analyzers(root_dir)
    for analyzer in analyzers_list:
        report = getattr(analyzers, f'use_{analyzer}')(files, ignore)
        reports[analyzer] = [report, len(report)]
    logging.info(reports)
    return reports
