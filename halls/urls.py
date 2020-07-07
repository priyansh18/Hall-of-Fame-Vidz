from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('dashboard',views.dashboard,name='dashboard'),
    path('halloffame/create',views.CreateHall.as_view(), name='create_hall'),
    path('halloffame/<int:pk>',views.DetailHall.as_view(), name='detail_hall'),
    path('halloffame/<int:pk>/update',views.UpdateHall.as_view(), name='update_hall'),
    path('halloffame/<int:pk>/delete',views.DeleteHall.as_view(), name='delete_hall'),
    path('halloffame/<int:pk>/addvideos',views.add_videos, name='add_videos'),
    path('video/search',views.video_search, name='video_search'),
    path('video/<int:pk>/delete',views.DeleteVideo.as_view(), name='delete_video'),
]
