from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Hall
# Create your views here.


def home(request):
    context = {}
    return render(request, 'halls/home.html', context)

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

class CreateHall(CreateView):
    model=Hall
    fields=['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('home')
