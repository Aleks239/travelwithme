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
    path('search_result', views.search_result, name='search_result'),
    path('create_trip', views.create_trip, name='create_trip'),
    path('rate_trip', views.rate_trip, name='rate_trip'),
    path('my_trip', views.my_trip, name='my_trip'),
    path('notification', views.notification, name='notification'),
]
