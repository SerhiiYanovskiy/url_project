import random
from django.contrib.auth.forms import UserCreationForm
import string
from django.contrib.auth import login, logout
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UrlForm
from .models import Url

from django.contrib.auth.decorators import login_required
# Create your views here.


def generate_key(length):
    letters = string.ascii_letters
    digits = string.digits
    key = ''.join(random.choice(letters + digits) for i in range(length))
    return key


def homepage(request):
    return render(request, 'homepage.html')


def create_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_bound and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'register.html', {'form': form})


@login_required
def url_page(request):
    form = UrlForm(request.POST or None)
    page_params = {
        'form': form,
    }
    if form.is_bound and form.is_valid():
        url = form.save(commit=False)
        url.user_id = request.user.id
        url.url_short = generate_key(5)
        url.save()
        page_params['url_short'] = url.url_short
    return render(request, 'url_page.html', page_params)


def url_redirect(request, url_key):
    url_info = Url.objects.get(pk=url_key)
    url_info.redirect_count += 1
    url_info.save()
    return redirect(url_info.url)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('./login')


