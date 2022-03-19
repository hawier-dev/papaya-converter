from django.http import HttpRequest
from django.shortcuts import render
from pytube import YouTube

# Create your views here.
def dashboard(request):
    if request.method == "POST":
        link = request.POST['url']
        video = YouTube(link)

        # VIDEO DATA
        title = video.title
        author = video.author
        thumbnail = video.thumbnail_url
        quality = []
        
        # QUALITY
        for stream in video.streams.order_by('resolution'):
            if stream.resolution not in quality:
                quality.append(stream.resolution)
        quality.reverse()
        return render(request, 'base.html', {'title': title, 'author': author, 'quality': quality, 'video_style': 'video-visible'})
    return render(request, 'base.html', {'title': '', 'author': '','quality': [],'video_style': 'video-hidden'})