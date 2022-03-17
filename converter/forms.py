from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    video_url = forms.CharField(max_length=100,required=True,widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "https://",
                "class": "text-input radius-small surface input-border uk-text-bold uk-text-default",
            }
        ),
        label="",
    )
    class Meta:
        model = Video
        exclude = ("user", )