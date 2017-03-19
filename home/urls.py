
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^teams/',views.teams, name='teams'),
  url(r'^matches/',views.matches, name='matches'),
  url(r'^auction/', views.auction, name='auction'),
  url(r'^resetdb/', views.resetdb, name='resetdb'),
  url(r'^$', views.index,name='index'),
]
