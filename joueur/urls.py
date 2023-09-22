from django.urls import path

from joueur.views import *


urlpatterns = [
    path('', home , name='home'),
]
