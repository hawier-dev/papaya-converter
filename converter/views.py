from django.http import HttpRequest
from django.shortcuts import render
from .forms import VideoForm
# Create your views here.
def dashboard(request):
    if request.method == "POST":
        pass
    form = VideoForm()
    return render(request, 'base.html', {'form': form})