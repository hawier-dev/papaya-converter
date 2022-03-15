from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return HttpRequest('Kanapa')