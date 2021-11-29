from django import forms
from urllib.parse import urlsplit
from .models import Url

class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['url']

    def check_url(self):
        url = self.cleaned_data['url']
        if not urlsplit(url).scheme in {'http', 'https', 'ftp'}:
            raise forms.ValidationError('URL. Error')
        return url
