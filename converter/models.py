from django.db import models

# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=100)
    quality = models.CharField(max_length=10)
    video_url = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Settings(models.Model):
    download_dir = models.CharField(max_length=150)

    def __str__(self):
        return self.download_dir
