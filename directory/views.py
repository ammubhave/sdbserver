from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Directory


def home(request):
    #d = Directory(firstname='amol')
    #d.save()
    directory = Directory.objects.filter(id__gt=2, lastname='Park')
    return HttpResponse(str([str(d) for d in directory]))
