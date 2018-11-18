from django.urls import path

from . import views

app_name = 'travelwithme'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_trips', views.search_trips, name='search_trips'),
    path('login', views.login_page, name='login'),
    path('signup', views.signup, name='signup'),
    path('signup_user', views.signup_user, name='signup_user'),
    path('create_trip', views.create_trip, name='create_trip'),
    path('logout', views.log_user_out, name='logout'),
    path('mytrips', views.mytrips, name='mytrips'),
    path('user_info/<int:traveller_id>', views.user_info, name='user_info'),
    path('log_user_in', views.log_user_in, name='log_user_in'),
]
