from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('halloffame/create',views.CreateHall.as_view(), name='create_hall')
]
