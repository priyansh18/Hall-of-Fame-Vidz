from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.conf import settings
from django.http import Http404
import urllib
from django.forms.utils import ErrorList
import requests
# Create your views here.

YOUTUBE_API_KEY = 'AIzaSyDN6etR9-Davwzw1dLsM4-jew8u6nvN_Ww'


def home(request):
    context = {}
    return render(request, 'halls/home.html', context)


def add_videos(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404

    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.hall = hall
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            response = requests.get(
                f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
            json = response.json()
            title = json['items'][0]['snippet']['title']
            if video_id:
                video.youtube_id = video_id[0]
                video.title = title
                video.save()
                return redirect('detail_hall', pk)
            else:
                error = form._errors.setdefault('url', ErrorList())
                error.append('Needs to be a Youtube Url')

    context = {
        'form': form,
        'search_form': search_form,
        'hall': hall

    }
    return render(request, 'halls/add_video.html', context)


def dashboard(request):
    context = {}
    return render(request, 'halls/dashboard.html', context)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        print(view)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateHall(CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('home')


class DetailHall(DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'


class UpdateHall(UpdateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/update_hall.html'
    success_url = reverse_lazy('dashboard')


class DeleteHall(DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')
