# 5. URL for our app

from django.urls import path  #to import path functions for defining url patterns 
from . import views           # . to import the views module from the current directory (the directory where the urls.py file is located)


urlpatterns=[
    path('login/',views.loginPage, name='login'),
    path('register/',views.registerPage, name='register'),
    path('logut/',views.logoutUser, name='logout'),
    path('',views.home, name='home'), #4. Will return to page home for empty string i.e default home page
    path('room/<str:pk>/',views.room, name='room'),  #11. we are passing the id into the url. <> angular brackets are used to send dynamic data
    path('profile/<str:pk>/',views.userProfile, name='user-profile'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message<str:pk>/', views.deleteMessage, name='delete-message'),
]
