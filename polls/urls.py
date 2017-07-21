from django.conf.urls import url
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'(?P<poll_id>[0-9]+)/$', views.PageView.as_view(), name='page'),
    url(r'(?P<poll_id>[0-9]+)/score$', views.ResultsView.as_view(), name='score'),

]
