import logging
import shutil
import tempfile
from contextlib import contextmanager
from git import Repo


@contextmanager
def get_from_git(repository):
    directory = tempfile.mkdtemp()
    repo = Repo.clone_from(repository, directory)
    repo = repo.clone(repository)
    logging.debug(f'Cloned {repository}')
    yield repo
    shutil.rmtree(directory)
