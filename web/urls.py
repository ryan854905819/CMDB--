from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^server.html$', views.server),
    url(r'^server_json.html$', views.server_json),
    url(r'^disk.html$', views.disk),
    url(r'^disk_json.html$', views.disk_json),
    url(r'^test.html$', views.test),

]
