from django.shortcuts import render
from django.template import loader


def index(request):
  context = {'message': 'Ma nigga ma nigga..Youre home'}
  return render(request,'home/index.html',context)

def addplayer(request):
  context={}
  return render(request,'home/addplayer.html',context)

def teams(request):
  context={}
  return render(request,'home/teams.html',context)

def matches(request):
  context={}
  return render(request,'home/matches.html',context)