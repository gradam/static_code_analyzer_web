from django.conf.urls import url
from .views import HomeView, DetailView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^detail/(?P<project_id>\d+)/$', DetailView.as_view(), name='detail')
]
