from uuid import uuid4

import pytest
from django.core.urlresolvers import reverse
from django.test import Client

from analyzer.models import Project


@pytest.mark.django_db
class TestHomeView:
    @pytest.fixture
    def url(self) -> str:
        return reverse('home')

    def test_response_code(self, client: Client, url: str):
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestDetailView:

    def get_detail_url(self, project: Project):
        return reverse('detail', kwargs={'slug': project.slug})

    def test_get_response_code(self, client: Client, project: Project):
        url = self.get_detail_url(project)
        response = client.get(url)
        assert response.status_code == 200

    def send_post(self, client: Client, project: Project):
        url = self.get_detail_url(project)
        new_name = str(uuid4())
        data = {
            'name': new_name,
            'analyzers': ['pylint'],
            'url': project.url,
        }
        response = client.post(url, data=data)
        return response, data

    def test_post_response_code(self, client: Client, project: Project):
        response, _ = self.send_post(client, project)
        assert response.status_code == 302

    def test_post_change(self, client: Client, project: Project):
        _, data = self.send_post(client, project)
        project.refresh_from_db()
        assert project.name == data['name']
