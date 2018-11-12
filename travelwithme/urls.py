from django.urls import path

from . import views

app_name = 'travelwithme'

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.users, name='users'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup, name='signup'),
    path('signup_user', views.signup_user, name='signup_user'),
    path('logout', views.log_user_out, name='logout'),
    path('log_user_in', views.log_user_in, name='log_user_in'),
]
