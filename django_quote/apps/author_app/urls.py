from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^welcome$', views.welcome),
    url(r'^create_quote$', views.create_quote),
    url(r'^poster/(?P<val>\d+)$', views.poster),
    url(r'^delete/(?P<val>\d+)$', views.delete),
    url(r'^edit$', views.edit),
    url(r'^update$', views.update),
    url(r'^logout$', views.logout),
]