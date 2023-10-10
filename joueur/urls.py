from django.urls import path

from joueur.views import *


urlpatterns = [
    path('', home , name='home'),
    path('login/', Login, name='login'),
    path('register/', register, name='register'),
    path('logout/', Logout, name='logout'),
    path('game_home',game_home, name='game_home'),
    path('start', start, name='start'),
    path('score_enr',score_enr, name='score_enr'),
    path('profile', profile, name='profile'),
]
