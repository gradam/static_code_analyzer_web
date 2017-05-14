from django.conf.urls import url
from .views import HomeView, DetailView, RunAnalysisView, DeleteSubscriptionView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^detail/(?P<slug>[-\w]+)/$', DetailView.as_view(), name='detail'),
    url(r'^run/(?P<project_id>\d+)/$', RunAnalysisView.as_view(), name='run'),
    url(r'^subscription/delete/(?P<subscription_id>\d+)', DeleteSubscriptionView.as_view(),
        name='delete-subscription')
]
