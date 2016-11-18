from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    #This route allows the other routes to send errors to be displayed on index.html
    url(r'^(?P<error>[\d])$', views.index),
    url(r'^new$', views.new),
    #Url is looking for an integer between 1 and 6 digits long
    url(r'^destroy/(?P<id>[\d]{1,6})$', views.destroy),
]
