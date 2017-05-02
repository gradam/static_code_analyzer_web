import logging
import tempfile
from contextlib import contextmanager
from git import Repo


@contextmanager
def get_from_git(repository):
    with tempfile.mkdtemp() as directory:
        repo = Repo.clone_from(repository, directory)
        repo = repo.clone(repository)
        logging.debug(f'Cloned {repository}')
        yield repo
