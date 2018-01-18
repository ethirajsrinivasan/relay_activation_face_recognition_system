from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^greet$', views.greet, name='greet'),
    url(r'^add$', views.add, name="add"),
]