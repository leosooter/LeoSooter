from django.conf.urls import url
from . import views

urlpatterns = [
    #home route- displays registration and login forms
    url(r'^$', views.index),
    #process registration form
    url(r'^register$', views.register),
    #process login form
    #sends to account on success to set security questions
    url(r'^login$', views.login),
    #displays info for logged-in users
    #sends to success on success
    url(r'^success$', views.success),
    #display form for updating user info and security questions
    url(r'^account$', views.account),
    #process update form
    #sends to success on success
    url(r'^update$', views.update),
    #display forgot-passowrd for on get request- process form on post request
    #sends to reset on success
    url(r'^retrieve$', views.retrieve),
    ##display reset-passowrd for on get request- process form on post request
    #sends to success on success
    url(r'^reset$', views.reset),
    #Logs user out
    #Sends to index
    url(r'^logout$', views.logout),
]
