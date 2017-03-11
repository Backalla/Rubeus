
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^addplayer/',views.addplayer, name='addplayer'),
  url(r'^teams/',views.teams, name='teams'),
  url(r'^matches/',views.matches, name='matches'),
  url(r'^$', views.index,name='index'),
]
