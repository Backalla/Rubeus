from django.shortcuts import render
from django.template import loader


def index(request):
  context = {'message': 'Ma nigga ma nigga..'}
  return render(request,'testing/index.html',context)

# Create your views here.
