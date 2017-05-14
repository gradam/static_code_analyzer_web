from uuid import uuid4
import pytest
from analyzer.models import Project


@pytest.fixture
def project():
    return Project.objects.create(
        name=str(uuid4()),
        url=str(uuid4()),
    )
