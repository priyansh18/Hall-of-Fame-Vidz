from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.conf import settings
from django.http import Http404, JsonResponse
import urllib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.utils import ErrorList
import requests
# Create your views here.
# Decorators & Mixins are used for maintaining url not to be changed

YOUTUBE_API_KEY = 'AIzaSyDN6etR9-Davwzw1dLsM4-jew8u6nvN_Ww'


def home(request):
    recent_halls = Hall.objects.all().order_by('id')[:3]
    popular_halls = [Hall.objects.get(
        pk=5), Hall.objects.get(pk=3), Hall.objects.get(pk=4)]
    context = {
        'recent_halls': recent_halls,
        'popular_halls': popular_halls
    }
    return render(request, 'halls/home.html', context)


@login_required
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
                errors = form._errors.setdefault('url', ErrorList())
                print(errors)

    context = {
        'form': form,
        'search_form': search_form,
        'hall': hall

    }
    return render(request, 'halls/add_video.html', context)


@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encode_search = urllib.parse.quote(
            search_form.cleaned_data['search_terms'])
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=8&q={encode_search}&key={YOUTUBE_API_KEY}')
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Not able to validate form'})


class DeleteVideo(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'halls/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.hall.user == self.request.user:
            raise Http404
        return video


@login_required
def dashboard(request):
    halls = Hall.objects.filter(user=request.user)
    context = {
        'halls': halls,
    }
    return render(request, 'halls/dashboard.html', context)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        print(view)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateHall(LoginRequiredMixin, CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('dashboard')


class DetailHall(DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'


class UpdateHall(LoginRequiredMixin, UpdateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/update_hall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall


class DeleteHall(LoginRequiredMixin, DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(DeleteHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall