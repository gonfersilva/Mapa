from django.conf.urls import url, include
from . import views
from .views import ReportListView, ReportCreateView, report_detail

app_name="report" 

urlpatterns = [
    
    url(r'^$', ReportListView.as_view(), name='report'),
    url(r'^create/$', ReportCreateView.as_view(), name='report_create'),
    url(r'^(?P<pk>\d+)/', report_detail, name='perfil_details'),
]