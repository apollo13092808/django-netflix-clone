from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('register/', views.sign_up, name='register'),
    path('logout/', views.sign_out, name='logout'),
    path('movie/<str:movie_uuid>/', views.movie, name='movie'),
    path('genre/<str:movie_genre>/', views.genre, name='genre'),
    path('my-list/', views.my_list, name='my_list'),
    path('add-to-list/', views.add_to_list, name='add_to_list'),
    path('search/', views.search, name='search'),
]
