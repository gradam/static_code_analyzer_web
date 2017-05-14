from uuid import uuid4

import pytest

from analyzer.models import Project, Result, Subscription


@pytest.fixture
def project() -> Project:
    return Project.objects.create(
        name=str(uuid4()),
        url=str(uuid4()),
    )


@pytest.fixture
def result(project: Project) -> Result:
    return Result.objects.create(
        results={
            "flake8": [
                [
                    {
                        "file": "tests/test_thread_server.py",
                        "position": "29:80",
                        "massage": "E501 line too long (91 > 79 characters)"
                    }
                ],
                1,
                ""
            ],
            "pylint": [
                [],
                0,
                "Your code has been rated at 10.00/10"
            ]
        },
        project=project
    )


@pytest.fixture
def subscription(project: Project) -> Subscription:
    return Subscription(
        email='test@127.0.0.1',
        project=project
    )
