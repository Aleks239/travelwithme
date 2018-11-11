from django.urls import path

from . import views

app_name = 'travelwithme'

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.users, name='users'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]
