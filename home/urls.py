
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^addplayer/',views.addplayer, name='addplayer'),
  url(r'^$', views.index,name='index'),
]
