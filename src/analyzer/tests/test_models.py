import pytest

from analyzer.models import Project, Result, Subscription


@pytest.mark.django_db
class TestProject:
    def test_creation(self, project: Project):
        pass

    def test_str(self, project: Project):
        assert str(project) == project.name


@pytest.mark.django_db
class TestResult:
    def test_creation(self, result: Result):
        pass

    def test_str(self, result: Result):
        assert str(result) == result.project.name

    def test_count(self, result: Result):
        assert result.count == 1


@pytest.mark.django_db
class TestSubscription:
    def test_creation(self, subscription: Subscription):
        pass
