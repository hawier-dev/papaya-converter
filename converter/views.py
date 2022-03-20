import os
from pathlib import Path
from django.http import HttpRequest
from django.shortcuts import render
from pytube import YouTube
import ffmpeg
from .models import Video, Settings

# Create your views here.


def dashboard(request):
    videos = Video.objects.all().order_by("-id")
    if not Settings.objects.all():
        settings = Settings()
        settings.download_dir = str(os.path.join(Path.home(), "Downloads"))
        settings.save()
    download_dir = Settings.objects.first().download_dir
    if request.method == "POST":
        if 'url' in request.POST:
            link = request.POST['url']
            video = YouTube(link)

            # VIDEO DATA
            title = video.title
            author = video.author
            quality = []

            # QUALITY
            for stream in video.streams.order_by('resolution'):
                if stream.resolution not in quality:
                    quality.append(stream.resolution)
            quality.reverse()
            return render(request, 'base.html', {'title': title, 'author': author, 'quality': quality, 'url': link, 'video_style': 'uk-visible', 'videos': videos})
        if 'quality' in request.POST:
            selected_quality = request.POST['quality']
            download_link = request.POST['download']
            youtube = YouTube(download_link)
            filename = download_dir + '/' + youtube.title + '.mp4'
            if os.path.exists(filename):
                os.remove(filename)

            # Get audio from video
            audio = youtube.streams.filter(
                only_audio=True).first().download(filename='audio.mp4')

            # Convert mp4 to mp3
            ffmpeg.output(ffmpeg.input('audio.mp4').audio, 'audio.mp3').run()
            os.remove('audio.mp4')

            # Download video
            video = youtube.streams.filter(
                res=selected_quality).first().download(filename='video.mp4')

            # Convert
            input_video = ffmpeg.input('audio.mp3')
            input_audio = ffmpeg.input('video.mp4')

            ffmpeg.output(input_audio, input_video, filename).run()
            os.remove('audio.mp3')
            os.remove('video.mp4')

            # Saving to history
            video_model = Video()
            video_model.title = youtube.title
            video_model.video_url = download_link
            video_model.quality = selected_quality
            if Video.objects.filter(video_url=download_link).exists() == False:
                video_model.save()
            return render(request, 'base.html', {'title': '', 'author': '', 'quality': [], 'url': '', 'video_style': 'uk-hidden', 'videos': videos})

    return render(request, 'base.html', {'title': '', 'author': '', 'quality': [], 'url': '', 'video_style': 'uk-hidden', 'videos': videos})
