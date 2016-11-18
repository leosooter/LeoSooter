from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^new$', views.new),
    url(r'^success$', views.success),
    url(r'^destroy/(?P<id>[\d]{1,4})$', views.destroy),
]
