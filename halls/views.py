from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from .models import Hall
# Create your views here.


def home(request):
    context = {}
    return render(request, 'halls/home.html', context)

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self,form):
        view = super(SignUp,self).form_valid(form)
        print(view)
        username,password = form.cleaned_data.get('username'),form.cleaned_data.get('password1')
        user = authenticate(username=username,password=password)
        login(self.request,user)
        return view

class CreateHall(CreateView):
    model=Hall
    fields=['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        form.instance.user = self.request.user
        super(CreateHall,self).form_valid(form)
        return redirect('home')
